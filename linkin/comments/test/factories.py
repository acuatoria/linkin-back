import datetime 

from faker import Faker

fake = Faker()


def CommentFactory():

    return {
        'user': fake.uuid4(),
        'user_name': fake.name(),
        'url': fake.url(),
        'comment': fake.text(),
        'updated_at': datetime.datetime.now()
    }