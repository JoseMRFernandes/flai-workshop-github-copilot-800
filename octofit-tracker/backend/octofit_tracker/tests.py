from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user._id)
    
    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'Test User')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
    
    def test_team_creation(self):
        """Test team is created correctly"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team')
        self.assertTrue(self.team._id)
    
    def test_team_str(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id='user123',
            activity_type='Running',
            duration=30,
            calories_burned=250,
            date=datetime.now()
        )
    
    def test_activity_creation(self):
        """Test activity is created correctly"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories_burned, 250)
        self.assertTrue(self.activity._id)


class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model"""
    
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_id='user123',
            team_id='team456',
            total_calories=1000,
            total_activities=10,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard entry is created correctly"""
        self.assertEqual(self.leaderboard.rank, 1)
        self.assertEqual(self.leaderboard.total_calories, 1000)
        self.assertTrue(self.leaderboard._id)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Run',
            description='A refreshing morning run',
            difficulty='Medium',
            duration=30,
            category='Cardio'
        )
    
    def test_workout_creation(self):
        """Test workout is created correctly"""
        self.assertEqual(self.workout.name, 'Morning Run')
        self.assertEqual(self.workout.difficulty, 'Medium')
        self.assertEqual(self.workout.category, 'Cardio')
        self.assertTrue(self.workout._id)


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='API Test User',
            email='apitest@example.com',
            password='password123'
        )
    
    def test_get_users_list(self):
        """Test retrieving users list"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        """Test creating a new user"""
        url = reverse('user-list')
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='API Test Team',
            description='Team for API testing'
        )
    
    def test_get_teams_list(self):
        """Test retrieving teams list"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_team(self):
        """Test creating a new team"""
        url = reverse('team-list')
        data = {
            'name': 'New Team',
            'description': 'A brand new team'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def test_get_activities_list(self):
        """Test retrieving activities list"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_activity(self):
        """Test creating a new activity"""
        url = reverse('activity-list')
        data = {
            'user_id': 'user123',
            'activity_type': 'Cycling',
            'duration': 45,
            'calories_burned': 300,
            'date': datetime.now().isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def test_get_workouts_list(self):
        """Test retrieving workouts list"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_workout(self):
        """Test creating a new workout"""
        url = reverse('workout-list')
        data = {
            'name': 'Test Workout',
            'description': 'A test workout routine',
            'difficulty': 'Easy',
            'duration': 20,
            'category': 'Strength'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
