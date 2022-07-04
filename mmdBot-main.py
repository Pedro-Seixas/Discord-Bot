import discord
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import asyncio
from discord_components import DiscordComponents, Button
from discord.ext import commands
import mysql.connector
from mysql.connector import Error
from piePlot import create_graph


client = discord.Client()
client = commands.Bot(command_prefix='~!')
DiscordComponents(client)


class WebScrapping:
    def see_id_database(self):
        try:
            connection = mysql.connector.connect(host='remotemysql.com', database='lQcUi31XZz', user='lQcUi31XZz', password='8nIEHO3Rx3')
            consult_sql = "select * from memes_enviados"
            cursor = connection.cursor()
            cursor.execute(consult_sql)
            cursor.fetchall()
    
        except Error as erro:
            print(erro)

        last_id = cursor.rowcount

        return last_id 

    def insert_database_memes_enviados(self,autor):

        try:
            connection = mysql.connector.connect(host='remotemysql.com', database='lQcUi31XZz', user='lQcUi31XZz', password='8nIEHO3Rx3')
            insert_memes = """INSERT INTO memes_enviados (autor) VALUES (%s)"""
            cursor = connection.cursor()
            cursor.execute(insert_memes,(autor,))
            connection.commit()
            print(cursor.rowcount, "Inserted")
            cursor.close()

        except Error as error:
            print(error)

        finally:
            if(connection.is_connected()):
                connection.close()
                print("Connection MySQL Ended")

    def check_database_memes_recebidos(self, link): 
        try:
            connection = mysql.connector.connect(host='remotemysql.com', database='lQcUi31XZz', user='lQcUi31XZz', password='8nIEHO3Rx3')
            consulta_sql = "SELECT link, COUNT(*) FROM memes_recebidos WHERE link = %s GROUP BY link"
            cursor = connection.cursor()
            cursor.execute(consulta_sql,(link,))
            cursor.fetchall()
    
        except Error as erro:
            print(erro)

        finally:
            if cursor.rowcount == 0:
                print("Meme Does Not Exist On DataBase")
                return 1
            else:
                print("Meme Exists On DataBase")
                return 0

    def insert_database(self, link, autor):
        try:
            connection = mysql.connector.connect(host='remotemysql.com', database='lQcUi31XZz', user='lQcUi31XZz', password='8nIEHO3Rx3')
            inserir_memes = """INSERT INTO memes_recebidos (autor,link) VALUES (%s,%s)"""
            cursor = connection.cursor()
            cursor.execute(inserir_memes,(autor,link,))
            connection.commit()
            print(cursor.rowcount, "Inserted")
            cursor.close()

        except Error as error:
            print(error)

        finally:
            if(connection.is_connected()):
                connection.close()
                print("Connection MySQL Ended")

    def __init__(self, discord_channel, pagina, delay, stop_bot):
        self.discord_channel = discord_channel
        self.pagina = pagina
        self.delay = delay
        self.stop_bot = stop_bot

    def change_delay(self, delay):
        self.delay = delay

    def change_canal(self, canal):
        self.discord_channel = canal

    def change_stop_status(self, stop_bot):
        self.stop_bot = stop_bot
      
    def stop_status(self):
        print(self.stop_bot)
        return self.stop_bot 
      
    def read_web_page(self):
        print(self.pagina)
        request_page = Request(self.pagina,
                               headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'})
        page_html = urlopen(request_page).read()
        html_soup = BeautifulSoup(page_html, 'html.parser')
        html_page = html_soup.find_all('div', class_="gallery-memes-container")

        return html_page

    def start_web_scrapping(self):
        html_page = self.read_web_page()
        for articles in html_page:
            articles_data_type = articles.find_all(
                'article', class_="gallery-item")

        return articles_data_type
    
    def next_page(self):
        html_page = self.read_web_page()
        
        for page_hidden in html_page:
            next_page = page_hidden.find(
                'nav', class_="hidden")
            next_page_link = next_page.a['href']
            print(f"Next Page = {next_page_link}")
            self.pagina = (f'https://pt.memedroid.com{next_page_link}')

    def change_page_bot(self, pagina):
        self.pagina = pagina

    async def both_request(self):
        memes_page = self.start_web_scrapping()
        channel = client.get_channel(int(self.discord_channel))
        counterImage = 0
        counterGif = 0
        countI = 0
        countG = 0

        for meme in memes_page:
            if countI <= counterImage and meme['data-type']=='1' and (self.stop_bot == 0 or self.stop_bot == 2):
                counterImage = counterImage + 1

                if meme.div.img['src'] != '/images/icons/icon_play.png' and meme.div.img:
                    links = meme.div.img['src']
                    rate = meme.span.text
                    username = meme.header.div.a.text

                    if self.check_database_memes_recebidos(links) == 1:
                        if int(rate[0]) <= 5 and rate != "100%":
                            await channel.send(f"**Autor: **{username}\n**Titulo:** {meme.a.text}\n{links}", components = [
                                [Button(label = f"{rate}", style ="4", custom_id = "button5")]])
                        else:
                            await channel.send(f"**Autor: **{username}\n**Titulo:** {meme.a.text}\n{links}", components = [
                                [Button(label = f"{rate}", style ="3", custom_id = "button5")]])    
                        await asyncio.sleep(0.2)
                        await channel.send(f"---------------------------------------------------------------------------------------")
                        print("Inserting DB")
                        self.insert_database(links, username)
                        await asyncio.sleep(self.delay)
                        countI = countI + 1
                    else: 
                        print(counterImage)
                        print(counterGif)
                        print(countI)
                        print(countG)
                        countI = countI + 1
                        print("Already Exists on DB, skipping to the next meme")
                        continue

            if countG <= counterGif and meme['data-type'] == '3' and (self.stop_bot == 0 or self.stop_bot == 2):    
                counterGif = counterGif + 1

                if meme.source:
                    links = meme.source['src']
                    rate = meme.span.text
                    username = meme.header.div.a.text
                    if self.check_database_memes_recebidos(links) == 1:

                        if int(rate[0]) <= 5 and rate != "100%":
                            await channel.send(f"**Autor: **{username}\n**Titulo:** {meme.a.text}\n{links}", components = [
                                [Button(label = f"{rate}", style ="4", custom_id = "button5")]])
                        else:
                            await channel.send(f"**Autor: **{username}\n**Titulo:** {meme.a.text}\n{links}", components = [
                                [Button(label = f"{rate}", style ="3", custom_id = "button4")]])    
                        await asyncio.sleep(0.2)
                        await channel.send(f"---------------------------------------------------------------------------------------")

                        print("Inserir database")
                        self.insert_database(links, username)

                        await asyncio.sleep(self.delay)

                        countG = countG + 1   
                    else:
                        print(counterImage)
                        print(counterGif)
                        print(countI)
                        print(countG)
                        countI = countG + 1
                        print("Already Exists on DB, skipping to the next meme")
                        continue

        if countI == counterImage and countG == counterGif and (self.stop_bot == 0 or self.stop_bot == 2):
            self.next_page()
            self.read_web_page()
            await self.both_request()



ws = WebScrapping(915332488728031292,
                  'https://pt.memedroid.com/memes/latest', 1000, 2)
                  
@client.event
async def on_ready():
    #If enters/is in another server, it will leave.
    for guild in client.guilds:
        if guild.id != 915330953918947368 and guild.id != 951157200091492392:
            await guild.leave()
    print("----------Bot Iniciado------------")
    print("By default, channel = memes-e-media\nDelay = 1000 seconds\nWebsite = https://pt.memedroid.com/memes/latest")
    print("You change change this value using the ~! commands")
    activityDiscord = discord.Game(name="~!ajuda")
    await client.change_presence(status=discord.Status, activity=activityDiscord)

#From now on the bot is configured to answer in portuguese brazilian, since it was made exclusive for a brazilian server of friends.

@client.event
async def on_guild_join(guild):
    if guild.id != 915330953918947368:
        await guild.leave()
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Comando Invalido! Use ~!ajuda para acessar a lista de comandos.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Complete o comando. Use ~!ajuda para acessar a lista de comandos')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply('Voce não tem permissão para usar o bot, somente moderadores.')


@client.command()
async def ajuda(ctx):
    embed = discord.Embed(
        title='Lista de Comandos',
        colour=discord.Colour.orange()
    )
    embed.add_field(name='**~!start**',
                    value='Inicializar o bot', inline=False)
    embed.add_field(name='**~!stop**', value='Pausar o bot', inline=False)
    embed.add_field(name='**~!timer**',
                    value='Definir o tempo em segundos entre os memes', inline=False)
    embed.add_field(name='**~!pagina**',
                    value='Definir o link do site do memedroid que o bot pegará os memes', inline=False)
    embed.add_field(name='**~!canal**',
                    value='Definir o id do canal que o bot enviará os memes', inline=False)
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
@commands.has_any_role(915332018827579504, 928026454447505468, 915333382018334781, 915333704090525756, 959241153323106334,954865503418069012)
async def start(ctx):
    if ws.stop_status() == 0:
        await ctx.channel.send(f"Bot já está ligado e mandando memes. Para alterar o intervalo entre os memes use ~!timer")
        
    else:
        await ctx.channel.send(f'**Bot Iniciado**')
        ws.change_stop_status(0)
        await ws.both_request()


@client.command()
@commands.has_any_role(915332018827579504, 928026454447505468, 915333382018334781, 915333704090525756, 959241153323106334,954865503418069012)
async def canal(ctx, canal):
    if canal.isnumeric():
        await ctx.reply(f'Canal configurado!')
        ws.change_canal(canal)
    else:
        await ctx.channel.send(f'Não é um id de canal!')


@client.command()
@commands.has_any_role(915332018827579504, 928026454447505468, 915333382018334781, 915333704090525756, 959241153323106334,954865503418069012)
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
@commands.has_any_role(915332018827579504, 928026454447505468, 915333382018334781, 915333704090525756, 959241153323106334,954865503418069012)
async def pagina(ctx, pagina_escolhida):
    ws.change_page_bot(pagina_escolhida)
    await ctx.reply(f'Pagina Configurada')


@client.command()
@commands.has_any_role(915332018827579504, 928026454447505468, 915333382018334781, 915333704090525756, 959241153323106334,954865503418069012)
async def stop(ctx):
    ws.change_stop_status(1)
    await ctx.reply(f'**Bot Pausado**')

@client.command()
async def jj(ctx):
    await ctx.reply(f'**Dias sem o JayJay tiltar: 0\nRecorde até agora: 0**')

@client.command()
async def memes(ctx):
    connection = mysql.connector.connect(host='remotemysql.com', database='lQcUi31XZz', user='lQcUi31XZz', password='8nIEHO3Rx3')
    consulta_sql = "select * from memes_recebidos"
    cursor = connection.cursor()
    cursor.execute(consulta_sql)
    linhas = cursor.fetchall()
    total = cursor.rowcount
    create_graph()
    
    await ctx.channel.send(f"O bot ja enviou {total} memes!", file =discord.File("topUsersPieChart.png"))
    

TOKEN = "OTUxMTU3MzI3Nzk1NDU4MDU4.YijYSg.j7H5l_lK0bkyLgoEGlmhPYZycC4"

client.run(TOKEN)