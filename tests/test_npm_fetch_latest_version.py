import io
import unittest.mock
from urllib.parse import urlparse

from nix_update.version import fetch_latest_version
from nix_update.version.version import VersionPreference
from tests import conftest


def fake_npm_urlopen(url: str) -> io.BytesIO:
    if url == "https://registry.npmjs.org/@anthropic-ai/claude-code/latest":
        return io.BytesIO(b'{"version": "1.0.43"}')

    if url == "https://registry.npmjs.org/express/latest":
        return io.BytesIO(b'{"version": "4.21.2"}')

    raise ValueError(f"Unexpected URL in test: {url}")  # noqa: EM102, TRY003


def test_scoped_npm(helpers: conftest.Helpers) -> None:
    del helpers
    with unittest.mock.patch("urllib.request.urlopen", fake_npm_urlopen):
        assert (
            fetch_latest_version(
                urlparse(
                    "https://registry.npmjs.org/@anthropic-ai/claude-code/-/claude-code-1.0.42.tgz",
                ),
                VersionPreference.STABLE,
                "(.*)",
            ).number
            == "1.0.43"
        )


def test_regular_npm(helpers: conftest.Helpers) -> None:
    del helpers
    with unittest.mock.patch("urllib.request.urlopen", fake_npm_urlopen):
        assert (
            fetch_latest_version(
                urlparse("https://registry.npmjs.org/express/-/express-4.21.1.tgz"),
                VersionPreference.STABLE,
                "(.*)",
            ).number
            == "4.21.2"
        )
