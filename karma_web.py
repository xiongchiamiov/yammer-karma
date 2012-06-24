#!/usr/bin/env python

# May you recognize your weaknesses and share your strengths.
# May you share freely, never taking more than you give.
# May you find love and love everyone you find.

import pickle
from jinja2 import Environment, FileSystemLoader

# Why is this done separately from karma.py?  I don't want to wait a gazillion
# years for the API scraping just to test this part.
userMapping = pickle.load(open('userMapping.pickle', 'rb'))
likeCounts = pickle.load(open('likeCounts.pickle', 'rb'))

# People who don't work here any more don't show up in the user list, but may
# still have had liked messages.  This lookup should be done dynamically, but
# I'm lazy.
userMapping[124313] = 'Steven Sanchez'
userMapping[1373613] = 'Andrew Guenther'
userMapping[512473] = 'Nat Welch'

userKarma = [ (userMapping[uid], karma) for (uid, karma) in likeCounts.iteritems() ]
userKarma = sorted(userKarma, key=lambda t: t[1], reverse=True)

env = Environment(loader=FileSystemLoader('.'))
print(env.get_template('karma.html').render(userKarma=userKarma))

