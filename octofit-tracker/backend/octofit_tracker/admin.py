from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['name', 'email', 'team_id']
    list_filter = ['team_id']
    search_fields = ['name', 'email']
    ordering = ['name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['activity_type', 'user_id', 'duration', 'calories_burned', 'date']
    list_filter = ['activity_type', 'date']
    search_fields = ['user_id', 'activity_type']
    ordering = ['-date']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['rank', 'user_id', 'team_id', 'total_calories', 'total_activities']
    list_filter = ['team_id']
    search_fields = ['user_id', 'team_id']
    ordering = ['rank']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['name', 'difficulty', 'duration', 'category']
    list_filter = ['difficulty', 'category']
    search_fields = ['name', 'description']
    ordering = ['name']
