from django.urls import include, path
from rest_framework.routers import Route, SimpleRouter

from users.views import UserFavViewset, UserSubViewset


class SubscriptionRouter(SimpleRouter):
    """Маршрутизатор для кастомных эндпойнтов для подписок."""

    routes = [
        Route(
            url=r'^{prefix}/subscriptions/$',
            mapping={'get': 'list'},
            name='subscriptions-list',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/(?P<user_id>\d+)/subscribe/$',
            mapping={'post': 'create', 'delete': 'destroy'},
            name='subscriptions',
            detail=False,
            initkwargs={}
        ),
    ]


class FavoriteRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/(?P<recipe_id>\d+)/favorite/$',
            mapping={'post': 'create', 'delete': 'destroy'},
            name='favorites',
            detail=False,
            initkwargs={}
        ),
    ]


router_subs = SubscriptionRouter()
router_subs.register('users', UserSubViewset, basename='subs')

router_faves = FavoriteRouter()
router_faves.register('recipes', UserFavViewset, basename='faves')


urlpatterns = [
    path('', include(router_subs.urls)),
    path('', include(router_faves.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
