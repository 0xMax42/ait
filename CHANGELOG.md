# Changelog

All notable changes to this project will be documented in this file.

## [unreleased]

### 📚 Documentation

- Update README project time badge URL - ([b08567a](https://git.0xmax42.io/maxp/ait/commit/b08567a8ad2b77975997738dd833fbca9ef0ebe9))

### ⚙️ Miscellaneous Tasks

- *(ci)* Set gitea env vars for release asset upload - ([480e076](https://git.0xmax42.io/maxp/ait/commit/480e0769f398a55c7d1bd390b820ceef21fed8ac))
- *(ci)* Use python 3.13 in release workflow - ([8619fe4](https://git.0xmax42.io/maxp/ait/commit/8619fe49a7ebd4365ce8d65a7946dfdbef379bfb))
- *(debian)* Add python3.11 package and fix architectures - ([1eacb6f](https://git.0xmax42.io/maxp/ait/commit/1eacb6f659aa67996c081d63c3dc53f9972051df))
- *(ci)* Drop debcrafter dependency from wheel release job - ([1a5fbd3](https://git.0xmax42.io/maxp/ait/commit/1a5fbd3a55f047efcddecf275ad94bfcf9af11a6))
- *(ci)* Simplify release workflows and remove nightly tooling - ([c7b4be8](https://git.0xmax42.io/maxp/ait/commit/c7b4be8e339424c8eab6e72d6e258f50188bb694))
- *(debian)* Add packaging configuration for debcrafter and dh-virtualenv - ([c608aa3](https://git.0xmax42.io/maxp/ait/commit/c608aa33abe3d2cd6ef60b480c433281e5013185))

## [0.3.0](https://git.0xmax42.io/maxp/ait/compare/v0.2.0..v0.3.0) - 2026-01-04

### 🚀 Features

- *(ait)* Support advanced git args, custom base URL and debug output - ([8487d8a](https://git.0xmax42.io/maxp/ait/commit/8487d8ac21461921b637ed7d8523d1958e2a7484))
- Add clipboard export option via wl-copy and config - ([4a86c46](https://git.0xmax42.io/maxp/ait/commit/4a86c4671160ddc610f500ffc4fc38e23314f5a9))
- Add context file and repo tree snapshot support - ([bdadc77](https://git.0xmax42.io/maxp/ait/commit/bdadc77187fc0e5df593d85d8dfa0bd64d35ee6f))

### 🐛 Bug Fixes

- Enable recursive tree listing with git ls-tree - ([26c29bc](https://git.0xmax42.io/maxp/ait/commit/26c29bc00462f388c2e4d46fc36a6a29f72ba77c))
- Update context markdown file naming convention - ([f0d8360](https://git.0xmax42.io/maxp/ait/commit/f0d8360fe5d0cc562df1411bb62e79fbdae4a5f4))

### ⚙️ Miscellaneous Tasks

- Remove changelog configuration file - ([eefbac9](https://git.0xmax42.io/maxp/ait/commit/eefbac9cbffb7b41e4531dcd2b9aa14beaaf80cf))
- *(ci)* Update release token to use secrets for deployment - ([c7fec60](https://git.0xmax42.io/maxp/ait/commit/c7fec60f8f5f2a6809a9699f24497cd9be78d0b2))

## [0.2.0](https://git.0xmax42.io/maxp/ait/compare/v0.1.0..v0.2.0) - 2025-12-18

### 🚀 Features

- Add support for max_completion_tokens argument - ([34d0f46](https://git.0xmax42.io/maxp/ait/commit/34d0f46510a8b08215ea24604e6f7c216b1f63c1))
- *(workflows)* Add release sync to GitHub and clean up - ([8d5f168](https://git.0xmax42.io/maxp/ait/commit/8d5f168a10e674effe27aab69d348c52f3f8a58f))
- *(workflows)* Add Gitea integration to sync action - ([81b2339](https://git.0xmax42.io/maxp/ait/commit/81b2339ea6d67a73dd62fb67b41db60388750610))
- *(workflows)* Add GitHub release sync workflow - ([e478576](https://git.0xmax42.io/maxp/ait/commit/e4785769eac1dae3945a388dd745fa43555ea4da))
- *(workflows)* Add GitHub release sync workflow - ([8b3117f](https://git.0xmax42.io/maxp/ait/commit/8b3117fdca5c9cd20cfb9ac3cfe0b0f1ee5f9656))

### 🐛 Bug Fixes

- *(workflows)* Correct token syntax in releases sync action - ([de05716](https://git.0xmax42.io/maxp/ait/commit/de05716b072f81351c603d82dafa17ee751b3dad))

### ⚙️ Miscellaneous Tasks

- *(ci)* Remove support for overriding release tag input - ([7deb7ca](https://git.0xmax42.io/maxp/ait/commit/7deb7cab92090be2fe624b8ce0a2131c92632d67))
- *(workflows)* Improve git-cliff installation and tagging - ([aa25ceb](https://git.0xmax42.io/maxp/ait/commit/aa25ceb957a07a5267bfd53dea8c58827c9c6840))
- *(workflows)* Enable release event handling in sync-github - ([e875e78](https://git.0xmax42.io/maxp/ait/commit/e875e781a73349e6ac7092e3c599bdfb2526e08e))
- *(workflows)* Remove unnecessary checkout step - ([45a6113](https://git.0xmax42.io/maxp/ait/commit/45a61134d6f8112c710fa1acdfb8c6205da287b4))

### 📦 Dependencies

- *(deps)* Update lockfile - ([e9aaec5](https://git.0xmax42.io/maxp/ait/commit/e9aaec5e274d3242759422ecbdfa05f899b4c36e))
- *(deps)* Update Python version requirement to >=3.11 - ([7c8b1f4](https://git.0xmax42.io/maxp/ait/commit/7c8b1f4dbffd0dfd3cd070ffab67da6f8a6cc313))

## [0.1.0] - 2025-05-24

### 🚀 Features

- Add project structure and dependency management - ([a9ed247](https://git.0xmax42.io/maxp/ait/commit/a9ed247cb486cfc22779da9d6ab2db15f25dc1e6))
- *(ci)* Add automated workflows for releases and nightly builds - ([579c70b](https://git.0xmax42.io/maxp/ait/commit/579c70b784d551426e841253a6d1de4cc53d65bd))

### ⚙️ Miscellaneous Tasks

- *(vscode)* Customize activity bar and peacock colors - ([db8fda1](https://git.0xmax42.io/maxp/ait/commit/db8fda15df7b6a08dbd8eb4167e9b4862712392e))


