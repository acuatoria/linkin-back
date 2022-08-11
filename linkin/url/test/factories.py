import factory


class UrlFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'url.Url'
        django_get_or_create = ('url', )

    id = factory.Faker('uuid4')
    url = factory.Faker('url')
