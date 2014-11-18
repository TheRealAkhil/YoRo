from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'yoroApp.views.index',name="index"),
    url(r'^createnote/', 'yoroApp.views.createNote',name="createnote"),
    url(r'^yo/', 'yoroApp.views.yo',name="yo"),
    url(r'^(?P<noteID>\d+)/', 'yoroApp.views.response', name="response"),
    # url(r'^response/', 'yoroApp.query.response',name="response"),
    url(r'^admin/', include(admin.site.urls)),
)