from django.conf.urls import url
from django.views.generic import TemplateView

from wagtail_ckeditor5.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
]