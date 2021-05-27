from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()


class SaveLastRequestMiddleware(MiddlewareMixin):
    """
    Middleware for saving datetime of last user request.
    """
    def process_response(self, request, response):
        if request.user.is_authenticated:
            User.objects.filter(pk=request.user.pk).update(last_request=now())
        return response
