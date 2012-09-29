Tabulate the number of likes each Yammer user has received.

This is some shitty code that I just banged out one weekend for the hell of it.
Also, Yammer apparently has a leaderboard that does the same thing, although
only for the top 10 or something.  But then again, it doesn't take forever to
run.

Why does this take forever to run?  Well, I went for the simplest algorithm,
not the fastest, and more importantly, the design of the Yammer API means that
we have to make a whole bunch of rate-limited calls.  So, start it running and
go play Borderlands or something.

