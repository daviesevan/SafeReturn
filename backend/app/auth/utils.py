import random
import time
import re
import bcrypt
import string

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

