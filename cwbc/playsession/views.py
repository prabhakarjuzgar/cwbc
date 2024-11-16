from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Player, PlaySession
from .serializers import PlayerSerializer, SessionSerializer


class ActionView(TemplateView):
    template_name = 'actions.html'

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser, IsAuthenticated]
        return [permission() for permission in permission_classes]


class Page1View(TemplateView):
    template_name = 'page1.html'


class IndexView(TemplateView):
    template_name = 'index.html'


class PlayerView(TemplateView):
    template_name = 'players.html'


class SessionView(TemplateView):
    template_name = 'generate.html'


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'players.html'  # Your template name

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        return Response({'players': queryset},
                        status=status.HTTP_200_OK,
                        template_name='list.html')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({'player': instance})

    # @action(detail=False, methods=['post'], url_path='actions/create')
    def ceate(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    # @action(detail=False, methods=['post'], url_path='generate')
    # def generate_session(self, request):
    #     players = request.data.get("players")
    #     if not players:
    #         return Response({"error": "No names provided"},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     # serializer = self.get_serializer(users, many=True)
    #     return Response(session_generator(players), status=status.HTTP_200_OK, template_name='page12.html')


class PlaySessionViewSet(viewsets.ModelViewSet):
    queryset = PlaySession.objects.all()
    serializer_class = SessionSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'page1.html'  # Your template name

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({'player': instance})

    @action(detail=False, methods=['post'], url_path='generate')
    def generate_session(self, request):
        players = request.data.get("players")
        if not players:
            return Response({"error": "No names provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        # serializer = self.get_serializer(users, many=True)
        return Response(session_generator(players), status=status.HTTP_200_OK, template_name='page12.html')


def session_generator(players):
    initialize_player(players)

    data = {}
    data["Session1"], data["Rested"] = session_1(players)
    data["Session2"], data["Rested"] = session_2(players)
    data["Session3"], data["Rested"] = session_3(players)
    data["Session4"], data["Rested"] = session_4(players)
    data["Session5"], data["Rested"] = session_5(players)

    return data


def initialize_player(players):
    for player in players:
        if "secondary_division" not in player or not player["secondary_division"]:
            player["secondary_division"] = player["division"] - 1
        player["allotted"] = 0
        player["1_played"] = 0
        player["1.5_played"] = 0
        player["mixed"] = 0


def reset_allotments(players):
    for player in players:
        player["allotted"] = 0


def rest_players(players, rest_indices):
    rested_players = []
    for i in rest_indices:
        players[i]["allotted"] = 1
        rested_players.append(players[i]["name"])
    return rested_players


def allocate_players(players, select_fn, session_num):
    courts = {}
    for court_num in range(1, 6):
        for _ in range(4):
            eligible_players = [p for p in players if not p["allotted"]]
            if eligible_players:
                try:
                    player = select_fn(eligible_players)
                    player["allotted"] = 1
                    if court_num not in courts:
                        courts[court_num] = []
                    courts[court_num].append(player)
                    if len(courts[court_num]) > 1:
                        player1 = courts[court_num][0]
                        player2 = courts[court_num][-1]
                        diff = abs(player1["division"] - player2["division"])
                        if diff == 1:
                            player2["1_played"] = 1
                        elif diff == 1.5:
                            player2["1.5_played"] = 1
                        elif diff > 1.5:
                            player2["mixed"] = 1
                except ValueError:
                    print(f"No eligible players for court {court_num} in session {session_num}")
                    break
            else:
                print(f"No eligible players for court {court_num} in session {session_num}")
                break

    return courts


def session_1(players):
    reset_allotments(players)
    rest_indices = list(range(5))
    rested_players = rest_players(players, rest_indices)
    print(f"Session 1 Rested Players: {rested_players}")

    return allocate_players(players, lambda players: max(players, key=lambda x: x["division"]), 1), rested_players


def session_2(players):
    reset_allotments(players)
    rest_indices = list(range(5, 10))
    rested_players = rest_players(players, rest_indices)
    print(f"Session 2 Rested Players: {rested_players}")

    courts = {}
    allocate_players(players, lambda players: min(players, key=lambda x: x["secondary_division"]), 2)

    return courts, rested_players


# Session 3 (Mixed Doubles) - No change needed here
def session_3(players):
    reset_allotments(players)
    rest_indices = list(range(10, 15))
    rested_players = rest_players(players, rest_indices)
    print(f"Session 3 Rested Players: {rested_players}")

    courts = {}

    def select_mixed_player(players):
        breakpoint()
        eligible_players = [p for p in players if p["mixed"] == 0]
        if not eligible_players:
            return None
        return min(eligible_players, key=lambda x: x["division"])

    for court_num in range(1, 6):
        while len(courts.get(court_num, [])) < 4:
            # Select Player 1
            selected_player = select_mixed_player([p for p in players if not p["allotted"]])
            if selected_player is None:
                break
            selected_player["allotted"] = 1
            selected_player["mixed"] = 1
            if court_num not in courts:
                courts[court_num] = []
            courts[court_num].append(selected_player)

            # Select Player 2 using the same criteria as Player 1
            selected_player_2 = select_mixed_player([p for p in players if not p["allotted"]])
            if selected_player_2 is None:
                break
            selected_player_2["allotted"] = 1
            selected_player_2["mixed"] = 1
            courts[court_num].append(selected_player_2)

            for _ in range(2):  # Now we select Players 3 and 4
                eligible_players = [p for p in players if not p["allotted"]]
                if eligible_players:
                    potential_players = [p for p in eligible_players if abs(p["division"] - selected_player["division"]) in {1, 1.5} or abs(p["division"] - selected_player_2["division"]) in {1, 1.5}]
                    if not potential_players:
                        potential_players = eligible_players
                    player = min(potential_players, key=lambda x: x["division"])
                    player["allotted"] = 1
                    courts[court_num].append(player)
                    if len(courts[court_num]) > 1:
                        player1 = courts[court_num][0]
                        player2 = courts[court_num][-1]
                        diff = abs(player1["division"] - player2["division"])
                        if diff == 1:
                            player2["1_played"] = 1
                        elif diff == 1.5:
                            player2["1.5_played"] = 1
                        elif diff > 1.5:
                            player2["mixed"] = 1

    return courts, rested_players


def session_4(players):
    reset_allotments(players)
    rest_indices = list(range(15, 20))
    rested_players = rest_players(players, rest_indices)
    print(f"Session 4 Rested Players: {rested_players}")

    courts = {}

    for court_num in range(1, 6):
        # Player 1: Highest-rated player
        eligible_players = [p for p in players if not p["allotted"]]
        if not eligible_players:
            break
        player1 = max(eligible_players, key=lambda x: x["secondary_division"])
        player1["allotted"] = 1
        if court_num not in courts:
            courts[court_num] = []
        courts[court_num].append(player1)

        # Player 2: Next highest-rated player
        eligible_players = [p for p in players if not p["allotted"]]
        if not eligible_players:
            break
        player2 = max(eligible_players, key=lambda x: x["secondary_division"])
        player2["allotted"] = 1
        courts[court_num].append(player2)

        # Players 3 & 4: Based on criteria (1.5 div less, 1 div less, 0.5 less, or lowest-rated if no match)
        for _ in range(2):
            eligible_players = [p for p in players if not p["allotted"]]
            if not eligible_players:
                break

            potential_players = [
                p for p in eligible_players
                if abs(p["division"] - player1["division"]) in {1, 2}
            ]

            # If no matching players are found, select the lowest-rated available player
            if not potential_players:
                potential_players = eligible_players

            player = min(potential_players, key=lambda x: x["division"])
            player["allotted"] = 1
            courts[court_num].append(player)
            if len(courts[court_num]) > 1:
                player1 = courts[court_num][0]
                player2 = courts[court_num][-1]
                diff = abs(player1["division"] - player2["division"])
                if diff == 1:
                    player2["1_played"] = 1
                elif diff == 1.5:
                    player2["1.5_played"] = 1
                elif diff > 1.5:
                    player2["mixed"] = 1

    return courts, rested_players


# Session 5 - Same logic as session 1 but based on Secondary_Division
def session_5(players):
    reset_allotments(players)
    rest_indices = list(range(20, 25))
    rested_players = rest_players(players, rest_indices)
    print(f"Session 5 Rested Players: {rested_players}")

    return allocate_players(players, lambda players: max(players, key=lambda x: x["secondary_division"]), 5), rested_players
