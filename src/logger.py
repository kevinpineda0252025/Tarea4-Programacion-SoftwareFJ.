import logging
import os

def configurar_logger():
    """Configura el sistema de registro (logs) en archivo."""
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s - [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler = logging.FileHandler("logs/sistema.log", encoding="utf-8")
        file_handler.setFormatter(formato)
        logger.addHandler(file_handler)

    return logger
