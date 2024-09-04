# Version 1.5 added a trivia question game, added Fallout 4 ending picker, and fixed minor bugs or spelling mistakes because I spell like a 4th grader
# Major thing was the advent of the trivia game command and gets it closer to a useable cool bot rather than boring... to be fiar its still boring
import asyncio
import discord
import random
from discord.ext import commands
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build

youtube_api_key = "YOUR API KEY"
youtube = build("youtube", "v3", developerKey = youtube_api_key)
CHANNELID = "YOUR CHANNEL ID"

TOKEN = "YOUR TOKEN"
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '!', intents = intents)

# Eventually want to store the questions in a Json file but, ran into issues with it earlier. So, I will revise it later.
triviaQuestion = [
    {"question": "QUESTION", "answer": "ANSWER"},
    {"question": "QUESTION", "answer": "ANSWER"},
    {"question": "QUESTION", "answer": "ANSWER"},
    {"question": "QUESTION","answer": "ANSWER"}
]

@client.event  
async def on_ready():      
    print('{0.user} is online'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name= f'Fallout 76')) 
    
# Picks a random play style for the user to try.
@client.command()
async def buildPicker(ctx):
    builds = ["gunslinger", "guerrilla", "gladiator", "slugger", "brawler", "rifleman", "commando", "hevay gun", "grenade", "explosive"]
    await ctx.send(f"You should play with a {random.choice(builds)} style")

# Picks a random New Vegas ending for your next playthrough.
@client.command()
async def FONVending(ctx):
    ending = ["NCR", "Leigion", "Mr.House", "Yes Man", "Father Elijah"]
    await ctx.send(f"In your next New Vegas Playthrough. You should side with the {random.choice(ending)}")
    
# Picks a random Fallout 4 ending for your next playthrough.
@client.command()
async def FO4Ending(ctx):
    ending = ["Minutemen", "Brotherhood of Steel", "Railroad", "Institute"]
    await ctx.send(f"In your next Fallout 4 Playthrough. You should side with the {random.choice(ending)}")
    
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
    total_points = 43  # Total points available after the base value of 1 for each attribute
    
    while total_points > 0:
        index = random.randint(0, 6)
        
        if special[index] < 15: 
            special[index] += 1
            total_points -= 1
    
    specialTotal = f"Strength: {special[0]}\nPerception: {special[1]}\nEndurance: {special[2]}\nChrisma: {special[3]}\nIntellegence, {special[4]}\nAgility: {special[5]}\nLuck: {special[6]}"
    await ctx.send("Your Random Special Stats\n" + specialTotal)
    
# sends a random Fallout qoute
@client.command()
async def qoute(ctx):
    qoutes = []
    with open("qoutes.txt", "r") as file:
    # Read the lines and store them in a list
        qoutes = file.readlines()
        
    await ctx.send(f"{random.choice(qoutes)}")

# Gives user a random Fallout trivia question
@client.command()
async def trivia(ctx):
    # Picks a random trivia question
    trivia_question = random.choice(triviaQuestion)
    question = trivia_question["question"]
    answer = trivia_question["answer"]

    await ctx.send(f"***Trivia Question:*** {question}")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        # Wait for the user's answer
        user_answer = await client.wait_for('message', timeout=30.0, check=check)
        
        if user_answer.content.lower() == answer.lower():
            await ctx.send(f"Correct! The answer is {answer}.")
        else:
            await ctx.send(f"Wrong! The correct answer was {answer}.")
    
    except asyncio.TimeoutError:
        await ctx.send(f"Time's up! The correct answer was {answer}.")
    
# Command for my fellow nerds that are curious about my rigs specs
@client.command()
async def specs(ctx):
    specs = "YOUR SPECS"
    await ctx.send(specs)

# command tells the user what is the most liked video on my channel
@client.command()
async def mostLiked(ctx):
    likedVideoID = ""
    max_likes = 0
    
    # Gets the uploads playlist ID
    request = youtube.channels().list(part = "contentDetails", id = CHANNELID)
    response = request.execute()
    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Gets the videos in the uploads playlsit
    request = youtube.playlistItems().list(part = "snippet", playlistId = uploads_playlist_id, maxResults = 25)
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
    num_results = 100
    
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