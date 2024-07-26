import os
import argparse
import time
import threading
from playsound import playsound
from plyer import notification

def play_sound(sound_file):
    """Plays a sound file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, sound_file)

    if os.path.isfile(file_path):
        try:
            playsound(file_path)
        except Exception as e:
            print(f"Error playing sound {sound_file}: {e}")
    else:
        print(f"Sound file {sound_file} not found at {file_path}")

def get_user_reply():
    """Gets user input for the check-in."""
    reply = input("Reply (yes/y/1 for yes, no/n/0 for no): ").strip().lower()
    return reply

def initialize():
    """Initializes the check-in process."""
    print("Sleep protocol initialized! Dim lights and go to sleep.")
    play_sound('startup.mp3')

def check(check_in_interval, sound_file, message):
    """Performs a single check-in.

    Args:
        check_in_interval: Time between checks in seconds.
        sound_file: Path to the ping sound file.
        message: Check-in message.
        notification_title: Notification title.
        notification_message: Notification message.
        notification_timeout: Notification timeout in seconds.

    Returns:
        True if the user responded positively, False otherwise.
    """
    time.sleep(check_in_interval)
    print(message)
    play_sound(sound_file)

    notification.notify(
        title=notification_title,
        message=notification_message,
        timeout=notification_timeout
    )

    reply_received = threading.Event()

    def get_reply_thread():
        reply = get_user_reply()
        reply_received.set()
        return reply

    reply_thread = threading.Thread(target=get_reply_thread)
    reply_thread.start()

    reply_thread.join(30)

    if reply_received.is_set():
        reply = reply_thread.result()
        return reply in ["yes", "y", "1"]
    else:
        print("No reply received.")
        return False

def end_condition(missed_pings):
    """Checks if the check-in loop should end.

    Args:
        missed_pings: Number of missed pings.

    Returns:
        True if the loop should end, False otherwise.
    """
    return missed_pings >= 2

def finalize():
    """Performs final actions after the check-in loop ends."""
    print("Sleep protocol deactivated!")
    play_sound('end.mp3')

def ping(check_in_interval, sound_file, message, notification_title, notification_message, notification_timeout, max_misses):
    """Main check-in loop.

    Args:
        check_in_interval: Time between checks in seconds.
        sound_file: Path to the ping sound file.
        message: Check-in message.
    """
    missed_pings = 0

    initialize()

    while not end_condition(missed_pings):
        if check(check_in_interval, sound_file, message):
            missed_pings = 0
        else:
            missed_pings += 1

    finalize()

def parse_args():
    parser = argparse.ArgumentParser(description="PingMe: A check-in tool")
    parser.add_argument("-i", "--interval", type=int, default=1800, help="Check-in interval in seconds (default: 1800)")
    parser.add_argument("-s", "--sound", type=str, default="ping.mp3", help="Sound file path (default: ping.mp3)")
    parser.add_argument("-m", "--message", type=str, default="Still awake?", help="Check-in message (default: Still awake?)")
    parser.add_argument("-n", "--max-misses", type=int, default=2, help="Maximum number of missed pings before stopping (default: 2)")
    parser.add_argument("-nt", "--notification-title", type=str, default="Ping Notification", help="Notification title (default: Ping Notification)")
    parser.add_argument("-nm", "--notification-message", type=str, default="Still awake?", help="Notification message (default: Still awake?)")
    parser.add_argument("-ntt", "--notification-timeout", type=int, default=10, help="Notification timeout in seconds (default: 10)")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    ping(args.interval, args.sound, args.message, args.max_misses, args.notification_title, args.notification_message, args.notification_timeout)    
