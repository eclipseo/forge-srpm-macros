# SPDX-License-Identifier: MIT
# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>

%bcond tests 1

Name:           forge-srpm-macros
Version:        0.0.1
Release:        0%{?dist}
Summary:        Macros to simplify packaging of forge-hosted projects

License:        GPL-1.0-or-later
URL:            https://git.sr.ht/~gotmax23/forge-rpm-macros
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  make
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-pyyaml
# For %%pytest definition
BuildRequires:  python3-rpm-macros
%endif
# We require macros and lua defined in redhat-rpm-config
# We constrain this to the version released after the code was split out that
# doesn't contain the same files.

# TODO: Replace with actual verion where the macros were split out
# Requires:       redhat-rpm-config >= XXX
Requires:       redhat-rpm-config


%description
%{summary}.


%prep
%autosetup -n %{name}-v%{version}


%install
%make_install RPMMACRODIR=%{_rpmmacrodir} RPMLUADIR=%{_rpmluadir}


%check
%if %{with tests}
export MACRO_DIR=%{buildroot}%{_rpmmacrodir}
export MACRO_LUA_DIR="%{buildroot}/usr/lib/rpm/lua"
%pytest
%endif


%files
%license LICENSES/GPL-1.0-or-later.txt
%doc README.md
%{_rpmmacrodir}/macros.forge
%{_rpmluadir}/fedora/srpm/forge.lua


%changelog
