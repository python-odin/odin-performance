from __future__ import print_function
import gzip
import os
import odin
import time
from odin.codecs import csv_codec


class Parent(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField(max_length=50)
    created = odin.DateTimeField()


if __name__ == '__main__':
    start = time.time()
    try:
        with open(os.path.join(os.path.dirname(__file__), 'long.csv'), 'r') as f:
            with gzip.GzipFile(fileobj=f) as g:
                for idx, r in enumerate(csv_codec.reader(g, Parent)):
                    if idx % 100000 == 0:
                        print("Processed:", idx, 'in', time.time() - start, "seconds")
    finally:
        total = time.time() - start
        print("Completed in:", total, "seconds @", idx / total, 'rows/second')
