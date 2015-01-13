from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from person import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quora.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',include('person.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/','person.views.login',name='login'),
    url(r'^user/(?P<usr>\d+)/','person.views.user_view',name='user'),
    url(r'^question/(?P<ques>\d+)/(?P<ans>\d+)','person.views.answer_it',name='answer'),
    url(r'^question/(?P<ques>\d+)/','person.views.answer_it',name='question'),
    url(r'^notifications','person.views.notifs',name='user_notifs'),
    url(r'^profile/(?P<name>\w+)/','person.views.display',name='user'),
    url(r'^test/','person.views.tester',name='test'),
    url(r'^content/','person.views.view_content',name='content'),
	url(r'^logout/','person.views.logout',name='logout')
    
)
