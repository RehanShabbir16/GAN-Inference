import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class Config:
    DOWNLOAD_DIR: str = "downloads"
    MAX_WORKERS: int = 4
    CHUNK_SIZE: int = 100000
    MAX_RETRIES: int = 3
    TIMEOUT: int = 300

    @staticmethod
    def load() -> "Config":
        return Config(
            DOWNLOAD_DIR=os.getenv("DOWNLOAD_DIR", Config.DOWNLOAD_DIR),
            MAX_WORKERS=int(os.getenv("MAX_WORKERS", Config.MAX_WORKERS)),
            CHUNK_SIZE=int(os.getenv("CHUNK_SIZE", Config.CHUNK_SIZE)),
            MAX_RETRIES=int(os.getenv("MAX_RETRIES", Config.MAX_RETRIES)),
            TIMEOUT=int(os.getenv("TIMEOUT", Config.TIMEOUT)),
        )
