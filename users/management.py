from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User
import users.models

# Creates the first UserProfile object for our root user.

def create_core_profile(app, created_models, verbosity, db, **kwargs):   
    user_list = User.objects.all()
    
    if users.models.UserProfile in created_models:
        for user in user_list:
            users.models.UserProfile.objects.create_profile(user=user)

post_syncdb.connect(create_core_profile, sender=users.models)
