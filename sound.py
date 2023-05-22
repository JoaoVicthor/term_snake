import subprocess
import random, time

VELOCITY = 10

SAMPLE_RATE = 44100

class Sound:
    process = []

    @staticmethod
    def play_sound(sound_command):
        command = "play --buffer 32 --multi-threaded -b 1 -q -n synth ".split()
        command.extend(sound_command.split())
        Sound.process.append(subprocess.Popen(command))

    @staticmethod
    def play_walking_sound():
        Sound.play_sound(f"{1/VELOCITY*.5} sin 100 gain -20 treble -20 tremolo {VELOCITY} 100")

    @staticmethod
    def play_eating_sound():
        for proc in Sound.process:
            proc.terminate()
        Sound.play_sound(f"{2/VELOCITY*.5} sin 440 gain -25 treble -20")

    @staticmethod
    def play_ghost_sound():
        Sound.play_sound(f"{10/VELOCITY*.5} sin {random.randint(90,150)}-{random.randint(90,150)} gain -{random.randint(18,22)} treble -25 bass +2")

    @staticmethod
    def play_death_sound():
        for proc in Sound.process:
            proc.terminate()
        Sound.play_sound(f"2 sin 90-30 gain -20 treble -25 bass +5")
