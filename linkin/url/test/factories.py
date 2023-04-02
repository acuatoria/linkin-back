import factory

from linkin.users.test.factories import UserFactory


class UrlFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'url.Url'
        django_get_or_create = ('url', )

    id = factory.Faker('uuid4')
    url = factory.Faker('url')
    public = factory.Faker('boolean')


class UrlUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'url.UrlUser'
        django_get_or_create = ('url', )

    url = factory.SubFactory(UrlFactory)
    user = factory.SubFactory(UserFactory)
    public = factory.Faker('boolean')
