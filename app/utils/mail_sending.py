from fastapi_mail import ConnectionConfig
import random
import string

conf = ConnectionConfig(
    MAIL_USERNAME="duynguyen1211204@gmail.com",
    MAIL_PASSWORD="mlfxqfschxrdlhse", 
    MAIL_FROM="duynguyen1211204@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

