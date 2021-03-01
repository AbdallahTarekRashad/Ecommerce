import json
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels_presence.models import Room, Presence, channel_layer
from django.db.models import Count, Q
from urllib import parse
from accounts.models import User


def destroy_room(room):
    # for destroy room with all channels
    # get all channels in the room
    presence = Presence.objects.filter(room=room)
    # close all and send close message to all to close in client side before close in server side
    for p in presence:
        async_to_sync(channel_layer.send)(p.channel_name, {'type': 'close_message', })
        room.remove_presence(presence=p)


# for generate room name by using user if auth generate name by username else by session_key
def get_room_name(scope):
    if scope['user'].is_authenticated:
        room_group_name = scope['user'].username + '_user_chat'
    else:
        if not scope['session'].exists(scope['session'].session_key):
            scope['session'].create()
        room_group_name = scope['session'].session_key + '_user_chat'
    return room_group_name


# for get seller to chat with him
def get_seller():
    # to get seller with number of rooms is less
    seller = Presence.objects.values('user').annotate(count=Count('room')).filter(user__type=1).order_by('count')
    # if there is seller connected continue else return None
    if seller:
        seller = seller.first()
        # get the empty channel to connect with it and added to room
        channel = Presence.objects.filter(Q(user=seller['user']) & Q(room__channel_name='EmptyRoom')).first()
        # get the seller account
        user = User.objects.get(pk=channel.user_id)
        # access main socket of seller to send to him to open new socket
        main = Presence.objects.get(room__channel_name=user.username)
        async_to_sync(channel_layer.send)(
            main.channel_name,
            {
                'type': 'seller_message',
                'message': 'open_new_socket'
            }
        )
        return channel, user
    else:
        return None, None


class ChatConsumer(AsyncWebsocketConsumer):
    customer = False
    # if the connection is seller it will be seller and if the connection was customer it will be customer
    sender = ''

    async def connect(self):
        # to access query parameter
        qs = self.scope['query_string'].decode("utf-8")
        qs = await sync_to_async(parse.parse_qsl)(qs)
        qs = await sync_to_async(dict)(qs)
        # check if query parameter has type to handle with it
        if 'type' in qs:
            self.sender = 'seller'
            # for main socket
            if qs['type'] == 'main_seller' and self.scope['user'].type == User.SELLER:
                self.room = await sync_to_async(Room.objects.add)(self.scope["user"].username, self.channel_name,
                                                                  self.scope["user"])
                await self.accept()
            # for empty socket
            elif qs['type'] == 'seller_socket' and self.scope['user'].type == User.SELLER:
                self.room = await sync_to_async(Room.objects.add)("EmptyRoom", self.channel_name,
                                                                  self.scope["user"])
                await self.accept()
            # if admin socket closed and reconnected it must connect to the same room
            elif qs['type'] == 'reconnect' and self.scope['user'].type == User.SELLER:
                self.room = await sync_to_async(Room.objects.add)(qs['room_name'], self.channel_name,
                                                                  self.scope["user"])
                await self.accept()
        # for customer connect if their is a seller connect with it else send massage to him
        else:
            self.sender = 'customer'
            # generate the room name by username of user if he is auth or with session_key if he not auth
            room_group_name = await sync_to_async(get_room_name)(self.scope)
            # added customer to room
            self.room = await sync_to_async(Room.objects.add)(room_group_name, self.channel_name)
            # get the seller to chat with him
            self.seller, user = await sync_to_async(get_seller)()
            # if there is a seller connect him else send message
            if self.seller:
                # add his Empty Socket to same room
                await sync_to_async(self.room.add_presence)(channel_name=self.seller.channel_name,
                                                            user=user)
                # remove his Empty Socket from EmptyRoom
                await sync_to_async(Room.objects.remove)('EmptyRoom', self.seller.channel_name)
                # send to seller the connect message with room name
                await self.channel_layer.send(
                    self.seller.channel_name,
                    {
                        'type': 'connect_message',
                        'message': 'connect_massage',
                        'room_name': self.room.__str__(),
                    }
                )
                # accept connection
                await self.accept()
                self.customer = True
            else:
                # there is no seller to chat with and send massage to apologise to him
                await self.accept()
                await self.send(text_data=json.dumps({
                    'message': 'There is no customer service now you can contact us later'
                }))

    async def disconnect(self, close_code):
        # if customer disconnect: destroy room with their channels by sending message to all channels to close socket
        if self.customer:
            await sync_to_async(destroy_room)(self.room)
        else:
            await sync_to_async(Room.objects.remove)(self.room.__str__(), self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room.__str__(),
            {
                'type': 'chat_message',
                'message': message,
                # send sender with massage to know the sender of message in front
                'sender': self.sender
            }
        )

    # Receive message from room group as chat message
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    # Receive message from server for connect seller with new customer
    async def connect_message(self, event):
        message = event['message']
        room_name = event['room_name']
        # change room object in consumer when connect seller to new customer to send to it
        self.room = await sync_to_async(Room.objects.get)(channel_name=room_name)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'room_name': room_name,
            'acc': self.room.__str__()
        }))

    # Receive message from server to deal with seller main socket
    async def seller_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    # Receive message from server to close socket on client side for seller
    async def close_message(self, event):
        message = 'close_socket'
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))
