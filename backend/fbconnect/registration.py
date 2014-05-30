from django_facebook import signals
from django_facebook.registration_backends import FacebookRegistrationBackend
from django_facebook.utils import get_user_model


class RegistrationBackend(FacebookRegistrationBackend):

    def register(self, request, form=None, **kwargs):
        """
        Create and immediately log in a new user.

        """
        fullname = request.GET.get('fullname', '')
        first_name = fullname.split(' ')[0]
        last_name = (' ').join(fullname.split(' ')[1:])
        username = email = request.GET.get('email', '')
        password = request.GET.get('password', '')

        # Create user doesn't accept additional parameters,
        new_user = get_user_model().objects.create_user(username, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        # don't need to auto authenticate
        #authenticated_user = self.authenticate(request, username, password)
        #return authenticated_user

        return new_user
