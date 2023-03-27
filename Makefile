# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
#
# SPDX-License-Identifier: GPL-1.0-or-later

# vim: set ts=4:
PREFIX := /usr
RPMMACRODIR := $(PREFIX)/lib/rpm/macros.d
RPMLUADIR := $(PREFIX)/lib/rpm/lua

install:
	install -Dpm 0644 rpm/macros.d/macros.* -t $(DESTDIR)$(RPMMACRODIR)/
	install -Dpm 0644 rpm/lua/fedora/srpm/*.lua -t $(DESTDIR)$(RPMLUADIR)/fedora/srpm/
