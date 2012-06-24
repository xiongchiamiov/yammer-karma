#!/usr/bin/env python

# May you recognize your weaknesses and share your strengths.
# May you share freely, never taking more than you give.
# May you find love and love everyone you find.

import json
import oauth2 as oauth
import pickle
import urlparse
from collections import defaultdict
from time import sleep

from local_settings import key, secret, token, tokenSecret

USERS_PER_PAGE = 50

consumer = oauth.Consumer(key=key, secret=secret)
token = oauth.Token(token, tokenSecret)
client = oauth.Client(consumer, token)

userMapping = {}
likeCounts = defaultdict(int)

# Go through each page of users.  Assume the number of employees is never
# evenly-divisible by USERS_PER_PAGE.
while len(userMapping) % USERS_PER_PAGE == 0:
	page = (len(userMapping) + USERS_PER_PAGE) / USERS_PER_PAGE
	url = 'https://www.yammer.com/api/v1/users.json?page=%s' % page
	response, content = client.request(url, 'GET')
	users = json.loads(content)
	for user in users:
		print "Looking at %s's likes..." % user['full_name']
		userMapping[user['id']] = user['full_name']

		baseMessageUrl = 'https://www.yammer.com/api/v1/messages/liked_by/' \
		               + str(user['id']) + '.json'

		# Paginate through liked messages
		messages = None
		while True:
			url = baseMessageUrl
			if messages:
				url += '?older_than=%s' % messages[-1]['id']
			response, content = client.request(url, 'GET')
			messages = json.loads(content)['messages']
			if not messages:
				print 'Reached end of liked messages.'
				break
			
			print 'Liked %s messages:' % len(messages)
			for message in messages:
				print 'user %s' % message['sender_id']
				print message['body']['plain']
				print '%s likes' % message['liked_by']['count']
				print
				# No matter how many times this message has been liked, we only
				# want to increment for this user so we don't double-count.
				likeCounts[message['sender_id']] += 1
				sleep(1) # For rate-limiting

# Cache this for our web view
pickle.dump(userMapping, open('userMapping.pickle', 'wb'))
pickle.dump(likeCounts, open('likeCounts.pickle', 'wb'))

for user, likes in likeCounts.iteritems():
	print '%s likes - %s' % (likes, userMapping[user])

