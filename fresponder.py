#!/usr/bin/env python3
# An instance of this class acts as a Fred bot

import markovify
from chatterbot import ChatBot

class Responder:
	def __init__(self):
		text = open("data/markov.txt", "r").read()
		self.model = markovify.Text(text)
		self.bot = ChatBot('Fred', trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
		# This part takes a while
		self.bot.train(["./data/chatter.yml"])

	def make_sentence(self):
		return self.model.make_sentence()

	def make_short_sentence(self, num):
		return self.model.make_short_sentence(num)
	
	def get_response(self, text):
		return self.bot.get_response(text)


# Try  it out: talk to Fred
if __name__ == "__main__":
	fred = Responder()

	print(fred.make_sentence())
	while True:
		print(fred.get_response(input(">")))
