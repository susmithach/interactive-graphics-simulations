import pygame

class Input:
    """
    Handles all keyboard and window input for the application.
    """

    def __init__(self):
        # Flag used by Base class to determine when to exit the main loop
        self.quit = False

        # Stores keys that were pressed THIS frame only
        self.keyDownList = []

        # Stores keys that are currently being held down
        self.keyPressedList = []

    def update(self):
        """
        Processes all pygame events for the current frame.
        This method:
        • Clears the one-frame keyDown list
        • Updates keyPressedList based on KEYDOWN and KEYUP events
        • Checks for quit events
        """

        # Reset one-frame list at the beginning of each update cycle
        self.keyDownList = []

        for event in pygame.event.get():

            # If the window close button is pressed
            if event.type == pygame.QUIT:
                self.quit = True

            # When a key is pressed down
            elif event.type == pygame.KEYDOWN:

                # Pressing ESC will exit the program
                if event.key == pygame.K_ESCAPE:
                    self.quit = True

                # Convert key code to readable string (e.g:, "up", "space")
                keyName = pygame.key.name(event.key)

                # Add to keyDownList
                if keyName not in self.keyDownList:
                    self.keyDownList.append(keyName)

                # Add to keyPressedList 
                if keyName not in self.keyPressedList:
                    self.keyPressedList.append(keyName)

            # When a key is released
            elif event.type == pygame.KEYUP:

                keyName = pygame.key.name(event.key)

                # Remove key from the held list once released
                if keyName in self.keyPressedList:
                    self.keyPressedList.remove(keyName)

    def isKeyDown(self, keyName):
        """
        Returns True only during the frame the key was initially pressed.
        Useful for single-trigger actions.
        """
        return keyName in self.keyDownList

    def isKeyPressed(self, keyName):
        """
        Returns True for as long as the key is being held down.
        Useful for continuous actions.
        """
        return keyName in self.keyPressedList