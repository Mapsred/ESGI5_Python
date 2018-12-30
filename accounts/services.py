from django.db.models import Q

from accounts.models import Message


def fetch_conversations(profile, contact):
    messages = Message.objects.filter(
        Q(profile=profile) & Q(receiver=contact) |
        Q(receiver=profile) & Q(profile=contact)
    )

    conversations = []
    for message in messages:
        conversations.append({
            'message': message.content,
            'sender_id': message.profile_id,
            'date': '%s&nbsp;|&nbsp;%s' % (
                message.created_at.strftime("%X %p"),
                message.created_at.strftime("%b %d %Y")
            )
        })

    return conversations
