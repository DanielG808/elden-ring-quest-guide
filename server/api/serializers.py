from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ['id', 'username', 'password', 'quest_steps_progress', 'quests_in_progress', 'quests_completed', 'bosses_defeated']