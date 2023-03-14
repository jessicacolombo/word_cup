from rest_framework.views import APIView, status, Response, Request
from django.forms.models import model_to_dict
from .models import Team
from .utils import (
    data_processing,
    NegativeTitlesError,
    InvalidYearCupError,
    ImpossibleTitlesError,
)


class TeamsViews(APIView):
    def post(self, request: Request) -> Response:
        try:
            data_processing(**request.data)
        except NegativeTitlesError as err:
            return Response({"error": f"{err.message}"}, status.HTTP_400_BAD_REQUEST)
        except InvalidYearCupError as err:
            return Response({"error": f"{err.message}"}, status.HTTP_400_BAD_REQUEST)
        except ImpossibleTitlesError as err:
            return Response({"error": f"{err.message}"}, status.HTTP_400_BAD_REQUEST)

        new_team = Team.objects.create(**request.data)
        new_team_dict = model_to_dict(new_team)

        return Response(new_team_dict, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        teams_list = [model_to_dict(team) for team in teams]
        print(teams_list)

        return Response(teams_list, status.HTTP_200_OK)


class TeamComposedViews(APIView):
    def get(self, request: Request, team_id) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def patch(self, request: Request, team_id) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        for key in request.data:
            setattr(team, key, request.data[key])

        team.save()
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, request: Request, team_id) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
