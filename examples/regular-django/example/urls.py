from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView


admin.autodiscover()

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", TemplateView.as_view(template_name="profile.html")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]
