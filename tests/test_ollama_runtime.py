import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.ollama_runtime import find_ollama_binary, _windows_fallback_paths, _unix_fallback_paths


def test_find_ollama_returns_path_when_which_succeeds(tmp_path):
    fake = tmp_path / "ollama"
    fake.write_text("#!/bin/sh\necho hi")
    fake.chmod(0o755)
    with patch("scripts.ollama_runtime.shutil.which", return_value=str(fake)):
        assert find_ollama_binary() == Path(str(fake))


def test_find_ollama_returns_none_when_nothing_found():
    with patch("scripts.ollama_runtime.shutil.which", return_value=None), \
         patch("scripts.ollama_runtime._candidate_fallbacks", return_value=[]):
        assert find_ollama_binary() is None


def test_find_ollama_uses_fallback_when_which_fails(tmp_path):
    fake = tmp_path / "ollama"
    fake.write_text("x")
    fake.chmod(0o755)
    with patch("scripts.ollama_runtime.shutil.which", return_value=None), \
         patch("scripts.ollama_runtime._candidate_fallbacks", return_value=[fake]):
        assert find_ollama_binary() == fake


def test_windows_fallback_paths_contain_localappdata():
    paths = _windows_fallback_paths()
    joined = " ".join(str(p) for p in paths)
    assert "Ollama" in joined


def test_unix_fallback_paths_contain_usr_local():
    paths = _unix_fallback_paths()
    joined = " ".join(str(p) for p in paths)
    assert "/usr/local/bin/ollama" in joined or "/opt/homebrew/bin/ollama" in joined
