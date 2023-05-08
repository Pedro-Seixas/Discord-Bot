import discord
from discord_components import DiscordComponents, Button
from discord.ext import commands
from piePlot import create_graph
from mmdWebscraping import WebScrapping


client = discord.Client()
client = commands.Bot(command_prefix='~!')
DiscordComponents(client)

#(ID CHANNEL, WEBSITE LINK, DELAY)

ws = WebScrapping(1104063740481122488,
                  'https://pt.memedroid.com/memes/latest', 1000, client)
                
@client.event
async def on_ready():
    #If enters/is in another server, it will leave.
    for guild in client.guilds:
        if guild.id != 1104063740481122484:
            await guild.leave()
    print("----------Bot Online------------")
    print("By default, channel = memes-e-media\nDelay = 1000 seconds\nWebsite = https://pt.memedroid.com/memes/latest")
    print("You can change this value using the ~! commands")
    activityDiscord = discord.Game(name="~!helpp")
    await client.change_presence(status=discord.Status, activity=activityDiscord)

#From now on the bot is configured to answer in brazilian portuguese, since it was made exclusive for a brazilian server of friends.

@client.event
async def on_guild_join(guild):
    if guild.id != 1104063740481122484:
        await guild.leave()
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Comando Invalido! Use ~!helpp para acessar a lista de comandos.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Complete o comando. Use ~!helpp para acessar a lista de comandos')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply('Voce não tem permissão para usar o bot, somente moderadores.')


@client.command()
async def helpp(ctx):
    embed = discord.Embed(
        title='Command List',
        colour=discord.Colour.orange()
    )
    embed.add_field(name='**~!start**',
                    value='Inicializar o bot', inline=False)
    embed.add_field(name='**~!stop**', value='Pausar o bot', inline=False)
    embed.add_field(name='**~!delay**',
                    value='Definir o tempo em segundos entre os memes', inline=False)
    embed.add_field(name='**~!page**',
                    value='Definir o link do site do memedroid que o bot pegará os memes', inline=False)
    embed.add_field(name='**~!channel**',
                    value='Definir o id do channel que o bot enviará os memes', inline=False)
    embed.add_field(name='**~!memes**',
                    value='Para ver o número de memes já enviado pelo bot', inline=False)
    embed.add_field(name='**~!upload**',
                    value='Para enviar um meme para o site do memedroid', inline=False)
    embed.add_field(name='**~!creator**',
                    value='Para ver o criador do bot', inline=False)
    embed.set_author(name="Memedroid Bot")
    embed.set_image(
        url='https://cdn.discordapp.com/avatars/951157327795458058/d95fa02708848715eb6a18b5ac358fcb.png?size=2048')
    await ctx.reply(embed=embed)


@client.command()
async def start(ctx):
    if ws.stop_status() == 0:
        await ctx.channel.send(f"Bot is already on. Use ~!delay to change the delay.")
        
    else:
        await ctx.channel.send(f'**Bot Started**')
        ws.change_stop_status(0)
        await ws.both_request()


@client.command()
async def channel(ctx, channel):
    if channel.isnumeric():
        await ctx.reply(f'Channel Set')
        ws.change_channel(channel)
    else:
        await ctx.channel.send(f'Is not a channel id!')


@client.command()
async def delay(ctx, delay_escolhido):
    if delay_escolhido.isnumeric():
        ws.change_delay(int(delay_escolhido))
        await ctx.reply(f'The delay was set to {delay_escolhido} seconds')
    else:
        await ctx.reply(f'Must be an number in seconds')


@client.command()
async def creator(ctx):
    await ctx.reply(f'My creator was Pedro1#6199')


@client.command()
async def page(ctx, page_escolhida):
    ws.change_page_bot(page_escolhida)
    await ctx.reply(f'Page Configured')


@client.command()
async def stop(ctx):
    ws.change_stop_status(1)
    await ctx.reply(f'**Bot Paused**')

@client.command()
async def memes(ctx):
    last_id = ws.see_id_database()
    create_graph()
    
    await ctx.channel.send(f"The bot has already sent {last_id} memes!", file =discord.File("topUsersPieChart.png"))
    

TOKEN = "OTUxMTU3MzI3Nzk1NDU4MDU4.GQvs9G.xI2iudp6pa27Md_hjP4FPkuQOCvmN8mcg25YsM"

client.run(TOKEN)