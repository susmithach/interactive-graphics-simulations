import pygame 

class Input:
    def __init__(self):
        self.quit = False 

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True 
            # check for ESC key press to quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit = True