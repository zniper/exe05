from rest_framework import serializers

from django_facebook.models import FacebookCustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookCustomUser
        fields = ('first_name', 'last_name', 'email',
                  'facebook_id', 'facebook_name', 'facebook_profile_url')
