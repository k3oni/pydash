from django.conf.urls import patterns, url
from django.conf import settings

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'pydash.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       # url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'main.views.index', name='index'),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},
                           name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'},
                           name='logout'),
                       url(r'^main/$', 'main.views.getall', name='main'),
                       url(r'^info/uptime/$', 'usage.views.uptime', name='uptime'),
                       url(r'^info/memory/$', 'usage.views.memusage', name='memusage'),
                       url(r'^info/cpuusage/$', 'usage.views.cpuusage', name='cpuusage'),
                       url(r'^info/getdisk/$', 'usage.views.getdisk', name='getdisk'),
                       url(r'^info/getusers/$', 'usage.views.getusers', name='getusers'),
                       url(r'^info/getips/$', 'usage.views.getips', name='getips'),
                       url(r'^info/gettraffic/$', 'usage.views.gettraffic', name='gettraffic'),
                       url(r'^info/proc/$', 'usage.views.getproc', name='getproc'),
                       url(r'^info/getdiskio/$', 'usage.views.getdiskio', name='getdiskio'),
                       url(r'^info/loadaverage/$', 'usage.views.loadaverage', name='loadaverage'),
                       url(r'^info/platform/([\w\-\.]+)/$', 'usage.views.platform', name='platform'),
                       url(r'^info/getcpus/([\w\-\.]+)/$', 'usage.views.getcpus', name='getcpus'),
                       url(r'^info/getnetstat/$', 'usage.views.getnetstat', name='getnetstat'))

urlpatterns += patterns('',
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.STATIC_ROOT}))
