#!/usr/bin/bash -x
# Copyright (C) 2023 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-1.0-or-later

set -euo pipefail

for i in fedora/37 fedora/38; do
    file=".builds/$(echo $i | cut -d/ -f2).yml"
    sed "s|@@IMAGE@@|$i|" ci.yml.in >$file
done
