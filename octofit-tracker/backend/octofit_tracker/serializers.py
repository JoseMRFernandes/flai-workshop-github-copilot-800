from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.CharField(source='name')
    team_name = serializers.SerializerMethodField()
    fitness_level = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'password', 'team_id', 'team_name', 'fitness_level', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None
    
    def get_team_name(self, obj):
        """Get team name from team_id"""
        if obj.team_id:
            try:
                team = Team.objects.get(_id=obj.team_id)
                return team.name
            except Team.DoesNotExist:
                return None
        return None
    
    def get_fitness_level(self, obj):
        """Default fitness level"""
        return "Intermediate"
    
    def get_date_joined(self, obj):
        """Default date joined"""
        from datetime import datetime
        return datetime.now().isoformat()


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'member_count', 'created_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None
    
    def get_member_count(self, obj):
        """Count team members"""
        team_id = str(obj._id) if hasattr(obj, '_id') and obj._id else None
        if team_id:
            return User.objects.filter(team_id=team_id).count()
        return 0
    
    def get_created_at(self, obj):
        """Default created date"""
        from datetime import datetime
        return datetime.now().isoformat()


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    calories = serializers.IntegerField(source='calories_burned')
    created_at = serializers.DateTimeField(source='date')
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_name', 'activity_type', 'duration', 'distance', 'calories', 'calories_burned', 'date', 'created_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None
    
    def get_user_name(self, obj):
        """Get user name from user_id"""
        if obj.user_id:
            try:
                user = User.objects.get(_id=obj.user_id)
                return user.name
            except User.DoesNotExist:
                return "Unknown"
        return "Unknown"
    
    def get_distance(self, obj):
        """Calculate approximate distance based on activity type and duration"""
        # Simple approximation: running ~10km/h, cycling ~20km/h, walking ~5km/h
        activity_speeds = {
            'Running': 10,
            'Cycling': 20,
            'Walking': 5,
            'Swimming': 2,
        }
        speed = activity_speeds.get(obj.activity_type, 5)
        return round((obj.duration / 60) * speed, 2)


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    total_points = serializers.IntegerField(source='total_calories')
    activity_count = serializers.IntegerField(source='total_activities')
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'team_id', 'user_name', 'team_name', 'total_points', 'total_calories', 'activity_count', 'total_activities', 'rank']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None
    
    def get_user_name(self, obj):
        """Get user name from user_id"""
        if obj.user_id:
            try:
                user = User.objects.get(_id=obj.user_id)
                return user.name
            except User.DoesNotExist:
                return "Unknown"
        return "Unknown"
    
    def get_team_name(self, obj):
        """Get team name from team_id"""
        if obj.team_id:
            try:
                team = Team.objects.get(_id=obj.team_id)
                return team.name
            except Team.DoesNotExist:
                return "No Team"
        return "No Team"


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    difficulty_level = serializers.CharField(source='difficulty')
    workout_type = serializers.CharField(source='category')
    calories_burned = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty', 'difficulty_level', 'duration', 'category', 'workout_type', 'calories_burned']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') and obj._id else None
    
    def get_calories_burned(self, obj):
        """Estimate calories burned based on duration and difficulty"""
        base_calories = {
            'Beginner': 5,
            'Intermediate': 8,
            'Advanced': 12
        }
        rate = base_calories.get(obj.difficulty, 8)
        return obj.duration * rate
