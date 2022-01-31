from django.db import models
from django.db.models import Q, Count

from . import utils
from .user import User

class Conversation(utils.CustomModel):
    participants = models.ManyToManyField(User)
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user1QtyUnread = models.IntegerField(default=0)
    user2QtyUnread = models.IntegerField(default=0)
    
    # find conversation given two user Ids
    def find_conversation(participants):
        # return conversation or None if it doesn't exist
        try:
            #Filter the conversation so that only the conversation containing all the participants is returned.
            conversation = Conversation.objects.filter(participants__in=participants).annotate(num_participants=Count('participants')).filter(num_participants=len(participants))
            if conversation:
                return conversation
            else:
                return None
        except:
            return None
