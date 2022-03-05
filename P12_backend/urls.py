"""P12_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.authenticate.views import RegisterView, UserViewset
import apps.API.views as APIviews
from apps.front import views as front
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView
from django.contrib.auth.views import LogoutView
from apps.front.views import LoginView
from rest_framework import routers

router = routers.SimpleRouter()
router.register('customers', APIviews.CustomersViewset, basename='customers')
router.register('contracts', APIviews.ContractViewset, basename='contracts')
router.register('events', APIviews.EventViewset, basename='events')
router.register('users', UserViewset, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoint
    path('api/', include(router.urls)),
    path('api/login/', TokenObtainPairView.as_view(),
         name='token_obtains_pairs'),
    path('api/login/refresh/', TokenRefreshView.as_view(),
         name='refresh_token'),
    path('api/signup/', RegisterView.as_view(), name='auth_register'),

    # Frontend endpoints
    path('', LoginView.as_view(template_name='front/login.html',
                               redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', front.home, name='home'),
    path('customers/', front.customers, name='customers'),
    path('customer/<int:customer_id>/', front.customer, name='customer_detail'),
    path('contracts/', front.contracts, name='contracts'),
    path('contract/<int:cont_id>/', front.contract, name='contract_detail'),
    path('events/', front.events, name='events'),
    path('event/<int:event_id>/', front.event, name='event_detail'),
    path('create_event/', front.event_create, name='event_create'),
    path('users/', front.users, name='users'),
    path('user/<int:user_id>/', front.user, name='user_detail')
]
