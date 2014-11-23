from django.conf.urls import patterns, include, url
# from django.contrib import admin

# For test 
urlpatterns = patterns('db_dup.views',
    # url(r'^$', 'home_view', name='homepage'),
)

# For usages
urlpatterns += patterns('db_dup.ogr',
    url(r'^$','db_homepage_view'),
    # url(r'^list_layer/$','list_layer_view'),
    url(r'^select_layer/$','select_layer_view'),
    url(r'^dup_layer/$','dup_layer_view'),
        
)
