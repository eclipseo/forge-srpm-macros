# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
#
# SPDX-License-Identifier: GPL-1.0-or-later

import pytest


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


@pytest.mark.parametrize(
    "forgeurl, tag, sourceurl, topdir",
    [
        pytest.param(
            "https://git.sr.ht/~gotmax23/golang-x-tools",
            "gopls/v0.9.0",
            "{forgeurl}/archive/{tag}.tar.gz#/golang-x-tools-gopls-v0.9.0.tar.gz",
            "golang-x-tools-gopls/v0.9.0",
            id="git.sr.ht",
        ),
        pytest.param(
            "https://github.com/golang/tools",
            "gopls/v0.9.0",
            "{forgeurl}/archive/{tag}/tools-gopls-v0.9.0.tar.gz",
            "tools-gopls-v0.9.0",
            id="github.com",
        ),
        pytest.param(
            "https://gitea.com/gitea/go-sdk",
            "gitea/v0.15.1",
            "{forgeurl}/archive/{tag}.tar.gz#/gitea-v0.15.1.tar.gz",
            "go-sdk",
            id="gitea.com",
        ),
    ],
)
def test_slash_tags(evaluater, forgeurl, tag, sourceurl, topdir):
    # Set a bogus version to make sure it doesn't impact results
    defines = {"forgeurl": forgeurl, "tag": tag, "version": "100.0.2"}
    for key, value in defines.items():
        defines[key] = value.format(**defines)
    out = evaluater(["%forgemeta", "%{forgesource} :: %{forgesetupargs}"], defines)

    sourceurl = sourceurl.format(**defines)
    topdir = topdir.format(**defines)
    assert out[0] == f"{sourceurl} :: -n {topdir}"


@pytest.mark.parametrize(
    "defines, name, ref, distprefix",
    [
        pytest.param(
            {
                "forgeurl": "https://gitlab.com/redhat/centos-stream/rpms/redhat-rpm-config",
                "commit": "446d35133d975f7a4cdc848cfdfa247b5a7f7ab6",
            },
            "redhat-rpm-config",
            "{commit}",
            ".git446d351",
            id="redhat-rpm-config snapshot",
        ),
        pytest.param(
            {
                "forgeurl": "https://gitlab.com/fedora/legal/fedora-license-data",
                "tag": "fedora-license-data-1.16-1",
            },
            "fedora-license-data",
            "{tag}",
            ".gitfedora.license.data.1.16.1",
            id="fedora-license-data tag",
        ),
    ],
)
def test_gitlab_nested(evaluater, defines, name, ref, distprefix):
    """
    Check that tag and commit forgeurls work with nested Gitlab groups
    """
    out = evaluater(
        ["%forgemeta", "%{forgesource} :: %{forgesetupargs} :: %{?distprefix}"], defines
    )
    ref = ref.format(**defines)
    sourceurl = "{forgeurl}/-/archive/{ref}/{name}-{ref}.tar.bz2"
    sourceurl = sourceurl.format(**defines, name=name, ref=ref)
    topdir = "{name}-{ref}".format(**defines, name=name, ref=ref)
    assert out[0] == f"{sourceurl} :: -n {topdir} :: {distprefix}"
