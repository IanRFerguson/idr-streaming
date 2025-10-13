import logging
import os

logger = logging.getLogger("idr_streaming")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

if os.environ.get("DEBUG", "false").lower() == "true":
    logger.setLevel(logging.DEBUG)
    logger.debug("** Debugger Active **")
