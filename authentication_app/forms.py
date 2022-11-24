# Code corresponding to the try "2. Secondly, [...] from Thierry Chappuis", see admin.py
"""
# Code from T.Chappuis 23nov2022. The objective is to allow creation of user
# via the django admin platform
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model 

User = get_user_model()

class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
"""


# Django documentation : "Si votre modèle d’utilisateur personnalisé est une sous-classe de
# AbstractUser, vous pouvez alors étendre ces formulaires de cette façon :
"""
from django.contrib.auth.forms import UserCreationForm
#from authentication_app.models import CustomUser
from authentication_app.models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('custom_field',)
"""