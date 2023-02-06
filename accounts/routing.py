from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/sendmail/(?P<room_name>\w+)/$", consumers.SendMailConsumer.as_asgi()),
]
