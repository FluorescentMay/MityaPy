import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pytubefix
from pytubefix import Playlist, YouTube
from pytubefix.cli import on_progress
from PIL import Image, ImageDraw, ImageFont
import wrap
# my eyes hurt
# ˚₊ ‧︵‿₊୨୧₊‿︵⠀‧˚₊ ˚ . ₊ ‧︵‿₊୨୧₊‿︵⠀‧˚₊
load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix='.',intents=intents)

# ˚₊ ‧︵‿₊୨୧₊‿︵⠀‧˚₊ ˚ . ₊ ‧︵‿₊୨୧₊‿︵⠀‧˚₊
playlist_link = "https://www.youtube.com/playlist?list=PL2dXnsTC3f1Iu-wzCuBjgjwEC6jCYZ7hB"
playlist_url = Playlist(playlist_link)
playlist_list = list(playlist_url.video_urls)
playlist_newLink = [url.replace("www.youtube.com", "koutu.be") for url in playlist_list]

images = ["./images/Mitya.png", "./images/Mitya2.png", "./images/Mitya3.png", "./images/Mitya4.png", "./images/Mitya5.png", "./images/Mitya6.png", "./images/Mitya7.png", "./images/Mitya8.png"]

DISCORD_TOKEN = os.getenv('BOT_TOKEN')

# ˚₊ ‧︵‿₊୨୧₊‿︵⠀‧˚₊ ˚ . ₊ ‧︵‿₊୨୧₊‿︵⠀‧˚₊
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="watching a Korolevsky Theatre performance..."))

@client.command()
async def r(ctx):
    dice = random.randint(1, 100);
    
    await ctx.send(f"You\'ve rolled {dice}!!!")

@client.command()
async def m(ctx):
    randomify = playlist_newLink.pop(random.randint(0,len(playlist_newLink) - 1));
    await ctx.send(f"-# [☆]({randomify})")  
    print(randomify.title)
    
@client.command()
async def d(ctx, url: str):
    yt = YouTube(url, on_progress_callback=on_progress)
    ys = yt.streams.get_audio_only()
    
    v_title = yt.title
    v_length = yt.length
    
    if v_length > 360:
        await ctx.send("Sorry friend! No can do. The video length is too long! <:MityaPray:1568885882629394542>")
    else:    
        ys.download(output_path="./output")
        await ctx.send(file=discord.File(f'./output/{v_title}.m4a'))  
        os.remove(f'./output/{v_title}.m4a')
    
@client.command()
async def q(ctx, *, repeat="erm"):
    if repeat.casefold() == "i'm stupid" or repeat.casefold() == "im stupid":
        await ctx.send("i know")
    else:
        # ˚₊ ‧︵‿₊୨୧₊‿︵⠀‧˚₊ ˚ . ₊ ‧︵‿₊୨୧₊‿︵⠀‧˚₊
        randImg = random.randint(0, len(images) - 1)
        img_path = images[randImg]
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)        
        text = repeat

        dynamicsize = img.width / 23
        font = ImageFont.truetype("./Fonts/NanumGothic/NanumGothic-ExtraBold.ttf", dynamicsize, encoding="UTF-8")
        wrapped = wrap.wrap(text, font, max_width=img.width - 15)

        draw.multiline_text((img.width / 2, img.height / 7), wrapped, font=font, stroke_width=2, stroke_fill=(43, 0, 158), fill=(214, 194, 255), anchor="mm", align="center", spacing=14)
        output_image_path = "./output/Mityas.png"
        img.save(output_image_path)
        await ctx.send(f'<@{ctx.author.id}>\'s quote:', file=discord.File(output_image_path))  
        
@client.command()
async def hi(ctx):
    embed=discord.Embed(title="Mitya bot Commands", description=f'Good morning, <@{ctx.author.id}>! Wait, is it morning? Ah, doesn\'t matter! Anyway, please step into my office... Great, sit right here. Someone will be right with you. Just tell them you\'re Mitya, an expert from the Energy Commission. Got that? Okay, bye bye!\n\n __Commands__\n`.q type_anything_here` - Make a quote with random Mitya images\n`.m` - Random Genshin music\n`.d Yt_Link` - Turn a Youtube video into audio only\n`.r` - Roll a number through 1 to 100', color=0x8256FF)
    embed.set_image(url="https://static.wikia.nocookie.net/gensin-impact/images/c/c2/Version_7.2_Event_Calendar_Wallpaper.png/revision/latest/scale-to-width-down/1000?cb=20261027042026")
    #embed.set_footer(text="Test Footer")
    
    await ctx.send(embed=embed)
    
client.run(DISCORD_TOKEN)    