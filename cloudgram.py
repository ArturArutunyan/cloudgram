import zipfile
import argparse
import json
import asyncio
import sys
import os
import subprocess
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

CONFIG_FILE = 'config.json'


def load_config():
    """Load configuration from file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None


def save_config(api_id, api_hash, phone_number, session_name):
    """Save configuration to file."""
    config = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone_number': phone_number,
        'session_name': session_name
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


def create_zip(folder_path):
    """Create a zip archive from the specified folder."""
    zip_filename = f"{folder_path}.zip"
    print(f"Creating zip archive: {zip_filename}...")

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

    print("Zip archive created successfully.")

    return zip_filename


async def send_message(api_id, api_hash, phone_number, message, file_path=None, tag=None, session_name=None):
    """Send a message to Telegram."""
    new_session = False
    if session_name is None:
        session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        new_session = True

    async with TelegramClient(session_name, api_id, api_hash) as client:
        await client.start()

        if isinstance(phone_number, str):
            try:
                await client.sign_in(phone_number)
            except SessionPasswordNeededError:
                password = input("Enter your password: ")
                await client.sign_in(password=password)

        # Определяем тег по умолчанию
        if tag is None:
            if file_path:
                tag = "cloudgram_file"
            else:
                tag = "cloudgram_message"

        formatted_message = (
            f"[#{tag}]\n"
            f"-----------------------------------------------------------\n\n"
            f"{message}\n\n"
            f"-----------------------------------------------------------\n"
            f"*This message was sent from rubberytg.*"
        )

        if file_path:
            if os.path.isdir(file_path):
                file_path = create_zip(file_path)
            print(f"Sending file: {file_path}")
            await client.send_file('me', file_path, caption=formatted_message)
            print("File sent successfully.")
            if os.path.exists(file_path) and file_path.endswith('.zip'):
                os.remove(file_path)
        else:
            await client.send_message('me', formatted_message)
            print("Message sent successfully!")

    if new_session:
        save_config(api_id, api_hash, phone_number, session_name)


async def perform_setup(api_id, api_hash, phone_number):
    """Perform initial setup and save configuration."""
    session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    save_config(api_id, api_hash, phone_number, session_name)
    print("Setup completed. Configuration saved.")


def main():
    venv_dir = os.path.join(os.path.dirname(__file__), 'venv')

    if not os.path.exists(venv_dir):
        subprocess.run([sys.executable, '-m', 'venv', venv_dir])

    activate_script = os.path.join(venv_dir, 'bin', 'activate_this.py')
    with open(activate_script) as f:
        exec(f.read(), dict(__file__=activate_script))

    """Main function for processing command-line arguments."""
    parser = argparse.ArgumentParser(description='Send messages to Telegram Saved Messages.')
    subparsers = parser.add_subparsers(dest='command')

    setup_parser = subparsers.add_parser('setup', help='Initial API setup')
    setup_parser.add_argument('-i', '--api_id', type=str, required=True, help='API ID')
    setup_parser.add_argument('-a', '--api_hash', type=str, required=True, help='API Hash')
    setup_parser.add_argument('-p', '--phone_number', type=str, required=True, help='Phone number')

    send_parser = subparsers.add_parser('send', help='Send a message')
    send_parser.add_argument('-m', '--message', type=str, required=True, help='Message to send')
    send_parser.add_argument('-f', '--file', type=str, nargs='?', help='Path to file or folder to send')
    send_parser.add_argument('-t', '--tag', type=str, help='Tag for the message')

    args = parser.parse_args()

    if args.command == 'setup':
        asyncio.run(perform_setup(args.api_id, args.api_hash, args.phone_number))
    elif args.command == 'send':
        config = load_config()
        if config is None:
            print("Error: Configuration not found. Please perform initial setup first.")
            return

        api_id = config['api_id']
        api_hash = config['api_hash']
        phone_number = config['phone_number']
        session_name = config['session_name']

        asyncio.run(send_message(api_id, api_hash, phone_number, args.message, args.file, args.tag, session_name))


if __name__ == '__main__':
    main()

