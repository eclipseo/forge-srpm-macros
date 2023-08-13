<!--
Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>

SPDX-License-Identifier: GPL-1.0-or-later
-->

# forge-srpm-macros

[![builds.sr.ht status](https://builds.sr.ht/~gotmax23/forge-srpm-macros/commits/main.svg)](https://builds.sr.ht/~gotmax23/forge-srpm-macros/commits/main?)

[![copr build status][badge-copr]][link-copr] (gotmax23/forge-srpm-macros)

[![copr build status][badge-copr-dev]][link-copr-dev] (gotmax23/forge-srpm-macros-dev)

These macros simplify the packaging of forge-hosted projects.
They automatically compute the Source urls based on macros set in the specfile.
This code has been split out from redhat-rpm-config to ease maintenance.

## Links

- [forge-srpm-macros project hub](https://sr.ht/~gotmax23/forge-srpm-macros)
- [forge-srpm-macros git.sr.ht repo](https://git.sr.ht/~gotmax23/forge-srpm-macros)
- [forge-srpm-macros tracker](https://todo.sr.ht/~gotmax23/forge-srpm-macros)
- [forge-srpm-macros mailing list][archives] ([~gotmax/forge-srpm-macros@lists.sr.ht][mailto])

[archives]: https://lists.sr.ht/~gotmax23/forge-srpm-macros
[mailto]: mailto:~gotmax/forge-srpm-macros@lists.sr.ht

## Compatibility

Fedora 37 / RPM 4.18 and above are tested in CI.

These macros do not yet use any RPM 4.18+ features,
but [there are plans][4.17] to adopt newer RPM features that are not available
on older distributions like EL 9.

[4.17]: https://todo.sr.ht/~gotmax23/forge-srpm-macros/3

## Contributing

See [CONTRIBUTING.md](https://git.sr.ht/~gotmax23/forge-srpm-macros/tree/main/item/CONTRIBUTING.md).

## License

This repository is licensed under

    SPDX-License-Identifer: GPL-1.0-or-later

[badge-copr]: https://copr.fedorainfracloud.org/coprs/gotmax23/forge-srpm-macros/package/forge-srpm-macros/status_image/last_build.png
[link-copr]: https://copr.fedorainfracloud.org/coprs/gotmax23/forge-srpm-macros/
[badge-copr-dev]: https://copr.fedorainfracloud.org/coprs/gotmax23/forge-srpm-macros-dev/package/forge-srpm-macros/status_image/last_build.png
[link-copr-dev]: https://copr.fedorainfracloud.org/coprs/gotmax23/forge-srpm-macros-dev/
