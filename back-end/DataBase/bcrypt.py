import bcrypt

def hash_password(plain_password):
    # Convert the password to bytes
    pw_bytes = plain_password.encode('utf-8')
    # Generate salt with cost factor 12
    salt = bcrypt.gensalt(rounds=12)
    # Hash the password
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed

def verify_password(plain_password, hashed):
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed
    )

hashed_pw = hash_password("MySecret123")
print("Hash:", hashed_pw)

is_valid = verify_password("MySecret123", hashed_pw)
print("Valid:", is_valid)
