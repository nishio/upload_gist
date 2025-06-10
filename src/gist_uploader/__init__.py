"""
gist_uploader
====================
A micro‑library + CLI for one‑off uploads to GitHub Gist.

Usage examples
--------------
Create a new *private* gist from a file:

    python -m gist_uploader path/to/report.md

Pipe JSON from another command and make the gist public:

    some_command | python -m gist_uploader -f data.json --public

Update an existing gist (provide GIST_ID via arg or env):

    python -m gist_uploader summary.txt --gist-id $GIST_ID

Environment variables
---------------------
* ``GITHUB_TOKEN`` or ``GH_TOKEN`` – personal access token with ``gist`` scope.
* ``GIST_ID`` – (optional) ID of a gist to update.

Library API
-----------
``upload_to_gist(content: str, filename: str, token=None, gist_id=None,
                description=None, public=False) -> dict``

Returns the GitHub API response on success or raises ``RuntimeError``.
"""

from ._core import upload_to_gist

__all__ = ["upload_to_gist"]
__version__ = "0.1.0"
