from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
import requests, random, json, time

r = lambda: random.randint(0,255)

#Create a text file with your webhook link to use this
with open('webhook.txt') as f:
    WebhookURL = f.read()

#read a json file with recents update. Create one if you don't have it
with open('publishedSongs.json') as f:
    data = json.load(f)

SiteURL = "https://m.mugzone.net/index"

page = requests.get(SiteURL)

soup = BeautifulSoup(page.content, "html.parser")

result = soup.find(id = "newMap")

mapLists = result.findAll(class_ = "g_map")

chartList = []

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
                mapURL = "https://m.mugzone.net" + mapLink
                mapPage = requests.get(mapURL)
                mapSoup = BeautifulSoup(mapPage.content, "html.parser")
                
                charts = mapSoup.findAll(class_ = "item")
                for chart in charts:
                    chartStatus = chart.find(class_ = 'col3').getText()
                    chartAuthor = chart.find(class_ = "col5 textfix")
                    if chartStatus == "Stable" and "/static/img/mode/mode-3.png" in chart.find('img')['src']:
                        chartList.append(f"{chart.find('a').getText()} | [{chartAuthor.getText()}](https://m.mugzone.net{chartAuthor.find("a")['href']})")
                
                webhook = DiscordWebhook(
                    url=WebhookURL, 
                    rate_limit_retry = True
                    )

                embed = DiscordEmbed(
                    title=mapTitle, 
                    description=mapSoup.find(class_ = 'textfix artist').getText(),
                    url=mapURL,
                    color='%02X%02X%02X' % (r(),r(),r()))

                data[mapLink] = mapTitle

                embed.set_author(
                    name="New Arrival!", 
                    icon_url="https://cdn.discordapp.com/app-icons/823408394098311178/68c5c14be69c732232a7d801ade229ab.png?size=512")

                embed.set_image(
                    url=mapCover
                    )

                embed.set_thumbnail(
                    url=mapMode
                    )
                
                embed.add_embed_field(
                    name="Charts:", 
                    value=f'{"\n".join(chartList)}'
                    )

                embed.set_footer(
                    text="Updated:"
                    )

                embed.set_timestamp()

                webhook.add_embed(embed)
                
                #Write song that are updated to json file
                with open('publishedSongs.json', 'w') as f:
                    json.dump(data, f)
                response = webhook.execute()
                i = 0
        else:
            print(f"{i} duplicated post")
            i = i + 1
    #anti spamming
    time.sleep(60)