from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db.models import FileField


@receiver(post_delete)
def auto_delete_file_on_model_delete(sender, instance, **kwargs):
    """Delete files on model delete (e.g., from admin list or bulk delete)."""
    for field in instance._meta.fields:
        if isinstance(field, FileField):
            file = getattr(instance, field.name)
            if file and file.name:
                file.delete(save=False)


@receiver(pre_save)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Delete old file when a new one is uploaded OR cleared in admin."""
    if not instance.pk:
        return  # new instance — no replacement needed

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    for field in instance._meta.fields:
        if isinstance(field, FileField):
            old_file = getattr(old_instance, field.name)
            new_file = getattr(instance, field.name)

            if old_file and (not new_file or old_file.name != new_file.name):
                old_file.delete(save=False)
