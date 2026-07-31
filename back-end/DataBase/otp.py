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

