import os
import time
import threading
from playsound import playsound
from plyer import notification

def play_sound(file):
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.join(script_dir, file) 

    if os.path.isfile(file_path):
        try:
            playsound(file_path)
        except Exception as e:
            print(f"Error playing sound {file}: {e}")
    else:
        print(f"Sound file {file} not found at {file_path}")

def ping():
    missed_pings = 0

    print("Sleep protocol initialized! Dim lights and go to sleep.")
    play_sound('startup.mp3')  # Replace with your own sound file if you want

    while True:
        time.sleep(1800)  # 30 minutes can change this too for ping durations

        print("Still awake? Baka!")
        play_sound('ping.mp3')  

        # Push notification
        notification.notify(
            title='Ping Notification',
            message='Still awake? Baka!',
            timeout=10
        )

        reply_received = threading.Event()

        def get_reply():
            reply = input("Reply (yes/y/1 for yes, no/n/0 for no): ").strip().lower()
            reply_received.set()
            return reply

        reply_thread = threading.Thread(target=get_reply)
        reply_thread.start()
        
        reply_thread.join(30)  # 30 seconds wait time for reply

        if reply_received.is_set():
            reply = get_reply()
            if reply in ["yes", "y", "1"]:
                missed_pings = 0
            elif reply in ["no", "n", "0"]:
                missed_pings += 1
            else:
                print("Invalid input, stopping pings due to unrecognized response")
                play_sound('error.mp3')  
                break
        else:
            print("Are you asleep? Good, but will keep a ping for confirmation.")
            missed_pings += 1

        if missed_pings >= 2:
            print("Ah so you finally went to sleep huh? Good, now remember to get out of coma in the morning.")
            break
    
    print("Sleep protocol deactivated!")
    play_sound('end.mp3') 
    return 0

def main():
    return ping()

if __name__ == "__main__":
    main()
