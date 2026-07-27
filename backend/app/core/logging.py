from pathlib import Path
import sys

from loguru import logger

# Project root -> backend/
BASE_DIR = Path(__file__).resolve().parents[2]

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

# Console Logger
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
)

# File Logger
logger.add(
    LOG_DIR / "platform.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG",
)

__all__ = ["logger"]