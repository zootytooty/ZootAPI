import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class GigModel(Model):
    class Meta:
        table_name = "gigs"
        if "IS_OFFLINE" in os.environ:
            host = "http://localhost:8000"
        else:
            region = "ap-southeast-2"
            host = "https://dynamodb.ap-southeast-2.amazonaws.com"

    def as_dict(self):
        """
        Takes the current model and reviews the attributes to then translate to a dict
        """
        return {key: getattr(self, key) for key in self._get_attributes().keys()}

    gig_id = UnicodeAttribute(hash_key=True, null=False)
    title = UnicodeAttribute(null=False)
    music_starts = UnicodeAttribute(null=True)
    doors_open = UnicodeAttribute(null=False)
    performance_date = UTCDateTimeAttribute(null=False)
    price = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=True)
    url = UnicodeAttribute(null=False)
    image_url = UnicodeAttribute(null=True)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=True)
