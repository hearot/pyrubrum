### Fixes

   - Delete `Menu.preliminary` in favour of the eponymous attribute ([a4023312360a6295f4748dd08349dde99b3805bd](https://github.com/hearot/pyrubrum/commit/a4023312360a6295f4748dd08349dde99b3805bd))

### New features

   - Do not pass parameters to content functions if not supported
   - Import all the public functions ([c0a7deb30fbe75d6b8c37f71dcaaa49ba8b3ab8f](https://github.com/hearot/pyrubrum/commit/c0a7deb30fbe75d6b8c37f71dcaaa49ba8b3ab8f))
   - Import database errors by default ([eb6bb8b5320676e1f474097e3738d54ddddb31e7](https://github.com/hearot/pyrubrum/commit/eb6bb8b5320676e1f474097e3738d54ddddb31e7))
   - Support providing multiple preliminary functions ([3938e308c2176bd280454cdab1875abbae470a28](https://github.com/hearot/pyrubrum/commit/3938e308c2176bd280454cdab1875abbae470a28))
   - Use `None` if parameterization is not supported (resolve #5) ([fd3af3fda4747a6ab4bf5f978bb15e4390aed5d1](https://github.com/hearot/pyrubrum/commit/fd3af3fda4747a6ab4bf5f978bb15e4390aed5d1))

### Other changes

   - Rename all variables named `tree`to `handler` ([b9acc90cc899cf4c08315a7123017cf8e7169106](https://github.com/hearot/pyrubrum/commit/b9acc90cc899cf4c08315a7123017cf8e7169106))
   - Update version to 0.1a1.dev6 ([477293742e2cc5b238d3bea9503045f2f41f8514](https://github.com/hearot/pyrubrum/commit/477293742e2cc5b238d3bea9503045f2f41f8514))

### ‼️ Breaking changes

   - Create specific directories for module entities ([25593e6d40fa34dbc47528ff3fa6fdc30c0a41b9](https://github.com/hearot/pyrubrum/commit/25593e6d40fa34dbc47528ff3fa6fdc30c0a41b9))
   - Preliminary functions are now passed as arguments (resolve #6) ([45687a4a0a2b407b8085ec78d008536bd598897a](https://github.com/hearot/pyrubrum/commit/45687a4a0a2b407b8085ec78d008536bd598897a))
   - `BaseDatabase.get` always returns a string (resolve #2) ([b1d0dac010d2d0cd46a4bcc41d2f07c2099d6ac9](https://github.com/hearot/pyrubrum/commit/b1d0dac010d2d0cd46a4bcc41d2f07c2099d6ac9))
