import time
from bs4 import BeautifulSoup
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# === CONFIG ===
URL = "https://checkvisaslots.com/latest-us-visa-availability.html"
BOT_TOKEN = "8117470985:AAGUZ1VYL494ZI3w5ekZgJem2zbpsV2y2QE"
CHAT_ID = "8188500454"
CHECK_INTERVAL = 300  # 5 minutes

# Initialize Telegram bot
bot = Bot(token=BOT_TOKEN)

# Setup Chrome in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")  # For Linux compatibility

# ✅ FIXED Chrome driver initialization
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def get_hyderabad_data():
    try:
        driver.get(URL)
        time.sleep(5)  # Wait for JavaScript content to load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")

        hyderabad_rows = [
            row.get_text(separator=" | ", strip=True)
            for row in rows if "Hyderabad" in row.text
        ]

        return "\n".join(hyderabad_rows)
    except Exception as e:
        print("Error fetching data:", e)
        return None

def send_telegram(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print("Error sending Telegram message:", e)

def monitor():
    print("Monitoring Hyderabad slot updates...")
    send_telegram("Test alert: Hyderabad visa slot bot is running successfully.")

    while True:
        current_data = get_hyderabad_data()

        if current_data and current_data != previous_data:
            print("Change detected. Sending Telegram message.")
            send_telegram("Hyderabad Visa Slot Updated:\n\n" + current_data)
            previous_data = current_data
        else:
            print("No change. Rechecking in 5 minutes.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()
