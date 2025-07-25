import os
import subprocess

import pytest

from nix_update import main
from tests import conftest


def test_github_feed(helpers: conftest.Helpers) -> None:
    with helpers.testpkgs(init_git=True) as path:
        main(["--file", str(path), "--commit", "github"])
        version = subprocess.run(
            [
                "nix",
                "eval",
                "--raw",
                "--extra-experimental-features",
                "nix-command",
                "-f",
                path,
                "github.version",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        assert tuple(map(int, version.split("."))) >= (8, 5, 2)
        commit = subprocess.run(
            ["git", "-C", path, "log", "-1"],
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        print(commit)
        assert version in commit
        assert "github" in commit
        assert "https://github.com/sharkdp/fd/compare/v8.0.0...v" in commit


@pytest.mark.skipif(
    "GITHUB_TOKEN" not in os.environ,
    reason="No GITHUB_TOKEN environment variable set",
)
def test_github_releases(helpers: conftest.Helpers) -> None:
    with helpers.testpkgs(init_git=True) as path:
        main(["--file", str(path), "--commit", "github", "--use-github-releases"])
        version = subprocess.run(
            [
                "nix",
                "eval",
                "--raw",
                "--extra-experimental-features",
                "nix-command",
                "-f",
                path,
                "github.version",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        assert tuple(map(int, version.split("."))) >= (8, 5, 2)
        commit = subprocess.run(
            ["git", "-C", path, "log", "-1"],
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        print(commit)
        assert version in commit
        assert "github" in commit
        assert "https://github.com/sharkdp/fd/compare/v8.0.0...v" in commit


@pytest.mark.skipif(
    "GITHUB_TOKEN" not in os.environ,
    reason="No GITHUB_TOKEN environment variable set",
)
def test_github_empty_fallback(helpers: conftest.Helpers) -> None:
    with helpers.testpkgs(init_git=True) as path:
        main(["--file", str(path), "--commit", "github-no-release"])
        version = subprocess.run(
            [
                "nix",
                "eval",
                "--raw",
                "--extra-experimental-features",
                "nix-command",
                "-f",
                path,
                "github-no-release.version",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        assert tuple(map(int, version.split("."))) >= (4, 4, 3)
        commit = subprocess.run(
            ["git", "-C", path, "log", "-1"],
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        print(commit)
        assert version in commit
        assert "github" in commit
        assert (
            "https://github.com/ProtonVPN/proton-vpn-gtk-app/compare/v4.3.2...v"
            in commit
        )


def test_github_tag(helpers: conftest.Helpers) -> None:
    with helpers.testpkgs(init_git=True) as path:
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setenv("GITHUB_TOKEN", "invalid_token")
        main(["--file", str(path), "--commit", "github-tag"])
        version = subprocess.run(
            [
                "nix",
                "eval",
                "--raw",
                "--extra-experimental-features",
                "nix-command",
                "-f",
                path,
                "github-tag.version",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        assert tuple(map(int, version.split("."))) >= (8, 5, 2)
        commit = subprocess.run(
            ["git", "-C", path, "log", "-1"],
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        print(commit)
        assert version in commit
        assert "github" in commit
        assert "https://github.com/sharkdp/fd/compare/v8.0.0...v" in commit


def test_github_feed_fallback(helpers: conftest.Helpers) -> None:
    with helpers.testpkgs(init_git=True) as path:
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setenv("GITHUB_TOKEN", "invalid_token")
        main(["--file", str(path), "--commit", "github"])
        version = subprocess.run(
            [
                "nix",
                "eval",
                "--raw",
                "--extra-experimental-features",
                "nix-command",
                "-f",
                path,
                "github.version",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        assert tuple(map(int, version.split("."))) >= (8, 5, 2)
        commit = subprocess.run(
            ["git", "-C", path, "log", "-1"],
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        print(commit)
        assert version in commit
        assert "github" in commit
        assert "https://github.com/sharkdp/fd/compare/v8.0.0...v" in commit


def test_github_fetchtree(helpers: conftest.Helpers) -> None:
    with helpers.testpkgs(init_git=True) as path:
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setenv("GITHUB_TOKEN", "invalid_token")
        main(["--file", str(path), "--commit", "github-fetchtree"])
        version = subprocess.run(
            [
                "nix",
                "eval",
                "--raw",
                "--extra-experimental-features",
                "nix-command fetch-tree",
                "-f",
                path,
                "github-fetchtree.version",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        assert tuple(map(int, version.split("."))) >= (8, 5, 2)
        commit = subprocess.run(
            ["git", "-C", path, "log", "-1"],
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        print(commit)
        assert version in commit
        assert "github" in commit


def test_github_fetchtree_private(helpers: conftest.Helpers) -> None:
    with helpers.testpkgs(init_git=True) as path:
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setenv("GITHUB_TOKEN", "invalid_token")
        main(["--file", str(path), "--commit", "github-fetchtree-private"])
        version = subprocess.run(
            [
                "nix",
                "eval",
                "--raw",
                "--extra-experimental-features",
                "nix-command fetch-tree",
                "-f",
                path,
                "github-fetchtree-private.version",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        assert tuple(map(int, version.split("."))) >= (8, 5, 2)
        commit = subprocess.run(
            ["git", "-C", path, "log", "-1"],
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        print(commit)
        assert version in commit
        assert "github" in commit
