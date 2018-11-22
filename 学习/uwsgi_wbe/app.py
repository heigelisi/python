#!/usr/bin/python3
import codecs, sys,time
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer);

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]

# uwsgi --http :5000 --wsgi-file test.py