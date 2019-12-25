from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from user_profile.forms import UserProfileForm, UserForm
from user_profile.models import UserProfile


def edit(request, user_id):
    return render(request, 'register.html')

# Create your views here.
def user_profile(request, user_id):
    if user_id is None or user_id <= 0:
        raise Http404

    user = get_object_or_404(get_user_model(), id=user_id)

    try:
        local_user_profile = UserProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        local_user_profile = UserProfile.objects.create(user=user)

    allow_edit = False
    if request.user is not None and hasattr(request.user, 'id') and request.user.id is not None and\
            request.user.id > 0 and request.user.id == user.id or request.user.is_superuser:
        allow_edit = True

    if request.method == 'GET':
        user_data = {
            'username': user.username,
            'email': user.email,
            'id': user.id,
            'first_name': local_user_profile.first_name,
            'last_name': local_user_profile.last_name,
            'mobile_phone': local_user_profile.mobile_phone,
            'balance': local_user_profile.balance,
            'about': local_user_profile.about_user,
            'photo': local_user_profile.photo
        }

        return render(request, 'userProfile.html', {'user': user_data, 'allow_edit': allow_edit})
    elif request.method == 'POST' and allow_edit:
        up_form = UserProfileForm(data=request.POST, files=request.FILES, instance=local_user_profile)
        u_form = UserForm(data=request.POST, instance=user)

        if u_form.is_valid():
            user = u_form.save(commit=False)
            user.save()
        else:
            return HttpResponse("Fields were empty: " + str(u_form.errors))

        if up_form.is_valid():
            local_user_profile = up_form.save(commit=False)
            local_user_profile.save()
        else:
            return HttpResponse("Fields were empty: " + str(up_form.errors))

        return redirect("/user/" + str(user.id) + '/')
    else:
        raise PermissionDenied()
