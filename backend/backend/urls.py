from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from django.contrib import admin

from rest_framework import viewsets, routers


class UserViewSet(viewsets.ModelViewSet):
    model = User


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'backend.views.home', name='home'),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
)
