# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-1.0-or-later

from __future__ import annotations

import dataclasses
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pytest
import yaml

HERE = Path(__file__).resolve().parent
VECTORS = HERE / "vectors.yaml"
SENTINEL = "*-*" * 20


@dataclasses.dataclass()
class _TestVector:
    # Test id
    id: str
    # Longer description
    description: str | None = None
    # Macros to %define
    defines: list[str] = dataclasses.field(default_factory=list)
    # Macros to %undefine
    undefines: list[str] = dataclasses.field(default_factory=list)
    # String to --eval
    evals: str | list[str] = dataclasses.field(default_factory=lambda: ["%forgemeta"])
    # Whether the tests should fail
    should_fail: bool = False
    # Any stdout
    stdout: str | None = None
    # Any stderr
    stderr: str | None = None
    # Macros that should be set in the end
    expected: dict[str, str] = dataclasses.field(default_factory=dict)
    # Macros that should be unset in the end
    expected_undefined: dict[str, str] = dataclasses.field(default_factory=dict)
    # These macros should be the same with and without a zero at the end
    zero_indexed: list[str] = dataclasses.field(default_factory=list)


def _param(item: dict[str, Any]):
    case = _TestVector(**item)
    return pytest.param(case, id=case.id)


def get_vectors() -> Iterable:
    with VECTORS.open() as fp:
        data = yaml.safe_load(fp)
    for item in data["cases"]:
        if isinstance(item.get("defines"), dict):
            yield _param(item)
            continue
        for index, defines in enumerate(item["defines"]):
            newitem = item | {"id": item["id"] + str(index), "defines": defines}
            yield _param(newitem)


def join_expected(
    lines: list[str], expected: dict[str, str]
) -> tuple[dict[str, str], dict[str, str]]:
    final: dict[str, str] = {}
    expected_expanded: dict[str, str] = {}
    macros = iter(expected)
    out: list[str] = []
    macro = next(macros, ...)
    if macro is ...:
        return final, expected_expanded
    for line in lines:
        if line != SENTINEL:
            out.append(line)
            continue
        if macro in final:
            expected_expanded[macro] = "\n".join(out)
            macro = next(macros, ...)
            if macro is ...:
                break
        else:
            final[macro] = "\n".join(out)
        out.clear()
    assert len(expected) == len(expected_expanded) == len(final)
    return final, expected_expanded


@pytest.mark.parametrize("case", list(get_vectors()))
def test_vectors(case: _TestVector, evaluater):
    expected_macros = case.expected.copy()
    # Handle zero indexed
    for macro in case.zero_indexed:
        name = macro + "0"
        expected_macros[name] = f"%{macro}"
    # Handle expected_undefined
    for macro in case.expected_undefined:
        expected_macros["{!?" + macro + ":UNDEFINED}"] = "UNDEFINED"

    # Set up evals
    evals = [case.evals] if isinstance(case.evals, str) else case.evals.copy()
    evals.append(SENTINEL)
    for macro, expected in expected_macros.items():
        evals.append(f"%{macro}")
        evals.append(SENTINEL)
        evals.append(expected)
        evals.append(SENTINEL)

    # Run commands
    stdout: str
    stderr: str
    stdout, stderr = evaluater(evals, case.defines, case.undefines, case.should_fail)

    lines = stdout.splitlines()
    idx = lines.index(SENTINEL)
    user_stdout = "\n".join(lines[:idx])
    macro_stdout_lines = lines[idx + 1 :]

    # Check case.expected
    final, expected_expanded = join_expected(macro_stdout_lines, expected_macros)
    assert final == expected_expanded

    if case.stdout is not None:
        assert user_stdout == case.stdout.strip()
    if case.stderr is not None:
        assert stderr == case.stderr.strip()
    else:
        # Help debugging
        print(stderr)
