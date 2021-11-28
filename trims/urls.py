from django.urls import path
from trims.views import TrimView

urlpatterns = [
    path('', TrimView.as_view()),
]