import discord
import random
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)
TOKEN = os.getenv('BOT_TOKEN')

reaction_roles = {}
commands = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    addReactionRole('1266926938233245756', 'Announcements')
    addReactionRole('1266930773186052189', 'Media announcements')
    addReactionRole('1266931255577153576', 'Plot announcements')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    print(message.channel.name+' | '+message.author.name+": "+message.content)

    if message.content.startswith('<:elegant:1202444263992860672>'):
        await message.add_reaction('<:elegant:1202444263992860672>')
    if message.content.startswith('<:noway:1188524394490888232>'):
        await message.reply('https://tenor.com/view/shock-shocker-shocked-black-guy-gif-27526370')
    if message.content == 'https://tenor.com/view/fade-away-oooooooooooo-aga-emoji-crumble-gif-20008708':
        await message.add_reaction('<:cunningplan:1217949407568199820>')
    if message.content == 'https://tenor.com/view/smile-anime-bandar-activision-gif-22654042':
        await message.add_reaction('<:trollface:1210746859149328485>')
    if message.content == 'replit':
        await message.reply('\N{SKULL}')
    if message.content == '<:trollface:1210746859149328485>':
        await message.add_reaction('<:trollface:1210746859149328485>')

    member = message.author  # Getting the member object

    if message.content.startswith('$'):
        await checkCommand(message, member)

    # Check if the member has a specific role
    role_name = ":skull:"
    role = discord.utils.get(member.roles, name=role_name)
    if role is not None:
        await message.add_reaction('\N{SKULL}')

@client.event
async def on_raw_reaction_add(payload):
    # Fetch the channel
    channel = await client.fetch_channel(payload.channel_id)
    # Fetch the message
    message = await channel.fetch_message(payload.message_id)

    # Get the guild from the payload
    guild = client.get_guild(payload.guild_id)

    # Get the member who reacted
    member = guild.get_member(payload.user_id)
    if member.id == client.application_id:
        return

    if str(message.id) in reaction_roles:
        # Fetch the role name from reaction_roles dictionary
        role_name = reaction_roles[str(message.id)]
        # Get the role object
        role = discord.utils.get(guild.roles, name=role_name)

        if role is not None and member is not None:
            # Add the role to the member
            await member.add_roles(role)
            print(f"Added role {role_name} to {member.name}")
        else:
            print("Role or member not found")
    else:
        print("Message ID not in reaction roles")



async def checkCommand(message: discord.Message, author: discord.User):
    params = message.content.split(' ')
    for cmd in commands:
        if (message.content.startswith('$'+cmd)):
            await commands[cmd](message, params)
            return
    await message.reply('Command not found')

def addCommand(name, func):
    commands[name] = func

def addReactionRole(message_id, role):
    if message_id in reaction_roles:
        return
    reaction_roles[message_id] = role

async def ball(msg, params):
    await msg.reply(random.choice(['Yes', 'No', 'Maybe']))

addCommand('8ball', ball)

client.run(TOKEN)

# 1147910177685766310