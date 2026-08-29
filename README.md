# Meteor Client Archive

This repository stores publicly obtainable Meteor Client JAR builds for Minecraft Java Edition. All retained files are under `historical-archive/`; `official-api/` is a temporary staging directory used only during the monthly update job and is removed after each successful run.

The historical collection was sourced from the public Meteor Archive and includes the Meteor Client files present in its archive tree, including extra builds. On the first day of each month, GitHub Actions reads Meteor's official archive page and homepage, downloads the current API builds, moves them into `historical-archive/`, and removes the `official-api/` staging directory. The workflow can also be started manually.

Files use the unique format `mc-<minecraft-version>__meteor-<actual-mod-version>.jar`. The second version is read from the JAR's `fabric.mod.json` (for example, `mc-1.20.4__meteor-0.5.6-1999.jar`), so it is the actual Meteor mod version/build rather than a repeated Minecraft version.

All files in the initial collection were checked as valid JAR/ZIP archives. See `meteor_complete_report.md` and `meteor_complete_results.json` for the initial inventory and SHA-256 values.

> Historical builds are unsupported by Meteor's developers. Use them at your own risk and verify compatibility with your Fabric/Minecraft instance.

## Sources

- Official site: https://meteorclient.com/
- Official archive: https://meteorclient.com/archive
- Download API: https://meteorclient.com/api/download?version={minecraft_version}
- Historical archive: https://maninmyvan.github.io/meteor-archive/
