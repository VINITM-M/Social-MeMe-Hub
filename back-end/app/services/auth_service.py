from app.repository.user_repository import get_user_by_email, create_user, find_user_by_email
from app.security.hashing import verify_password


def login_details_validation(email, login_password):

    user = find_user_by_email(email)

    if user is None:
        return None 

    if verify_password(login_password, user['password']):
        return True

    return 'Incorrect Password'


def register_user_service(first_name, last_name, email, login_password):
    user = get_user_by_email(email)
    if user:
        return user['email'], False

    new_user = create_user(first_name, last_name, email, login_password)
    if new_user and isinstance(new_user, dict) and 'email' in new_user:
        return new_user['email'], True
    return email, False
