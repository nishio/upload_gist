from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from ._core import upload_to_gist


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Upload text/JSON to GitHub Gist.")
    p.add_argument(
        "path",
        nargs="?",
        help="Path of the file to upload. If omitted, read from STDIN.",
    )
    p.add_argument(
        "-f",
        "--filename",
        help="Filename stored in the gist (defaults to basename or stdin.txt).",
    )
    p.add_argument(
        "-d",
        "--description",
        help="Gist description. Uses a timestamp if omitted.",
    )
    p.add_argument("--public", action="store_true", help="Create a *public* gist.")
    p.add_argument("--gist-id", help="Update an existing gist instead of creating new.")
    p.add_argument("--token", help="GitHub token (overrides environment variable).")

    group = p.add_mutually_exclusive_group()
    group.add_argument(
        "--indent",
        type=int,
        metavar="N",
        help="Pretty‑print JSON with indentation N (detects JSON).",
    )
    group.add_argument(
        "--raw-json",
        action="store_true",
        help="Treat input as *raw* JSON and upload minified.",
    )

    return p.parse_args(argv)


def _read_content(path: str | None) -> tuple[str, str]:
    """Return (content, inferred_filename)."""
    if path:
        content = Path(path).read_text()
        filename = Path(path).name
    else:
        content = sys.stdin.read()
        filename = "stdin.txt"
    return content, filename


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    content, default_filename = _read_content(args.path)

    if args.raw_json or args.indent is not None:
        try:
            data = json.loads(content)
            if args.raw_json:
                content = json.dumps(data, separators=(",", ":"))
            else:
                content = json.dumps(data, ensure_ascii=False, indent=args.indent)
        except json.JSONDecodeError:
            print("⚠️  Input is not valid JSON; continuing as plain text.", file=sys.stderr)

    filename = args.filename or default_filename

    try:
        info = upload_to_gist(
            content,
            filename=filename,
            token=args.token,
            gist_id=args.gist_id or os.getenv("GIST_ID"),
            description=args.description,
            public=args.public,
        )
        print(f"✅ Uploaded: {info['html_url']}")
    except Exception as exc:
        print(f"❌ {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
