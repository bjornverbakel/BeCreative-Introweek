import serial
import vlc
import time

# SETTINGS

COM_PORT = "COM8"

AUDIO_FILE = r"C:\Users\bjorn\BeCreative-Introweek\laptop-receiver\audio.aac"

# Timestamps in seconds
CHAOS_TIME = 0       # 0:00
CALM_TIME = 30       # 0:30

# End of the chaos section
CHAOS_END = 29       # 0:29

# START VLC

print("Starting VLC...")

instance = vlc.Instance()

player = instance.media_player_new()

media = instance.media_new(AUDIO_FILE)

player.set_media(media)

player.play()

time.sleep(1)

# Start at CHAOS
player.set_time(CHAOS_TIME * 1000)

print("Audio started.")
print("Starting in CHAOS mode.")


# CONNECT TO MICRO:BIT

print("Connecting to micro:bit on", COM_PORT)

ser = serial.Serial(
    COM_PORT,
    115200,
    timeout=1
)

print("Connected!")
print("Waiting for helmet...")
print()


# Current state
current_state = "CHAOS"


# MAIN LOOP

while True:

    try:

        # CHECK FOR MICRO:BIT MESSAGE

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


        # LOOP CHAOS SECTION

        if current_state == "CHAOS":

            current_time = player.get_time() / 1000

            if current_time >= CHAOS_END:

                print("Chaos section finished. Looping back to 0:00")

                player.set_time(CHAOS_TIME * 1000)

                if not player.is_playing():
                    player.play()


        time.sleep(0.05)


    except KeyboardInterrupt:

        print()
        print("Stopping installation...")

        player.stop()

        ser.close()

        break


    except Exception as e:

        print("Error:", e)

        time.sleep(1)