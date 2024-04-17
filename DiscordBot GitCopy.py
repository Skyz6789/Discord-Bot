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
CHANNELID = "YOUR CHANNEL ID"

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
    
# Acts like a fortune teller to answer user's questions abotu whatever they ask it.
@client.command()
async def fortuneTeller(ctx, *, question):
    user = ctx.author
    response = ["yes", 
                "No", 
                "Maybe", 
                "Why you asking me like im some sort of fortune teller", 
                "uncertain", "Of course!", 
                "Fuck Off I Am Busy!", 
                "Try again later", 
                "leave me alone", 
                "not looking bright", 
                "My sight is losing power... I NEED JET",
                "I am not fester leave me alone!",
                "looks bleak"]
    
    if not question:
        await ctx.send(f"@{user} Please ask a question!")
        return
    
    await ctx.send(f"@{user} {random.choice(response)}")

#command that generates a random Fallout 76 SPEICAL stat foe the user to base their build around. Doesnt take into account legendary perk cards.
@client.command()
async def randomSpecial(ctx):
    special = [1, 1, 1, 1, 1, 1, 1]
    for i in range(50):
        index = random.randint(0, 6)
        
        if special[index] < 15: 
            special[index] += 1
    
    specialTotal = f"Strength: {special[0]}\nPerception: {special[1]}\nEndurance: {special[2]}\nChrisma: {special[3]}\nIntellegence, {special[4]}\nAgility: {special[5]}\nLuck: {special[6]}"
    await ctx.send("Your Random Special Stats\n" + specialTotal)
    
# Command for my fellow nerds that are curious about my rigs specs
@client.command()
async def specs(ctx):
    specs = "Alright fellow nerd here is skyz PCs specs\nCUP: i7-10700 8 Core\nGPU: RXT 3060 12gb vram\nRam: 32Ggb of Corsair Vengence DDR4\nMoBo: ASUS TUFF Z-590 LGA 1200\nPower Supply: Corsair Shift 850 watt\nCase: Corsair 4000D Airflow (yes he knows hes a basic bitch for this)"
    await ctx.send(specs)

# command tells the user what is the most liked video on my channel
@client.command()
async def mostLiked(ctx):
    likedVideoID = ""
    max_likes = 0
    
    # Gets the uploads playlist ID
    request = youtube.channels().list(part="contentDetails", id=CHANNELID)
    response = request.execute()
    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Gets the videos in the uploads playlsit
    request = youtube.playlistItems().list(part="snippet", playlistId=uploads_playlist_id, maxResults=50)
    response = request.execute()

    # Iterates through the videos in the uplaods playlist
    for item in response["items"]:
        video_id = item["snippet"]["resourceId"]["videoId"]

        video_request = youtube.videos().list(part="statistics", id=video_id)
        video_response = video_request.execute()
        statistics = video_response["items"][0]["statistics"]

        likes = int(statistics.get("likeCount", 0))

        # Checks if the current video's like is greater than the original max
        if likes > max_likes:
            max_likes = likes
            likedVideoID = video_id
            
    await ctx.send(f"https://www.youtube.com/watch?v={likedVideoID}")
    
# Picks a random video from my YouTube channel.
@client.command()
async def video(ctx):
    num_results = 200
    
    request = youtube.search().list(
        part = "id",
        channelId = CHANNELID,
        type = "video",
        order = "date",
        maxResults = num_results
    )
    response = request.execute()
    video_id = random.choice(response['items'])['id']['videoId']
    
    await ctx.send(f"https://www.youtube.com/watch?v={video_id}")   
    
client.run(TOKEN)