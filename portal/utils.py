from django.core.validators import RegexValidator


# upload to the media_cdn
def upload_location(instance, filename):
    return f'{instance.id}{filename}'

# phone number regex
phone_regex = RegexValidator(
    r'^\d{11}$',
    message="Input a valid phone number (must be 11 digits)."
    )

# school session regex
school_session_regex = RegexValidator(
    r'^\d{4}\/\d{4}$',
    message="Input a valid session year ie.yyyy/yyy"
    )


def intcomma(value):
    """Add comma on every 10^3. Returns string."""
    value = str(value)

    dot_position = value.find('.')

    if dot_position != -1:
        int_part, decimal_part = value[:dot_position], value[dot_position:]
    else:
        int_part, decimal_part = value, ''

    comma_position = int_part.find(',')

    if comma_position != -1:
        left, right = int_part[:comma_position], int_part[comma_position:]
    else:
        left, right = int_part, ''

    if len(left) > 3:
        comma_ready = ''.join((intcomma(left[:-3]), ',', left[-3:], right))
        if decimal_part:
            return ''.join((comma_ready, decimal_part))
        else:
            return comma_ready
    return value