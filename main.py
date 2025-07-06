from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot
import asyncio

# ✅ Your working bot token and chat ID
BOT_TOKEN = "8117470985:AAGUZ1VYL494ZI3w5ekZgJem2zbpsV2y2QE"
CHAT_ID = "8188500454"

async def send_message(text):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)

def check_slot():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://checkvisaslots.com/latest-us-visa-availability.html")  # ⛳ Replace this with actual slot website
    page_title = driver.title
    driver.quit()

    return f"Slot page title is: {page_title}"

if __name__ == "__main__":
    slot_text = check_slot()
    asyncio.run(send_message(f"Hyderabad Slot Update:\n\n{slot_text}"))
