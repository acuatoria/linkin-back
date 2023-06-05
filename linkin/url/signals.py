from corsheaders.signals import check_request_enabled

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UrlUser, Url
from .tasks import clean_urls_task, update_public_urls_task, update_category_urls_task, fetch_url_info_task


@receiver(post_delete, sender=UrlUser)
def clean_urls(sender, instance, **kwargs):
    clean_urls_task.apply_async()


@receiver(post_save, sender=Url)
def post_save_url(sender, instance, **kwargs):
    fetch_url_info_task.apply_async([str(instance.url), ])
    update_public_urls_task.apply_async([str(instance.id), ])
    update_category_urls_task.apply_async([str(instance.id), ])

def cors_allow_api_to_everyone(sender, request, **kwargs):
    return request.path.startswith("/api/v1/urls") and request.method == 'POST'
check_request_enabled.connect(cors_allow_api_to_everyone)