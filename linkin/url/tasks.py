import uuid

import requests
from bs4 import BeautifulSoup
from celery import shared_task

from django.conf import settings
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
    title = ''

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string

    if title:
        Url.objects.filter(url=url).update(title=soup.title.string)
    else:
        query_url = f'https://www.googleapis.com/customsearch/v1?key={settings.GOOGLE_API_KEY}\
            &cx={settings.GOOGLE_SEARCH_ENGINE_ID}&q={url}&num=1'
        response = requests.request("GET", query_url)
        if not response.json().get('items'):
            return None
        Url.objects.filter(url=url).update(title=response.json().get('items')[0].get('title'))
