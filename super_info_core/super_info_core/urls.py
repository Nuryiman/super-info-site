"""
URL configuration for super_info_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from news.views import HomeView, ContactView, PublicationDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n'), name='lang_url'),

]

urlpatterns += i18n_patterns(
    path('', HomeView.as_view(), name='home_url'),
    path('contact/', ContactView.as_view(), name='contact_url'),
    path('publication_detail/<int:pk>/', PublicationDetailView.as_view(), name='publication_url'),
    path('publication_detail/<int:pk>/comment/', PublicationDetailView.as_view(), name='comment_url'),
    path('home/?category_pk=', HomeView.as_view(), name='?category_pk='),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
