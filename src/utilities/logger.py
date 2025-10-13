import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger("idr_stream")

if os.environ.get("DEBUG", "false").lower() == "true":
    logger.setLevel(logging.DEBUG)
    logger.debug("** Debugger Active **")
