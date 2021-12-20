import pygame

class Sounds: 
    def __init__(self):
        pass

    def hit_sound(self): 
        """
        Play hit sound
        """
        # sounds
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.music.load("./sounds/player/whoosh-6316.mp3")
        pygame.mixer.music.play() 

    def body_hit_sound(self): 
        """
        Play body hit sound
        """
        # sounds
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.music.load("./sounds/player/hit.wav")
        pygame.mixer.music.play()