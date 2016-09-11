from django.conf.urls import url, include
from rest_framework import routers
from hello import views

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'notes', views.NoteViewSet)
router.register(r'fbposts', views.FbPostViewSet)
router.register(r'wotd', views.WOTDViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='index'),
    url(r'^db', views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', views.returnString, name='return_string'),
    url(r'^webhook/$', views.webhook, name='webhook'),
    url(r'^entry', views.entry, name='entry'),
]


'''
from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
'''
