from django.contrib.auth.views import LoginView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ActionView,
    IndexView,
    Page1View,
    PlayerView,
    PlayerViewSet,
    SessionView,
)

router = DefaultRouter()
# router.register(r'players', PlayerViewSet, basename='players')
# router.register(r'playsession', PlayerViewSet, basename='playsession')
router.register(r'player_crud', PlayerViewSet, basename='player_crud')

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('', IndexView.as_view(), name='index'),
    path('page1/', Page1View.as_view(), name='page1'),
    path('actions/', ActionView.as_view(), name='actions'),
    path('login/', LoginView.as_view(template_name='login.html',
                                     # redirect_authenticated_user=True,
                                     success_url='/api/actions/'),
         name='login',
         ),
    path('players/', PlayerView.as_view(), name='players'),
    path('generate/', SessionView.as_view(), name='generate'),
    path('', include(router.urls)),
]
