from django.db import models
from django.conf import settings


class FacebookUserPicture(models.Model):
    """ Holds the picture of FB friends """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='picture')
    url = models.CharField(max_length=256, default='')

    def __unicode__(self):
        return 'User Picture: %s' % self.user.name

class APIToken(models.Model):
    """ Stores token of each login session """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='local_token')
    token = models.CharField(max_length=16)
    issue_on = models.DateTimeField(blank=True)

    def __unicode__(self):
        return '%s (%s)' % (self.user.email, self.token)
