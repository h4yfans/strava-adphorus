from django.urls import path

from .views import (
    LeaderBoardsAPIView,
    RiderCountAPIView
)

app_name = 'api'

urlpatterns = [
    path('rider-count/',
         RiderCountAPIView.as_view(),
         name='rider-count'),
    path(
        'score/',
        LeaderBoardsAPIView.as_view(),
        name='leaderboards')
]
