from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
import telegram

# Your Telegram bot token and chat ID (replace with your actual token and chat ID)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Retrieve from environment variables
CHAT_ID = os.getenv("CHAT_ID", "7228218507")  # Chat ID (can also be stored in GitHub secrets)

# URL of the Amazon Jobs page
URL = "https://hiring.amazon.ca/locations/montreal-jobs#/"

# Set up Telegram bot
bot = telegram.Bot(token=BOT_TOKEN)

# Function to send a notification to Telegram
def send_notification(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Set up Selenium WebDriver (ensure ChromeDriver path is correct)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# Function to check for jobs using Selenium
def check_jobs():
    try:
        # Load the Amazon Jobs page
        driver.get(URL)

        # Wait for the page to load (adjust time as needed)
        time.sleep(5)
        print(driver.page_source)

        # Check if the page contains a job-related keyword (e.g., "jobs found")
        if "jobs found" in driver.page_source.lower():
            print("Jobs are available!")
            send_notification("New jobs found on the Amazon Montreal page!")
        else:
            print("No jobs found.")

    except Exception as e:
        send_notification(f"An error occurred while checking for jobs: {e}")

# Main function to continuously check for jobs
def main():
    check_jobs()  # Run the check once for GitHub Actions

# Run the script
if __name__ == "__main__":
    main()

# Make sure to close the driver after you're done
driver.quit()
