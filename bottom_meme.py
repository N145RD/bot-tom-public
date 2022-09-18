import discord
import copy
import sys
from PIL import Image, ImageSequence, ImageDraw, ImageFont
from PIL.Image import Resampling
import requests
import re
import os



if (len(sys.argv) != 2):
    exit(84)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if str.lower(message.content).startswith('bottom'):
        replied = await message.channel.fetch_message(message.reference.message_id)
        print(f'Parsing message {replied} of content {replied.content}')
        custom_emojis = re.findall(r'<\w*:\w*:\d*>', replied.content)
        print(f'Found emojis {custom_emojis}')
        for e in custom_emojis[:1]:
            print(f'Checking emoji {e}')
            emoji = discord.PartialEmoji.from_str(e)
            url = emoji.url
            ftype = url.split('/')[-1]
            myfile = requests.get(url)
            print(f'Getting file from {ftype}')
            open(f'{ftype}', 'wb').write(myfile.content)
            background = Image.open('unknown.png')
            foreground = Image.open(ftype)
            drawspace = ImageDraw.Draw(background)
            font = ImageFont.truetype("Ldfcomicsans.ttf", 20)
            drawspace.text((100, 250), replied.author.name, fill=(0,0,0), font=font)
            drawspace.text((350, 350), message.author.name, fill=(0,0,0), font=font)
            if emoji.animated:
                print(f'Animated emoji found')
                frames = []
                for i in ImageSequence.Iterator(foreground):
                    frame_back = copy.deepcopy(background)
                    i = i.resize((100, 100), Resampling.LANCZOS)
                    frame_back.paste(i, (370, 80))
                    #i.thumbnail((50, 50), Image.ANTIALIAS)
                    i = i.resize((40,40),Resampling.LANCZOS)
                    frame_back.paste(i, (160, 550))
                    frames.append(frame_back)
                frame_one = frames[0]
                frame_one.save("out.gif", format="GIF", append_images=frames, duration=100)
                await replied.reply(file=discord.File('out.gif'))
                os.remove('out.gif')
            else:
                print(f'Static emoji found')
                background.paste(foreground, (350, 80), mask=foreground)
                foreground.thumbnail((50, 50), Image.ANTIALIAS)
                background.paste(foreground, (160, 550), mask=foreground)
                background.save('out.png')
                await replied.reply(file=discord.File('out.png'))
                os.remove('out.png')
            foreground.close()
            os.remove(ftype)

client.run(sys.argv[1])
