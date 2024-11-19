from django.contrib.auth.views import LoginView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ActionView,
    IndexView,
    Page1View,
    PlayerView,
    PlayerViewSet,
    PlaySessionViewSet,
    SessionView,
)

router = DefaultRouter()
# router.register(r'players', PlayerViewSet, basename='players')
router.register(r'playsession', PlayerViewSet, basename='playsession')
router.register(r'session/generate', PlaySessionViewSet, basename='session/generate')
# router.register(r'player_crud', PlayerViewSet, basename='player_crud')

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
    # path('session/', SessionView.as_view({'get': 'list',
    #                                               'generate': 'post'},
    #                                              template_name='generate.html'),
    #      name='generate'),
    path('session/', SessionView.as_view(template_name='session.html'),
         name='session'),
    path('', include(router.urls)),
]
