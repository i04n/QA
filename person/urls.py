from django.conf.urls import patterns, include, url

from person import views

urlpatterns = patterns('quora.person.views',
    # Examples:
    # url(r'^$', 'quora.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',views.register,name='home'),
    url(r'^login/$',views.login,name='login')
)
