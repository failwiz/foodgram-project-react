from rest_framework.routers import Route, SimpleRouter


class SubscriptionRouter(SimpleRouter):
    """Маршрутизатор для кастомных эндпойнтов для подписок."""

    routes = [
        Route(
            url=r'^{prefix}/subscriptions/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/(?P<user_id>\d+)/subscribe/$',
            mapping={'post': 'create', 'delete': 'destroy'},
            name='{basename}',
            detail=False,
            initkwargs={}
        ),
    ]
