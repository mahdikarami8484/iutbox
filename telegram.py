import re
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

USERNAME = os.getenv("USERNAME")
PASS = os.getenv("PASS")
UPLOAD_URL = f"https://iutbox.iut.ac.ir/remote.php/dav/files/{USERNAME}/"


def parse_telegram_link(link):
    
    m = re.search(r"t\.me/(c/)?([^/]+)/(\d+)", link)
    if not m:
        raise ValueError("Invalid link")

    is_private = m.group(1)
    chat = m.group(2)
    message_id = int(m.group(3))

    if is_private:
        chat_id = "-100"+ chat
    else:
        chat_id = f"@{chat}"

    return chat_id, message_id


def get_last_update():
    r = requests.get(
    f"{TELEGRAM_API_URL}/getUpdates"
    ).json()
    return r


def parse_update_get_file_id(update, allowed_chat_id):
    try:
        message = update.get("message")
        if not message:
            raise ValueError("No message in update")
        
        # Check chat ID
        chat_id = message.get("chat", {}).get("id")
        if chat_id != allowed_chat_id:
            raise ValueError(f"Chat ID {chat_id} not allowed. Expected: {allowed_chat_id}")
        
        # Try to extract file ID from different message types
        file_id = None
        file_name = None
        
        if "document" in message:
            file_id = message["document"].get("file_id")
            file_name = message["document"].get("file_name")
        elif "photo" in message:
            # Photos are arrays, get the last (highest quality) one
            file_id = message["photo"][-1].get("file_id")
        elif "audio" in message:
            file_id = message["audio"].get("file_id")
        elif "video" in message:
            file_id = message["video"].get("file_id")
        elif "voice" in message:
            file_id = message["voice"].get("file_id")
        elif "video_note" in message:
            file_id = message["video_note"].get("file_id")
        elif "animation" in message:
            file_id = message["animation"].get("file_id")
        
        if not file_id:
            raise ValueError("No file found in message")
        
        return file_id, file_name
        
    except KeyError as e:
        raise ValueError(f"Invalid update structure: {e}")


def download_file(file_id, file_name=None):
    try:
        # Get file info
        r = requests.get(
            f"{TELEGRAM_API_URL}/getFile",
            params={"file_id": file_id}
        ).json()

        if not r.get("ok"):
            raise ValueError("Failed to get file info")

        file_path = r["result"]["file_path"]
        file_size = r["result"].get("file_size", "Unknown")
        
        # Extract file name and extension from file_path
        original_filename = file_path.split("/")[-1]
        
        # Use custom filename or original filename
        save_as = file_name if file_name else original_filename
        
        # Get file type from extension
        file_type = original_filename.split(".")[-1] if "." in original_filename else "unknown"
        
        # Download file
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        data = requests.get(file_url).content

        # Save file
        with open(save_as, "wb") as f:
            f.write(data)

        print(f"✓ Downloaded: {save_as}")
        print(f"  Original name: {original_filename}")
        print(f"  File type: {file_type}")
        print(f"  File size: {file_size} bytes")
        
        return save_as
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None


def reset_updates():
    try:
        r = requests.get(
            f"{TELEGRAM_API_URL}/getUpdates"
        ).json()
        
        updates = r.get("result", [])
        
        if not updates:
            print("No updates to reset")
            return
        
        last_update_id = updates[-1]["update_id"]
        
        # Set offset to skip all previous updates
        r = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
            params={"offset": last_update_id + 1}
        ).json()
        
        print(f"Updates reset. Last update ID was: {last_update_id}")
        return True
        
    except Exception as e:
        print(f"Error resetting updates: {e}")
        return False

def upload_to_iutbox(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    filename = file_path.split("/")[-1]
    
    r = requests.put(
        UPLOAD_URL + filename,
        data=file_data,
        auth=(USERNAME, PASS)
    )
    
    if r.status_code in [200, 201, 204]:
        print(f"✓ Uploaded to IUTBox: {filename}")
        return True
    else:
        print(f"Error uploading to IUTBox: {r.status_code} - {r.text}")
        return False

def main():
    updates = get_last_update()
    allowed_chat_id = CHAT_ID
    file_id = None
    file_name = None
    for update in updates.get("result", []):
        try:
            file_id, file_name = parse_update_get_file_id(update, allowed_chat_id)
            if file_id:
                break
        except ValueError as e:
            print("Skipping update: ", e)
    if not file_id:
        print("No file found in recent updates.")
        return 

    file_path = download_file(file_id, file_name)
    print("File saved to: ", file_path)
    reset_updates()
    upload_to_iutbox(file_path)

if __name__ == "__main__":
    main()
