"""
Input Validators
AuditPro Enterprise - Data validation functions
"""

import re
from datetime import date, datetime
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format

    Args:
        email: Email address to validate

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not email:
        return False, "Email is required"

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Valid email"
    else:
        return False, "Invalid email format"


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username format

    Args:
        username: Username to validate

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not username:
        return False, "Username is required"

    if len(username) < 3:
        return False, "Username must be at least 3 characters"

    if len(username) > 50:
        return False, "Username must be less than 50 characters"

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"

    return True, "Valid username"


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength

    Args:
        password: Password to validate

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not password:
        return False, "Password is required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters"

    # Optional: Add more complex requirements
    # has_upper = any(c.isupper() for c in password)
    # has_lower = any(c.islower() for c in password)
    # has_digit = any(c.isdigit() for c in password)

    # if not (has_upper and has_lower and has_digit):
    #     return False, "Password must contain uppercase, lowercase, and number"

    return True, "Valid password"


def validate_date_range(start_date: date, end_date: date) -> Tuple[bool, str]:
    """
    Validate date range

    Args:
        start_date: Start date
        end_date: End date

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not start_date or not end_date:
        return False, "Both start and end dates are required"

    if end_date < start_date:
        return False, "End date must be after start date"

    return True, "Valid date range"


def validate_score(score: float, min_score: float = 0, max_score: float = 100) -> Tuple[bool, str]:
    """
    Validate score value

    Args:
        score: Score value
        min_score: Minimum allowed score
        max_score: Maximum allowed score

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if score is None:
        return False, "Score is required"

    if score < min_score or score > max_score:
        return False, f"Score must be between {min_score} and {max_score}"

    return True, "Valid score"


def validate_required_field(value: any, field_name: str) -> Tuple[bool, str]:
    """
    Validate required field

    Args:
        value: Field value
        field_name: Name of field (for error message)

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        return False, f"{field_name} is required"

    return True, "Valid"


def validate_code(code: str, max_length: int = 50) -> Tuple[bool, str]:
    """
    Validate code/identifier format

    Args:
        code: Code to validate
        max_length: Maximum length

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not code:
        return False, "Code is required"

    if len(code) > max_length:
        return False, f"Code must be less than {max_length} characters"

    if not re.match(r'^[A-Z0-9_-]+$', code):
        return False, "Code can only contain uppercase letters, numbers, hyphens, and underscores"

    return True, "Valid code"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove invalid characters

    Args:
        filename: Original filename

    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)

    # Replace spaces with underscores
    filename = filename.replace(' ', '_')

    # Limit length
    if len(filename) > 200:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:190] + (f'.{ext}' if ext else '')

    return filename


def validate_file_extension(filename: str, allowed_extensions: set) -> Tuple[bool, str]:
    """
    Validate file extension

    Args:
        filename: Filename to check
        allowed_extensions: Set of allowed extensions (e.g., {'pdf', 'xlsx'})

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not filename:
        return False, "Filename is required"

    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

    if ext not in allowed_extensions:
        return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"

    return True, "Valid file type"


def format_date(date_obj: date, format_str: str = "%Y-%m-%d") -> str:
    """
    Format date object to string

    Args:
        date_obj: Date object
        format_str: Format string

    Returns:
        str: Formatted date string
    """
    if not date_obj:
        return ""

    if isinstance(date_obj, str):
        return date_obj

    return date_obj.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> date:
    """
    Parse date string to date object

    Args:
        date_str: Date string
        format_str: Format string

    Returns:
        date: Date object or None if parsing fails
    """
    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, format_str).date()
    except ValueError:
        return None
