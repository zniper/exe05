from django.dispatch import receiver

from django_facebook.signals import user_registered


@receiver(user_registered)
def update_new_user(user, request, *args, **kwargs):
    """ Update the user profile following registration form """
    return
    fullname = request.GET.get('fullname', '')
    user.first_name = fullname.split(' ')[0]
    user.last_name = (' ').join(fullname.split(' ')[1:])
    user.email = request.GET.get('email', '')
    user.set_password(request.GET.get('password',''))
    user.save()
