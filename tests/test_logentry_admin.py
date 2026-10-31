import pytest
from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.checks import run_checks
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from logentry_admin.admin import ActionListFilter, UserListFilter
from tests.urls import other_site

CHANGELIST_URL = "/admin/admin/logentry/"


@pytest.fixture
def model_admin():
    return admin.site.get_model_admin(LogEntry)


@pytest.fixture
def user_content_type(db):
    return ContentType.objects.get_for_model(User)


@pytest.fixture
def make_entry(admin_user, user_content_type):
    """Create a log entry, by default a change to the admin user."""

    def _make_entry(**fields):
        values = {
            "user": admin_user,
            "content_type": user_content_type,
            "object_id": str(admin_user.pk),
            "object_repr": "the object",
            "action_flag": CHANGE,
            **fields,
        }
        return LogEntry.objects.create(**values)

    return _make_entry


@pytest.fixture
def make_staff_user(django_user_model):
    """Create a staff user holding the given log entry permissions."""

    def _make_staff_user(username, *codenames):
        user = django_user_model.objects.create_user(username, is_staff=True)
        user.user_permissions.set(
            Permission.objects.filter(codename__in=codenames)
        )
        return user

    return _make_staff_user


def listed_reprs(response):
    return {entry.object_repr for entry in response.context["cl"].result_list}


def filter_choices(response, filter_class):
    (spec,) = (
        spec
        for spec in response.context["cl"].filter_specs
        if isinstance(spec, filter_class)
    )
    return list(spec.lookup_choices)


class TestRegistration:
    def test_log_entries_listed_on_admin_index(self, admin_client):
        response = admin_client.get("/admin/")

        assert response.status_code == 200
        assert "Log entries" in response.content.decode()

    def test_system_checks_pass(self, db):
        assert run_checks() == []


class TestChangelist:
    def test_lists_log_entries(self, admin_client, make_entry):
        make_entry(object_repr="first")
        make_entry(object_repr="second")

        response = admin_client.get(CHANGELIST_URL)

        assert response.status_code == 200
        assert listed_reprs(response) == {"first", "second"}

    def test_action_filter_offers_each_action(self, admin_client):
        response = admin_client.get(CHANGELIST_URL)

        choices = filter_choices(response, ActionListFilter)
        assert [(value, str(label)) for value, label in choices] == [
            (ADDITION, "Addition"),
            (DELETION, "Deletion"),
            (CHANGE, "Change"),
        ]

    def test_action_filter_shows_only_that_action(
        self, admin_client, make_entry
    ):
        make_entry(object_repr="added", action_flag=ADDITION)
        make_entry(object_repr="deleted", action_flag=DELETION)

        response = admin_client.get(CHANGELIST_URL, {"action_flag": ADDITION})

        assert listed_reprs(response) == {"added"}

    def test_staff_user_filter_offers_only_staff(
        self, admin_client, admin_user, django_user_model
    ):
        editor = django_user_model.objects.create_user("editor", is_staff=True)
        django_user_model.objects.create_user("visitor")

        response = admin_client.get(CHANGELIST_URL)

        choices = filter_choices(response, UserListFilter)
        assert choices == [(admin_user.pk, "admin"), (editor.pk, "editor")]

    def test_staff_user_filter_shows_only_their_entries(
        self, admin_client, make_entry, make_staff_user
    ):
        editor = make_staff_user("editor")
        make_entry(object_repr="by admin")
        make_entry(object_repr="by editor", user=editor)

        response = admin_client.get(CHANGELIST_URL, {"user": editor.pk})

        assert listed_reprs(response) == {"by editor"}

    def test_search_matches_object_repr(self, admin_client, make_entry):
        make_entry(object_repr="Invoice 17")
        make_entry(object_repr="Order 4")

        response = admin_client.get(CHANGELIST_URL, {"q": "invoice"})

        assert listed_reprs(response) == {"Invoice 17"}

    @pytest.mark.parametrize(
        ("stored", "shown"),
        [
            pytest.param(
                '[{"changed": {"fields": ["Email address"]}}]',
                "Changed Email address.",
                id="json-from-the-admin",
            ),
            pytest.param("Changed email.", "Changed email.", id="plain-text"),
        ],
    )
    def test_shows_the_change_message_as_text(
        self, admin_client, make_entry, stored, shown
    ):
        make_entry(change_message=stored)

        response = admin_client.get(CHANGELIST_URL)

        assert shown in response.content.decode()

    def test_query_count_does_not_grow_with_the_entries(
        self, admin_client, make_entry, make_staff_user
    ):
        def changelist_queries():
            with CaptureQueriesContext(connection) as queries:
                admin_client.get(CHANGELIST_URL)
            return len(queries)

        make_entry(user=make_staff_user("first"))
        one_entry = changelist_queries()
        for username in ("second", "third", "fourth"):
            make_entry(user=make_staff_user(username))

        assert changelist_queries() == one_entry

    def test_offers_no_bulk_actions(self, admin_client, make_entry):
        make_entry()

        response = admin_client.get(CHANGELIST_URL)

        assert response.context["action_form"] is None


class TestDetailPage:
    def test_shows_the_entry(self, admin_client, make_entry):
        entry = make_entry(object_repr="Invoice 17")

        response = admin_client.get(
            reverse("admin:admin_logentry_change", args=[entry.pk])
        )

        assert response.status_code == 200
        assert "Invoice 17" in response.content.decode()

    def test_hides_the_history_link(self, admin_client, make_entry):
        entry = make_entry()

        response = admin_client.get(
            reverse("admin:admin_logentry_change", args=[entry.pk])
        )

        history_url = reverse("admin:admin_logentry_history", args=[entry.pk])
        assert history_url not in response.content.decode()

    def test_offers_no_save_button(self, admin_client, make_entry):
        entry = make_entry()

        response = admin_client.get(
            reverse("admin:admin_logentry_change", args=[entry.pk])
        )

        assert 'name="_save"' not in response.content.decode()


class TestPermissions:
    def test_user_with_view_permission_sees_the_log(
        self, client, make_staff_user
    ):
        client.force_login(make_staff_user("viewer", "view_logentry"))

        response = client.get(CHANGELIST_URL)

        assert response.status_code == 200

    def test_user_with_change_permission_sees_the_log(
        self, client, make_staff_user
    ):
        client.force_login(make_staff_user("editor", "change_logentry"))

        response = client.get(CHANGELIST_URL)

        assert response.status_code == 200

    def test_staff_user_without_permission_is_refused(
        self, client, make_staff_user
    ):
        client.force_login(make_staff_user("intern"))

        response = client.get(CHANGELIST_URL)

        assert response.status_code == 403

    def test_entries_cannot_be_changed(self, admin_client, make_entry):
        entry = make_entry(object_repr="original")

        response = admin_client.post(
            reverse("admin:admin_logentry_change", args=[entry.pk]),
            {"object_repr": "rewritten"},
        )

        assert response.status_code == 403
        entry.refresh_from_db()
        assert entry.object_repr == "original"

    def test_entries_cannot_be_added(self, admin_client):
        response = admin_client.get(reverse("admin:admin_logentry_add"))

        assert response.status_code == 403

    def test_entries_cannot_be_deleted(self, admin_client, make_entry):
        entry = make_entry()

        response = admin_client.post(
            reverse("admin:admin_logentry_delete", args=[entry.pk]),
            {"post": "yes"},
        )

        assert response.status_code == 403
        assert LogEntry.objects.filter(pk=entry.pk).exists()


class TestObjectLink:
    def test_links_to_the_object(self, model_admin, make_entry, admin_user):
        entry = make_entry(object_repr="admin", action_flag=ADDITION)

        link = model_admin.object_link(entry)

        url = reverse("admin:auth_user_change", args=[admin_user.pk])
        assert link == f'<a href="{url}">admin</a>'

    def test_links_within_its_own_admin_site(self, make_entry, admin_user):
        entry = make_entry(object_repr="admin")

        link = other_site.get_model_admin(LogEntry).object_link(entry)

        url = reverse("other_admin:auth_user_change", args=[admin_user.pk])
        assert link == f'<a href="{url}">admin</a>'

    def test_deleted_object_is_not_linked(self, model_admin, make_entry):
        entry = make_entry(object_repr="gone", action_flag=DELETION)

        assert model_admin.object_link(entry) == "gone"

    def test_object_outside_the_admin_is_not_linked(
        self, model_admin, make_entry
    ):
        entry = make_entry(
            content_type=ContentType.objects.get(model="session"),
            object_id="5",
            object_repr="a session",
        )

        assert model_admin.object_link(entry) == "a session"

    def test_entry_without_content_type_is_not_linked(
        self, model_admin, make_entry
    ):
        """Content types can be deleted as stale (issue #21)."""
        entry = make_entry(content_type=None, object_repr="orphan")

        assert model_admin.object_link(entry) == "orphan"

    def test_object_repr_is_escaped(self, model_admin, make_entry):
        entry = make_entry(object_repr="<b>bold</b>", action_flag=DELETION)

        assert model_admin.object_link(entry) == "&lt;b&gt;bold&lt;/b&gt;"


class TestUserLink:
    def test_links_to_the_user(self, model_admin, make_entry, admin_user):
        entry = make_entry()

        link = model_admin.user_link(entry)

        url = reverse("admin:auth_user_change", args=[admin_user.pk])
        assert link == f'<a href="{url}">admin</a>'

    def test_links_within_its_own_admin_site(self, make_entry, admin_user):
        entry = make_entry()

        link = other_site.get_model_admin(LogEntry).user_link(entry)

        url = reverse("other_admin:auth_user_change", args=[admin_user.pk])
        assert link == f'<a href="{url}">admin</a>'

    @pytest.mark.urls("tests.urls_without_user_admin")
    def test_user_outside_the_admin_is_not_linked(
        self, model_admin, make_entry
    ):
        entry = make_entry()

        assert model_admin.user_link(entry) == "admin"

    def test_username_is_escaped(
        self, model_admin, make_entry, make_staff_user
    ):
        entry = make_entry(user=make_staff_user("<i>me</i>"))

        assert "&lt;i&gt;me&lt;/i&gt;" in model_admin.user_link(entry)


@pytest.mark.parametrize(
    ("action_flag", "description"),
    [(ADDITION, "Addition"), (CHANGE, "Change"), (DELETION, "Deletion")],
)
def test_action_description(model_admin, action_flag, description):
    entry = LogEntry(action_flag=action_flag)

    assert model_admin.action_description(entry) == description
