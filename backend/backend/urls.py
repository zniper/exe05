from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import viewsets, routers

from fbconnect.views import Authenticate, FriendList, FriendContact, UserDetails


class UserViewSet(viewsets.ModelViewSet):
    model = User


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'backend.views.home', name='home'),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^authenticate/?$', Authenticate.as_view(), name="authenticate"),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^users/(?P<id>\d+)/?$', UserDetails.as_view(), name="user_details"),
    url(r'^users/(?P<uid>\d+)/friends/?$', FriendList.as_view(), name="friend_list"),
    url(r'^contacts/(?P<id>\d+)/?$', FriendContact.as_view(), name="friend_contact"),
    url(r'^accounts/', include('django_facebook.auth_urls')),
) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
