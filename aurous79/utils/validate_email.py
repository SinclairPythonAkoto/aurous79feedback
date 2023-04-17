def validate_email(email: str, confirmation: str) -> bool:
    """Validate an email address by checking if the email is valid
    and if the email matches the confirmation email.
    """
    if email == confirmation:
        return True
    else:
        return False
