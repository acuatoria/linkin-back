from django.db.models.signals import post_save, post_delete
from django.contrib.postgres.aggregates import BoolOr
from django.db.models.aggregates import Count, Max
from django.db.models.expressions import F
from django.dispatch import receiver

from .models import UrlUser, Url


@receiver(post_delete, sender=UrlUser)
def clean_urls(sender, instance, **kwargs):
    # TODO Better place for this is a periodic task

    Url.objects.filter(urluser__isnull=True, comments=0).delete()


@receiver(post_save, sender=UrlUser)
def update_public_urls(sender, instance, **kwargs):
    # TODO Better place for this is a periodic task
    Url.objects.filter(id=instance.url.id, public=False, urluser__public=True).\
        update(public=True)
    Url.objects.filter(id=instance.url.id, public=True).\
        annotate(annotate_public=BoolOr('urluser__public')).filter(annotate_public=False).\
        update(public=False)

@receiver(post_save, sender=UrlUser)
def update_category_urls(sender, instance, **kwargs):
    # TODO Better place for this is a periodic task
    category_most = Url.objects.filter(id=instance.url.id, public=True).values('urluser__category').\
        annotate(total=Count('urluser__id')).order_by('-total').first().get('urluser__category')
    Url.objects.filter(id=instance.url.id, public=True).update(category=category_most)
