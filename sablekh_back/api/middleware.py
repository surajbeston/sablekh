from .models import Visitor, ImplicitData, RestrictedIP
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

class ExtractData(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_ips_objs = RestrictedIP.objects.all()
        restricted_ips = [restricted_ips_obj.ip for restricted_ips_obj in restricted_ips_objs]
        if request.META["REMOTE_ADDR"] in restricted_ips:
            return HttpResponse("You're restricted. Contact query@sablekh.com for more information.")
        if request.get_full_path() in ["/users", "/token", "/library", "/file", "/all-libraries", "/all-files", "/get-library", "/download", "/search", "/change-link", "/link", "/send-password-key", "/reset-password", "/like", "/all-likes", "/check-like", "/all-downloads", "/tags"]:
            ip = request.META["REMOTE_ADDR"]
            user_agent = request.headers["User-Agent"]
            origin = request.META["REMOTE_HOST"]
            method = request.META["REQUEST_METHOD"]
            time_taken = request.headers["timetaken"]
            referer = request.headers["site"]
            link = request.headers["link"]
            print (type(request.get_full_path()))
            api_link = request.get_full_path()
            try:
                token = request.headers["Authorization"].split(" ")[1]
                token_obj = Token.objects.get(key = token)
                user = Visitor.objects.get(email = token_obj.user.email)
                data = ImplicitData(ip = ip, user_agent=user_agent, referer = referer, link = link, user= user, origin = origin, time_taken=time_taken, api_link = api_link, method=method)
            except:
                data = ImplicitData(ip = ip, user_agent=user_agent, referer = referer, link = link, origin = origin, time_taken=time_taken, api_link = api_link, method=method)
            data.save()
        return self.get_response(request)
