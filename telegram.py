import os
import asyncio
import re
from telethon import TelegramClient
from telethon.sessions import StringSession

# Load credentials from environment variables
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE = os.getenv("TELEGRAM_PHONE")
SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING")

USERNAME = os.getenv("IUTBOX_USERNAME")
PASS = os.getenv("IUTBOX_PASSWORD")
UPLOAD_URL = f"https://iutbox.iut.ac.ir/remote.php/dav/files/{USERNAME}/"

# Create client
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


def parse_telegram_link(link):
    try:
        # Match patterns: t.me/username/123 or t.me/c/123456/123
        m = re.search(r"t\.me/(c/)?([^/]+)/(\d+)", link)
        if not m:
            return None, None
        
        is_private = m.group(1)
        chat = m.group(2)
        message_id = int(m.group(3))
        
        if is_private:
            # Private channel: -100 + channel_id
            chat_id = -100 * int(chat)
        else:
            # Public channel/group: @username
            chat_id = chat
        
        return chat_id, message_id
    except Exception as e:
        print(f"❌ Error parsing link: {e}")
        return None, None


async def download_file_from_link(link):
    """Download file from a Telegram message link"""
    # Parse the link
    chat_id, message_id = parse_telegram_link(link)
    
    if not chat_id or not message_id:
        print("❌ Invalid Telegram link format")
        return
    
    try:
        print(f"📍 Chat: {chat_id}, Message: {message_id}")
        
        # Get the message
        message = await client.get_messages(chat_id, ids=message_id)
        
        if not message:
            print("❌ Message not found")
            return
        
        # Check if message has media
        if not message.media:
            print("❌ This message has no file/media to download")
            return
        
        # Extract file name
        file_name = None
        if message.document:
            if message.document.attributes:
                file_name = message.document.attributes[0].file_name
        
        print("⬇️  Downloading file...")
        
        # Download the file
        file_path = await message.download_media(file_name=file_name)
        
        if not file_path:
            print("❌ Failed to download file")
            return
        
        print(f"✅ Downloaded: {file_path}")
        
        # Upload to IUTBox
        await upload_to_iutbox(file_path)
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def upload_to_iutbox(file_path):
    """Upload file to IUTBox"""
    try:
        import requests
        
        if not os.path.exists(file_path):
            print("❌ File not found")
            return
        
        filename = os.path.basename(file_path)
        
        print(f"⬆️  Uploading to IUTBox: {filename}")
        
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        r = requests.put(
            UPLOAD_URL + filename,
            data=file_data,
            auth=(USERNAME, PASS),
            timeout=300
        )
        
        if r.status_code in [200, 201, 204]:
            print(f"✅ Uploaded to IUTBox: {filename}")
        else:
            print(f"❌ Upload failed: {r.status_code} - {r.text}")
        
        # Cleanup
        try:
            os.remove(file_path)
            print(f"🗑️  Cleaned up local file")
        except:
            pass
            
    except Exception as e:
        print(f"❌ Upload error: {e}")


async def main():
    """Main async function"""
    # Connect to Telegram
    await client.start(phone=PHONE)
    print("✅ Connected to Telegram!\n")
    
    # Get message link from user
    link = input("📎 Enter Telegram message link: ").strip()
    
    if not link:
        print("❌ No link provided")
        return
    
    # Download and upload
    await download_file_from_link(link)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
