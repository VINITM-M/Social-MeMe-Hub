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
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(plain_password, hashed)
