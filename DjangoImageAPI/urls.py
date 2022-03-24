"""DjangoImageAPI URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

import oauth2_provider.views as oauth2_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api-auth/', include('rest_framework.urls')), # for  REST framework's login and logout views
    path('api/v1/images/', include('images.urls', namespace='images')), # getting the list of all urls in images app
    path('api/v1/accounts/', include('accounts.urls', namespace='accounts')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')), # parent oauth provider url


    # # provider endpoints
    # path('oauth/authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    # path('oauth/token/', oauth2_views.TokenView.as_view(), name="token"),
    # path('oauth/revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),

    # # application management endpoints
    # path('oauth/applications/', oauth2_views.ApplicationList.as_view(), name="list"),
    # path('oauth/applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
    # path('oauth/applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
    # path('oauth/applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
    # path('oauth/applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    
    # # token management endpoints
    # path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
    # path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(), name="authorized-token-delete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
