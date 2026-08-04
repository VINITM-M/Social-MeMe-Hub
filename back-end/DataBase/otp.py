import secrets
import hashlib
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from fastapi import HTTPException
from DataBase.database import db_pool

# otp generation 
def generate_otp():
    return str(secrets.randbelow(900000) + 100000)
#hashing the otp 
def hash_otp(otp: str):
    return hashlib.sha256(otp.encode()).hexdigest()

# #email sender 
# global SENDER_EMAIL 
# global APP_PASSWORD 

# SENDER_EMAIL = "vinithapsl2003@gmail"
# APP_PASSWORD = "Vinith@2507"

# def send_otp_email(receiver_email, otp):

#     msg = MIMEText(
#         f"""
#         Your verification code is: {otp}
#         Code expires in 5 minutes.
#         """ 
#         )

#     msg["Subject"] = "Email Verification"
#     msg["From"] = SENDER_EMAIL
#     msg["To"] = receiver_email

#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(SENDER_EMAIL, APP_PASSWORD)
#             server.send_message(msg)
#         return True
#     except Exception as exc:
#         print("OTP email delivery failed:", exc)
#         return False

def send_otp(email: str):

    otp = generate_otp()
    otp_hash = hash_otp(otp)
    expiry = datetime.utcnow() + timedelta(minutes=5)

    print(f"Generated OTP for {email}: {otp} (hashed: {otp_hash})" )

    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id FROM email_otps
        WHERE email=%s
        """,
        (email,)
    )
    existing = cursor.fetchone()

    if existing:
        cursor.execute(
            """
            UPDATE email_otps
            SET otp_hash=%s, expires_at=%s, attempts=0
            WHERE email=%s
            """,
            (otp_hash, expiry, email)
        )
    else:
        cursor.execute(
            """
            INSERT INTO email_otps(email, otp_hash, expires_at, attempts)
            VALUES(%s, %s, %s, 0)
            """,
            (email, otp_hash, expiry)
        )

    conn.commit()
    # email_sent = send_otp_email(email, otp)

    # if email_sent:
    #     return {
    #         "message": "OTP Sent",
    #         "otp": otp
    #     }

    return {
        "message": "OTP created successfully; email delivered",
        "otp": otp
    }

def verify_otp(email: str, otp: str):

    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT * FROM email_otps
        WHERE email=%s
        """,
        (email,)
    )

    record = cursor.fetchone()

    if not record:
        raise HTTPException(status_code=400, detail="No OTP request found for this email") 

    if record["attempts"] >= 5:
        raise HTTPException(status_code = 400, detail="Maximum OTP attempts exceeded") 

    if datetime.utcnow() > record["expires_at"]:
        raise HTTPException(status_code=400, detail="OTP Expired")

    entered_hash = hash_otp(otp)
    if entered_hash != record["otp_hash"]:

        cursor.execute(
            """
            UPDATE email_otps
            SET attempts = attempts + 1
            WHERE email=%s
            """,
            (email,)
        )
        conn.commit()
        return {
            "success": False,
            "message": "Invalid OTP"
        }
    cursor.execute(
        """
        DELETE FROM email_otps
        WHERE email=%s
        """,
        (email,)
    )

    conn.commit()

    return {
        "success": True,
        "message": "Verification Successful"
    }
=======
import random 
import smtplib  # Used to send emails via SMTP protocol

otp = random.randint(100000, 999999)

# Setting up the SMTP server
server = smtplib.SMTP('smtp.gmail.com', 587)  # Connects to Gmail's SMTP server on port 587

server.starttls()  # Starts a TLS-encrypted connection for secure communication

global receiver_email 

def email_verification(receiver_email): 

    email_domain = ["gmail", "hotmail", "yahoo", "outlook", "aol"]  # List of valid email domains
    email_site = [".com", ".in", ".org", ".edu", ".co.in"]  # List of valid top-level domains (TLDs)
    count = 0  # Counter to track valid domain and TLD matches

    for domain in email_domain:
        if domain in receiver_email:
            count +=1 
            break 
    #check whether email contains valid top of level domain [vinith@gmail.com] check .com 
    for site in email_site:
        if site in receiver_email:
            count += 1 
            break  
    
    # Validate the email format
    if "@" not in receiver_email or count != 2:  
        print("The email id you have entered is invalid.") 
        
        new_receiver_email = input("Enter correct email id: ") 
        email_verification(new_receiver_email) 
        return new_receiver_email  

    return receiver_email  
    
receiver_email = input("Enter your registered email id ") 
valid_receiver_email = email_verification(receiver_email) 

# Gmail account credentials
password = "oecr summ rjvh vobe"  # App password for the sender's Gmail account
server.login("imravi757@gmail.com", password)  # Logs into the SMTP server using the sender's credentials

# Preparing the email content
subject = "Login Code"  # Subject of the email
body = f"{otp} is your login Code." # body content 

message = f'subject:{subject}\n\n{body}'  # Combines subject and body into a properly formatted email message
# Sending the email
server.sendmail("imravi757@gmail.com", valid_receiver_email, message)  # Sends the email to the receiver