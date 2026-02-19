from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Delete existing data
        self.stdout.write('Deleting existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Assemble! The mightiest heroes unite for fitness.'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League members pushing their limits.'
        )

        # Create Users - Marvel Heroes
        self.stdout.write('Creating users...')
        marvel_users = [
            User.objects.create(
                name='Tony Stark',
                email='ironman@marvel.com',
                password='arc_reactor_3000',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Steve Rogers',
                email='captain@marvel.com',
                password='super_soldier_serum',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Natasha Romanoff',
                email='blackwidow@marvel.com',
                password='red_room_elite',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Bruce Banner',
                email='hulk@marvel.com',
                password='gamma_radiation',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Thor Odinson',
                email='thor@marvel.com',
                password='mjolnir_worthy',
                team_id=str(team_marvel._id)
            ),
        ]

        # Create Users - DC Heroes
        dc_users = [
            User.objects.create(
                name='Bruce Wayne',
                email='batman@dc.com',
                password='dark_knight_rises',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Clark Kent',
                email='superman@dc.com',
                password='kryptonite_weakness',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Diana Prince',
                email='wonderwoman@dc.com',
                password='lasso_of_truth',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Barry Allen',
                email='flash@dc.com',
                password='speed_force',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Arthur Curry',
                email='aquaman@dc.com',
                password='trident_power',
                team_id=str(team_dc._id)
            ),
        ]

        all_users = marvel_users + dc_users

        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'HIIT']
        
        for user in all_users:
            # Create 5-10 activities for each user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                calories = duration * random.randint(5, 10)
                date = datetime.now() - timedelta(days=random.randint(0, 30))
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    calories_burned=calories,
                    date=date
                )

        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        for user in all_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_calories = sum(activity.calories_burned for activity in user_activities)
            total_activities = user_activities.count()
            
            Leaderboard.objects.create(
                user_id=str(user._id),
                team_id=user.team_id,
                total_calories=total_calories,
                total_activities=total_activities,
                rank=0  # Will be calculated later
            )

        # Update ranks
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_calories')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()

        # Create Workouts
        self.stdout.write('Creating workouts...')
        workouts_data = [
            {
                'name': 'Hero Training Circuit',
                'description': 'High-intensity circuit training to build superhero strength and endurance.',
                'difficulty': 'Advanced',
                'duration': 45,
                'category': 'HIIT'
            },
            {
                'name': 'Speedster Sprint',
                'description': 'Speed-focused cardio workout inspired by the fastest heroes.',
                'difficulty': 'Intermediate',
                'duration': 30,
                'category': 'Running'
            },
            {
                'name': 'Warrior Strength',
                'description': 'Build power and muscle with this strength-focused workout.',
                'difficulty': 'Advanced',
                'duration': 60,
                'category': 'Weightlifting'
            },
            {
                'name': 'Mystic Yoga Flow',
                'description': 'Find balance and flexibility with this calming yoga session.',
                'difficulty': 'Beginner',
                'duration': 40,
                'category': 'Yoga'
            },
            {
                'name': 'Atlantean Swim',
                'description': 'Master the waters with this comprehensive swim workout.',
                'difficulty': 'Intermediate',
                'duration': 50,
                'category': 'Swimming'
            },
            {
                'name': 'Combat Training',
                'description': 'Learn fighting techniques with this boxing and martial arts workout.',
                'difficulty': 'Advanced',
                'duration': 55,
                'category': 'Boxing'
            },
            {
                'name': 'Beginner Hero Boot Camp',
                'description': 'Start your hero journey with this beginner-friendly full-body workout.',
                'difficulty': 'Beginner',
                'duration': 25,
                'category': 'HIIT'
            },
            {
                'name': 'Endurance Challenge',
                'description': 'Push your limits with this long-duration cardio challenge.',
                'difficulty': 'Intermediate',
                'duration': 75,
                'category': 'Cycling'
            },
        ]

        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)

        # Display summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\nDatabase populated successfully!'))
