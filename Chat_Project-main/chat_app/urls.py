from django.urls import path

from .views import login, chat_home, register, AddConversationView
# Create your urls here

urlpatterns = [
    path('login/', login, name = 'login'),
    path('register/', register, name = 'register'),
    path('home/', chat_home, name = 'home'),
    path('addConv/', AddConversationView.as_view(), name = 'add_conversation')
]