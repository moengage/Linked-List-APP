from django.conf.urls import url
from .views import LinkedListAPI, LinkedListPopAPI, ReverseLinkedList


urlpatterns = [
    url(r'^link/$', LinkedListAPI.as_view()),
    url(r'^link/(?P<unique_id>[\w\d-]+)/$', LinkedListAPI.as_view()),
    url(r'^link/reverse/(?P<unique_id>[\w\d-]+)/$', ReverseLinkedList.as_view()),
    url(r'^link/pop/(?P<unique_id>[\w\d-]+)/$', LinkedListPopAPI.as_view())
]
