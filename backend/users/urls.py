from django.urls import include, path

from users.views import UserSubViewset
from users.routers import SubscriptionRouter


router_subs = SubscriptionRouter()
router_subs.register('users', UserSubViewset, basename='subscription')


urlpatterns = [
    path('', include(router_subs.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
