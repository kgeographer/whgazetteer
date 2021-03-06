from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView

from main import views
from datasets.views import DashboardView, PublicListsView

app_name='main'
#handler404 = 'datasets.views.handler404',
handler500 = 'main.views.custom_error_view'

urlpatterns = [
    #path('', views.Home.as_view(), name="home"),
    #path('', views.Home.as_view(), name="home2beta"),
    path('', views.Home2a.as_view(), name="home"),

    # apps
    path('search/', include('search.urls')),
    path('maps/', include('maps.urls')),
    path('datasets/', include('datasets.urls')),
    path('areas/', include('areas.urls')),
    path('collections/', include('collection.urls')),
    path('places/', include('places.urls')),
    path('tutorials/', include('main.urls')),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('public_data/', PublicListsView.as_view(), name='public-lists'),

    # static content
    url(r'^contributing/$', TemplateView.as_view(template_name="main/contributing.html"), name="contributing"),
    url(r'^usingapi/$', TemplateView.as_view(template_name="main/usingapi.html"), name="usingapi"),
    url(r'^community/$', TemplateView.as_view(template_name="main/community.html"), name="community"),
    url(r'^about/$', TemplateView.as_view(template_name="main/about.html"), name="about"),
    url(r'^credits/$', TemplateView.as_view(template_name="main/credits.html"), name="credits"),
    url(r'^system/$', TemplateView.as_view(template_name="main/system.html"), name="system"),
    url(r'^licensing/$', TemplateView.as_view(template_name="main/licensing.html"), name="licensing"),

    path('heat/', TemplateView.as_view(template_name="main/mb-heatmap.html"), name="heat"),

    path('comment/<int:rec_id>', views.CommentCreateView.as_view(), name='comment-create'),
    path('contact/', views.contactView, name='contact'),
    path('success/', views.contactSuccessView, name='success'),
    path('status/', views.statusView, name='status'),

    # backend stuff
    path('api/', include('api.urls')),
    path('accounts/', include('allauth.urls')),
    #path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),

    re_path(r'^celery-progress/', include('celery_progress.urls')),  # the endpoint is configurable

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
