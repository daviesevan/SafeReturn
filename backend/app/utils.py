import random
import time
import re
import bcrypt
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def unique_id():
    return int(time.time() * 100000) + random.randint(0, 999999)

def validateEmail(email):
    emailRegex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(emailRegex, email))

def hashPassword(password):
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(
        password.encode('utf-8'),
        salt
    )
    return hashedPassword.decode('utf-8')

def verifyPassword(password, hashedPassword):
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashedPassword.encode('utf-8')
    )

# Generate a random 6-digit code
def generate_reset_code():
    return ''.join(random.choices(string.digits, k=6))

def send_email(to_email, subject, body):
    from_email = 'tanuilelan254@gmail.com'
    from_password = 'tppzacwdtxzaqdvp'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')
