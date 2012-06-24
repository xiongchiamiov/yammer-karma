#!/usr/bin/env python

# May you recognize your weaknesses and share your strengths.
# May you share freely, never taking more than you give.
# May you find love and love everyone you find.

import json
import oauth2 as oauth
import urlparse
from collections import defaultdict
from time import sleep

from local_settings import key, secret, token, tokenSecret

consumer = oauth.Consumer(key=key, secret=secret)
token = oauth.Token(token, tokenSecret)
client = oauth.Client(consumer, token)

url = 'https://www.yammer.com/api/v1/messages.json'
response, content = client.request(url, 'GET')

users = defaultdict(int)

messages = json.loads(content)['messages']
for message in messages:
	print 'user %s' % message['sender_id']
	print message['body']['plain']
	print '%s likes' % message['liked_by']['count']
	print
	users[message['sender_id']] += message['liked_by']['count']

print users

for user, likes in users.iteritems():
	url = 'https://www.yammer.com/api/v1/users/%s.json' % user
	response, content = client.request(url, 'GET')
	user = json.loads(content)
	print '%s likes - %s' % (likes, user['full_name'])
	print user['mugshot_url']
	sleep(1) # For rate-limiting

