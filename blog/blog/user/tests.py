from django.test import TestCase
import json
# Create your tests here.


s = {"name":"leinian"}



print( json.loads('{"name":"leinian"}'))
print( json.loads(b'{"name":"leinian"}'))

