import discord
import copy
import sys
from PIL import Image, ImageSequence, ImageDraw, ImageFont
from PIL.Image import Resampling
import requests
import re
import os
import emoji
from twemoji_parser import TwemojiParser
import regex



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
    if str.lower(message.content).startswith('bottom') or str.lower(message.content).startswith('softbottom'):
        replied = await message.channel.fetch_message(message.reference.message_id)
        print(f'Parsing message {replied} of content {replied.content}')
        custom_emojis = re.findall(r'<\w*:\w*:\d*>', replied.content)
        print(f'Found emojis {custom_emojis}')
        for e in custom_emojis:
            print(f'Checking emoji {e}')
            emoji = discord.PartialEmoji.from_str(e)
            url = emoji.url
            ftype = url.split('/')[-1]
            myfile = requests.get(url)
            print(f'Getting file from {ftype}')
            open(f'{ftype}', 'wb').write(myfile.content)

            if str.lower(message.content).startswith('bottom'):
                background = Image.open('unknown.png')
                foreground = Image.open(ftype)
                drawspace = ImageDraw.Draw(background)
                font = ImageFont.truetype("Ldfcomicsans.ttf", 20)
                drawspace.text((100, 250), replied.author.name, fill=(0,0,0), font=font)
                drawspace.text((320, 350), message.author.name, fill=(0,0,0), font=font)
                if emoji.animated:
                    print(f'Animated emoji found')
                    src_duration = foreground.info["duration"]
                    frames = []
                    for i in ImageSequence.Iterator(foreground):
                        frame_back = copy.deepcopy(background).convert('RGBA')
                        i = i.convert("RGBA")
                        scaleRatio = await findScaleRatio(85, 85, i.width, i.height)
                        i = await scaleResizeImage(i, scaleRatio)
                        frame_back.paste(i, (int(415-i.width/2), int(130-i.height/2)), i)
                        print ("!")
                        scaleRatio = await findScaleRatio(40, 40, i.width, i.height)
                        i = await scaleResizeImage(i, scaleRatio)
                        frame_back.paste(i, (int(190-i.width/2), int(570-i.height/2)), i)

                        frame_back = frame_back.convert('RGBA')
                        frames.append(frame_back)
                    print(frames[0])
                    frames[0].save("out.gif", format="GIF", append_images=frames[1:], duration=src_duration, disposal=2, save_all=True, optimize=False, loop=0)
                    await replied.reply(file=discord.File('out.gif'))
                    os.remove('out.gif')
                else:
                    print(f'Static emoji found')
                    foreground = foreground.convert('RGBA')
                    scaleRatio = await findScaleRatio(85, 85, foreground.width, foreground.height)
                    foreground = await scaleResizeImage(foreground, scaleRatio)
                    background.paste(foreground, ( int(415-foreground.width/2), int(130-foreground.height/2)), foreground)
                    scaleRatio = await findScaleRatio(40, 40, foreground.width, foreground.height)
                    foreground = await scaleResizeImage(foreground, scaleRatio)
                    background.paste(foreground, (int(190-foreground.width/2), int(570-foreground.height/2)), foreground)
                    background.save('out.png')
                    await replied.reply(file=discord.File('out.png'))
                    os.remove('out.png')
                foreground.close()
                os.remove(ftype)

            if str.lower(message.content).startswith('softbottom'):
                background = Image.open('softbottom.jpg')
                foreground = Image.open(ftype)
                drawspace = ImageDraw.Draw(background)
                font = ImageFont.truetype("Ldfcomicsans.ttf", 50)
                drawspace.text((220, 170), replied.author.name, fill=(0,0,0), font=font)
                drawspace.text((550, 1110), message.author.name, fill=(0,0,0), font=font)
                if emoji.animated:
                    print(f'Animated emoji found')
                    src_duration = foreground.info["duration"]
                    frames = []
                    for i in ImageSequence.Iterator(foreground):
                        i = i.convert("RGBA")
                        frame_back = copy.deepcopy(background).convert('RGBA')
                        scaleRatio = await findScaleRatio(180,180,i.width,i.height)
                        i = await scaleResizeImage(i,scaleRatio)
                        frame_back.paste(i, (int(820-i.width/2), int(430-i.height/2)), i)
                        frame_back = frame_back.convert('RGBA')
                        frames.append(frame_back)
                    frames[0].save("out.gif", format="GIF", append_images=frames[1:], duration=src_duration, disposal=2, save_all=True, optimize=False, loop=0)
                    await replied.reply(file=discord.File('out.gif'))
                    os.remove('out.gif')
                else:
                    print(f'Static emoji found')
                    foreground = foreground.convert('RGBA')
                    scaleRatio = await findScaleRatio(180,180,foreground.width,foreground.height)
                    foreground = await scaleResizeImage(foreground, scaleRatio)
                    background.paste(foreground, (int(820-foreground.width/2), int(430-foreground.height/2)), mask=foreground)
                    background.save('out.png')
                    await replied.reply(file=discord.File('out.png'))
                    os.remove('out.png')
                foreground.close()
                os.remove(ftype)
            return

        if str.lower(message.content).startswith('bottom'):
            default_emojis = await split_count(replied.content)
            print("found default emojies: " + str(default_emojis))
            for default_emoji in default_emojis:
                background = Image.open('unknown.png')
                parser = TwemojiParser(background)
                font = ImageFont.truetype("Ldfcomicsans.ttf", 100)
                await parser.draw_text((370, 70), default_emoji, font=font)
                await parser.close()
                drawspace = ImageDraw.Draw(background)
                font = ImageFont.truetype("Ldfcomicsans.ttf", 20)
                drawspace.text((100, 250), replied.author.name, fill=(0,0,0), font=font)
                drawspace.text((320, 350), message.author.name, fill=(0,0,0), font=font)
                parser = TwemojiParser(background)
                font = ImageFont.truetype("Ldfcomicsans.ttf", 30)
                await parser.draw_text((165, 555), default_emoji, font=font)
                await parser.close()
                background.save('out.png')
                await replied.reply(file=discord.File('out.png'))
                os.remove('out.png')
                break

        if str.lower(message.content).startswith('softbottom'):
            default_emojis = await split_count(replied.content)
            print("found default emojies: " + str(default_emojis))
            for default_emoji in default_emojis:
                background = Image.open('softbottom.jpg')
                parser = TwemojiParser(background)
                font = ImageFont.truetype("Ldfcomicsans.ttf", 200)
                await parser.draw_text((730, 320), default_emoji, font=font)
                await parser.close()
                drawspace = ImageDraw.Draw(background)
                font = ImageFont.truetype("Ldfcomicsans.ttf", 50)
                drawspace.text((220, 170), replied.author.name, fill=(0,0,0), font=font)
                drawspace.text((550, 1110), message.author.name, fill=(0,0,0), font=font)
                background.save('out.png')
                await replied.reply(file=discord.File('out.png'))
                os.remove('out.png')
                break

async def findScaleRatio(maxwidth, maxheight, currentwidth, currentheight):
    return min(maxwidth/currentwidth, maxheight/currentheight)

async def scaleResizeImage(image, scaleRatio):
    newWidth = int(image.width * scaleRatio)
    newHeight = int(image.height * scaleRatio)
    return image.resize((newWidth, newHeight), Resampling.LANCZOS)

async def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI['en'] for char in word):
            emoji_list.append(word)

    return emoji_list
client.run(sys.argv[1])
