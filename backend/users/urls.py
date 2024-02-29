from django.urls import include, path

from users.views import UserSubViewset, CustomUserViewset
from users.routers import UsersRouter, SubscriptionRouter


router_subs = SubscriptionRouter()
router_subs.register('users', UserSubViewset, basename='subscription')


router_users = UsersRouter()
router_users.register('users', CustomUserViewset, 'users')

urlpatterns = [
    path('', include(router_subs.urls)),
    path('', include(router_users.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
