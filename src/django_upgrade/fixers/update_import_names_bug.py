import ast
from functools import partial
from typing import Iterable, List, Tuple

from tokenize_rt import Offset, Token

from django_upgrade.ast import ast_start_offset, is_rewritable_import_from
from django_upgrade.data import Fixer, State, TokenFunc
from django_upgrade.tokens import (
    OP,
    extract_indent,
    find,
    insert,
    parse_call_args,
    replace,
    update_import_names,
)

fixer = Fixer(
    __name__,
    min_version=(2, 2),
)

MODULE = "django.utils.timezone"
OLD_NAMES = {"c", "d"}


@fixer.register(ast.ImportFrom)
def visit_ImportFrom(
    state: State,
    node: ast.ImportFrom,
    parent: ast.AST,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if (
        node.module == MODULE
        and is_rewritable_import_from(node)
        and any(alias.name in OLD_NAMES for alias in node.names)
    ):
        yield ast_start_offset(node), partial(fix_import_from, node=node)


def fix_import_from(tokens: List[Token], i: int, *, node: ast.ImportFrom) -> None:
    j, indent = extract_indent(tokens, i)
    update_import_names(tokens, i, node=node, name_map={n: "" for n in OLD_NAMES})