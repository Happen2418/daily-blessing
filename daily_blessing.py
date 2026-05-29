import smtplib
import requests
import os
from email.mime.text import MIMEText

MIMO_KEY = os.environ["MIMO_KEY"]      # 读取名叫 MIMO_KEY 的变量
QQ_EMAIL = os.environ["QQ_EMAIL"]      # 读取名叫 QQ_EMAIL 的变量
AUTH_CODE = os.environ["AUTH_CODE"]    # 读取名叫 AUTH_CODE 的变量

response = requests.post(
    "https://api.xiaomimimo.com/v1/chat/completions",
    headers={
        "api-key": MIMO_KEY,
        "Content-Type": "application/json"
    },
    json={
        "model": "mimo-v2.5-pro",
        "messages": [
            {
                "role": "user",
                "content": "给女友一个早安祝福，并推荐给她中午吃什么减脂餐，最后署名亲爱的小华华"
            }
        ],
        "max_completion_tokens": 256,
        "temperature": 1.0,
        "stream": False
    }
)

data = response.json()
blessing = data["choices"][0]["message"]["content"]
print("MiMo 说：" + blessing)

msg = MIMEText(blessing, "plain", "utf-8")
msg["Subject"] = "今日早安祝福"
msg["From"] = QQ_EMAIL
msg["To"] = QQ_EMAIL

server = smtplib.SMTP_SSL("smtp.qq.com", 465)
server.login(QQ_EMAIL, AUTH_CODE)
server.send_message(msg)
server.quit()

print("发送成功！")
