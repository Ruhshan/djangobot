from django.conf.urls import include, url
from .views import BotView
urlpatterns = [
                  url(r'^/?$', BotView.as_view())
               ]