import os
import zipfile
import argparse
import json
import asyncio
from datetime import datetime
from telethon import TelegramClient

CONFIG_FILE = 'config.json'


def load_config():
    """Load configuration from file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None


def save_config(api_id, api_hash, session_name):
    """Save configuration to file."""
    config = {
        'api_id': api_id,
        'api_hash': api_hash,
        'session_name': session_name
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)


def create_zip(folder_path):
    """Create a zip archive from the specified folder."""
    zip_filename = f"{folder_path}.zip"
    print(f"Creating zip archive: {zip_filename}...")

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    print("Zip archive created successfully.")
    return zip_filename


def show_telegram_guide():
    """Show Telegram API setup guide."""
    print("\nTo send messages, you need Telegram API credentials:")
    print("1. Go to https://my.telegram.org/apps")
    print("2. Create application with these settings:")
    print("   - App title: CloudGram")
    print("   - Short name: cloudgram")
    print("   - Platform: Desktop")
    print("3. You'll receive API ID and API Hash\n")


async def get_telegram_credentials():
    """Prompt user for Telegram API credentials."""
    print("Please enter your Telegram API credentials:")
    api_id = input("API ID: ").strip()
    api_hash = input("API Hash: ").strip()
    return api_id, api_hash


async def send_message(message, file_path=None, tag=None):
    """Send a message to Telegram."""
    config = load_config()

    if not config or not os.path.exists(f"{config['session_name']}.session"):
        show_telegram_guide()
        api_id, api_hash = await get_telegram_credentials()
        session_name = f"cloudgram_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        save_config(api_id, api_hash, session_name)
    else:
        api_id = config['api_id']
        api_hash = config['api_hash']
        session_name = config['session_name']

    try:
        async with TelegramClient(session_name, api_id, api_hash) as client:
            await client.start()

            if tag is None:
                tag = "cloudgram_file" if file_path else "cloudgram_message"

            formatted_message = (
                f"[#{tag}]\n"
                f"-----------------------------------------------------------\n\n"
                f"{message}\n\n"
                f"-----------------------------------------------------------\n"
                f"*Sent via CloudGram*"
            )

            if file_path:
                if os.path.isdir(file_path):
                    file_path = create_zip(file_path)
                print(f"Sending file: {file_path}")
                await client.send_file('me', file_path, caption=formatted_message)
                print("File sent successfully.")
                if file_path.endswith('.zip'):
                    os.remove(file_path)
            else:
                await client.send_message('me', formatted_message)
                print("Message sent successfully!")

    except Exception as e:
        print(f"\nError: {str(e)}")
        if "Cannot use empty API ID" in str(e):
            print("Invalid API credentials. Please delete config.json and try again.")


def main():
    """Main function for processing command-line arguments."""
    parser = argparse.ArgumentParser(description='Send messages to Telegram Saved Messages.')

    parser.add_argument('message', help='Message text to send')
    parser.add_argument('-f', '--file', help='Attach file/folder')
    parser.add_argument('-t', '--tag', help='Custom message tag')

    args = parser.parse_args()

    asyncio.run(send_message(args.message, args.file, args.tag))


if __name__ == '__main__':
    main()
