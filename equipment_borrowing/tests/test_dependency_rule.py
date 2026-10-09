"""Check that the real source-code imports match the architecture diagram.

Each layer may import only from the layers listed for it. The test reads the
import statements of every module, so a wrong-way import fails here even if
every behaviour test still passes.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1] / "src" / "equipment_borrowing"

ALLOWED_IMPORTS = {
    "domain": {"domain"},
    "application": {"application", "domain"},
    "infrastructure": {"infrastructure", "application", "domain"},
    "interface": {"interface", "application", "infrastructure"},
}


def imported_layers(module: Path) -> set[str]:
    layers = set()
    for node in ast.walk(ast.parse(module.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        elif isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        else:
            continue
        for name in names:
            parts = name.split(".")
            if parts[0] == "equipment_borrowing" and len(parts) > 1:
                layers.add(parts[1])
    return layers


@pytest.mark.parametrize("layer", sorted(ALLOWED_IMPORTS))
def test_each_layer_imports_only_from_the_layers_it_may_depend_on(layer: str) -> None:
    violations = {
        str(module.relative_to(PACKAGE)): sorted(imported_layers(module) - ALLOWED_IMPORTS[layer])
        for module in (PACKAGE / layer).rglob("*.py")
        if imported_layers(module) - ALLOWED_IMPORTS[layer]
    }

    assert violations == {}
