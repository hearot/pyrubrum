# Changelog

## Table of contents

   * [Current version](#Current-version)
   * [v0.1a1.dev4 - 2020-06-09](#v01a1dev4---2020-06-09)
   * [v0.1a1.dev3 - 2020-06-09](#v01a1dev3---2020-06-09)
   * [v0.1a1.dev2 - 2020-06-09](#v01a1dev2---2020-06-09)
   * [v0.1a1.dev1 - 2020-06-09](#v01a1dev1---2020-06-09)
   * [v0.1a1.dev0 - 2020-06-09](#v01a1dev0---2020-06-09)
   * [v0.1a0 - 2020-06-09](#v01a0---2020-06-09)

## Current version

### Documentation

   - Add docstrings to `BaseDatabase` ([d3fd9a769e62196f01d3764b87896761bbaf77d6](https://github.com/hearot/pyrubrum/commit/d3fd9a769e62196f01d3764b87896761bbaf77d6))
   - Add docstrings to `BaseHandler` ([455a0a94977c1652b445b623df561f9606a0615e](https://github.com/hearot/pyrubrum/commit/455a0a94977c1652b445b623df561f9606a0615e))
   - Add docstrings to `BaseMenu` ([3a7ad4e3b23bfb85a9faa8c3c056e76abb87b771](https://github.com/hearot/pyrubrum/commit/3a7ad4e3b23bfb85a9faa8c3c056e76abb87b771))
   - Add docstrings to all the database exceptions
   - Add issue templates ([64c006258e373a97d0a9f83318af02c4310b585b](https://github.com/hearot/pyrubrum/commit/64c006258e373a97d0a9f83318af02c4310b585b))
   - Add the official pronunciation for Pyrubrum ([b6d1fe8e01f79007338cd4a6dfe409c406c12cba](https://github.com/hearot/pyrubrum/commit/b6d1fe8e01f79007338cd4a6dfe409c406c12cba))
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

## v0.1a1.dev4 - 2020-06-09

### Documentation

   - Add a reference to `hitchhiker_bot.py` ([b14423f7586f193a0024d016eb4c98b1e5165ba8](https://github.com/hearot/pyrubrum/commit/b14423f7586f193a0024d016eb4c98b1e5165ba8))
   - Add reference to the changelog ([862839c9cb33c80a512485148c2f132e59ce659b](https://github.com/hearot/pyrubrum/commit/862839c9cb33c80a512485148c2f132e59ce659b))
   - Add the official logo ([d9da10bada6335c1d50c6be9e663259313c5d333](https://github.com/hearot/pyrubrum/commit/d9da10bada6335c1d50c6be9e663259313c5d333))

### Fixes

   - Correct a typo regarding `hitchhiker_bot.py` ([a43bf4bc97e024237a447443be402b5f990384b7](https://github.com/hearot/pyrubrum/commit/a43bf4bc97e024237a447443be402b5f990384b7))
   - Do not use git hooks while generating the changelog ([ef705c3451f8c5b028153664598a4734f4f2a16a](https://github.com/hearot/pyrubrum/commit/ef705c3451f8c5b028153664598a4734f4f2a16a))
   - Generate changelog using the previous commit ([7eecd3ad26d0586077f4a65b443f24b490eda207](https://github.com/hearot/pyrubrum/commit/7eecd3ad26d0586077f4a65b443f24b490eda207))
   - Render sha-1 hashes as links ([415e34c8f467d2f21db47fbfcc2875a3a5a0a8d1](https://github.com/hearot/pyrubrum/commit/415e34c8f467d2f21db47fbfcc2875a3a5a0a8d1))
   - Render sha-1 hashes in a proper way ([0dd5b36883b314c640813fb84635d34937a5d274](https://github.com/hearot/pyrubrum/commit/0dd5b36883b314c640813fb84635d34937a5d274))

### New features

   - Add a changelog generator script ([e2663e2e23ce84415e536cd305661b221431081f](https://github.com/hearot/pyrubrum/commit/e2663e2e23ce84415e536cd305661b221431081f))

### Other changes

   - Update version to 0.1a1.dev4 ([29c4f20d4e91ac89c56d1e491fc4be0fc8b858b0](https://github.com/hearot/pyrubrum/commit/29c4f20d4e91ac89c56d1e491fc4be0fc8b858b0))

### Refactoring

   - Use pre-commit as a local testing system ([8898c9a6409b5e7a37c29024b293ec7799379dc6](https://github.com/hearot/pyrubrum/commit/8898c9a6409b5e7a37c29024b293ec7799379dc6))

### Style changes

   - Reorder classifiers ([2bd2de48916a8ba2c794ad0dac6b9e2d7b3919b8](https://github.com/hearot/pyrubrum/commit/2bd2de48916a8ba2c794ad0dac6b9e2d7b3919b8))

## v0.1a1.dev3 - 2020-06-09

### Fixes

   - Media now support inline keyboards ([d268afedb61b0ebb54d30608e39a599c47a64c6c](https://github.com/hearot/pyrubrum/commit/d268afedb61b0ebb54d30608e39a599c47a64c6c))

### New features

   - Add an example for sending media ([5bc4aae9b3e35d8e3940a2a1961a60e3dd307879](https://github.com/hearot/pyrubrum/commit/5bc4aae9b3e35d8e3940a2a1961a60e3dd307879))
   - `InputMedia`is now allowed to be sent as message ([5c054ea9f7eaaabc5af0f0625c5475681d1e1fce](https://github.com/hearot/pyrubrum/commit/5c054ea9f7eaaabc5af0f0625c5475681d1e1fce))

### Other changes

   - Update version to 0.1a1.dev3 ([0459153cd238bf3d73318e5908c418bf35523fbe](https://github.com/hearot/pyrubrum/commit/0459153cd238bf3d73318e5908c418bf35523fbe))

## v0.1a1.dev2 - 2020-06-09

### Build changes

   - Ignore `ModuleNotFound` error ([b80d94254de8445345bcdcec82f41a3128cf6887](https://github.com/hearot/pyrubrum/commit/b80d94254de8445345bcdcec82f41a3128cf6887))

### Documentation

   - Add branding information ([b64560b5bdaceaf7ea89963c1aa54161bc4ee0eb](https://github.com/hearot/pyrubrum/commit/b64560b5bdaceaf7ea89963c1aa54161bc4ee0eb))
   - Add versioning specification & thanks ([e9832c2adcaf2854af8e64af9512edcc6dce7b89](https://github.com/hearot/pyrubrum/commit/e9832c2adcaf2854af8e64af9512edcc6dce7b89))
   - Refer only to Telegram bots page ([8ec71abbee5425a880fa0a27ba543370ceaaa412](https://github.com/hearot/pyrubrum/commit/8ec71abbee5425a880fa0a27ba543370ceaaa412))

### Other changes

   - Update version to 0.1a1.dev2 ([24e68eb18a2691f88938bdf30d1caa90216cfb07](https://github.com/hearot/pyrubrum/commit/24e68eb18a2691f88938bdf30d1caa90216cfb07))

## v0.1a1.dev1 - 2020-06-09

### Build changes

   - Redis is now not installed by default ([bedaa03da1635c9d52765dc6de67d77758b556e0](https://github.com/hearot/pyrubrum/commit/bedaa03da1635c9d52765dc6de67d77758b556e0))

### Other changes

   - Update version to 0.1a1.dev1 ([068ae25d49632d11082ddc9c2f539ecca5f512ec](https://github.com/hearot/pyrubrum/commit/068ae25d49632d11082ddc9c2f539ecca5f512ec))

## v0.1a1.dev0 - 2020-06-09

### ‼️ Breaking changes

   - Rename handlers & menus ([22eec554399fe3f250b414f79c45f5af9b9dd2b0](https://github.com/hearot/pyrubrum/commit/22eec554399fe3f250b414f79c45f5af9b9dd2b0))

## v0.1a0 - 2020-06-09

### New features

   - A callable object is now supported ([1ce23a93f26813ba686e08ec66d1eeaae25acfbf](https://github.com/hearot/pyrubrum/commit/1ce23a93f26813ba686e08ec66d1eeaae25acfbf))
   - Add Action ([b41f03ab0d47b628ee42dfeeacc0b58684fc37b6](https://github.com/hearot/pyrubrum/commit/b41f03ab0d47b628ee42dfeeacc0b58684fc37b6))
   - Add BaseDatabase & DictDatabase ([ce59115815025a18f41388b1735bbca789675aef](https://github.com/hearot/pyrubrum/commit/ce59115815025a18f41388b1735bbca789675aef))
   - Add CalendarBot ([f640efb16aa7c59cc39bfedc62e532292f347cdb](https://github.com/hearot/pyrubrum/commit/f640efb16aa7c59cc39bfedc62e532292f347cdb))
   - Add ParameterizedTreeHandler and ParameterizedHandler ([823a0436e3b6c8e75a0710f67b420d4810fff808](https://github.com/hearot/pyrubrum/commit/823a0436e3b6c8e75a0710f67b420d4810fff808))
   - Add SampleBot & README.md ([f4838f8f80eac5f41ef6f234160c86524b339402](https://github.com/hearot/pyrubrum/commit/f4838f8f80eac5f41ef6f234160c86524b339402))
   - Add TreeHandler and TreeMenu ([bfec481b41e791809d82ca9e75620f94c9ace45c](https://github.com/hearot/pyrubrum/commit/bfec481b41e791809d82ca9e75620f94c9ace45c))
   - Add a blank line to README.md ([6338308089c46b08dc301b646e28579e0d63af92](https://github.com/hearot/pyrubrum/commit/6338308089c46b08dc301b646e28579e0d63af92))
   - Add subtitle ([82dd5f08f7a0c7eeb10d11e7c576630fd804b58c](https://github.com/hearot/pyrubrum/commit/82dd5f08f7a0c7eeb10d11e7c576630fd804b58c))
   - Add support for paging ([87af4882d5b89a293332a3ff31d614d9dfab40ac](https://github.com/hearot/pyrubrum/commit/87af4882d5b89a293332a3ff31d614d9dfab40ac))
   - Add unique_id ([334d5a0576d9ecf383115399b83a7aab7b5f116e](https://github.com/hearot/pyrubrum/commit/334d5a0576d9ecf383115399b83a7aab7b5f116e))
   - Add versioning, change name to 'pyrubrum' & update setup.py ([5174a672e6322eeccc3744a3b3e49c5faaa7d707](https://github.com/hearot/pyrubrum/commit/5174a672e6322eeccc3744a3b3e49c5faaa7d707))
   - Delete Button.set_name ([4624a2cc66b5b236918130a3a6ec16e685ea63da](https://github.com/hearot/pyrubrum/commit/4624a2cc66b5b236918130a3a6ec16e685ea63da))
   - Delete blank lines from README.md ([5609d2383a49dfc36c2d8a547f5f3e03e7fea153](https://github.com/hearot/pyrubrum/commit/5609d2383a49dfc36c2d8a547f5f3e03e7fea153))
   - Fix classifiers ([051564e3460d44fb17d95718fa86b94044512c1e](https://github.com/hearot/pyrubrum/commit/051564e3460d44fb17d95718fa86b94044512c1e))
   - Implement parameters using JSON ([0b848266fd45f99dad3910313b8ec61943502b6b](https://github.com/hearot/pyrubrum/commit/0b848266fd45f99dad3910313b8ec61943502b6b))
   - Implement the propagation of parameters ([0a128c99358d918d3f379449ee352b1d4193354a](https://github.com/hearot/pyrubrum/commit/0a128c99358d918d3f379449ee352b1d4193354a))
   - Iterables are now supported as dictionary values ([4052f630ad7ef30def4586db952b02b132277d8d](https://github.com/hearot/pyrubrum/commit/4052f630ad7ef30def4586db952b02b132277d8d))
   - Rename Action to Element & id to element_id ([b187e00933139b5e98dff0922f080ec80f387de4](https://github.com/hearot/pyrubrum/commit/b187e00933139b5e98dff0922f080ec80f387de4))
   - Stop using keyword-arguments, use a dictionary instead ([a3b4ccb70bdacb2e50d6859b8095dd8996e589e8](https://github.com/hearot/pyrubrum/commit/a3b4ccb70bdacb2e50d6859b8095dd8996e589e8))
   - Stop using regex ([2cd8e969c90b3dd425164ee1a107fb12148f4079](https://github.com/hearot/pyrubrum/commit/2cd8e969c90b3dd425164ee1a107fb12148f4079))
   - Support Redis ([8756a59b3214f676aad4ead76ec8f071c4dc4418](https://github.com/hearot/pyrubrum/commit/8756a59b3214f676aad4ead76ec8f071c4dc4418))
   - Update README.md (fix markdown issues) ([772f745351b1f494cfe57cb814315c6533b61f98](https://github.com/hearot/pyrubrum/commit/772f745351b1f494cfe57cb814315c6533b61f98))
