from django_upgrade.data import Settings
from tests.fixers.tools import check_noop, check_transformed

settings = Settings(target_version=(2, 2))


def test_name_import_erased_other_order():
    check_transformed(
        """\
        from django.utils.timezone import b, c, d
        """,
        """\
        from django.utils.timezone import b
        """,
        settings,
    )