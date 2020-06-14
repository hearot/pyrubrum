### Documentation

   - Add Sphinx integration and stop using`dataclasses` ([63b3ad54ab218ec41c72cdf65086ff1e07a64200](https://github.com/hearot/pyrubrum/commit/63b3ad54ab218ec41c72cdf65086ff1e07a64200))
   - Add docstrings to `Types` ([9482313b2e8adae5e9271bd7f451413065b94a4a](https://github.com/hearot/pyrubrum/commit/9482313b2e8adae5e9271bd7f451413065b94a4a))
   - Add the Types class to the documentation ([880c52c04e1d3feab948d23fb8651393c9072d37](https://github.com/hearot/pyrubrum/commit/880c52c04e1d3feab948d23fb8651393c9072d37))
   - Automatically copy files from the main directory ([6474feee10ca1dcf1ebc58a49770063f5c931ab9](https://github.com/hearot/pyrubrum/commit/6474feee10ca1dcf1ebc58a49770063f5c931ab9))
   - Update assets ([9d6ca77f936e12b1d851c34ae1ddc39376107063](https://github.com/hearot/pyrubrum/commit/9d6ca77f936e12b1d851c34ae1ddc39376107063))

### Fixes

   - Delete `Menu.preliminary` in favour of the eponymous attribute ([a4023312360a6295f4748dd08349dde99b3805bd](https://github.com/hearot/pyrubrum/commit/a4023312360a6295f4748dd08349dde99b3805bd))
   - Edit documentation for `Menu.default` ([003137fdda1de337e6aa7fb0e81c7fcdfc4337d9](https://github.com/hearot/pyrubrum/commit/003137fdda1de337e6aa7fb0e81c7fcdfc4337d9))
   - Upload correct changelog links to PyPi

### New features

   - Add `PageStyle` for customizing `PageMenu` layouts ([46a14edb7f57d0d5b23f11091c806b5b8e2ada58](https://github.com/hearot/pyrubrum/commit/46a14edb7f57d0d5b23f11091c806b5b8e2ada58))
   - Do not pass parameters to content functions if not supported ([dad5907521d635701cbea12ac736b4f0362e41e6](https://github.com/hearot/pyrubrum/commit/dad5907521d635701cbea12ac736b4f0362e41e6))
   - Import all the public functions ([c0a7deb30fbe75d6b8c37f71dcaaa49ba8b3ab8f](https://github.com/hearot/pyrubrum/commit/c0a7deb30fbe75d6b8c37f71dcaaa49ba8b3ab8f))
   - Import database errors by default ([eb6bb8b5320676e1f474097e3738d54ddddb31e7](https://github.com/hearot/pyrubrum/commit/eb6bb8b5320676e1f474097e3738d54ddddb31e7))
   - Support providing multiple preliminary functions ([3938e308c2176bd280454cdab1875abbae470a28](https://github.com/hearot/pyrubrum/commit/3938e308c2176bd280454cdab1875abbae470a28))
   - Use `None` if parameterization is not supported (resolve #5) ([fd3af3fda4747a6ab4bf5f978bb15e4390aed5d1](https://github.com/hearot/pyrubrum/commit/fd3af3fda4747a6ab4bf5f978bb15e4390aed5d1))

### Other changes

   - Do not restrict callbacks to `Message` and `CallbackQuery` ([ec6bab8600efa7015964a79839046c46a91ebe29](https://github.com/hearot/pyrubrum/commit/ec6bab8600efa7015964a79839046c46a91ebe29))
   - Rename all variables named `tree`to `handler` ([b9acc90cc899cf4c08315a7123017cf8e7169106](https://github.com/hearot/pyrubrum/commit/b9acc90cc899cf4c08315a7123017cf8e7169106))
   - Update version to 0.1a1.dev6 ([477293742e2cc5b238d3bea9503045f2f41f8514](https://github.com/hearot/pyrubrum/commit/477293742e2cc5b238d3bea9503045f2f41f8514))

### ‼️ Breaking changes

   - Add support for having multiple text commands (resolve #4) ([80bfb7d0360091f0e4126b7c4709823e82f1191e](https://github.com/hearot/pyrubrum/commit/80bfb7d0360091f0e4126b7c4709823e82f1191e))
   - Create specific directories for module entities ([25593e6d40fa34dbc47528ff3fa6fdc30c0a41b9](https://github.com/hearot/pyrubrum/commit/25593e6d40fa34dbc47528ff3fa6fdc30c0a41b9))
   - Move `recursive_add` and `transform`to `pyrubrum.tree.node` ([74fa78d207cac97c7f01fcdc562c75b0bc81db7c](https://github.com/hearot/pyrubrum/commit/74fa78d207cac97c7f01fcdc562c75b0bc81db7c))
   - Move `types` to a brand new directory ([7d6b33b3af33a7a69999966aa4caf6728ade7598](https://github.com/hearot/pyrubrum/commit/7d6b33b3af33a7a69999966aa4caf6728ade7598))
   - Preliminary functions are now passed as arguments (resolve #6) ([45687a4a0a2b407b8085ec78d008536bd598897a](https://github.com/hearot/pyrubrum/commit/45687a4a0a2b407b8085ec78d008536bd598897a))
   - Rename `on_callback_node` to `recursive_add` ([461d34e9fb293347ca0b38aa41a18511c25b857c](https://github.com/hearot/pyrubrum/commit/461d34e9fb293347ca0b38aa41a18511c25b857c))
   - `BaseDatabase.get` always returns a string (resolve #2) ([b1d0dac010d2d0cd46a4bcc41d2f07c2099d6ac9](https://github.com/hearot/pyrubrum/commit/b1d0dac010d2d0cd46a4bcc41d2f07c2099d6ac9))
