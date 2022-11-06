from django.conf import settings

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, UTCDateTimeAttribute
)


class Comment(Model):
    class Meta:
        table_name = settings.COMMENTS_TABLE
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

    url = UnicodeAttribute(hash_key=True)
    user = UnicodeAttribute(range_key=True)
    user_name = UnicodeAttribute(attr_name='user_n')
    comment = UnicodeAttribute()
    updated_at = UTCDateTimeAttribute()
