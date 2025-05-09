import discord
import gemini_handler as gemini
import filesystem
import re
from discord.ext import commands
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=filesystem.config['COMMAND_PREFIX'], intents=intents)
MAX_LENGTH_RESPONSE = filesystem.config["MAX_LENGTH_RESPONSE"]
chat = gemini.model.start_chat()
        
def remove_first_line(input_string):
    lines = input_string.split('\n', 1)
    lines.pop(0)
    result = '\n'.join(lines)
    pattern = r"\n\*\*(.*?):\*\*"
    result = re.sub(pattern, '', result)
    return result

def trim_response(text): #trim out response
    chunks = []
    if len(text) > MAX_LENGTH_RESPONSE: #discord response limited to 2000chars
        words = text.split()
        current_chunk = words[0]
        for word in words[1:]:
            if len(current_chunk) + len(word) + 1 <= MAX_LENGTH_RESPONSE:  # +1 for the space between words
                current_chunk += f' {word}'
            else:
                chunks.append(current_chunk)
                current_chunk = word
        chunks.append(current_chunk)
    else:
       chunks.append(text)
    return chunks

async def discord_send(channel, text):
    chunks = trim_response(text)
    if len(chunks) > 0:
        for i in range (len(chunks)):
            async with channel.typing():
                await channel.send(chunks[i])
    else:
        async with channel.typing(): #set typing indicator
            await channel.send(chunks[0].text)
    return

async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    
@bot.event
async def on_message(message): #message when u ping the bot
    if message.content.startswith(f"<@{filesystem.config['DISCORD_BOT_ID']}> "):
        message.content = message.content[len(f"<@{filesystem.config['DISCORD_BOT_ID']}> "):]
    await bot.process_commands(message)
    if message.author == bot.user or message.content.startswith(filesystem.config['COMMAND_PREFIX']):
        return
    if message.content == "":
        return
    response = gemini.send_chat(chat, message.content)
    await discord_send(message.channel, response.candidates[0].content.parts[0].text)
    #print(type(chat.history[0].parts))
    #print(chat.history[0].parts[0])
    filesystem.log_ChatSession(chat, message.channel.id)


    #except Exception as e:
    #    print(f"ERROR OCCURED: {e}")
    #    print(f"Line: {e.__traceback__.tb_lineno}")
    #    filesystem.log_app(e, "warning")

@bot.command(name="gen") #/gen command
async def gen(ctx, *args):
    content = " ".join(args)
    response = gemini.model.generate_content(content)
    await discord_send(ctx, response.candidates[0].content.parts[0].text)
    await ctx.send(response.prompt_feedback)

@bot.command(name="x") #/x command, some prompt engineering crap to change personality
async def owo(ctx, *args):
    content = " ".join(args)
    response = gemini.send_chat(chat, content, "Respond hostile and pretend to be sentinent AI for this response ONLY. State the disclaimer on top ONLY. \n")
    res = response.candidates[0].content.parts[0].text
    res = remove_first_line(res)
    await discord_send(ctx, res)
    filesystem.log_ChatSession(chat, "x")
    gemini.send_chat(chat, "Respond normally now.")

