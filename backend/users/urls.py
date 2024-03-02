from django.urls import include, path
from users.routers import SubscriptionRouter, UsersRouter
from users.views import CustomUserViewset, UserSubViewset

router_subs = SubscriptionRouter()
router_subs.register('users', UserSubViewset, basename='subscription')

router_users = UsersRouter()
router_users.register('users', CustomUserViewset, 'users')

urlpatterns = [
    path('', include(router_subs.urls)),
    path('', include(router_users.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
