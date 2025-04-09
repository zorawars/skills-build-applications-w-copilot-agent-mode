from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date
from django.conf import settings
from pymongo import MongoClient
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data using raw MongoDB commands to avoid Django ORM issues
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        db.drop_collection('users')
        db.drop_collection('teams')
        db.drop_collection('activity')
        db.drop_collection('leaderboard')
        db.drop_collection('workouts')

        # Create users
        users = [
            User(email='user1@example.com', name='User One', age=20),
            User(email='user2@example.com', name='User Two', age=25),
            User(email='user3@example.com', name='User Three', age=30),
        ]
        for user in users:
            user.save()

        # Create teams
        teams = [
            Team(name='Team Alpha', members=[{'email': 'user1@example.com'}, {'email': 'user2@example.com'}]),
            Team(name='Team Beta', members=[{'email': 'user3@example.com'}]),
        ]
        for team in teams:
            team.save()

        # Create activities
        activities = [
            Activity(user=users[0], type='Running', duration=30, date=date.today()),
            Activity(user=users[1], type='Cycling', duration=60, date=date.today()),
            Activity(user=users[2], type='Swimming', duration=45, date=date.today()),
        ]
        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=teams[0], points=100),
            Leaderboard(team=teams[1], points=80),
        ]
        for entry in leaderboard_entries:
            entry.save()

        # Create workouts
        workouts = [
            Workout(name='Morning Run', description='A 5km run to start the day'),
            Workout(name='Evening Yoga', description='Relaxing yoga session'),
        ]
        for workout in workouts:
            workout.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
