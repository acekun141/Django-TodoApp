from django.urls import path
from todo.views import AllTodoView, TodoDetail, AddNewView, EditTodoView

urlpatterns = [
    path('', view=AllTodoView.as_view(), name='home_page'),
    path('todo/<uuid:pk>', view=TodoDetail.as_view(), name='todo_detail'),
    path('todo/add-new/', view=AddNewView.as_view(), name='add'),
    path('todo/edit/<uuid:pk>/', view=EditTodoView.as_view(), name='edit'),
]
