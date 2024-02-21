from django.urls import include, path
from rest_framework.routers import Route, SimpleRouter

from users.views import UserSubViewset


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
            name='subscriptions-create',
            detail=False,
            initkwargs={}
        ),
    ]


router = SubscriptionRouter()

router.register('users', UserSubViewset, basename='subs')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
