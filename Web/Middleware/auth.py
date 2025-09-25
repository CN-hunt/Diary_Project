from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from Web import models
from django.shortcuts import redirect


class DiaryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        user_obj = models.UserInfo.objects.filter(id=user_id).first()

        print(request.path_info)
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not user_obj:
            return redirect('login')
