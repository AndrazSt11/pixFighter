import pygame

class Sounds: 
    def __init__(self): 
        """
        Class made for playing sounds
        """
        pass

    def hit_sound(self): 
        """
        Play hit sound
        """
        # sounds
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        hit = pygame.mixer.Sound("./sounds/player/whoosh-6316.wav")
        hit.play() 
        hit.set_volume(0.3)

    def body_hit_sound(self): 
        """
        Play body hit sound
        """
        # sounds
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        body_hit = pygame.mixer.Sound("./sounds/player/hit.wav")
        body_hit.play() 
        body_hit.set_volume(0.2) 

    def jump_sound(self): 
        """
        Play jump sound
        """
        # sounds
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        body_hit = pygame.mixer.Sound("./sounds/player/Jump.mp3")
        body_hit.play() 
        body_hit.set_volume(0.2) 

    def healup_sound(self): 
        """
        Play healup sound
        """
        # sounds
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        body_hit = pygame.mixer.Sound("./sounds/player/healup.wav")
        body_hit.play() 
        body_hit.set_volume(0.2) 

    def teleport_sound(self): 
        """
        Play teleport sound
        """
        # sounds
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        body_hit = pygame.mixer.Sound("./sounds/player/Teleport.mp3")
        body_hit.play() 
        body_hit.set_volume(0.17)

    def background_music(self): 
        """
        Play music
        """
        # sounds
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        music = pygame.mixer.music.load("./sounds/music/Background_song.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.05) 

    def pause_music(self):
        """
        Pause music
        """
        pygame.mixer.music.pause() 

    def unpause_music(self): 
        """
        Unpause music
        """ 
        pygame.mixer.music.unpause()