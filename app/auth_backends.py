from hashlib import sha256
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse


class RememberMeBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user is None:
            return None

        # Generate a unique key (e.g., hash of the user's password)
        cookie_key = sha256(user.password.encode()).hexdigest()

        # Check if the user has an existing cookie
        cookies_user = request.COOKIES.get(cookie_key)
        if cookies_user is None:
            # New login (not from cookie)
            remember_me = request.POST.get('remember_me')
            response_data = {'Message': 'You are successfully logged in'}
            if remember_me:
                # Set the cookie (adjust expiration time as needed)
                response = HttpResponse(response_data, status=200)
                response.set_cookie(cookie_key, user.username, max_age=3600 * 24 * 30)  # 30 days
            else:
                response = HttpResponse(response_data, status=200)
        else:
            # Returning user (from cookie)
            response_data = {'Message': 'You are successfully logged in', 'Username': 'cookies_user'}
            response = HttpResponse(response_data, status=200)

        # Attach the user object to the response (for authentication purposes)
        print(response)
        print(user)
        response.user = user
        return response
