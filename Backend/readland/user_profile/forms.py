from django import forms
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile, UserList


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False
        self.fields['about_user'].required = False
        self.fields['mobile_phone'].required = False

    class Meta:
        model = UserProfile
        exclude = ['balance', 'user']


class UserListForm(forms.ModelForm):
    class Meta:
        model = UserList
        exclude = ['user']


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
