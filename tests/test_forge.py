# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
#
# SPDX-License-Identifier: GPL-1.0-or-later

import pytest


def test_github_forgesource_simple(evaluater):
    """
    Ensure that a simple Github repository works as expected
    """
    forgeurl = "https://github.com/ansible/ansible"
    defines = {"forgeurl": forgeurl, "version": "2.14.0"}

    out = evaluater(["%forgemeta", "%forgesource"], defines)
    expected = f"{forgeurl}/archive/v2.14.0/ansible-2.14.0.tar.gz"
    assert out[0] == expected


@pytest.mark.parametrize(
    "archiveext", [pytest.param(None), pytest.param("tar.bz2"), pytest.param("tar.gz")]
)
def test_gitlab_forgesource_archiveext(archiveext, evaluater):
    """
    Ensure that a simple Gitlab repository works as expected.
    Test custom %{archiveext} and ensure that tar.bz2 is the default.
    """
    forgeurl = "https://gitlab.com/fdroid/fdroidclient"
    defines = {"version": "1.16.2", "forgeurl": forgeurl}
    if archiveext:
        defines["archiveext"] = archiveext
    else:
        archiveext = "tar.bz2"
    out = evaluater(["%forgemeta", "%forgesource"], defines)

    sourceurl = f"{forgeurl}/-/archive/1.16.2/fdroidclient-1.16.2.{archiveext}"
    assert out[0] == sourceurl


def test_sourcehut_v(evaluater):
    """
    Ensure that a v-prefixed sourcehut repository works as expected.
    Check that zero indexing works and ensure that distprefix isn't set.
    """
    forgeurl = "https://git.sr.ht/~gotmax23/fedrq"
    defines = {
        "forgeurl": forgeurl,
        "version": "0.5.0",
        "tag": "v%{version}",
    }
    out = evaluater(
        [
            "%forgemeta",
            # Check that zero indexing works properly
            "%{forgesource} :: %{forgesource0} :: "
            "%{!?distprefix:nil} :: %{!?distprefix0:nil} :: "
            "%{forgesetupargs} :: %{forgesetupargs0}",
        ],
        defines,
    )

    sourceurl = f"{forgeurl}/archive/v0.5.0.tar.gz#/fedrq-0.5.0.tar.gz"
    expected = (
        f"{sourceurl} :: {sourceurl} :: "
        "nil :: nil :: "
        "-n fedrq-v0.5.0 :: -n fedrq-v0.5.0"
    )
    assert out[0] == expected


def test_github_commit(evaluater):
    forgeurl = "https://github.com/ansible/ansible"
    commit = "520bb66f8ab6d53750f48f024287572962d975fa"
    defines = {"forgeurl": forgeurl, "version": "2.14.0", "commit": commit}
    out = evaluater(
        [
            "%forgemeta",
            # Check that zero indexing works properly
            "%{forgesource} :: %{forgesource0} :: "
            "%{distprefix} :: %{distprefix0} :: "
            "%{forgesetupargs} :: %{forgesetupargs0}",
        ],
        defines,
    )

    sourceurl = f"{forgeurl}/archive/{commit}/ansible-{commit}.tar.gz"
    expected = (
        f"{sourceurl} :: {sourceurl} :: "
        ".git520bb66 :: .git520bb66 :: "
        f"-n ansible-{commit} :: -n ansible-{commit}"
    )
    assert out[0] == expected
