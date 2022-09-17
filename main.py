import discord, os, asyncio, logging, sys, json
from discord.ext import commands, tasks

#For unverified Bots.
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "!", intents = intents)

"""
#For verified bots
_i = discord.Intents.default()
_i.members = True
#Only enable the bottom intent if you have it available. 
#_i.presence = True
client = commands.Bot(command_prefix=commands.when_mentioned, intents = ) 
#client = commands.AutoShardedBot(command_prefix = commands.when_mentioned, intents = _i, shard_count = 1)
#Only enable above and remove already existing client if your bot needs sharding, and then add the appropriate shard count needed. 3k servers = 3 shards, 4k servers = 4 shards, etc.
"""


#Ignore this, just console logging and config stuff.
with open("./config.json", "r") as file:
  config = json.load(file)
  embedFooterText = config["embedFooterText"]
  embedFootericonURL = config['embedFootericonURL']
  embedImageURL = config['embedImageURL']
  embedThumbnailURL = config['embedThumbnailURL']
  botToken = config['token']
  

#Turn to cog?
class _AnsiColorizer(object):
    _colors = dict(black=30, red=31, green=32, yellow=33,
                   blue=34, magenta=35, cyan=36, white=37)

    def __init__(self, stream):
        self.stream = stream

    @classmethod
    def supported(cls, stream=sys.stdout):
        if not stream.isatty():
            return False  
        try:
            import curses
        except ImportError:
            return False
        else:
            try:
                try:
                    return curses.tigetnum("colors") > 2
                except curses.error:
                    curses.setupterm()
                    return curses.tigetnum("colors") > 2
            except:
                raise
                return False

    def write(self, text, color):

        color = self._colors[color]
        self.stream.write('\x1b[%s;1m%s\x1b[0m' % (color, text))

class ColorHandler(logging.StreamHandler):
    def __init__(self, stream=sys.stderr):
        super(ColorHandler, self).__init__(_AnsiColorizer(stream))

    def emit(self, record):
        msg_colors = {
            logging.DEBUG: "green",
            logging.INFO: "blue",
            logging.WARNING: "yellow",
            logging.ERROR: "red"
        }

        color = msg_colors.get(record.levelno, "blue")
        self.stream.write(record.msg + "\n", color)


logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(ColorHandler())

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
for handler in LOG.handlers:
    LOG.removeHandler(handler)

LOG.addHandler(ColorHandler())


@client.event
async def on_connect():
  logging.info('[INFO] [Connected to the API.]')

@client.event
async def on_ready():
  await client.change_presence(status= discord.Status.online, activity = discord.Game(name="A status here..."))
  logging.debug(f"[INFO] {client.user} is online.")
  

@client.event
async def on_message(message):
  messaged = "User DM"
  if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
    try:
      async with message.channel.typing():
        await asyncio.sleep(3)
      #Start making your embed here.
      dmEmbed = discord.Embed(title="Embed title", description = "A description here with an emoji. :thumbsup: Custom emojis are supported.", color = 0xFF0000) # Change the description, title as you wish. The hex code will be after the 0x
      dmEmbed.set_image(url=embedImageURL) #Set the bots image of embed in config.json [embedImageURL]
      dmEmbed.set_footer(text=embedFooterText or "-", icon_url =embedFootericonURL or "https://media.discordapp.net/attachments/980486928472342558/1019661366296051752/unknown.png") #Set embed footer icon URL in config.json [embedFootericonURL] and set embed footer text in config.json [embedFooterText]
      dmEmbed.set_thumbnail(url=embedThumbnailURL or "https://media.discordapp.net/attachments/980486928472342558/1019661366296051752/unknown.png") #Set embed thumbnail icon URL in config.json [embedThumbnailURL] 
      deleteAfter = await message.channel.send(embed=dmEmbed)
      #Embed stops here, don't mess anything up below. 
      logging.debug(f"[{messaged}] | {message.author} dm'ed me - Sent DM.")
      await asyncio.sleep(300)
      await deleteAfter.delete()
      logging.error(f"[DM Delete] Deleted A DM - [{message.author}]")
    except discord.HTTPException:
      logging.error(f'Cannot DM this user: [{message.author.id}]')
    except Exception as exc:
      logging.error(f"Ignoring Error: {exc}")
  await client.process_commands(message)
      
      
      
      
      
      
      
  


if __name__ == '__main__':
  try:
    client.run(botToken)
  except Exception as exc:
    logging.error(f'[INVALID] Token Provided Is Invalid: {exc}')
