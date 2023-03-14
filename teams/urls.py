from django.urls import path
from .views import TeamsViews, TeamComposedViews

urlpatterns = [
    path("teams/", TeamsViews.as_view()),
    path("teams/<int:team_id>/", TeamComposedViews.as_view()),
]
