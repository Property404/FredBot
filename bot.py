#!/usr/bin/env python3
import praw
import sys
import getpass
import fresponder
import time

c_id = open("secret/client_id").read()
c_secret = open("secret/client_secret").read()

reddit = praw.Reddit(client_id = c_id,
	client_secret = c_secret,
	user_agent = "FredBot",
	username = "FredHamptonsGhostv2",
	password = getpass.getpass(prompt="password>") 
	)

# Subreddits we're monitoring
subreddit_names = ["Playground404"]
run_type = "debug"
if(len(sys.argv)>1 and sys.argv[1] == "release"):
	run_type = "release"
	subreddit_names.append("blackfellas")
print(f"Run type: {run_type}")
subreddits = [reddit.subreddit(sr_name) for sr_name in ["Playground404"]]

# Users whose posts we can directly respond to
good_users = ["Automoderator", "Property404", "FredHamptonsGhost"]

# Fred the AI
fred = fresponder.Responder()

def getLatestSubmission(subreddit):
	for post in subreddit.new(limit=1):
		return post

def main():
	latest_ids = [getLatestSubmission(sr).id for sr in subreddits]

	while True:
		for i in range(len(subreddits)):
			subreddit = subreddits[i]
			current_submission = getLatestSubmission(subreddit)
			current_submission_id = current_submission.id
			if latest_ids[i] != current_submission_id:
				print("New submission!")
				if current_submission.author in good_users:
					print("\tThis submission was made by the proper user")
					current_submission.reply(fred.make_sentence())
					print("\tPosted")
				else:
					print("\tSkipping though...")
				latest_ids[i] = current_submission_id

		for item in reddit.inbox.unread(True, limit=10):
			print("Fan message received")
			if isinstance(item, praw.models.Comment):
				print("\tResponding to a fan...")
				item.reply(fred.get_response(item.body))
			item.mark_read()

while True:
	try:
		main()
	except Exception as e:
		seconds_to_wait = 60*3
		print(f"Exception occured: {e}\nWaiting for {seconds_to_wait} seconds")
		time.sleep(seconds_to_wait)
		print("Restarting")
