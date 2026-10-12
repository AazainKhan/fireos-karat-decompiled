# Notice

This repository is independent research for interoperability. It is not affiliated with or endorsed by Amazon.com, Inc. Amazon, Fire TV and Fire OS are trademarks of Amazon.com, Inc. or its affiliates.

What is here:
- Scripts written for this project (MIT, see LICENSE).
- Indexes derived from the Fire OS 8 OTA: package and component names, manifest facts, dependency edges, class names, method and field declarations, and string constants used for integration (intent actions, extras, URIs, settings keys).

What is not here, by design:
- No Amazon APKs, firmware images, decompiled method bodies or source files, resources or artwork.
- No encryption keys.

To reproduce the indexes, use your own copy of the OTA with `scripts/reproduce.sh`. Everything it extracts stays in a git-ignored `.work/` directory.

If you are a rights holder and believe something here should not be, open an issue and it will be removed.
