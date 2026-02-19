from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer,
    TeamSerializer,
    ActivitySerializer,
    LeaderboardSerializer,
    WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        user_id = str(user._id)
        activities = Activity.objects.filter(user_id=user_id)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        team_id = str(team._id)
        members = User.objects.filter(team_id=team_id)
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        """
        Optionally filter activities by user_id
        """
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leaderboard
    """
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer
    
    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top 10 performers"""
        top_users = Leaderboard.objects.all().order_by('rank')[:10]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workouts
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    def get_queryset(self):
        """
        Optionally filter workouts by difficulty and category
        """
        queryset = Workout.objects.all()
        difficulty = self.request.query_params.get('difficulty', None)
        category = self.request.query_params.get('category', None)
        
        if difficulty is not None:
            queryset = queryset.filter(difficulty=difficulty)
        if category is not None:
            queryset = queryset.filter(category=category)
        
        return queryset
