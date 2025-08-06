from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Meeting, MeetingMinutes, Task, MeetingRole
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MeetingSerializer(serializers.ModelSerializer):
    user_role = serializers.SerializerMethodField()
    managers = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = ['id', 'title', 'datetime', 'user_role', 'managers', 'participants']

    def get_user_role(self, obj):
        user = self.context['request'].user
        role = MeetingRole.objects.filter(meeting=obj, user=user).first()
        return role.role if role else None
    
    def get_managers(self, obj):
        roles = MeetingRole.objects.filter(meeting=obj, role='manager')
        return UserSerializer([r.user for r in roles], many=True).data

    def get_participants(self, obj):
        roles = MeetingRole.objects.filter(meeting=obj, role='participant')
        return UserSerializer([r.user for r in roles], many=True).data

class MeetingMinutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingMinutes
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
class MeetingRoleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = MeetingRole
        fields = ['user', 'role']

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,  # optional
        }


class AssignMeetingRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRole
        fields = ['user', 'role']