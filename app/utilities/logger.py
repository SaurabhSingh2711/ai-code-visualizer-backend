import logging

# Configure logging once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Export a logger instance
logger = logging.getLogger("app_logger")
