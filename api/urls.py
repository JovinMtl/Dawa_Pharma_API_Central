from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, \
                                            TokenRefreshView,\
                                                  TokenVerifyView)


# from .views import EntrantImiti, ImitiOut, Rapport,\
#     Assurances, GeneralOps
from .views import GeneralOperations, InputOperations, OutputOperations


router = DefaultRouter()

router.register(r'gOps', GeneralOperations, basename='general' )
router.register(r'in', InputOperations, basename='input' )
router.register(r'out', OutputOperations, basename='output' )

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view()),
    path('check/', TokenVerifyView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]