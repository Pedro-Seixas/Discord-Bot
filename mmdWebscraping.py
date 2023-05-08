from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import asyncio
import sqlite3
from discord_components import DiscordComponents, Button
from discord.ext import commands
import discord

class WebScrapping:
    def __init__(self, discord_channel, page, delay, client):
        self.discord_channel = discord_channel
        self.page = page
        self.delay = delay
        self.stop_bot = 2
        self.client = client

    def see_id_database(self):
        try:
            conn = sqlite3.connect('memes.db')
            cursor = conn.cursor()
            check_db = "SELECT COUNT(*) FROM memes_sent"
            cursor.execute(check_db)
            last_id = cursor.fetchone()[0]
            return last_id 
        
        except sqlite3.Error as error:
            print(error)


    def check_database(self, link): 
        try:
            conn = sqlite3.connect('memes.db')
            cursor = conn.cursor()
            check_db = "SELECT link, COUNT(*) FROM memes_sent WHERE link = '{}' GROUP BY link".format(link)
            cursor.execute(check_db)
            result = cursor.fetchall()

            if len(result) == 0:
                print("Meme Does Not Exist On DataBase")
                return 1
            else:
                print("Meme Exists On DataBase")
                return 0

        except sqlite3.Error as error:
            print(error)

        finally:
            conn.close()

    def insert_database(self, link, autor):
        try:
            conn = sqlite3.connect('memes.db')
            cursor = conn.cursor()
            insert_memes = """INSERT INTO memes_sent (username, link) VALUES (?,?)"""
            cursor.execute(insert_memes,(autor,link,))
            conn.commit()
            print(cursor.rowcount, "Inserted")
            conn.close()

        except sqlite3.Error as error:
            print(error)

    def change_delay(self, delay):
        self.delay = delay

    def change_channel(self, channel):
        self.discord_channel = channel

    def change_stop_status(self, stop_bot):
        self.stop_bot = stop_bot
      
    def stop_status(self):
        print(self.stop_bot)
        return self.stop_bot 
      
    def read_web_page(self):
        print(self.page)
        request_page = Request(self.page,
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
            self.page = (f'https://pt.memedroid.com{next_page_link}')

    def change_page_bot(self, page):
        self.page = page

    async def both_request(self):
        memes_page = self.start_web_scrapping()
        channel = self.client.get_channel(int(self.discord_channel))
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
                    print(links)
                    if self.check_database(links) == 1:
                        if int(rate[0]) <= 5 and rate != "100%":
                            await channel.send(f"**User: **{username}\n**Title:** {meme.a.text}\n{links}", components = [
                                [Button(label = f"{rate}", style ="4", custom_id = "button5")]])
                        else:
                            await channel.send(f"**User: **{username}\n**Title:** {meme.a.text}\n{links}", components = [
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
                    if self.check_database(links) == 1:

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
