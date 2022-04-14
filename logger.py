import logging
import logging.handlers
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv(verbose=True)
GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def set_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s][PID:%(process)d][%(module)s][%(funcName)s]%(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        f"log/{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}.log"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    mail_handler = logging.handlers.SMTPHandler(
        ("smtp.gmail.com", 587),
        f"{GMAIL_USERNAME}@gmail.com",
        [f"{GMAIL_USERNAME}@gmail.com",],
        "Logger Test",
        (f"{GMAIL_USERNAME}@gmail.com", GMAIL_PASSWORD),
        [],#TLS
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(mail_handler)
    return logger
