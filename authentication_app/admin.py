# 1. First I tried the following code
# The 'team' field is present on both creation and modification forms on Django administration
# website : 
# http://127.0.0.1:8000/admin/authentication_app/user/add/
# http://127.0.0.1:8000/admin/authentication_app/user/9/change/
# However, the password is not hashed and then user creation is not functional
"""
from django.contrib import admin
from authentication_app.models import User

admin.site.register(User)
"""

# 2. Secondly, I tried the following code, from Thierry Chappuis
# With definition of UserCreationForm in forms.py
# The password is hashed and allows to create a User which can be logged to the API
# However, the 'team' field is absent from both the creation and change form.

## On http://127.0.0.1:8000/admin/authentication_app/user/add/:
### Username
### Password1
### Password2

## On http://127.0.0.1:8000/admin/authentication_app/user/9/change/
### Username
### Password : hashed + link
### Personal info
### -First name
### -Last name
### -Email adress
### Permissions
### -Active
### -Staff status
### -Superuser stats
### -Groups
### -User permissions
### Important dates
### -Last login
### -Date joined

"""
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
"""

# 3. Thirdly, i copy-pasted the code from Django documentation : 
# https://docs.djangoproject.com/fr/4.1/topics/auth/customizing/#a-full-example

# Not sufficient: 
"""
https://docs.djangoproject.com/fr/4.1/topics/auth/customizing/#extending-the-existing-user-model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication_app.models import User

admin.site.register(User, UserAdmin)
"""

#Pour finir, les formulaires suivants sont liés à la classe User et doivent être réécrits ou
# étendus pour fonctionner avec un modèle d’utilisateur personnalisé : 
# UserCreationForm + UserChangeForm. Si votre modèle d’utilisateur personnalisé est une sous-classe
# de AbstractUser, vous pouvez alors étendre ces formulaires de cette façon :

#Does not works; misses something 
"""
from django.contrib.auth.forms import UserCreationForm
from authentication_app.models import User as CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('team',)
"""


#Il sera aussi nécessaire d’inscrire le modèle d’utilisateur personnalisé à l’interface 
# d’administration. Si votre modèle hérite de django.contrib.auth.models.AbstractUser, 
# vous pouvez utiliser la classe existante de Django django.contrib.auth.admin.UserAdmin

# Errors about str and tuple concatenation, etc.
"""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

#from myapp.models import CustomUser
from authentication_app.models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('team',)

#je copie colle pour essayer de modifier le formulaire de changement et non pas de creation
#pas d'exemple dans la doc, donc copié collé
class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        print(UserChangeForm.Meta.fields)
        fields = UserChangeForm.Meta.fields
        #fields = UserChangeForm.Meta.fields + ('custom_field',)
        #fields = ('username', 'password', 'team',)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from .models import User

#perso:
from authentication_app.models import User

admin.site.register(User, UserAdmin)
"""

#Django documentation : Si vous utilisez une classe ModelAdmin personnalisée qui hérite de 
# django.contrib.auth.admin.UserAdmin, vous devez alors ajouter vos champs personnalisés à
# fieldsets (pour les champs qui doivent faire partie de l’édition des utilisateurs) et à
# add_fieldsets (pour les champs qui doivent faire partie de la création des utilisateurs).
# Par exemple …

# I copy-pasted the code of the django documentation example and provided some changes
# https://docs.djangoproject.com/fr/4.1/topics/auth/customizing/#extending-the-existing-user-model


# 'date_of_birth' by 'team'
# got and error :  Unknown field(s) (is_admin) specified for User
# fieldsets and add_fieldsets


from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

#from customauth.models import MyUser
from authentication_app.models import User as MyUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        #fields = ('email', 'team')
        fields = ('username', 'team')


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        #fields = ('email', 'password', 'team', 'is_active', 'is_admin')
        fields = ('username', 'password', 'team', 'is_active')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    #list_display = ('email', 'team', 'is_admin')
    list_display = ('username', 'team', 'email')

    #list_filter = ('is_admin',)

    fieldsets = (
        #(None, {'fields': ('email', 'password')}),
        (None, {'fields': ('username', 'password', 'team')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        #('Permissions', {'fields': ('is_admin',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})


    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            #'fields': ('email', 'team', 'password1', 'password2'),
            'fields': ('username', 'password1', 'password2', 'team'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    search_fields = ('username',)
    ordering = ('email',)
    filter_horizontal = ()




# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
