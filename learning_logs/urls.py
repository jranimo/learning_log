"""Defines URL patterns for learning_logs."""

from django.conf.urls import url

from . import views

urlpatterns = [
   # Home page
   url(r'^$', views.index, name='index'),

   # Show all topics.
   url(r'^topics/$', views.topics, name='topics'),

   #Detail page for a single topic
   url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

   #Page for adding a new topic
   url(r'^new_topic/$', views.new_topic, name='new_topic'),

   # Page for adding a new entry
   url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

   # Page for editing an entry
   url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

   # Page to delete an entry
   url(r'^delete_entry/(?P<entry_id>\d+)/$', views.delete_entry, name='delete_entry'),

      # Page to delete atopic
   url(r'^delete_topic/(?P<topic_id>\d+)/$', views.delete_topic, name='delete_topic'),
]
