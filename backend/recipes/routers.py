from rest_framework.routers import Route, SimpleRouter


class FavesAndCartRouter(SimpleRouter):
    """Маршрутизатор для эндпойнтов избранного и списка покупок."""

    routes = [
        Route(
            url=r'^{prefix}/download_shopping_cart/$',
            mapping={'get': 'download_cart'},
            name='download_shopping_cart',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/(?P<recipe_id>\d+)/shopping_cart/$',
            mapping={'post': 'add_to_cart', 'delete': 'remove_from_cart'},
            name='shopping_cart',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/(?P<recipe_id>\d+)/favorite/$',
            mapping={'post': 'favorite', 'delete': 'unfavorite'},
            name='favorites',
            detail=False,
            initkwargs={}
        ),
    ]
