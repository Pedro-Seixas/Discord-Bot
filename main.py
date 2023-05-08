import discord
from discord_components import DiscordComponents, Button
from discord.ext import commands
import sqlite3
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

#From now on the bot is configured to answer in portuguese brazilian, since it was made exclusive for a brazilian server of friends.

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
        title='Lista de Comandos',
        colour=discord.Colour.orange()
    )
    embed.add_field(name='**~!start**',
                    value='Inicializar o bot', inline=False)
    embed.add_field(name='**~!stop**', value='Pausar o bot', inline=False)
    embed.add_field(name='**~!timer**',
                    value='Definir o tempo em segundos entre os memes', inline=False)
    embed.add_field(name='**~!page**',
                    value='Definir o link do site do memedroid que o bot pegará os memes', inline=False)
    embed.add_field(name='**~!channel**',
                    value='Definir o id do channel que o bot enviará os memes', inline=False)
    embed.add_field(name='**~!memes**',
                    value='Para ver o número de memes já enviado pelo bot', inline=False)
    embed.add_field(name='**~!upload**',
                    value='Para enviar um meme para o site do memedroid', inline=False)
    embed.add_field(name='**~!autor**',
                    value='Para ver o criador do bot', inline=False)
    embed.set_author(name="Memedroid Bot")
    embed.set_image(
        url='https://cdn.discordapp.com/avatars/951157327795458058/d95fa02708848715eb6a18b5ac358fcb.png?size=2048')
    await ctx.reply(embed=embed)


@client.command()
async def start(ctx):
    if ws.stop_status() == 0:
        await ctx.channel.send(f"Bot já está ligado e mandando memes. Para alterar o intervalo entre os memes use ~!timer")
        
    else:
        await ctx.channel.send(f'**Bot Started**')
        ws.change_stop_status(0)
        await ws.both_request()


@client.command()
async def channel(ctx, channel):
    if channel.isnumeric():
        await ctx.reply(f'Channel Configured!')
        ws.change_channel(channel)
    else:
        await ctx.channel.send(f'Não é um id de channel!')


@client.command()
async def timer(ctx, timer_escolhido):
    if timer_escolhido.isnumeric():
        ws.change_delay(int(timer_escolhido))
        await ctx.reply(f'Timer configurado para {timer_escolhido} segundos')
    else:
        await ctx.reply(f'Coloque um numero em segundos!')


@client.command()
async def autor(ctx):
    await ctx.reply(f'O meu criador foi o Penguin (Pedro1#6199) UwU')


@client.command()
async def page(ctx, page_escolhida):
    ws.change_page_bot(page_escolhida)
    await ctx.reply(f'Page Configured')


@client.command()
async def stop(ctx):
    ws.change_stop_status(1)
    await ctx.reply(f'**Bot Pausado**')

@client.command()
async def memes(ctx):
    #TODO use function inside class
    # conn = sqlite3.connect('memes.db')
    # cursor = conn.cursor()
    # check_db = "SELECT COUNT(*) FROM memes_sent"
    # cursor.execute(check_db)
    # last_id = cursor.fetchone()[0]
    last_id = ws.see_id_database()
    create_graph()
    
    await ctx.channel.send(f"O bot ja enviou {last_id} memes!", file =discord.File("topUsersPieChart.png"))
    

TOKEN = "OTUxMTU3MzI3Nzk1NDU4MDU4.GQvs9G.xI2iudp6pa27Md_hjP4FPkuQOCvmN8mcg25YsM"

client.run(TOKEN)