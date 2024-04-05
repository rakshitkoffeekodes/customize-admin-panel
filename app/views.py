from hashlib import sha256

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from pip._internal.utils._jaraco_text import _


def my_login_view(request):

    global remember_me
    if request.method == 'POST':
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        cookie_key = sha256(password.encode()).hexdigest()
        cookies_user = request.COOKIES.get(cookie_key)

        if cookies_user is None:
            username = request.POST.get('username')
            remember_me = request.POST.get('remember_me')
            response_data = {'Message': 'You are successfully logged in', 'remember_me': remember_me}

        else:
            username = cookies_user
            response_data = {'Message': 'You are successfully logged in', 'Username': cookies_user, 'remember_me': remember_me}

        user = User.objects.get(username=username)
        if user.check_password(password):
            auth = authenticate(username=user.username, password=password)

            if auth is not None:
                response = JsonResponse(response_data, status=200)
                print('======', response)
                if cookies_user is None and remember_me is not None:
                    response.set_cookie(cookie_key, username)
                print('-----', response_data)
                return render(request, 'admin/app_index.html', {'form': cookies_user, 'remember_me': remember_me}, status=200)

            else:
                return render(request, 'admin/login.html', {'form': 'username or password is invalid.', 'data': response_data}, status=400)

        else:
            return render(request, 'admin/login.html', {'form': 'password is invalid', 'data': response_data}, status=400)

    else:
        return render(request, 'admin/login.html', {
            'form': 'form',
            'title': _('Log in'),
        })

    # if request.method == 'POST':
    #     print(request.POST)
    #     form = RememberMeAuthenticationForm(request.POST)
    #     print('========', form.is_valid())
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         # Check if the "Remember me" checkbox was checked
    #         if form.cleaned_data.get('remember_me'):
    #             # Set the session expiration time to 1 hour
    #             request.session.set_expiry(3600)
    #         else:
    #             # Expire the session at browser close
    #             request.session.set_expiry(0)
    #         # Redirect to the admin index page
    #         return redirect('admin:index')
    # else:
    #     form = RememberMeAuthenticationForm()
    #     print('====', form)
    #
    # return render(request, 'admin/login.html', {
    #     'form': form,
    #     'title': _('Log in'),
    # })
