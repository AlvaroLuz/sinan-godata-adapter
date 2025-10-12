import logging

# Configuração global do logger
logging.basicConfig(
    level=logging.INFO,  # nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s [%(levelname)s] %(message)s",  # formato da mensagem
)

logger = logging.getLogger(__name__)