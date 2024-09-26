import requests
from bs4 import BeautifulSoup
import time
import telegram
import os

# Your Telegram bot token and chat ID
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = '7228218507'

# URL of the Amazon jobs page
URL = "https://hiring.amazon.ca/locations/montreal-jobs#/"

# Initialize the Telegram bot
bot = telegram.Bot(token=BOT_TOKEN)

# Function to send notification via Telegram
def send_notification(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Function to scrape the page and look for the keyword "job found"
def scrape_jobs():
    response = requests.get(URL)
    
    # Check if the keyword "job found" is present in the page content
    if "no jobs available" in response.text.lower():
        return True
    return False

def main():
    last_notified = False

    while True:
        jobs_found = scrape_jobs()

        # Send notification if "job found" is detected and no previous notification was sent
        if jobs_found and not last_notified:
            send_notification("Keyword 'job found' detected on the Amazon Montreal jobs page!")
            last_notified = True
        elif not jobs_found and last_notified:
            last_notified = False  # Reset the notification flag if the keyword is no longer found

        # Check the webpage every 10 minutes (600 seconds)
	
        time.sleep(0.6)

if __name__ == "__main__":
    main()
