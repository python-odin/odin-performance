import datetime
import os
import string
import random
import csv
import gzip

import odin
from odin.codecs import json_codec
from odin.resources import ResourceIterable


class Child(odin.Resource):
    name = odin.StringField(max_length=50)
    age = odin.IntegerField()


class Parent(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField(max_length=50)
    created = odin.DateTimeField()
    account_type = odin.IntegerField(1, 5)
    children = odin.ListOf(Child)


def parent_range(count):
    """
    Generator that generates a *count* parents resources with between 0 and 5 kids.
    """
    for idx in range(count):
        yield Parent(
            idx,  # id
            ''.join(random.sample(string.ascii_letters, 50)),  # name
            datetime.datetime.fromtimestamp(random.randrange(0, 2^32)),  # created
            random.randint(1, 5),  # account type
            [
                Child(
                    name=''.join(random.sample(string.ascii_letters, 50)),
                    age=random.randrange(1, 32)
                )
                for _ in range(0, 5)
            ]  # children
        )


if __name__ == '__main__':
    resources = ResourceIterable(parent_range(10000000))  # 10 Million
    with open(os.path.join(os.path.dirname(__file__), 'long.csv.gz'), 'w') as f:
        with gzip.GzipFile(fileobj=f) as g:
            c = csv.DictWriter(g, [rf.name for rf in Parent._meta.fields if rf.name != 'children'])
            c.writeheader()
            for resource in resources:
                d = resource.to_dict()
                c.writerow({k: v for k, v in d.items() if k != 'children'})

        # json_codec.dump(resources, f)
