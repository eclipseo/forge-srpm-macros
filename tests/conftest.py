# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
#
# SPDX-License-Identifier: GPL-1.0-or-later

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

PARENT = Path(__file__).resolve().parent.parent
# e.g. MACRO_DIR=%{buildroot}%{_rpmmacrodir} \
#      MACRO_LUA_DIR=%{buildroot}%{_rpmluadir} \
#      pytest
# MACRO_DIR="" MACRO_LUA_DIR="" to only use system paths
MACRO_DIR = Path(os.environ.get("MACRO_DIR", PARENT / "rpm/macros.d"))
MACRO_LUA_DIR = Path(os.environ.get("MACRO_LUA_DIR", PARENT / "rpm/lua"))


@pytest.fixture(scope="session")
def macros_path() -> list[str]:
    if MACRO_DIR == "":
        return []
    path = subprocess.run(
        # Don't judge. It works.
        "rpm --showrc | grep 'Macro path' | awk -F ': ' '{print $2}'",
        shell=True,
        text=True,
        check=True,
        capture_output=True,
    ).stdout.strip()
    return ["--macros", f"{path}:{MACRO_DIR}/macros.*"]


@pytest.fixture(scope="session")
def lua_path() -> list[str]:
    if MACRO_LUA_DIR == "":
        return []
    path = subprocess.run(
        ["rpm", "-E", "%{lua: print(package.path)}"],
        text=True,
        check=True,
        capture_output=True,
    ).stdout.strip()
    path = f"{MACRO_LUA_DIR}/?.lua;{path}"
    return ["-E", "%{lua: package.path = " + repr(path) + "}"]


@pytest.fixture
def evaluater(
    macros_path: list[str], lua_path: list[str]
) -> Callable[..., tuple[str, str]]:
    def runner(
        exps: str | Sequence[str],
        defines: dict[str, str] | None = None,
        undefines: Sequence[str] = (),
        should_fail: bool = False,
    ) -> tuple[str, str]:
        cmd: list[str] = ["rpm", *macros_path, *lua_path]
        defines = defines or {}
        for name, value in defines.items():
            cmd.extend(("--define", f"{name} {value}"))
        for name in undefines:
            cmd.extend(("-E", f"%undefine {name}"))
        if isinstance(exps, str):
            cmd.extend(("-E", exps))
        else:
            for exp in exps:
                cmd.extend(("-E", exp))
        proc = subprocess.run(cmd, text=True, capture_output=True)
        if should_fail:
            assert proc.returncode != 0
        else:
            assert proc.returncode == 0, proc.stderr
        return proc.stdout.strip(), proc.stderr.strip()

    return runner
