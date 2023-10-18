from django.urls import include, path

from school.views import students_list
from website import settings

if settings.DEBAG:

    urlpatterns = [
        path('', students_list, name='students'),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
