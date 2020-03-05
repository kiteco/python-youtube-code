import os
import discord
from dotenv import load_env
import asyncio
import random
import time

load_env()
token = os.getenv("DISCORD_API_TOKEN")

bot = discord.Client()


@bot.event
async def on_member_join(member):
	if member.id = bot.id:
		return
	response = f"Welcome to Kite Fitness, {member.mention}."
	await bot.send_message(member, response)


@bot.event
async def on_message(message):
	channel = message.channel
	keywords = ["work", "workout", "push", "push up", "up"]
	for keyword in keywords:
		if keyword in message:
			response = f"Did someone say {keyword}? Drop and give me 20 @{message.author.id}!"
			await channel.send(response)



@loop(seconds = 3600)
async def workout_time():
	await bot.wait_until_ready()
	online_members = []
	for member in bot.get_all_members():
		if member.status != discord.Status.offline:
			online_members.append(member.mention)
	user = random.choice(online_members)
	time = time.localtime()
	await bot.send_message(user, f"It's {time}! Time for some push ups {user.name}")



bot.run(token)