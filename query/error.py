class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(
            ChatGroup, group_name=self.chatroom_name)
        self.room_group_name = f'chat_{self.chatroom_name}'

        print(f'Chatroom: {self.chatroom}')
        print(f'User: {self.user}')
        print(f'Online Users: {self.chatroom.users_online.all()}')
        print(f'''Is user in online users: {
            self.user in self.chatroom.users_online.all()}''')
        print(f'Online Users:{self.chatroom.users_online.count()}')
        if self.user not in self.chatroom.users_online.all():
            print(f'''connect || {
                self.user} was not in the chatroom and is being added''')
            self.chatroom.users_online.add(self.user)
            self.update_online_count()
        else:
            print(f'connect || {self.user} was already in the chatroom')

        self.accept()

    # Rest of the method...

    def disconnect(self, close_code):

        # remove and update to online users
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        print("Recieved the message")
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )

        event = {'type': 'message_handler', 'message_id': message.id}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, event
        )

    def message_handler(self, event):
        print("Message handler is called.")
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
        }
        html = render_to_string(
            "a_rtchat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)

    def update_online_count(self):
        print("update online users was called")
        online_count = self.chatroom.users_online.count()
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        print(f'''Sending event to group: {
              self.room_group_name} || type: {event['type']}''')
        try:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, event)
            print('Group send completed successfully')
        except Exception as e:
            print(f'Error in group_send: {str(e)}')
        print('Waiting for online_count_handler to be called...')

    def online_count_handler(self, event):
        print("online_count_handler was called.")
        online_count = event['online_count']
        print(f"Currently {online_count} users are online")
        html = render_to_string(
            "a_rtchat/partials/online_count.html", {'online_count': online_count})
        print(f'Html: {html}')
        self.send(text_data=html)
