import secrets
import hashlib
import hmac
import logging
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException
from DataBase.database import get_db

logger = logging.getLogger(__name__)

OTP_EXPIRY_MINUTES = 5
MAX_OTP_ATTEMPTS = 5


def background_scheduler():
    """Automatically delete expired OTPs from the database."""
    try:
        with get_db() as (conn, cursor):
            cursor.execute(
                """
                DELETE FROM email_otps
                WHERE expires_at < NOW()
                """
            )
            conn.commit()
        logger.info("Background scheduler: expired OTPs cleaned up successfully.")

    except Exception as e:
        logger.error("Background scheduler failed: %s", e)

# generate OTP
def generate_otp() -> str:
    """Generate a secure 6-digit OTP."""
    return str(secrets.randbelow(900000) + 100000)

# hash the OTP
def hash_otp(otp: str) -> str:
    """Return SHA-256 hash of OTP."""
    return hashlib.sha256(otp.encode()).hexdigest()

def delete_otp(email: str):
    """Delete OTP record for the given email."""
    try:
        with get_db() as (conn, cursor):
            cursor.execute(
                """
                DELETE FROM email_otps
                WHERE email = %s
                """,
                (email,)
            )
            conn.commit()
        logger.info("OTP deleted successfully for %s", email)

    except Exception as e:
        logger.error("Failed to delete OTP for %s: %s", email, e)


# generate and store OTP
def send_otp(email: str):
    """Generate a new OTP, replacing any existing one, and store its hash."""
    otp = generate_otp()
    print(f"Generated OTP: {otp}")
    otp_hash = hash_otp(otp)
    expiry = datetime.now(UTC) + timedelta(minutes=OTP_EXPIRY_MINUTES)

    logger.info("Generating OTP for %s", email)

    try:
        with get_db() as (conn, cursor):

            # Delete previous OTP if one exists
            cursor.execute(
                """
                SELECT 1 FROM email_otps WHERE email = %s
                """,
                (email,)
            )
            result = cursor.fetchone()

            if result:
                cursor.execute(
                    """
                    DELETE FROM email_otps WHERE email = %s
                    """,
                    (email,)
                )

            # Insert the new OTP
            cursor.execute(
                """
                INSERT INTO email_otps
                (email, otp_hash, expires_at, attempts)
                VALUES (%s, %s, %s, 0)
                """,
                (email, otp_hash, expiry)
            )

            conn.commit()

    except Exception as e:
        logger.error("Failed to store OTP for %s: %s", email, e)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate OTP. Please try again."
        )

    return {
        "message": "OTP generated successfully"
    }


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