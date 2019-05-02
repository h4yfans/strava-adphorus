from django.urls import path

from .views import LeaderBoardsAPIView, SegmentLeaderboardRiderCountAPIView

app_name = 'api'

urlpatterns = [
    path('segments/',
         SegmentLeaderboardRiderCountAPIView.as_view(),
         name='rider-count'),
    path(
        'leaderboards/',
        LeaderBoardsAPIView.as_view(),
        name='leaderboards')
]
