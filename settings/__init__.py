DB_URI = "mysql+aiomysql://root:1234@127.0.0.1:3306/ainame?charset=utf8mb4"


"qdoykpgfkgnedjee"
# 邮箱相关配置--yaml
MAIL_USERNAME="2440784496@qq.com"
MAIL_PASSWORD="qdoykpgfkgnedjee"
MAIL_FROM="2440784496@qq.com"
MAIL_PORT=587
MAIL_SERVER="smtp.qq.com"
MAIL_FROM_NAME="AiName起名助手"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False

from datetime import timedelta

JWT_SECRET_KEY = "qwertyuiop"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)