from django.dispatch import receiver

from django_facebook.signals import user_registered


@receiver(user_registered)
def update_new_user(user, request, *args, **kwargs):
    """ Update the user profile following registration form """
    pass
