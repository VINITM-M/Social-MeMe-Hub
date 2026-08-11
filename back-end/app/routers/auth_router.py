from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import Login, Signup, OtpVerify, Validation
from app.services.auth_service import login_details_validation, register_user_service
from app.security.otp import send_otp, verify_otp
from app.utils.validation import validation_email
from app.algorithms.bloom_filter import DatabaseEmailBloomFilter
from app.repository.user_repository import get_user_by_email

router = APIRouter()

email_bloom = DatabaseEmailBloomFilter()


@router.post("/login")
def login(login_details: Login):

    if not validation_email(login_details.email_id):
        raise HTTPException(status_code=401, detail="Invalid Email Format")

    # Bloom filter fast-miss 
    if not email_bloom.might_contain(login_details.email_id):
        raise HTTPException(status_code=404, detail="User not found")

    result = login_details_validation(
        login_details.email_id,
        login_details.password)

    if result == True:
        raise HTTPException(status_code=200, detail='Login Successfully')
    else:
        raise HTTPException(status_code=401, detail="Invalid password")


@router.post('/signup')
def signup(sign_details: Signup):
    """Register a new user.

    Bloom filter duplicate-guard path
    ──────────────────────────────────
    • might_contain() == True  → email *may* already be registered
                                  → confirm with a real DB check before rejecting.
                                  (Bloom false-positives are caught here so we never
                                   wrongly block a genuinely new user.)
    • might_contain() == False → email is definitely new → skip DB check, register.
    After a successful registration the new email is added to the filter so
    future login attempts can use the fast-miss path immediately.
    """
    if not validation_email(sign_details.email_id):
        raise HTTPException(status_code=401, detail="Invalid Email Format")

    if email_bloom.might_contain(sign_details.email_id):
        existing = get_user_by_email(sign_details.email_id)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

    result = register_user_service(
        sign_details.first_name,
        sign_details.last_name,
        sign_details.email_id,
        sign_details.password)

    # Add the newly registered email into the Bloom filter
    email_bloom.add(sign_details.email_id)

    return result


@router.post('/otp')
def otp_verify(request: OtpVerify):
    return send_otp(request.email_id)


@router.post("/verify-otp")
def validate_otp(request: Validation):
    return verify_otp(request.email_id, request.otp)
