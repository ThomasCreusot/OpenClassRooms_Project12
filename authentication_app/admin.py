from django.contrib import admin

"""
# Code initial
from authentication_app.models import User

admin.site.register(User)
"""

# Code from T.Chappuis 23nov2022; slightly modificated. The objective is to allow creation of user
# via the django admin platform
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model 

from authentication_app.forms import UserCreationForm #, UserChangeForm

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    #form = UserChangeForm
    model = User
