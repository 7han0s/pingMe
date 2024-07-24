# pingMe 

# Multipurpose Check-in Script

This is a multipurpose script designed to be used for regular check-ins, such as sleep protocols or activity reminders. The script sends notifications and plays sounds to prompt for user responses. If the user does not respond within a set time, it logs the missed responses and stops after a certain number of missed check-ins.

## Features
- Periodic notifications and sound prompts
- Customizable messages and sounds
- Tracks user responses and stops after consecutive missed check-ins

## Prerequisites
- Python 3.x
- Required Python packages: `playsound`, `plyer`

Install the required packages using:
```sh
pip install playsound plyer
```

## Usage
1. Ensure all sound files (`startup.mp3`, `ping.mp3`, `error.mp3`, `end.mp3`) are in the same directory as the script.
2. Run the script using:
```sh
python pingMe.py
```

## Customization
### Text Messages
To customize the text messages, update the corresponding print statements in the `ping` function. Here are the key messages and where to find them:

- **Initial Message**: 
  ```python
  print("Custom start message! Do something.")
  ```
  Change this message to your desired start message.

- **Ping Message**:
  ```python
  print("Custom ping message!")
  ```
  Change this message to your desired ping message.

- **No Reply Message**:
  ```python
  print("Custom no reply message.")
  ```
  Change this message to your desired no reply message.

- **Stop Message**:
  ```python
  print("Custom stop message.")
  ```
  Change this message to your desired stop message.

- **Deactivation Message**:
  ```python
  print("Custom end message.")
  ```
  Change this message to your desired end message.

### Sound Files
Replace the sound files with your own sounds and ensure they are named:
- `startup.mp3`: Initial sound
- `ping.mp3`: Ping sound
- `error.mp3`: Error sound
- `end.mp3`: End sound

Update the paths in the `play_sound` function if your sound files are located elsewhere:
```python
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
```

## Example
Here's a modified example of the script with custom messages:
```python
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

    print("Custom start message! Do something.")
    play_sound('startup.mp3')

    while True:
        time.sleep(15)

        print("Custom ping message!")
        play_sound('ping.mp3')

        notification.notify(
            title='Ping Notification',
            message='Custom ping message!',
            timeout=10
        )

        reply_received = threading.Event()

        def get_reply():
            reply = input("Reply (yes/y/1 for yes, no/n/0 for no): ").strip().lower()
            reply_received.set()
            return reply

        reply_thread = threading.Thread(target=get_reply)
        reply_thread.start()
        
        reply_thread.join(30)

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
            print("Custom no reply message.")
            missed_pings += 1

        if missed_pings >= 2:
            print("Custom stop message.")
            break
    
    print("Custom end message.")
    play_sound('end.mp3')
    return 0

def main():
    return ping()

if __name__ == "__main__":
    main()
```

Feel free to customize the script to fit your specific needs!
Note: Can be useful for keeping task accountablity
