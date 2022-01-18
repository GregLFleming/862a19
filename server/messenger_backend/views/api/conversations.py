from django.contrib.auth.middleware import get_user
from django.db.models import Max, Q
from django.db.models.query import Prefetch
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from online_users import online_users
from rest_framework.views import APIView
from rest_framework.request import Request


class Conversations(APIView):
    """get all conversations for a user, include latest message text for preview, and all messages
    include other user model so we have info on username/profile pic (don't include current user info)
    TODO: for scalability, implement lazy loading"""

    def get(self, request: Request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)
            user_id = user.id

            conversations = (
                Conversation.objects.filter(Q(user1=user_id) | Q(user2=user_id))
                .prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("createdAt")
                    )
                )
                .all()
            )


            conversations_response = []
            for convo in conversations:
                convo_dict = {
                    "id": convo.id,
                    "messages": [
                        message.to_dict(["id", "text", "senderId", "createdAt", "lastRead"])
                        for message in convo.messages.all()
                    ]
                }

                # set properties for notification count and latest message preview
                convo_dict["latestMessageText"] = convo_dict["messages"][-1]["text"]
                if convo.user1.id == user_id:
                    convo_dict["qtyUnread"] = convo.user1QtyUnread
                else:
                    convo_dict["qtyUnread"] = convo.user2QtyUnread

                # set a property "otherUser" so that frontend will have easier access
                user_fields = ["id", "username", "photoUrl"]
                if convo.user1 and convo.user1.id != user_id:
                    convo_dict["otherUser"] = convo.user1.to_dict(user_fields)
                elif convo.user2 and convo.user2.id != user_id:
                    convo_dict["otherUser"] = convo.user2.to_dict(user_fields)

                # set property for online status of the other user
                if convo_dict["otherUser"]["id"] in online_users:
                    convo_dict["otherUser"]["online"] = True
                else:
                    convo_dict["otherUser"]["online"] = False

                conversations_response.append(convo_dict)
            conversations_response.sort(
                key=lambda convo: convo["messages"][-1]["createdAt"],
                reverse=True,
            )
            return JsonResponse(
                conversations_response,
                safe=False,
            )
        except Exception as e:
            return HttpResponse(status=500)

class QtyUnreadReset(APIView):
    def put(self, request: Request):
        #Verify user authorization
        try:
            user = get_user(request)
            if user.is_anonymous:
                return HttpResponse(status=401)
            
            conversation_id=request.GET.get('conversation', '')
            user_id = get_user(request).id
            conversation = Conversation.objects.filter(id=conversation_id).prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("createdAt")
                    )
                ).first()
            #If user is not a member of the conversation, return an error reponse.
            if user_id not in [conversation.user1.id, conversation.user2.id]:
                return HttpResponse(status=401)

            #remove the lastRead marker from the previous lastRead message
            for message in reversed(conversation.messages.all()):
                if user_id != message.senderId:
                    if message.lastRead == True:
                        message.lastRead = False
                        message.save()
                        break
            
            #Add a lastRead marker to the final message sent by the other user
            for message in reversed(conversation.messages.all()):
                if user_id != message.senderId:
                    if message.lastRead == False:
                        message.lastRead = True
                        message.save()
                        break

            #Set each message's read status to True.
            for message in reversed(conversation.messages.all()):
                if user_id != message.senderId:
                    if message.read == True:
                        break
                    message.read = True
                    message.save()

            #reset the unread message counter in conversation object.
            if user_id == conversation.user1.id:
                conversation.user1QtyUnread = 0
            else:
                conversation.user2QtyUnread = 0
            conversation.save()

            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)