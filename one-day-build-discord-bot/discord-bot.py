import os
import discord
import asyncio
import random
import datetime

token = os.getenv("DISCORD_API_TOKEN")

bot = discord.Client()


@bot.event
async def on_member_join(member):
	if member.id == bot.id:
		return
	channel = discord.utils.get(bot.guilds[0].channels, name="general")
	response = f"Welcome to Kite Fitness, {member.name}."
	await channel.send(response)


@bot.event
async def on_message(message):
	print(vars(bot))
	if message.author == bot.user:
		return
	channel = message.channel
	keywords = ["work", "workout", "push", "push up", "up"]
	for keyword in keywords:
		if keyword.lower() in message.content.lower():
			response = f"Did someone say {keyword.lower()}? Drop and give me 10 <@{message.author.id}>!"
			await channel.send(response)


@bot.event
async def workout_time():
	while(True):
		await bot.wait_until_ready()
		online_members = []
		for member in bot.get_all_members():
			if member.status != discord.Status.offline and member.id != bot.user.id:
				online_members.append(member.id)
		if len(online_members) > 0:
			user = random.choice(online_members)
			current_time = int(datetime.datetime.now().strftime("%I"))
			channel = discord.utils.get(bot.guilds[0].channels, name="general")
			message = f"It's {current_time} o'clock! Time for some push ups <@{user}>"

			await channel.send(message)
		await asyncio.sleep(3600)


bot.loop.create_task(workout_time())
bot.run(token)
