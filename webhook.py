from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
import requests, random, json, time

r = lambda: random.randint(0,255)

with open('webhook.txt') as f:
    WebhookURL = f.read()

with open('publishedSongs.json') as f:
    data = json.load(f)

SiteURL = "https://m.mugzone.net/index"

page = requests.get(SiteURL)

soup = BeautifulSoup(page.content, "html.parser")

result = soup.find(id = "newMap")

mapLists = result.findAll(class_ = "g_map")

i = 0

##Please ignore this ugly implementation I spent 10 minutes learning Python
while(True):
    for mapList in mapLists:
        if "song" in mapList.find(class_ = "link")['href'] and mapList.find(class_ = "link")['href'] not in data:
            mapLink =  mapList.find(class_ = "link")['href']
            mapCoverLink = mapList.find(class_ = "link")['href']
            mapCover = "http://cni.machart.top/cover/" + mapCoverLink.replace("/song/", "")
            mapMode = "https://m.mugzone.net" + mapList.find(class_ = "mode")['src']
            mapTitle = mapList.find(class_ = "title textfix").getText()
            mapDifficulty = mapList.find(class_ = "version textfix").getText()

            if mapMode == "https://m.mugzone.net/static/img/mode/mode-3.png":
                webhook = DiscordWebhook(url=WebhookURL, rate_limit_retry = True)

                # create embed object for webhook
                embed = DiscordEmbed(title=mapTitle, url="https://m.mugzone.net" + mapLink, description=mapDifficulty, color='%02X%02X%02X' % (r(),r(),r()))
                data[mapLink] = mapTitle

                # set author
                embed.set_author(name="New Arrival!", icon_url="https://cdn.discordapp.com/app-icons/823408394098311178/68c5c14be69c732232a7d801ade229ab.png?size=512")

                # set image
                embed.set_image(url=mapCover)

                # set thumbnail
                embed.set_thumbnail(url=mapMode)

                # set footer
                embed.set_footer(text="Updated:")

                # set timestamp (default is now) accepted types are int, float and datetime
                embed.set_timestamp()

                webhook.add_embed(embed)
                with open('publishedSongs.json', 'w') as f:
                    json.dump(data, f)
                response = webhook.execute()
                i = 0
        else:
            print(f"{i} duplicated post")
            i = i + 1
    time.sleep(60)