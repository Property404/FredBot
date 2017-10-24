#!/usr/bin/env python3
# This is an independent script to download Fred's post history
# And organize the data for Markovify and ChatterBot

import yaml
import praw

c_id = open("secret/client_id").read()
c_secret = open("secret/client_secret").read()

# Get Fred
reddit = praw.Reddit(client_id=c_id, client_secret=c_secret, user_agent="FredBot")
fred = reddit.redditor("FredHamptonsGhost")

# ChatterBot data is in YAML format, Markov data is in regular ol' text
chatter_file= open("chatter.yml", "w")
markov_file= open("markov.txt", "w")

# Part of the YAML data
conversations = []

count = 0
limit = 4000
for comment in fred.comments.new(limit=limit):
	text = comment.body
	if comment.is_root:
		markov_file.write(text+"\n")
	else:
		parent_text = comment.parent().body
		conversations.append([parent_text, text])
	count += 1

# Write YAML data
yams = {'categories': ["Fred", "Fred as a Bot"], 'conversations': conversations}
chatter_file.write(yaml.dump(yams))

chatter_file.close()
markov_file.close()
