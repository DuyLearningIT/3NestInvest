from fastapi_mail import ConnectionConfig
from fastapi_mail import MessageSchema, MessageType, FastMail
from app.models import User, Role
from sqlalchemy.orm import Session
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

# Send email to sale and channel to confirm the submission was rejected or approved (If rejected, It would have a reason for that decision)
async def send_email(name: str, email: str, status: str, reason: str, title: str):
    try:
        subject = f"{title}"
        body = f"""
        Dear {name or 'User'},
        
        After reviewing your submission, we {status} that !
        Reason: {reason or 'No reason'}
        
        Regards,
        3Nest Invest Developer Team
        """
        message = MessageSchema(
            subject=subject,
            recipients=[email],  
            body=body,
            subtype=MessageType.plain
        )
        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as ex:
        return get_internal_server_error(ex)

# Send email to manager of team 3Nest to have a look at the new submission and review it
async def send_request_to_review(name: str, email: str, title: str):
    try:
        subject = f"{title}"
        body = f"""
        Dear {name or 'User'},
        
        You have a new submision. 
        Please take a look and review it ! 
        
        Regards,
        3Nest Invest Developer Team
        """
        message = MessageSchema(
            subject=subject,
            recipients=[email],  
            body=body,
            subtype=MessageType.plain
        )
        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as ex:
        return get_internal_server_error(ex)
    
# Find all managers and send email to them
async def send_email_to_managers(db: Session, title: str):
    users = db.query(User) \
                .join(Role, User.role_id == Role.role_id) \
                .filter(Role.role_name == 'manager') \
                .all()
    for user in users:
        await send_request_to_review(user.user_name, user.user_email, title)
