from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from telegram.error import TimedOut
import os
import time
import telegram
import asyncio

# Your Telegram bot token and chat ID (replace with your actual token and chat ID)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Retrieve from environment variables
CHAT_ID = os.getenv("CHAT_ID", "7228218507")  # Chat ID (can also be stored in GitHub secrets)

# URL of the Amazon Jobs page
URL = "https://hiring.amazon.ca/locations/montreal-jobs#/"

# Set up Telegram bot
bot = telegram.Bot(token=BOT_TOKEN)

# Function to send a notification to Telegram
async def send_notification(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except TimedOut:
         await asyncio.sleep(60)
         await bot.send_message(chat_id=CHAT_ID, text=message)

# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use WebDriverManager to automatically download and configure the correct ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to check for jobs using Selenium
def check_jobs():
    try:
        # Load the Amazon Jobs page
        driver.get(URL)

        # Wait for the page to load (adjust time as needed)
        time.sleep(5)
       

        # Check if the page contains a job-related keyword (e.g., "jobs found")
        if "no jobs available" in driver.page_source.lower():
            print("Jobs are available!")
            asyncio.run(send_notification("TEST-New jobs found on the Amazon Montreal page!"))
        else:
            print("No jobs found.")

    except Exception as e:
        asyncio.run(send_notification(f"An error occurred while checking for jobs: {e}"))

if __name__ == "__main__":
    while True:
        check_jobs()  # Run the check
        time.sleep(0.6)  # Wait for 60 seconds before checking again

# Make sure to close the driver after you're done
driver.quit()
