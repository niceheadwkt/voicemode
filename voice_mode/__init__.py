"""
voice-mode - Voice interaction capabilities for Model Context Protocol (MCP) servers

This package provides MCP servers for voice interactions through multiple transports:
- Local microphone recording and playback
- LiveKit room-based voice communication
- Configurable OpenAI-compatible STT/TTS services
"""

import os
import platform
from collections import namedtuple

# Windows compat polyfill for os.uname()
if not hasattr(os, "uname"):
    UnameResult = namedtuple("UnameResult", ["sysname", "nodename", "release", "version", "machine"])
    def dummy_uname():
        # Avoid recursion by not calling platform functions that call os.uname()
        arch = os.environ.get("PROCESSOR_ARCHITECTURE", "AMD64").lower()
        if arch == "arm64":
            machine = "arm64"
        else:
            machine = "x86_64"
        return UnameResult(
            sysname="Windows",
            nodename=os.environ.get("COMPUTERNAME", "localhost"),
            release="10",
            version="",
            machine=machine
        )
    os.uname = dummy_uname

# Monkeypatch subprocess to always default to UTF-8 when text=True on Windows
if platform.system() == "Windows":
    import subprocess
    _orig_run = subprocess.run
    _orig_Popen = subprocess.Popen

    def _patched_run(*args, **kwargs):
        if (kwargs.get("text") or kwargs.get("universal_newlines")) and "encoding" not in kwargs:
            kwargs["encoding"] = "utf-8"
        return _orig_run(*args, **kwargs)

    class _PatchedPopen(_orig_Popen):
        def __init__(self, *args, **kwargs):
            if (kwargs.get("text") or kwargs.get("universal_newlines")) and "encoding" not in kwargs:
                kwargs["encoding"] = "utf-8"
            super().__init__(*args, **kwargs)

    subprocess.run = _patched_run
    subprocess.Popen = _PatchedPopen

from .version import __version__

# DJ module - background music playback for voice sessions
from .dj import (
    # Core playback
    DJController,
    TrackStatus,
    CommandResult,
    MpvPlayer,
    MpvBackend,
    SocketBackend,
    # MFP integration
    MfpService,
    MfpEpisode,
    RssFetcher,
    HttpFetcher,
    # Chapter handling
    Chapter,
    convert_cue_to_ffmetadata,
    convert_cue_file,
    parse_cue_content,
    get_chapter_count,
    # Music library
    MusicLibrary,
    Track,
    LibraryStats,
    FileScanner,
)

__all__ = [
    "__version__",
    # DJ Core
    "DJController",
    "TrackStatus",
    "CommandResult",
    "MpvPlayer",
    "MpvBackend",
    "SocketBackend",
    # DJ MFP
    "MfpService",
    "MfpEpisode",
    "RssFetcher",
    "HttpFetcher",
    # DJ Chapters
    "Chapter",
    "convert_cue_to_ffmetadata",
    "convert_cue_file",
    "parse_cue_content",
    "get_chapter_count",
    # DJ Library
    "MusicLibrary",
    "Track",
    "LibraryStats",
    "FileScanner",
]