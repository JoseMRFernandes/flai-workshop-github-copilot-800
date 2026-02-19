from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'team_id']
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'calories_burned', 'date']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'team_id', 'total_calories', 'total_activities', 'rank']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty', 'duration', 'category']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None
