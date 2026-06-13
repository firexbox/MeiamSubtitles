#!/usr/bin/env python3
"""Linux-compatible packaging script for MeiamSubtitles.

Usage: python3 publish.py <version>
Example: python3 publish.py 1.0.14.1

Creates:
  Release/Jellyfin_v<version>.zip
  Release/Emby_v<version>.zip

Cross-platform: zip entries use forward slashes (works on Linux, macOS, Windows).
"""

import json, os, sys, zipfile
from datetime import datetime, timezone

RELEASE_DIR = "Release"
TEMP_DIR = os.path.join(RELEASE_DIR, "temp_pack")


def update_meta(path: str, version: str, timestamp: str) -> None:
    with open(path) as f:
        meta = json.load(f)
    meta["version"] = version
    meta["timestamp"] = timestamp
    with open(path, "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    print(f"  Updated meta: {path}")


def pack_zip(name: str, src_dir: str) -> str:
    zip_path = os.path.join(RELEASE_DIR, f"{name}_v{version}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src_dir):
            for f in files:
                filepath = os.path.join(root, f)
                arcname = os.path.relpath(filepath, src_dir)
                zf.write(filepath, arcname)
    size = os.path.getsize(zip_path)
    print(f"  Created: {zip_path} ({size:,} bytes)")
    return zip_path


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <version>")
        sys.exit(1)

    global version
    version = sys.argv[1]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.0000000Z")

    print(f"=== Packaging MeiamSubtitles v{version} ===")
    print(f"Timestamp: {timestamp}")

    # Update meta.json files
    update_meta(
        "Jellyfin.MeiamSub.Shooter/meta.json",
        version, timestamp,
    )
    update_meta(
        "Jellyfin.MeiamSub.Thunder/meta.json",
        version, timestamp,
    )

    # Build directory structure
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Jellyfin Shooter
    shooter_dir = os.path.join(
        TEMP_DIR, f"Jellyfin.MeiamSub.Shooter_{version}"
    )
    os.makedirs(shooter_dir, exist_ok=True)
    for f in ["Jellyfin.MeiamSub.Shooter.dll", "meta.json", "thumb.png"]:
        src = os.path.join("Jellyfin.MeiamSub.Shooter", f)
        if f == "Jellyfin.MeiamSub.Shooter.dll":
            src = os.path.join(RELEASE_DIR, f)
        if os.path.exists(src):
            with open(src, "rb") as s, open(os.path.join(shooter_dir, f), "wb") as d:
                d.write(s.read())

    # Jellyfin Thunder
    thunder_dir = os.path.join(
        TEMP_DIR, f"Jellyfin.MeiamSub.Thunder_{version}"
    )
    os.makedirs(thunder_dir, exist_ok=True)
    for f in ["Jellyfin.MeiamSub.Thunder.dll", "meta.json", "thumb.png"]:
        src = os.path.join("Jellyfin.MeiamSub.Thunder", f)
        if f == "Jellyfin.MeiamSub.Thunder.dll":
            src = os.path.join(RELEASE_DIR, f)
        if os.path.exists(src):
            with open(src, "rb") as s, open(os.path.join(thunder_dir, f), "wb") as d:
                d.write(s.read())

    # Emby
    emby_dir = os.path.join(TEMP_DIR, "Emby")
    os.makedirs(emby_dir, exist_ok=True)
    for f in ["Emby.MeiamSub.Shooter.dll", "Emby.MeiamSub.Thunder.dll"]:
        src = os.path.join(RELEASE_DIR, f)
        if os.path.exists(src):
            with open(src, "rb") as s, open(os.path.join(emby_dir, f), "wb") as d:
                d.write(s.read())

    # Create zip archives
    jellyfin_zip = pack_zip("Jellyfin", TEMP_DIR)
    emby_zip = pack_zip("Emby", emby_dir)

    # Cleanup
    import shutil
    shutil.rmtree(TEMP_DIR)
    print("=== Done ===")


if __name__ == "__main__":
    main()
