from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from app.forms import LoginForm


class UpdatedLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        global remember_me
        password = form.cleaned_data['password']
        cookies_user = self.request.COOKIES.get('username')
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
                    response.set_cookie('username', username)
                return super().form_valid(form)
            else:
                return JsonResponse({'Message': 'Invalid username or password.'}, status=400)
        else:
            return JsonResponse({'Message': 'Invalid username or password.'}, status=400)


@api_view(['POST'])
def remember_me(request):
    try:
        password = request.POST['password']
        get_cookie = request.COOKIES.get('username')
        if get_cookie is None:
            user_data = get_cookie
            username = request.POST['username']
            remember_me = request.POST.get('remember_me')
            message_data = {"message": "you are login successfully.", "username": user_data}

        else:
            username = get_cookie
            message_data = {"message": "you are login successfully.", "username": username}

        print('user=======>', username)
        user = User.objects.get(username=username)
        if user.check_password(password):
            auth = authenticate(username=username, password=password)
            if auth is not None:
                response_data = JsonResponse(message_data, status=status.HTTP_200_OK)
                if get_cookie is None and remember_me:
                    response_data.set_cookie('username', username)
                return response_data
            else:
                return JsonResponse({"message": 'Please enter correct username and password.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"message": 'Please enter correct username and password.'}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return JsonResponse({"message": f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
