from django.http import Http404
from django.contrib.auth import authenticate
import warnings

from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response

from django_facebook.models import FacebookUser, FacebookCustomUser

from utils import create_token
from serializers import ProfileSerializer
import handlers


class Authenticate(APIView):
    """ """
    def get(self, request, format=None):
        email = request.GET.get('email', '').lower()
        password = request.GET.get('password', '')
        user = authenticate(username=email, password=password)
        data = {}
        if user:
            data['result'] = 'success'
            data['uid'] = user.id
            data['token'] = create_token(user)
        else:
            data['result'] = 'failed'
        return Response(data)


class FriendList(ListAPIView):
    model = FacebookUser

    def list(self, request, *args, **kwargs):
        uid = kwargs['uid']
        # ugghhhh....
        # django_facebook just put all FB users to one bag, now I don't
        # know who is friend of who
        qset = self.get_queryset().filter(user_id=uid)
        self.object_list = self.filter_queryset(qset)

        # Default is to allow empty querysets.  This can be altered by setting
        # `.allow_empty = False`, to raise 404 errors on empty querysets.
        if not self.allow_empty and not self.object_list:
            warnings.warn(
                'The `allow_empty` parameter is due to be deprecated. '
                'To use `allow_empty=False` style behavior, You should override '
                '`get_queryset()` and explicitly raise a 404 on empty querysets.',
                PendingDeprecationWarning
            )
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        # Switch between paginated or standard style responses
        page = self.paginate_queryset(self.object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)

        return Response(serializer.data)


class UserDetails(RetrieveAPIView):
    model = FacebookCustomUser
    serializer_class = ProfileSerializer
    lookup_field = 'id'


class FriendContact(RetrieveUpdateAPIView):
    model = FacebookUser
    lookup_field = 'id'

