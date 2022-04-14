import logging
import logging.handlers
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv(verbose=True)
GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
KAKAO_TOKEN = os.getenv("KAKAO_TOKEN")


class KakaoHandler(logging.handlers.HTTPHandler):
    def __init__(self, token):
        super().__init__(host='kapi.kakao.com', 
                        url='/v2/api/talk/memo/default/send',
                        secure=True)
        self.token = token

    def emit(self, record):
        try:
            import requests
            url = f"https://{self.host}{self.url}"
            header = {"Content-type":"application/x-www-form-urlencoded",'Authorization': f'Bearer {self.token}'}
            data = self.mapLogRecord(record)
            res = requests.post(url, data=data, headers = header)
    
        except Exception:
            self.handleError(record)

    def mapLogRecord(self, record):
        if self.formatter is None:  # Formatter가 설정되지 않은 경우
            text = record.msg
        else:
            text = self.formatter.format(record)

        return {"template_object":'{"object_type": "text",  "text": "'+text+'",  "link": {"web_url": "http://103.22.220.149:55555", "mobile_web_url": "http://103.22.220.149:55555" },  "button_title": "바로 확인" }'}

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

    kakao_handler = KakaoHandler(KAKAO_TOKEN)
    kakao_handler.setLevel(logging.ERROR)
    kakao_handler.setFormatter(formatter) 
    
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(kakao_handler)
    logger.addHandler(mail_handler)
    
    return logger
