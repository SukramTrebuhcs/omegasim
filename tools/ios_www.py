#!/usr/bin/env python3
"""Build the web bundle embedded by the OmegaSim iOS application."""

import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import app_update  # noqa: E402

TARGET = os.path.join(REPO, "ios", "www")


def main():
    with open(os.path.join(REPO, "app-update.json"), encoding="utf-8") as source:
        manifest = json.load(source)

    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)

    mismatches = []
    for entry in manifest["dateien"]:
        contents = app_update.inhalt(entry["p"])
        if hashlib.sha256(contents).hexdigest() != entry["h"]:
            mismatches.append(entry["p"])

        destination = os.path.join(TARGET, *entry["p"].split("/"))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "wb") as output:
            output.write(contents)

    shutil.copyfile(
        os.path.join(REPO, "app-update.json"),
        os.path.join(TARGET, "app-update.json"),
    )

    if mismatches:
        print(
            "app-update.json does not match the source files; run tools/build.py first: "
            + ", ".join(mismatches[:5]),
            file=sys.stderr,
        )
        return 1

    print(
        "ios/www: %d files, version %s"
        % (len(manifest["dateien"]), manifest["version"])
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
