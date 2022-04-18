from celery import shared_task
from .models import Owner

from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)

# Create your tasks here


# Example Task
@shared_task
def update_all_from_esi():
    owners = Owner.objects.all()
    for owner in owners:
        update_owner(owner.pk)

@shared_task
def update_owner(owner_pk):
    owner = Owner.objects.get(pk=owner_pk)
    owner.fetch_tracking_data_from_esi()
