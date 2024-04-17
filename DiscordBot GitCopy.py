# Version 1.0 of the bot bare bones and no super cool features added
import discord
import random
from discord.ext import commands
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build

youtube_api_key = "YOUR API KEY"
youtube = build("youtube", "v3", developerKey = youtube_api_key)

TOKEN = "YOUR TOKEN"
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '!', intents = intents)

@client.event  
async def on_ready():      
    print('{0.user} is online'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name= f'Fallout 76')) 

# Picks a random play style for the user to try.
@client.command()
async def buildPicker(ctx):
    builds = ["gunslinger", "guerrilla", "gladiator", "slugger", "brawler", "rifleman", "commando", "hevay gun", "grenade", "explosive"]
    await ctx.send(f"You should play with a {random.choice(builds)} style")

# Picks a random New Vegas Ending.
@client.command()
async def newVegasEnding(ctx):
    ending = ["NCR", "Leigion", "Mr.House", "Yes Man", "Father Elijah"]
    await ctx.send(f"In your next New Vegas Playthrough. You should side with {random.choice(ending)}")

# Picks a random video from my YouTube channel.
@client.command()
async def video(ctx):
    channel_id = "YOUR CHANNEL ID"
    num_results = 200
    
    request = youtube.search().list(
        part = "id",
        channelId = channel_id,
        type = "video",
        order = "date",
        maxResults = num_results
    )
    response = request.execute()
    video_id = random.choice(response['items'])['id']['videoId']
    
    await ctx.send(f"https://www.youtube.com/watch?v={video_id}")    
    
client.run(TOKEN)