<!--
A new scriv changelog fragment.

Uncomment the section that is right (remove the HTML comment wrapper).
For top level release notes, leave all the headers commented out.
-->

### Fixed

- Script adapter and Flux interface discovery no longer uses `pkgutil.get_loader` (removed in Python 3.14) or `Loader.load_module` (slated for removal in Python 3.15); the modules are imported with `importlib` instead, so `maestrowf` imports and runs on Python 3.14. Discovery also now returns the classes already registered at import rather than re-executing every adapter module on each call. Fixes [#486](https://github.com/llnl/maestrowf/issues/486) and [#489](https://github.com/llnl/maestrowf/issues/489). Implemented in [PR #TBD](https://github.com/llnl/maestrowf/pull/TBD).

### Maintenance

- CI's pip matrix now covers Python 3.14 and checks that the installed package imports and `maestro --version` runs. Implemented in [PR #TBD](https://github.com/llnl/maestrowf/pull/TBD).
