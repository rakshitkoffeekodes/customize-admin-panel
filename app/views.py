from hashlib import sha256
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
from app.forms import LoginForm


class UpdatedLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        global remember_me
        password = form.cleaned_data['password']
        cookie_key = sha256(password.encode()).hexdigest()
        cookies_user = self.request.COOKIES.get(cookie_key)
        if cookies_user is None:
            username = form.cleaned_data['username']
            remember_me = form.cleaned_data.get('remember_me')
            response_data = {'Message': 'You are successfully logged in'}
        else:
            username = cookies_user
            response_data = {'Message': 'You are successfully logged in', 'Username': cookies_user}

        user = User.objects.get(username=username)
        if user.check_password(password):
            auth = authenticate(username=user.username, password=password)
            if auth is not None:
                response = JsonResponse(response_data, status=200)
                if cookies_user is None and remember_me:
                    response.set_cookie(cookie_key, username)
                return super().form_valid(form)
            else:
                return JsonResponse({'Message': 'Invalid username or password.'}, status=400)
        else:
            return JsonResponse({'Message': 'Invalid username or password.'}, status=400)
