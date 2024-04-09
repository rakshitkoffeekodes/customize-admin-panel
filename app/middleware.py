# middleware.py

from django.shortcuts import redirect
from django.urls import reverse


class RememberMeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is accessing the admin panel
        if request.path.startswith(reverse('admin:index')):
            # If user is authenticated and remember_me cookie is set, redirect to admin dashboard
            if request.user.is_authenticated and request.COOKIES.get('remember_me') == 'true':
                return redirect('/admin/')  # Change '/admin/' to your admin dashboard URL

        return response
