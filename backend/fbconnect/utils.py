from datetime import datetime
from hashlib import sha1

from models import APIToken


def create_token(user):
    """ Generate the token string for an user """
    value = sha1(user.email)
    value.update(datetime.now().strftime('%Y%m%d%H%M%S'))
    value = value.hexdigest()[16:32]
    try:
        token = APIToken.objects.get(user=user)
    except APIToken.DoesNotExist:
        token = APIToken(user=user)
    finally:
        token.token = value
        token.issue_on = datetime.now()
        token.save()
    return value


def verify_token(token):
    """ Check if the provide credentials are valid """
    try:
        atoken = APIToken.objects.get(token=token)
        return atoken.user.is_authenticated()
    except:
        pass
    return False
