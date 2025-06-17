from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model


USER = get_user_model()


@receiver(pre_save, sender=USER)
def user_pre_save(sender, instance, *args, **kwargs) -> None:
    instance.username = str(instance.username).lower()
