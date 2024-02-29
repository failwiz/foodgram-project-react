from rest_framework.routers import Route, SimpleRouter


class FavoriteRouter(SimpleRouter):
    """Маршрутизатор для кастомный эндпойнтов для Избранного."""
    routes = [
        Route(
            url=r'^{prefix}/(?P<recipe_id>\d+)/favorite/$',
            mapping={'post': 'create', 'delete': 'destroy'},
            name='favorites',
            detail=False,
            initkwargs={}
        ),
    ]


class ShoppingListRouter(SimpleRouter):
    """Маршрутизатор для кастомных эндпойнтов для списка покупок."""

    routes = [
        Route(
            url=r'^{prefix}/download_shopping_cart/$',
            mapping={'get': 'download'},
            name='download_shopping_cart',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/(?P<recipe_id>\d+)/shopping_cart/$',
            mapping={'post': 'create', 'delete': 'destroy'},
            name='shopping_cart',
            detail=False,
            initkwargs={}
        ),
    ]
