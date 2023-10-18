from django.urls import include, path

from articles.views import articles_list
from website import settings

if settings.DEBUG:

    urlpatterns = [
        path('', articles_list, name='articles'),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
