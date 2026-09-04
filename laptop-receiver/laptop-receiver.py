import serial
import vlc
import time
from pathlib import Path

# SETTINGS

COM_PORT = "COM11"

AUDIO_FILE = Path(__file__).parent / "audio.aac"

CHAOS_TIME = 0       # 0:00
CALM_TIME = 30       # 0:30
CHAOS_END = 29       # 0:29

# CHECK AUDIO FILE

if not AUDIO_FILE.is_file():
    raise FileNotFoundError(
        f"Audio file not found: {AUDIO_FILE}"
    )

print(f"Using audio file: {AUDIO_FILE}")

# START VLC

print("Starting VLC...")

instance = vlc.Instance()
player = instance.media_player_new()

media = instance.media_new(str(AUDIO_FILE))
player.set_media(media)

player.play()

time.sleep(1)

if player.get_state() == vlc.State.Error:
    raise RuntimeError("VLC could not play the audio file")

player.set_time(CHAOS_TIME * 1000)

print("Audio started.")
print("Starting in CHAOS mode.")


# CONNECT TO MICRO:BIT

print("Connecting to micro:bit on", COM_PORT)

ser = serial.Serial(
    COM_PORT,
    115200,
    timeout=0.05
)

print("Connected!")
print("Waiting for helmet...")
print()

# CURRENT STATE

current_state = "CHAOS"


# MAIN LOOP

try:

    while True:

        # Check for micro:bit message

        message = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if message:

            print("Received:", message)

            # CHAOS

            if message == "CHAOS":

                current_state = "CHAOS"

                print("Jumping to CHAOS at 0:00")

                player.set_time(CHAOS_TIME * 1000)

                if not player.is_playing():
                    player.play()


            # CALM

            elif message == "CALM":

                current_state = "CALM"

                print("Jumping to CALM at 0:30")

                player.set_time(CALM_TIME * 1000)

                if not player.is_playing():
                    player.play()


        # Loop chaos section

        if current_state == "CHAOS":

            current_time_ms = player.get_time()

            if current_time_ms >= 0:

                current_time = current_time_ms / 1000

                if current_time >= CHAOS_END:

                    print("Chaos section finished. Looping to 0:00")

                    player.set_time(CHAOS_TIME * 1000)


        time.sleep(0.05)


except KeyboardInterrupt:

    print()
    print("Stopping installation...")


finally:

    player.stop()
    ser.close()