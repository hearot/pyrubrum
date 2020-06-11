### Documentation

   - Add docstrings to `BaseDatabase` ([d3fd9a769e62196f01d3764b87896761bbaf77d6](https://github.com/hearot/pyrubrum/commit/d3fd9a769e62196f01d3764b87896761bbaf77d6))
   - Add docstrings to `BaseHandler` ([455a0a94977c1652b445b623df561f9606a0615e](https://github.com/hearot/pyrubrum/commit/455a0a94977c1652b445b623df561f9606a0615e))
   - Add docstrings to `BaseMenu` ([3a7ad4e3b23bfb85a9faa8c3c056e76abb87b771](https://github.com/hearot/pyrubrum/commit/3a7ad4e3b23bfb85a9faa8c3c056e76abb87b771))
   - Add docstrings to `Button` ([73a0848e8bd7159599d2023d86249f192fde65b4](https://github.com/hearot/pyrubrum/commit/73a0848e8bd7159599d2023d86249f192fde65b4))
   - Add docstrings to `DictDatabase` ([7776cdc6f50e5fdda3774dd4e59a0c7bc81b41d2](https://github.com/hearot/pyrubrum/commit/7776cdc6f50e5fdda3774dd4e59a0c7bc81b41d2))
   - Add docstrings to `RedisDatabase`
   - Add docstrings to all the database exceptions ([0e561554d9d37ef755202cb7ef2905aadbd84700](https://github.com/hearot/pyrubrum/commit/0e561554d9d37ef755202cb7ef2905aadbd84700))
   - Add issue templates ([64c006258e373a97d0a9f83318af02c4310b585b](https://github.com/hearot/pyrubrum/commit/64c006258e373a97d0a9f83318af02c4310b585b))
   - Add the official pronunciation for Pyrubrum ([b6d1fe8e01f79007338cd4a6dfe409c406c12cba](https://github.com/hearot/pyrubrum/commit/b6d1fe8e01f79007338cd4a6dfe409c406c12cba))
   - Create the changelog of the current release separately ([318172a986e666ac4abf6f7a4480922cb135e734](https://github.com/hearot/pyrubrum/commit/318172a986e666ac4abf6f7a4480922cb135e734))
   - Delete duplicate issue templates ([10cba65c31a5c3556b39cc328d097b62dfbd5e1b](https://github.com/hearot/pyrubrum/commit/10cba65c31a5c3556b39cc328d097b62dfbd5e1b))
   - Make relative clauses more formal ([6b0d84effd65838668b3ba070a677d03ce016581](https://github.com/hearot/pyrubrum/commit/6b0d84effd65838668b3ba070a677d03ce016581))
   - Stop using `typing.NewType` and use aliases instead ([600191f337178baf21ea5ffe3e9caaa19dbf22e0](https://github.com/hearot/pyrubrum/commit/600191f337178baf21ea5ffe3e9caaa19dbf22e0))
   - Update the disclaimer notices ([b5039179f28a24ecf967b66200c9440cb6b6c6ec](https://github.com/hearot/pyrubrum/commit/b5039179f28a24ecf967b66200c9440cb6b6c6ec))

### Fixes

   - Add space before reference links ([dfbf7a55f3a7de666703b1dced404d1ce7b0ee7a](https://github.com/hearot/pyrubrum/commit/dfbf7a55f3a7de666703b1dced404d1ce7b0ee7a))
   - Capitalize only the first character of a commit message ([2996f7c91723902b4e998fb94b6d31c60685d386](https://github.com/hearot/pyrubrum/commit/2996f7c91723902b4e998fb94b6d31c60685d386))
   - Do no more raise `TypeError` while formatting commits ([56f1e533c12bdf75e63714d125319bb72da7d916](https://github.com/hearot/pyrubrum/commit/56f1e533c12bdf75e63714d125319bb72da7d916))
   - Fix `commit-message` for Dependabot ([a13cfeae848d83339a902373ddcb0287fc306d87](https://github.com/hearot/pyrubrum/commit/a13cfeae848d83339a902373ddcb0287fc306d87))
   - Hide the sha-1 hash of the current commit ([ab6478e610ef828744d5c6e54a1d54fff92372e8](https://github.com/hearot/pyrubrum/commit/ab6478e610ef828744d5c6e54a1d54fff92372e8))
   - Make databases consistent with the documentation ([d5debbfa52eb16e012ad8e022a5b3d8a06051a59](https://github.com/hearot/pyrubrum/commit/d5debbfa52eb16e012ad8e022a5b3d8a06051a59))

### New features

   - Automatically detect the commit URL for changelog ([a5be95bf1f782bff658552ee4b54552f611409c4](https://github.com/hearot/pyrubrum/commit/a5be95bf1f782bff658552ee4b54552f611409c4))
   - Include the release dates inside changelog ([d4397f396c64eeec6549cd90c64cef6359017dd5](https://github.com/hearot/pyrubrum/commit/d4397f396c64eeec6549cd90c64cef6359017dd5))
   - Integrate Dependabot ([2bb0a43b0f7f8266c7d0544209194c2b26b878a4](https://github.com/hearot/pyrubrum/commit/2bb0a43b0f7f8266c7d0544209194c2b26b878a4))
   - Make parameters optional for `on_callback` and `on_message` ([562f323da2d19913405a5efcfe531e37fa54baf5](https://github.com/hearot/pyrubrum/commit/562f323da2d19913405a5efcfe531e37fa54baf5))
   - Support `datetime.timedelta` as an expire object ([6b3453f5a888fe758f868592c17a88ed1678936f](https://github.com/hearot/pyrubrum/commit/6b3453f5a888fe758f868592c17a88ed1678936f))

### Testing changes

   - Version is now tested to be compliant with PEP 440 ([5f5928bd49e7457d331229440c008665d91647ea](https://github.com/hearot/pyrubrum/commit/5f5928bd49e7457d331229440c008665d91647ea))

### ‼️ Breaking changes

   - Use `abstractmethod` for the methods of base classes ([d5d2edd51cc2137287568a353dd3dc821c29a16c](https://github.com/hearot/pyrubrum/commit/d5d2edd51cc2137287568a353dd3dc821c29a16c))
