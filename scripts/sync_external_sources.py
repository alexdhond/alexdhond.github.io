#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, cwd=None):
    subprocess.check_call(cmd, cwd=cwd)


def capture(cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd, text=True).strip()


def copy_item(src_repo_dir: Path, rel_path: str, dest_root: Path, allow_missing: bool):
    src = src_repo_dir / rel_path
    dest = dest_root / rel_path

    if not src.exists():
        msg = f"Missing path in source repo: {rel_path}"
        if allow_missing:
            print(f"[warn] {msg}")
            return
        raise FileNotFoundError(msg)

    dest.parent.mkdir(parents=True, exist_ok=True)

    if src.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def sync_source(source: dict, out_dir: Path, allow_missing: bool):
    name = source["name"]
    repo = source["repo"]
    ref = source.get("ref", "main")
    paths = source["paths"]

    repo_url = f"https://github.com/{repo}.git"

    with tempfile.TemporaryDirectory(prefix=f"sync-{name}-") as tmp:
        tmp_path = Path(tmp)
        clone_dir = tmp_path / name

        run(["git", "clone", "--depth", "1", "--quiet", repo_url, str(clone_dir)])
        run(["git", "checkout", "-q", ref], cwd=clone_dir)

        sha = capture(["git", "rev-parse", "HEAD"], cwd=clone_dir)

        dest_root = out_dir / name
        dest_root.mkdir(parents=True, exist_ok=True)

        for rel_path in paths:
            copy_item(clone_dir, rel_path, dest_root, allow_missing=allow_missing)

        (dest_root / ".source.json").write_text(
            json.dumps(
                {"name": name, "repo": repo, "ref": ref, "sha": sha, "paths": paths},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )


def main():
    parser = argparse.ArgumentParser(description="Sync selected files from external GitHub repos into external/.")
    parser.add_argument("--manifest", default="external-sources.json")
    parser.add_argument("--out", default="external")
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    out_dir = Path(args.out)

    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sources = manifest.get("sources", [])

    if not sources:
        print("No sources configured; nothing to sync.")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)

    for source in sources:
        print(f"[sync] {source['repo']} @ {source.get('ref','main')}")
        sync_source(source, out_dir=out_dir, allow_missing=args.allow_missing)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
