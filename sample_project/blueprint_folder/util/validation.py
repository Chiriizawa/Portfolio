import re
from datetime import datetime

def validate_first_name(first_name: str) -> str:
    regex = r'^[A-Za-z\s]+$'
    repeated_char_regex = r'(.)\1{2,}'
    max_length = 20

    if not first_name:
        return "Firstname is required."
    if not re.match(regex, first_name.strip()):
        return "Firstname must not contain special characters or numbers."
    if len(first_name.strip()) < 3:
        return "Firstname must be at least 3 characters long."
    if len(first_name.strip()) > max_length:
        return f"Firstname must be at most {max_length} characters long."
    if re.search(repeated_char_regex, first_name.strip()):
        return "Firstname must not contain repeated characters."
    return ""

def validate_middle_name(middle_name: str) -> str:
    regex = r'^[A-Za-z\s]+$'
    repeated_char_regex = r'(.)\1{2,}'
    max_length = 20

    if middle_name:
        if not re.match(regex, middle_name.strip()):
            return "Middlename must not contain special characters or numbers."
        if len(middle_name.strip()) < 3:
            return "Middlename must be at least 3 characters long."
        if len(middle_name.strip()) > max_length:
            return f"Middlename must be at most {max_length} characters long."
        if re.search(repeated_char_regex, middle_name.strip()):
            return "Middlename must not contain repeated characters."
    return ""

def validate_last_name(last_name: str) -> str:
    regex = r'^[A-Za-z\s]+$'
    repeated_char_regex = r'(.)\1{2,}'
    max_length = 20

    if not last_name:
        return "Lastname is required."
    if not re.match(regex, last_name.strip()):
        return "Lastname must not contain special characters or numbers."
    if len(last_name.strip()) < 3:
        return "Lastname must be at least 3 characters long."
    if len(last_name.strip()) > max_length:
        return f"Lastname must be at most {max_length} characters long."
    if re.search(repeated_char_regex, last_name.strip()):
        return "Lastname must not contain repeated characters."
    return ""

def validate_birthday(birthday: str, age: int) -> str:
    if not birthday:
        return "Birthday is required."

    try:
        birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format."

    current_date = datetime.now()
    sixty_years_ago = datetime(1950, 1, 1)

    if birthday_date > current_date:
        return "Birthday cannot be a future date."
    if birthday_date < sixty_years_ago:
        return "Birthdates before January 1, 1950, are not allowed"

    calculated_age = current_date.year - birthday_date.year
    if (current_date.month, current_date.day) < (birthday_date.month, birthday_date.day):
        calculated_age -= 1

    if calculated_age != age:
        return f"The age ({age}) does not match the birthday."

    return ""

def validate_age(age: int) -> str:
    if age is None:
        return "Age is required."
    if age < 18:
        return "Age must be at least 18."
    if age > 60:
        return "Age must be less than or equal to your birthdate."
    return ""

def validate_contact_number(contact_number: str) -> str:
    regex = r'^09\d{9}$'

    if not contact_number:
        return "Contact number is required."

    trimmed_contact_number = contact_number.strip()

    if not re.match(regex, trimmed_contact_number):
        return "Contact number must be a valid Philippine mobile number."
    if re.search(r'(\d)\1{3,}', trimmed_contact_number):
        return "Contact number must not contain 4 or more repeating digits."

    return ""


def validate_email(email: str) -> str:
    valid_providers = [
    'gmail.com', 'yahoo.com', 'yahoo.com.ph', 'outlook.com', 'hotmail.com', 'aol.com', 
    'icloud.com', 'gov.ph', 'dfa.gov.ph', 'dip.gov.ph', 'deped.gov.ph', 'neda.gov.ph', 
    'doh.gov.ph', 'dti.gov.ph', 'dswd.gov.ph', 'dbm.gov.ph', 'pcso.gov.ph', 'pnp.gov.ph', 
    'bsp.gov.ph', 'prc.gov.ph', 'psa.gov.ph', 'dpwh.gov.ph', 'lto.gov.ph', 'boi.gov.ph',
    'hotmail.co.uk', 'hotmail.fr', 'msn.com', 'yahoo.fr', 'wanadoo.fr', 'orange.fr', 
    'comcast.net', 'yahoo.co.uk', 'yahoo.com.br', 'yahoo.com.in', 'live.com', 
    'rediffmail.com', 'free.fr', 'gmx.de', 'web.de', 'yandex.ru', 'ymail.com', 
    'libero.it', 'uol.com.br', 'bol.com.br', 'mail.ru', 'cox.net', 'hotmail.it', 
    'sbcglobal.net', 'sfr.fr', 'live.fr', 'verizon.net', 'live.co.uk', 'googlemail.com', 
    'yahoo.es', 'ig.com.br', 'live.nl', 'bigpond.com', 'terra.com.br', 'yahoo.it', 
    'neuf.fr', 'yahoo.de', 'alice.it', 'rocketmail.com', 'att.net', 'laposte.net', 
    'facebook.com', 'bellsouth.net', 'yahoo.in', 'hotmail.es', 'charter.net', 
    'yahoo.ca', 'yahoo.com.au', 'rambler.ru', 'hotmail.de', 'tiscali.it', 'shaw.ca', 
    'yahoo.co.jp', 'sky.com', 'earthlink.net', 'optonline.net', 'freenet.de', 
    't-online.de', 'aliceadsl.fr', 'virgilio.it', 'home.nl', 'qq.com', 'telenet.be', 
    'me.com', 'yahoo.com.ar', 'tiscali.co.uk', 'yahoo.com.mx', 'voila.fr', 'gmx.net', 
    'mail.com', 'planet.nl', 'tin.it', 'live.it', 'ntlworld.com', 'arcor.de', 
    'yahoo.co.id', 'frontiernet.net', 'hetnet.nl', 'live.com.au', 'yahoo.com.sg', 
    'zonnet.nl', 'club-internet.fr', 'juno.com', 'optusnet.com.au', 'blueyonder.co.uk', 
    'bluewin.ch', 'skynet.be', 'sympatico.ca', 'windstream.net', 'mac.com', 
    'centurytel.net', 'chello.nl', 'live.ca', 'aim.com', 'bigpond.net.au',
    'up.edu.ph', 'addu.edu.ph', 'ateneo.edu.ph', 'dlsu.edu.ph', 'ust.edu.ph', 'lu.edu.ph'
]

    email = email.strip()

    if not email:
        return "Email is required."

    local_part = email.split('@')[0]
    if len(local_part) > 50:
        return "The local part (before the '@') of the email address cannot exceed 50 characters."

    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}(\.[a-z]{2,})?$')

    if not email_regex.match(email):
        return "Invalid email format. Please enter a valid email address."

    
    domain = email.split('@')[1]

    
    is_strict_gov_ph = any(re.fullmatch(f'^{provider}$', domain) for provider in valid_providers)

    if not is_strict_gov_ph:
        return f"Invalid email domain. {domain} is not a recognized email provider."

    return ""