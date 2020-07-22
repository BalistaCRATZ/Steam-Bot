from bs4 import BeautifulSoup
import requests
import pandas as pd
from twilio.rest import Client
from time import sleep

account_id = #your twilio account_id
auth_token = #your twilio auth_token

client = Client(account_id, auth_token)

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def getPrices(results):
    
    price_list = []
    i = 1
    
    while i <= len(results):
    
        space = results[i].text.find(" ")
        
        value = float(results[i].text[1:space])
        
        price_list.append(float("{:.2f}".format(value * 0.8)))
        
        i = i + 2
    
    return price_list    

def getNamesAndQualities(results):
    
    name_list = []
    quality_list = []
    
    for result in results:
    
        vert = result.text.find("|")
        bracket = findOccurrences(result.text, "(")
        
        name = result.text[vert + 2: bracket[-1] - 1]
        
        name_list.append(name)
        
        quality = result.text[bracket[-1] + 1: len(result.text) - 1]
        
        quality_list.append(quality)
    
    return [name_list, quality_list]

def isStatTrak(results):
    
    stattrak_list = []
    
    for result in results:
        
        if "StatTrak" in result.text:
            
            stattrak_list.append(True)
            
        else:
            
            stattrak_list.append(False)
    
    return stattrak_list
    
def getLink(results):
    
    links = []
    
    for link in results:
        
        links.append(link["href"])
    
    return links
    
URL = "https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_m4a1&category_730_Rarity%5B%5D=tag_Rarity_Mythical_Weapon&category_730_Rarity%5B%5D=tag_Rarity_Legendary_Weapon&category_730_Rarity%5B%5D=tag_Rarity_Ancient_Weapon&category_730_Rarity%5B%5D=tag_Rarity_Mythical_Character&category_730_Rarity%5B%5D=tag_Rarity_Legendary_Character&category_730_Rarity%5B%5D=tag_Rarity_Ancient_Character&category_730_Rarity%5B%5D=tag_Rarity_Ancient&category_730_Rarity%5B%5D=tag_Rarity_Mythical&category_730_Rarity%5B%5D=tag_Rarity_Legendary&appid=730"

listofnames = ["Griffin", "Desolate Space", "Neo-Noir", "龍王 (Dragon King)", "The Emperor", "Hellfire"]

while True:
    
   sleep(10)
   
   page = requests.get(URL)

   soup = BeautifulSoup(page.content, "html.parser")
    
   price_results = soup.findAll(class_="normal_price")
   name_results = soup.findAll(class_ = "market_listing_item_name")
   link_results = soup.findAll(class_ = "market_listing_row_link", href = True)
    
   prices = getPrices(price_results)

   names = getNamesAndQualities(name_results)[0]
   qualities = getNamesAndQualities(name_results)[1] 

   stattrak = isStatTrak(name_results)

   links = getLink(link_results)
    
   data = {"Name": names, "Price": prices, "Quality": qualities, "StatTrak?": stattrak, "Link": links}

   df = pd.DataFrame(data)
   
   print(df)
    
   for index, row in df.iterrows():
       
    stattrakstate = ""
    
    if 6.00 < row["Price"] < 10.00:
        
        if row["Name"] in listofnames:
            
            if row["StatTrak?"] == True:
                
                stattrakstate = "StatTrak"
            
            message = client.messages.create(body = "I found a {} M4A4 {} for {}. \n \n Link: {}".format(stattrakstate, row["Name"], row["Price"], row["Link"] ), 
                                             messaging_service_sid = #your messaging service sid, 
                                             to = #your phone number)
            
            print("I found a {} M4A4 {} for {}. \n \n Link: {}".format(stattrakstate, row["Name"], row["Price"], row["Link"] ))
            
    else:
        
        pass
