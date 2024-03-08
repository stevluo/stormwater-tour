"""
Tour URL configuration for the stormwater_tour project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from . import views

# urlpatterns = [
#     # ex: /tour/<tour_name>/
#     url(r'^tour/(?P<tour_slug>[\w-]+)/$', views.map_page, name='map_page'),
#     url(r'^tour/(?P<tour_slug>[\w-]+)/', include([
#         # ex: tour/<tour_name>/landing
#         url(r'^landing/$', views.landing_page, name='landing_page'),
#         # ex: tour/<tour_name>/feedback
#         url(r'^feedback/$', views.feedback, name='feedback'),
#         # ex: tour/<tour_name>/feedback/thank_you
#         url(r'^feedback/thank_you/$', views.thank_you, name='thank_you'),
#         # ex: tour/<tour_name>/about
#         url(r'^about/$', views.about, name='about'),
#         # ex: tour/<tour_name>/site/<site_name>
#         url(r'^site/(?P<site_slug>[\w-]+)/$',
#             views.location_with_tabs_and_dropbar, name='site')
#     ])),
# ]

urlpatterns = [
    # ex: /tour/<tour_slug>/
    url(
        r'^tour/(?P<tour_slug>[\w-]+)/$',
        views.landing_page, name='landing'
    ),
    url(r'^tour/(?P<tour_slug>[\w-]+)/', include([
        # ex: /tour/<tour_slug>/query_current/
        url(r'^query_current/$', views.query_current, name='query_current'),
        # ex: /tour/<tour_slug>/select_site/
        url(r'^select_site/$', views.select_site, name='select_site'),
        # ex: /tour/<tour_slug>/map/
        url(r'^map/$', views.map_page, name='map_page'),
        # ex: /tour/<tour_slug>/feedback/
        url(r'^feedback/$', views.feedback, name='feedback'),
        # ex: /tour/<tour_slug>/feedback/thank_you/
        url(r'^feedback/thank_you/$', views.thank_you, name='thank_you'),
        # ex: /tour/<tour_slug>/about/
        url(r'^about/$', views.about, name='about'),
        # ex: /tour/<tour_name>/site/<site_name>/
        url(
            r'^site/(?P<site_slug>[\w-]+)/$',
            views.location_with_tabs_and_dropbar, name='site'
        )
    ])),
    # ex: /
    url(r'^$', views.tour_index, name='tour_index'),
]

# Server media files during development
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
