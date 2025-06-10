from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Optional

import requests

API_URL = "https://api.github.com/gists"


def upload_to_gist(
    content: str,
    *,
    filename: str,
    token: str | None = None,
    gist_id: str | None = None,
    description: str | None = None,
    public: bool = False,
) -> dict | None:
    """Create or update a GitHub Gist.

    Parameters
    ----------
    content : str
        File content to upload (plain text or JSON string).
    filename : str
        File name that will appear in the gist.
    token : str, optional
        GitHub personal access token; falls back to ``GITHUB_TOKEN``/``GH_TOKEN``.
    gist_id : str, optional
        If provided, the existing gist is *patched* instead of creating a new one.
    description : str, optional
        Short description; timestamped default is used if omitted.
    public : bool, default ``False``
        ``True`` for a public gist, ``False`` for secret.

    Returns
    -------
    dict | None
        Parsed JSON response when successful.

    Raises
    ------
    RuntimeError
        On missing token or HTTP error.
    """

    token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise RuntimeError("GitHub token not provided. Set GITHUB_TOKEN or GH_TOKEN.")

    if description is None:
        description = (
            "Uploaded with gist_uploader - "
            + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        )

    payload = {
        "description": description,
        "public": bool(public),
        "files": {filename: {"content": content}},
    }

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": f"gist_uploader/{__import__('gist_uploader').__version__}",
    }

    if gist_id:
        url = f"{API_URL}/{gist_id}"
        resp = requests.patch(url, json=payload, headers=headers, timeout=30)
    else:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)

    if resp.status_code in (200, 201):
        return resp.json()

    raise RuntimeError(f"GitHub API error {resp.status_code}: {resp.text}")
