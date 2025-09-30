import requests

def get_telegram_chat_id():
    BOT_TOKEN = input("Enter your bot token: ")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["ok"] and data["result"]:
            chat_id = data["result"][0]["message"]["chat"]["id"]
            print(f"Your Chat ID: {chat_id}")
            return chat_id
        else:
            print("No messages found. Send a message to your bot first.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Telegram Chat ID Getter")
    print("1. Create bot with @BotFather")
    print("2. Send any message to your bot")
    print("3. Run this script\n")
    
    get_telegram_chat_id()