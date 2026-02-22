from notifications.models import Notification

def create_notification(*, recipient, actor, verb, target=None):
    # Don't notify yourself
    if recipient == actor:
        return None

    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target=target
    )