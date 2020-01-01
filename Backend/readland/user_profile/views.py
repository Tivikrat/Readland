from PIL import Image as Im
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from books.models import Book
from user_profile.forms import UserProfileForm, UserForm, UserListForm
from user_profile.models import UserProfile, UserList, UserListBook


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
    if request.user is not None and hasattr(request.user, 'id') and request.user.id is not None and \
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
        lists = UserList.objects.filter(user=request.user)


        return render(request, 'userProfile.html', {'user': user_data,
                                                    'allow_edit': allow_edit,
                                                    'lists': lists}
                      )
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


@login_required
def user_list_create(request, user_id):
    if user_id is None or user_id <= 0:
        raise Http404

    user = get_object_or_404(get_user_model(), id=user_id)

    allow_edit = False
    if request.user is not None and hasattr(request.user, 'id') and request.user.id is not None and \
            request.user.id > 0 and request.user.id == user.id or request.user.is_superuser:
        allow_edit = True

    if request.method == 'POST' and allow_edit:
        list_form = UserListForm(data=request.POST, files=request.FILES)

        if list_form.is_valid():
            user_list = list_form.save(commit=False)
            user_list.user = user
            user_list.save()
        else:
            return HttpResponse("Error! Empty fields: " + str(list_form.errors))

        return redirect("/user/" + str(user.id) + '/')
    else:
        raise PermissionDenied()


@login_required
def user_list_update(request, user_id, list_id):
    if user_id is None or user_id <= 0:
        raise Http404

    user = get_object_or_404(get_user_model(), id=user_id)
    u_list_obj = get_object_or_404(UserList, id=list_id)

    allow_edit = False
    if request.user is not None and hasattr(request.user, 'id') and request.user.id is not None and \
            request.user.id > 0 and request.user.id == user.id and u_list_obj.user == user or request.user.is_superuser:
        allow_edit = True

    if request.method == 'POST' and allow_edit:
        list_form = UserListForm(data=request.POST, files=request.FILES, instance=u_list_obj)

        if list_form.is_valid():
            user_list = list_form.save(commit=False)
            user_list.user = user
            user_list.save()
        else:
            return HttpResponse("Error! Empty fields: " + str(list_form.errors))

        return redirect("/user/" + str(user.id) + '/')
    else:
        raise PermissionDenied()


@login_required
def user_list_add_book(request, user_id, list_id, book_id):
    if user_id is None or user_id <= 0:
        raise Http404

    user = get_object_or_404(get_user_model(), id=user_id)
    u_list_obj = get_object_or_404(UserList, id=list_id)
    book_obj = get_object_or_404(Book, id=book_id)

    allow_edit = False
    if request.user is not None and hasattr(request.user, 'id') and request.user.id is not None and \
            request.user.id > 0 and request.user.id == user.id and u_list_obj.user == user or request.user.is_superuser:
        allow_edit = True

    if allow_edit:
        user_list_book = UserListBook(list=u_list_obj, book=book_obj)
        user_list_book.save()

        return redirect("/user/" + str(user.id) + '/')
    else:
        raise PermissionDenied()


@login_required
def user_list_remove_book(request, user_id, list_id, list_book_id):
    if user_id is None or user_id <= 0:
        raise Http404

    user = get_object_or_404(get_user_model(), id=user_id)
    u_list_obj = get_object_or_404(UserList, id=list_id)
    u_list_book_obj = get_object_or_404(UserListBook, id=list_book_id)

    allow_edit = False
    if request.user is not None and hasattr(request.user, 'id') and request.user.id is not None and \
            request.user.id > 0 and request.user.id == user.id and u_list_obj.user == user or request.user.is_superuser:
        allow_edit = True

    if allow_edit:
        u_list_book_obj.delete()
    else:
        raise PermissionDenied()

    return redirect("/user/" + str(user.id) + '/')


@login_required
def user_list_remove(request, user_id, list_id):
    if user_id is None or user_id <= 0:
        raise Http404

    user = get_object_or_404(get_user_model(), id=user_id)
    u_list_obj = get_object_or_404(UserList, id=list_id)

    allow_edit = False
    if request.user is not None and hasattr(request.user, 'id') and request.user.id is not None and \
            request.user.id > 0 and request.user.id == user.id and u_list_obj.user == user or request.user.is_superuser:
        allow_edit = True

    if allow_edit:
        u_list_obj.delete()
    else:
        raise PermissionDenied()

    return redirect("/user/" + str(user.id) + '/')


def get_list_image_preview(img1_path, img2_path, img3_path, string_list_name):
    image3 = Im.open(img1_path)
    image = Im.open(img2_path)
    image2 = Im.open(img3_path)

    new_image = Im.new("RGBA", (260, 360), 1)

    image.thumbnail((200, 300), Im.ANTIALIAS)
    image2.thumbnail((200, 300), Im.ANTIALIAS)
    image3.thumbnail((200, 300), Im.ANTIALIAS)

    new_image.paste(image, (0, 0))
    new_image.paste(image2, (30, 30))
    new_image.paste(image3, (60, 60))

    new_image.save(string_list_name + ".png")
    #imshow(np.asarray(new_image))
    return new_image