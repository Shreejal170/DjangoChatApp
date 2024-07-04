from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_view, name='home'),
    path('chat/new-groupchat', create_groupchat, name="new-groupchat"),
    path('chat/<username>', get_or_create_chatroom, name='start-chat'),
    path('chatroom/<chatroom_name>', chat_view, name='chatroom'),
    path('edit-chatroom/<chatroom_name>',
         chatroom_edit_view, name="edit-chatroom"),
    path('delete-chatroom/<chatroom_name>',
         chatroom_delete_view, name="chatroom-delete"),
    path('chatroom-leave/<chatroom_name>',
         chatroom_leave_view, name='chatroom-leave'),
    path('chat/fileupload/<chatroom_name>',
         chat_file_upload, name="chat-file-upload")
]
