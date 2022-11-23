# Code from T.Chappuis 23nov2022. The objective is to allow creation of user
# via the django admin platform
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model 

User = get_user_model()

class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User


