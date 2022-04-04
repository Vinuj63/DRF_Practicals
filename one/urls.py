from django.urls import path
from one.views import LoginView, RegisterApi ,SearchAPIView
from rest_framework_simplejwt import views as jwt_views
from one  import views


urlpatterns = [
      path('register/', RegisterApi.as_view()),
      path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
      path('login',LoginView.as_view(), name='login'),  
      path('search/',views.SearchAPIView.as_view()),
      path('sendemail/',views.EmailViewSet.as_view())
]