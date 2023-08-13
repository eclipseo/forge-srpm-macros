# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-1.0-or-later

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import nox

RELEASERR = "releaserr @ git+https://git.sr.ht/~gotmax23/releaserr"
LINT_SESSIONS = ("static", "formatters", "typing")
PY_FILES = ("tests", "noxfile.py")
YAML_FILES = (".builds", "tests/vectors.yaml")

nox.options.sessions = (*LINT_SESSIONS, "test")

# Helpers


def git(session: nox.Session, *args, **kwargs):
    return session.run("git", *args, **kwargs, external=True)


# General


@nox.session(venv_backend="none")
def lint(session: nox.Session):
    """
    Run python linters
    """
    for notify in LINT_SESSIONS:
        session.notify(notify)


@nox.session
def static(session: nox.Session):
    session.install("ruff", "reuse", "yamllint")
    session.run("ruff", *session.posargs, *PY_FILES)
    session.run("yamllint", *YAML_FILES)
    session.run("reuse", "lint")


@nox.session
def formatters(session: nox.Session, posargs: Sequence[str] | None = None):
    if posargs is None:
        posargs = session.posargs
    session.install("black", "isort")
    session.run("black", *posargs, *PY_FILES)
    session.run("isort", *posargs, *PY_FILES)


@nox.session
def formatters_check(session: nox.Session):
    formatters(session, ["--check"])


@nox.session
def typing(session: nox.Session):
    session.install("mypy", "nox", "pytest", "pyyaml", "types-pyyaml")
    session.run("mypy", *session.posargs, *PY_FILES)


@nox.session
def test(session: nox.Session):
    session.install("pytest", "pyyaml")
    session.run("pytest", *session.posargs)


@nox.session
def srpm(session: nox.Session, posargs: Sequence[str] | None = None):
    session.install("fclogr")
    posargs = posargs or session.posargs
    session.run("fclogr", "--debug", "dev-srpm", *posargs)


@nox.session
def mockbuild(session: nox.Session):
    tmp = Path(session.create_tmp())
    srpm(session, ("-o", str(tmp), "--keep"))
    spec_path = tmp / "fedrq.spec"
    margs = [
        # fmt: off
        "mock",
        "--spec", str(spec_path),
        "--source", str(tmp),
        *session.posargs,
        # fmt: on
    ]
    if not session.interactive:
        margs.append("--verbose")
    session.run(*margs, external=True)


@nox.session
def bump(session: nox.Session):
    version = session.posargs[0]
    session.install(RELEASERR, "fclogr")
    session.run("releaserr", "check-tag", version)
    session.run(
        "fclogr", "bump", "--new", version, "--comment", f"Update to {version}."
    )
    git(session, "add", "forge-srpm-macros.spec")
    session.run("releaserr", "clog", version, "--tag")
