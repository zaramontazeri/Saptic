from django.urls import path
from rest_framework.routers import DefaultRouter
from users_info import views
from .views import AddressViewSet

router = DefaultRouter()
router.register(r'address', AddressViewSet)

urlpatterns = router.urls

# urlpatterns = +[
#     # path('google/', views.GoogleLogin.as_view()),
#     # path('me/', views.GetMe.as_view()),
#     # path('profile/', views.GetProfile.as_view()),
#
#     # path("test_data/",views.GetGoogle.as_view())
# ]
