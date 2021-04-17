
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from urllib import parse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


@deconstructible
class UnicodeMobileNumberValidator(validators.RegexValidator):
    regex = r'09(\d{9})$'
    message = _(
        'Enter a valid mobile number. This value may contain only numbers.'
    )
    flags = 0
    

def validate_website_url(website):
    """Validate website into valid URL"""
    msg = "Cannot validate this website: %s" % website
    validate = URLValidator(message=msg)
    try:
        validate(website)
    except:
        o = parse.urlparse(website)
        if o.path:
            path = o.path
            while path.endswith('/'):
                path = path[:-1]
            path = "http://"+path
            validate(path)
            return path
        else:
            raise ValidationError(message=msg)
    return website 