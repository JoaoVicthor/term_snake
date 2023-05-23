import subprocess
import random
from constants import VELOCITY
class Sound:
    process_counter = 0
    process = [None] * 8
    background_noise = None

    @staticmethod
    def play_sound(sound_command):
        command = "play --buffer 32 --multi-threaded -b 1 -q -n -c1 synth ".split()
        command.extend(sound_command.split())

        if(Sound.process[Sound.process_counter] is not None and Sound.process[Sound.process_counter].poll() is None):
            Sound.process[Sound.process_counter].terminate()
        Sound.process[Sound.process_counter] = subprocess.Popen(command)
        if(Sound.process_counter <7):
            Sound.process_counter+=1
        else:
            Sound.process_counter=0
        
    @staticmethod
    def play_background_noise():
        Sound.background_noise = subprocess.Popen("play --buffer 32 --multi-threaded -b 1 -q -n -c1 -n synth brownnoise gain -35 band -n 700 300 tremolo .05 40 reverb 100".split())

    @staticmethod
    def stop_background_noise():
        Sound.background_noise.terminate()
        Sound.background_noise = None

    @staticmethod
    def play_start_sound():
        Sound.play_sound(f"1 sin 125 gain -10 tremolo 0.5 100")

    @staticmethod
    def play_pause_sound():
        subprocess.run("play --buffer 32 --multi-threaded -b 1 -q -n -c1 -n synth 0.3 sin 523 gain -18 : synth 0.3 sin 660 gain -18 : synth 0.3 sin 784 gain -18".split())

    @staticmethod
    def play_walking_sound():
        Sound.play_sound(f"{1/VELOCITY*.5} sin 100 gain -12 tremolo {VELOCITY} 100")

    @staticmethod
    def play_eating_sound():
        for proc in Sound.process:
            proc.terminate()
        Sound.play_sound(f"{2/VELOCITY*.5} sin 420 gain -12 tremolo {2/VELOCITY*.5} 100")

    @staticmethod
    def play_ghost_sound():
        Sound.play_sound(f"{10/VELOCITY*.5} sin {random.randint(90,150)}-{random.randint(90,150)} gain -{random.randint(8,12)} tremolo {10/VELOCITY} 100")

    @staticmethod
    def play_death_sound():
        for proc in Sound.process:
            proc.terminate()
        Sound.stop_background_noise()
        Sound.play_sound(f"2 sin 90/20 gain -10 tremolo 0.25 100")
