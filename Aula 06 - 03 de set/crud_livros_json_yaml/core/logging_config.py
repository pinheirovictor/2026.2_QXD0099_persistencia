import logging
import logging.config
from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING_FILE = BASE_DIR / "logging.yaml"

with open(LOGGING_FILE, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Garante que app.log seja criado na raiz do projeto.
config["handlers"]["file"]["filename"] = str(BASE_DIR / "app.log")

logging.config.dictConfig(config)

logger = logging.getLogger("persistencia_api")
logger.info("Sistema de logging inicializado.")
