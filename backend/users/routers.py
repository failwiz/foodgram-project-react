from rest_framework.routers import Route, SimpleRouter


class UsersRouter(SimpleRouter):
    """Маршрутизатор эндпойнтов пользователей."""

    routes = [
        Route(
            url=r'^{prefix}/me/',
            mapping={'get': 'me'},
            name='{basename}-me',
            detail=True,
            initkwargs={'suffix': 'Me'}
        ),
        Route(
            url=r'^{prefix}/set_password/',
            mapping={'post': 'set_password'},
            name='{basename}-set-password',
            detail=False,
            initkwargs={'suffix': 'Set password'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/',
            mapping={'post': 'create'},
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),
    ]


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
