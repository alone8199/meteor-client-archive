# Meteor Client Archive

This repository stores publicly obtainable Meteor Client JAR builds for Minecraft Java Edition. Historical files are under `historical-archive/`; official API downloads are under `official-api/`.

The historical collection was sourced from the public Meteor Archive and includes the Meteor Client files present in its archive tree, including extra builds. The `official-api/` directory is refreshed automatically every Monday by GitHub Actions from Meteor's official archive page, homepage, and download API.

Files are named with the target Minecraft version first, followed by the original Meteor build name. This avoids overwriting builds when multiple Meteor releases target the same Minecraft version.

All files in the initial collection were checked as valid JAR/ZIP archives. See `meteor_complete_report.md` and `meteor_complete_results.json` for the initial inventory and SHA-256 values.

> Historical builds are unsupported by Meteor's developers. Use them at your own risk and verify compatibility with your Fabric/Minecraft instance.

## Sources

- Official site: https://meteorclient.com/
- Official archive: https://meteorclient.com/archive
- Download API: https://meteorclient.com/api/download?version={minecraft_version}
- Historical archive: https://maninmyvan.github.io/meteor-archive/
