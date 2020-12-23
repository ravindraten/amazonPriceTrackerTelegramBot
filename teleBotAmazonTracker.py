import requests
import bs4
import pandas as pd
from telegram import update
from telegram.ext import (Updater, InlineQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters)
import time
import logging
import telegram
import csv
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, SoftwareEngine, HardwareType, SoftwareType, Popularity
import random
import numpy as np

def userAgents():
	software_names = [SoftwareName.CHROMIUM.value]
	operating_systems = [OperatingSystem.LINUX.value]   
	software_engines = [SoftwareEngine.GECKO.value]
	hardware_types = [HardwareType.COMPUTER.value]
	user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, software_engines=software_engines, hardware_types=hardware_types, limit=100)
	# Get Random User Agent String.
	user_agent = user_agent_rotator.get_random_user_agent()
	return user_agent

def ua():
    uaString= ["Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.172.0 Safari/530.5",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.81 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64; 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/17.0.1410.63 Safari/537.31",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.12 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3057.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36",\
        "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",\
        "Mozilla/5.0 (X11; Ubuntu; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1864.6 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2599.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2036.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2705.45 Safari/537.36",\
        "Mozilla/5.0 (X11; CentOS; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/602.5.2 (KHTML, like Gecko) Chrome/58.0.2939.53 Safari/602.5.2",
        "Mozilla/5.0 (Linux; IM-A860S Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.99 Apple Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/Chrome/63.0.3239.84 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2527.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.68 Safari/537.36",\
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.5 Safari/532.2",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2163.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/55.0.2883",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2409.0 Safari/537.36",\
        "Linux / Chrome 55: Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/599.0+ (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2946.0 Safari/537.36",\
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/530.0 (KHTML, like Gecko) Chrome/2.0.162.0 Safari/530.0",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2442.0 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686 (x86_64)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.50 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.6.1 Chrome/45.0.2454.101 Safari/537.36",\
        "Mozilla/5.0 (Linux; diordnA 7.0; BAH-L09 Build/HUAWEIBAH-L09; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) Build/NPJS25.93-14.7-8; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Safari/537.36",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/70.0.3538.57 Safari/537.36 Hawk/TurboBrowser/v3.0.0.4.9.09"]
    return random.choice(uaString)

#logging.basicConfig(filename="bot.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)

spreadsheet_url = "db.csv"

def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Hey "+str(update.message.from_user.first_name)+" Welcome!!. Click '/help' to know the different commands on how to use me")
	#check(update, context)
	context.job_queue.run_repeating(check, interval=600, context=update.message.chat_id)
	
def stop(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="BOT Stopped. Good bye!!")
	
	context.job_queue.stop()

def tracker(url, TrackingPrice):
	res = requests.get(url, headers = ({"User-Agent":''+ua()+''}))
	soup = bs4.BeautifulSoup(res.content, 'html.parser')
	print(({"User-Agent":''+ua()+''}))
	time.sleep(20)

	title = soup.find(id="productTitle").get_text().strip()
	try:
		amount = soup.find(id="priceblock_ourprice").get_text()[2:]
	except:
		amount = soup.find(id="priceblock_dealprice").get_text()[2:]
	real_price = ""
	for i in range(len(amount)):
		if amount[i] != ',':
			real_price += amount[i]
	real_price = int(float(real_price))
	print(real_price)
	print(TrackingPrice)
	if real_price <= TrackingPrice:
		return "Hey the price has dropped for \n*{0}*.\nCurrent Price: *₹{1}* \nTracking Price was: *₹{2}*\n\nLink:\n*{3}*".format(title, amount, TrackingPrice, url)
	else:
		return "The product \n*{0}*\nwhich you are tracking is not under good offer right now, \nThe current price is *₹{1}* and \nyour tracking price is *₹{2}*".format(url, amount, TrackingPrice), "No Offers"

def check(update, context):
	
	df = pd.read_csv(spreadsheet_url)
	print(update.effective_chat.id)
	exists = int(update.effective_chat.id) in df.values
	if exists:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Checking if the prices have dropped for all the products that you have added.... Please wait",parse_mode=telegram.ParseMode.MARKDOWN)
		for i in range(0, len(df["userID"])):
			print(len(df["URL"]))
			if(df["userID"][i]==update.effective_chat.id):
				msg = tracker(df["URL"][i], df["TrackingPrice"][i])
				print(msg)
				if msg[1] != "No Offers":
					context.bot.send_message(chat_id=update.effective_chat.id, text=msg,parse_mode=telegram.ParseMode.MARKDOWN)
				else:
					context.bot.send_message(chat_id=update.effective_chat.id, text=msg[0],parse_mode=telegram.ParseMode.MARKDOWN,disable_web_page_preview=True)
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="No products are been tracked. Start adding products",parse_mode=telegram.ParseMode.MARKDOWN)

def add_item(update, context):
    try:
        pn = str(context.args[0]).upper()
        price = int(context.args[1])
        user = int(update.effective_chat.id)
        firstName = str(update.message.from_user.first_name)
        
        code = requests.get("https://www.amazon.in/dp/" + pn, headers = ({"User-Agent":''+ua()+''})).status_code
        print(code)
        if(code == 200 or code == 503):
            print("Awesome")
            df = pd.read_csv(spreadsheet_url)
            df1 = pd.DataFrame(df, columns=['URL', 'TrackingPrice', 'userID','firstName'])
            df1['bol'] = np.where((df['URL'] == str("https://www.amazon.in/dp/" + pn)) & (df['userID'] == int(update.effective_chat.id))
                     , "true", np.nan)
            print(df1)
            if("true" in df1.values):
                update.message.reply_text("You are trying to add the same product which you have previously added.To change the tracking price please delete the item using /deleteitem command and add the product with new price")
            else:
                l = len(df["URL"])
                
                df.loc[l, ["URL"]] = "https://www.amazon.in/dp/" + pn
                df.loc[l, ["TrackingPrice"]] = price
                df.loc[l,["userID"]] = user
                df.loc[l,["firstName"]] = firstName
                df.to_csv(spreadsheet_url, index=False)
                update.message.reply_text("Product https://www.amazon.in/dp/" + pn+" is successfully added for tracking")
        elif(code == 404):
            update.message.reply_text("Product https://www.amazon.in/dp/" + pn+" is currently not listed on amazon")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /additem <amazon product number> <tracking_price>")

def delete_item(update, context):
	try:
		rm = str(context.args[0]).upper()
		user = int(update.effective_chat.id)
		print(rm)
		df = pd.read_csv(spreadsheet_url)
		df = df[~((df['URL'] == "https://www.amazon.in/dp/"+rm) & (df['userID'] == user))]
		df.to_csv(spreadsheet_url, index=False)
		update.message.reply_text("The product is now deleted")
	except (IndexError, ValueError):
		update.message.reply_text("Usage: /deleteitem <amazon product number>")

def delete_all(update, context):
	try:
		user = int(update.effective_chat.id)
		df = pd.read_csv(spreadsheet_url)
		df = df[~(df['userID'] == user)]
		df.to_csv(spreadsheet_url, index=False)
		update.message.reply_text("All the products are now deleted")
	except (IndexError, ValueError):
		update.message.reply_text("Usage: /deleteAll")


def debug_connection(update, context):
	msg = "Bot running"
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
	
def debug_tracking(update, context):
	df = pd.read_csv(spreadsheet_url)
	try:
		msg = tracker(df["URL"][0], df["TrackingPrice"][0])
		context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
	except:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing to track for now")

def help(update, context):
	msg = """
	/start
	Start the BOT
	
	/stop
	Stop the BOT
	
	/help
	This message
	
	/additem <amazon product number> <tracking_price>
	To add a new item to the database add item like below.. Go to the Indian amazon website and every product has a Product code in the url.
	example "/additem B07NDDV67F 18000"
	
	/deleteitem <amazon product number>
	To delete an item from the database..
	example "/deleteitem B07NDDV67F "

	/deleteAll
	To delete all items added by you
	
	/checkPriceDrop
	Checks if prices are dropped for the items you are tracking.Atleast add one item for this to work

	/debugconnection
	Check if the bot is still running
	"""
	
	context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def main():
	BotToken = ""
	u = Updater(token=BotToken, use_context=True)
	logging.basicConfig(filename="bot2.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
	u.dispatcher.add_handler(CommandHandler("start", start, pass_job_queue=True))
	u.dispatcher.add_handler(CommandHandler("stop", stop, pass_job_queue=True))
	u.dispatcher.add_handler(CommandHandler("help", help))
	u.dispatcher.add_handler(CommandHandler("debugconnection", debug_connection))
	u.dispatcher.add_handler(CommandHandler("debugtracking", debug_tracking))
	u.dispatcher.add_handler(CommandHandler("additem", add_item))
	u.dispatcher.add_handler(CommandHandler("deleteitem", delete_item))
	u.dispatcher.add_handler(CommandHandler("checkPriceDrop", check))
	u.dispatcher.add_handler(CommandHandler("deleteall", delete_all))
	u.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check, run_async=True))
	#u.dispatcher.add_handler(CommandHandler("url",url))
	u.start_polling()

	u.idle()
	
if __name__ == "__main__":
	main()