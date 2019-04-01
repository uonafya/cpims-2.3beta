"""Registry section urls."""
from django.conf.urls import patterns, url

# This should contain urls related to registry ONLY
urlpatterns = patterns(
    'cpovc_registry.views',
    url(r'^ou/$', 'home', name='registry'),
    url(r'^ou/new/$', 'register_new', name='registry_new'),
    url(r'^ou/view/(?P<org_id>\d+)/$', 'register_details',
        name='register_details'),
    url(r'^ou/edit/(?P<org_id>\d+)/$', 'register_edit', name='registry_edit'),
    url(r'^person/search/$', 'persons_search', name='search_persons'),
    url(r'^person/user/(?P<id>\d+)/$', 'new_user', name='new_user'),
    url(r'^person/$', 'person_actions', name='person_actions'),
    url(r'^person/new/$', 'new_person', name='new_person'),
    url(r'^person/edit/(?P<id>\d+)/$', 'edit_person', name='edit_person'),
    url(r'^person/view/(?P<id>\d+)/$', 'view_person', name='view_person'),
    url(r'^person/delete/(?P<id>\d+)/$', 'delete_person',
        name='delete_person'),
    url(r'^lookup/$', 'registry_look', name='reg_lookup'), )
# {% url 'view_person' id=result.id %}
