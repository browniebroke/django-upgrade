from __future__ import annotations

from django_upgrade.data import Settings
from tests.fixers.tools import check_noop, check_transformed

settings = Settings(target_version=(4, 1))


def test_not_deprecated_import():
    check_noop(
        """\
        from django.utils.timezone import get_fixed_timezone
        """,
        settings,
    )


def test_unrecognized_import_format():
    check_noop(
        """\
        from django.utils import timezone

        timezone.utc
        """,
        settings,
    )


def test_already_fixed():
    check_noop(
        """\
        from datetime.timezone import utc
        """,
        settings,
    )


def test_simple():
    check_transformed(
        """\
        from django.utils.timezone import utc
        """,
        """\
        from datetime.timezone import utc
        """,
        settings,
    )


def test_multiple():
    check_transformed(
        """\
        from django.utils.timezone import get_fixed_timezone, utc
        """,
        """\
        from datetime.timezone import utc
        from django.utils.timezone import get_fixed_timezone
        """,
        settings,
    )
