import os.path
import pygame
import state
import random
import utilities


class StartScreen(state.State):
    def __init__(self, game):
        state.State.__init__(self, game)
        self.background = utilities.loadImage(os.path.join("data", "images"), "skygrad.png")
        self.grassimage = utilities.loadImage(os.path.join("data", "images"), "grass.png", 1)
        self.grassshadow = utilities.loadImage(os.path.join("data", "images"), "grasshadow.png", 1)

        self.titletext = self.game.large_font.render("Moes Adventure", True, (255, 255, 255))
        self.titletext2 = self.game.large_font.render("Moes Adventure", True, (25, 25, 25))
        self.titletextrect = self.titletext.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 4))

        # Core Navigation Array: Modes tracking index 0 and 1, Settings at 2, Quit at 3
        self.menu_options = ["Normal Mode", "Hard Mode", "Settings", "Quit Game"]
        self.selected_index = 0

        self.starttext = self.game.small_font.render("Press Enter to Confirm Selection", True, (255, 255, 255))
        self.starttextrect = self.starttext.get_rect(
            center=(self.game.screen_width / 2, self.game.screen_height / 2 - 60))

        self.controls_text1 = self.game.small_font.render("Controls: WASD / Arrow Keys to Move Focus", True,
                                                          (255, 255, 255))
        self.controls_text2 = self.game.small_font.render("Space to Jump, Enter / Click to Confirm", True,
                                                          (255, 255, 255))
        self.controls_rect1 = self.controls_text1.get_rect(
            center=(self.game.screen_width / 2, self.game.screen_height - 80))
        self.controls_rect2 = self.controls_text2.get_rect(
            center=(self.game.screen_width / 2, self.game.screen_height - 40))

        self.musicstart = False
        self.input_delay = 0

        # Track collision bounding boxes dynamically for mouse tracking
        self.option_rects = []

    def handle_mouse_input(self):
        """Calculates screen-space mouse coordinates to allow dual menu input selection profiles."""
        if self.input_delay > 0 or not self.option_rects:
            return

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]  # Left Click Verification

        for idx, rect in enumerate(self.option_rects):
            # Check if the hardware cursor positions fall within any text bounding boxes
            if rect.collidepoint(mouse_pos):
                if self.selected_index != idx:
                    self.selected_index = idx

                # If a direct click occurs over the active option, trigger confirmation
                if mouse_clicked:
                    self.input_delay = 20
                    self.confirm_selection()
                    break

    def confirm_selection(self):
        """Applies configuration metrics across game layers or fires global termination pipelines."""
        if self.selected_index == 0:  # NORMAL MODE
            self.game.mode = "Normal"
            self.game.platformer.health = 5
            self.game.platformer.lives = 3
            self.start_game()

        elif self.selected_index == 1:  # HARD MODE
            self.game.mode = "Hard"
            self.game.platformer.health = 1
            self.game.platformer.lives = 1
            self.start_game()


        elif self.selected_index == 2:  # SETTINGS

            # FIXED: Wipe local screen entries and execute the settings state entry hook

            self.exit()

            for action in list(self.game.actions.keys()):
                self.game.actions[action] = False

            self.game.settings.enter()

        elif self.selected_index == 3:  # QUIT GAME
            self.game.running = False
            pygame.quit()
            import sys
            sys.exit()

    def start_game(self):
        """Standardized exit routine wrapper cleanly switching execution context to Level Select."""
        self.exit()
        pygame.mixer.music.stop()
        self.musicstart = False

        # Cleanly drop stale key tracking flags to break instant frame fires
        for action in list(self.game.actions.keys()):
            self.game.actions[action] = False

        self.game.levelselection.enter()

    def update(self):
        if self.musicstart == False:
            pygame.mixer.music.load(os.path.join("data", "music", "moesstartscreen.ogg"))
            pygame.mixer.music.play(-1, 0, 10)
            self.musicstart = True

        if self.input_delay > 0:
            self.input_delay -= 1

        # 1. Read real-time cursor navigation loops
        self.handle_mouse_input()

        # 2. Keyboard Navigation Fallback Loops (Maintains absolute compatibility)
        if self.input_delay == 0:
            if self.game.actions["down"]:
                self.selected_index = (self.selected_index + 1) % len(self.menu_options)
                self.input_delay = 15
            elif self.game.actions["up"]:
                self.selected_index = (self.selected_index - 1) % len(self.menu_options)
                self.input_delay = 15

            if self.game.actions["start"]:
                self.confirm_selection()

    def render(self):
        tempsurf = pygame.Surface((self.game.screen_width, self.game.screen_height))
        tempsurf.blit(pygame.transform.scale(self.background, (800, 640)), (0, 0))
        tempsurf.blit(pygame.transform.scale(self.grassshadow, (800, 640)), (random.randint(0, 5), 50))
        tempsurf.blit(pygame.transform.scale(self.grassimage, (800, 640)), (0, 55))
        tempsurf.blit(pygame.transform.scale(pygame.transform.flip(self.grassshadow, True, False), (800, 640)),
                      (random.randint(0, 5), 75))
        tempsurf.blit(pygame.transform.scale(pygame.transform.flip(self.grassimage, True, False), (800, 640)), (0, 80))

        tempsurf.blit(self.titletext2,
                      utilities.add_pos(self.titletextrect.topleft, (random.randint(5, 10), (random.randint(5, 10)))))
        tempsurf.blit(self.titletext, self.titletextrect)

        self.starttext.set_alpha(random.randint(50, 150))
        tempsurf.blit(self.starttext, self.starttextrect)

        # Clear active rectangles mapping list before rebuilding components on the frame
        self.option_rects = []

        # Render rows fields dynamically from our unified options array
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_index else (160, 160, 160)

            # Highlight selected item with a prefix arrow
            prefix = "> " if i == self.selected_index else "  "
            option_text = self.game.small_font.render(f"{prefix}{option}", True, color)

            # Position elements vertically down the display grid matrix
            option_rect = option_text.get_rect(
                center=(self.game.screen_width / 2, self.game.screen_height / 2 + (i * 45)))

            # Store the live rect bounds so handle_mouse_input can evaluate collision masks accurately
            self.option_rects.append(option_rect)
            tempsurf.blit(option_text, option_rect)

            if i == self.selected_index:
                rcolor = random.randint(20, 60)
                pygame.draw.rect(tempsurf, (rcolor, rcolor, rcolor),
                                 option_rect.inflate(random.randint(15, 25), random.randint(10, 15)), 1)

        tempsurf.blit(self.controls_text1, self.controls_rect1)
        tempsurf.blit(self.controls_text2, self.controls_rect2)

        tempsurf.set_colorkey((0, 0, 0))
        self.game.screen.blit(tempsurf, (0, 0))