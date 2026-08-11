import secrets
import hashlib
import hmac
import logging
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException
from app.database.connection import get_db

logger = logging.getLogger(__name__)

OTP_EXPIRY_MINUTES = 5
MAX_OTP_ATTEMPTS = 5

# generate OTP ---------------------------------------------
def generate_otp() -> str:
    """Generate a secure 6-digit OTP."""
    return str(secrets.randbelow(900000) + 100000)

# hash the OTP
def hash_otp(otp: str) -> str:
    """Return SHA-256 hash of OTP."""
    return hashlib.sha256(otp.encode()).hexdigest()

def send_otp(email: str):

    with get_db() as (conn, cursor):
        cursor.execute(
            "SELECT last_seen, attempts FROM email_otps WHERE email = %s",
            (email,)
        )
        result = cursor.fetchone()

    # ONLY check: Hard cooldown (prevent abuse)
    if result:
        last_seen = result["last_seen"]
        if last_seen.tzinfo is None:
            last_seen = last_seen.replace(tzinfo=UTC)
        
            elapsed_seconds = (datetime.now(UTC) - last_seen).total_seconds()
                
            if elapsed_seconds < 30:  # OTP_RESEND_COOLDOWN
                remaining = int(30 - elapsed_seconds)
                raise HTTPException(
                    status_code=429,
                    detail=f"Please wait {remaining} seconds before requesting a new OTP."
                )
    
    if result['attempts'] >= MAX_OTP_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Maximum OTP attempts exceeded. Please request a new OTP."
        )  

    # Generate and store NEW OTP
    otp = generate_otp()
    otp_hash = hash_otp(otp)
    expiry = datetime.now(UTC) + timedelta(minutes=OTP_EXPIRY_MINUTES)

    try:
        if result:
            #Delete previous OTPs if any
            cursor.execute("DELETE FROM email_otps WHERE email = %s", (email,))
            
        cursor.execute(
                "INSERT INTO email_otps (email, otp_hash, expires_at, attempts) VALUES (%s, %s, %s, 0)",
                (email, otp_hash, expiry)
            )
        
        cursor.execute( 
            """ 
            UPDATE email_otps
            SET attempts = attempts + 1
            WHERE email = %s
            """, 
            (email,)
        )
        conn.commit()

    except Exception as e:
        logger.error("Failed to store OTP for %s: %s", email, e)
        raise HTTPException(status_code=500, detail="Failed to generate OTP.")

    return {"message": "OTP sent successfully"}

# resend OTP
def resend_otp(email: str):
    """Resend (regenerate) OTP for the given email."""
    return send_otp(email)


# verify OTP
def verify_otp(email: str, otp: str):
    """Verify the provided OTP for the given email."""

    try:
        with get_db() as (conn, cursor):

            cursor.execute(
                """
                SELECT otp_hash, expires_at, attempts
                FROM email_otps
                WHERE email = %s
                LIMIT 1
                """,
                (email,)
            )

            record = cursor.fetchone()

            if not record:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid or expired OTP."
                )

            if record["attempts"] >= MAX_OTP_ATTEMPTS:
                raise HTTPException(
                    status_code=400,
                    detail="Maximum OTP attempts exceeded. Please request a new OTP."
                )

            expires_at = record["expires_at"]

            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                
            if isinstance(expires_at, datetime) and expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=UTC)

            if datetime.now(UTC) > expires_at:
                cursor.execute(
                    """
                    DELETE FROM email_otps
                    WHERE email = %s
                    """,
                    (email,)
                )
                conn.commit()

                raise HTTPException(
                    status_code=400,
                    detail="OTP has expired. Please request a new one."
                )

            entered_hash = hash_otp(otp)

            if not hmac.compare_digest(entered_hash, record["otp_hash"]):

                cursor.execute(
                    """
                    UPDATE email_otps
                    SET attempts = attempts + 1
                    WHERE email = %s
                    """,
                    (email,)
                )
                conn.commit()

                return {
                    "success": False,
                    "message": "Invalid OTP."
                }

            # OTP is correct — clean up
            cursor.execute(
                """
                DELETE FROM email_otps WHERE email = %s
                """,
                (email,)
            )
            conn.commit()

    except HTTPException:
        raise

    except Exception as e:
        logger.error("OTP verification failed for %s: %s", email, e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )

    logger.info("OTP verified successfully for %s", email)

    return {
        "success": True,
        "message": "Verification successful."
    }