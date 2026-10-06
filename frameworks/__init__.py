"""
Verification Frameworks Package

Contains battle-tested verification tools developed through
AI agent collaboration in the AI Village.
"""

__version__ = "1.0.0"
__author__ = "AI Village Agents"
__license__ = "MIT"

from .wave.wave_verifier import WaveVerifier
from .archival.archival_verifier import ArchivalVerifier
from .protocol.cold_verification_protocol import ColdVerificationProtocol

__all__ = [
    "WaveVerifier",
    "ArchivalVerifier", 
    "ColdVerificationProtocol",
]
