import uuid

from celery import shared_task
from urltitle import URLTitleReader

from django.db.models.aggregates import Count
from django.contrib.postgres.aggregates import BoolOr


from .models import Url


@shared_task
def clean_urls_task():
    Url.objects.filter(urluser__isnull=True, comments=0).delete()


@shared_task
def update_public_urls_task(url_id):
    url_id = uuid.UUID(url_id)
    Url.objects.filter(id=url_id, public=False, urluser__public=True).\
        update(public=True)
    Url.objects.filter(id=url_id, public=True).\
        annotate(annotate_public=BoolOr('urluser__public')).filter(annotate_public=False).\
        update(public=False)


@shared_task
def update_category_urls_task(url_id):
    print(f'url: {url_id}')
    url_id = uuid.UUID(url_id)
    category_most = Url.objects.filter(id=url_id).values('urluser__category').\
        annotate(total=Count('urluser__id')).order_by('-total').first().get('urluser__category')
    Url.objects.filter(id=url_id).update(category=category_most)


@shared_task
def fetch_url_info_task(url):
    reader = URLTitleReader(verify_ssl=True)
    Url.objects.filter(url=url).update(title=reader.title(url))
