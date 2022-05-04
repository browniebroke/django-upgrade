"""
Replace django.utils.timezone.utc alias to datetime.timezone.utc:
https://docs.djangoproject.com/en/dev/releases/4.1/#deprecated-features-4-1
"""
from __future__ import annotations

import ast
from functools import partial
from typing import Iterable

from tokenize_rt import Offset

from django_upgrade.ast import ast_start_offset, is_rewritable_import_from
from django_upgrade.data import Fixer, State, TokenFunc
from django_upgrade.tokens import update_import_modules

fixer = Fixer(
    __name__,
    min_version=(4, 1),
)


@fixer.register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
        node.module == "django.utils.timezone"
        and is_rewritable_import_from(node)
        and any(alias.name == "utc" for alias in node.names)
    ):
        yield ast_start_offset(node), partial(
            update_import_modules,
            node=node,
            module_rewrites={"utc": "datetime.timezone"},
        )
