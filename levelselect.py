import os.path
import pygame
import level
import utilities
import state


class LevelSelect(state.State):
    def __init__(self, game):
        state.State.__init__(self, game)
        self.mapimage = utilities.loadImage(os.path.join("data", "images"), "mapselect.png")
        self.points = [(622, 622), (650, 506), (738, 379), (688, 234), (520, 365), (345, 365), (333, 250), (469, 232),
                       (496, 102), (383, 134), (246, 109), (81, 135)]
        self.current_sel = 0
        self.pressedonce = False
        self.musicplaying = False
        self.movesound = utilities.loadSound(os.path.join("data", "sounds"), "selmove.wav")
        self.levellock = level.levellocks

        # Text definitions updated to large_font for increased scale
        self.back_text_normal = self.game.large_font.render("Back to Title", True, (0, 0, 0))  # Bigger black text
        self.back_text_hover = self.game.large_font.render("Back to Title", True,
                                                           (128, 128, 128))  # Bigger grey hover text

        # Position dynamically calculated for the bottom-left corner
        self.back_rect = self.back_text_normal.get_rect(
            bottomleft=(20, self.game.screen_height - 20)
        )

        self.mouse_over_back = False
        self.input_delay = 0

    def handle_mouse_navigation(self):
        """Monitors real-time cursor bounds over the back button and world map node points."""
        if self.input_delay > 0:
            return

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]  # Left Hardware Click Snap

        # 1. Check collision overlap against the back button bounds
        if self.back_rect.collidepoint(mouse_pos):
            self.mouse_over_back = True
            if mouse_clicked:
                self.input_delay = 20
                self.return_to_start()
                return
        else:
            self.mouse_over_back = False

        # 2. Check collision overlap against individual world map node positions
        for idx, point in enumerate(self.points):
            # Create a virtual interaction hitbox around the 14-pixel circle node radius
            node_rect = pygame.Rect(point[0] - 14, point[1] - 14, 28, 28)

            if node_rect.collidepoint(mouse_pos):
                # Hover selects the node and plays audio if focus shifted
                if self.current_sel != idx:
                    self.current_sel = idx
                    if self.movesound:
                        self.movesound.play()

                # Direct left-click launches the highlighted level map selection
                if mouse_clicked:
                    self.input_delay = 20
                    self.launch_level()
                    break

    def launch_level(self):
        """Validates current lock arrays constraints and passes game engine tracking into platformer."""
        if self.levellock[self.current_sel] == 0 or self.levellock[self.current_sel] == 2:
            self.exit()
            self.musicplaying = False

            # Flush action dictionary to eliminate instant-trigger cycles on frame 1
            for action in list(self.game.actions.keys()):
                self.game.actions[action] = False

            self.game.platformer.enter()

            # Map dynamic index coordinates over to our level maps templates
            level_map = [
                self.game.platformer.level1, self.game.platformer.level2, self.game.platformer.level3,
                self.game.platformer.level4,
                self.game.platformer.level5, self.game.platformer.level6, self.game.platformer.level7,
                self.game.platformer.level8,
                self.game.platformer.level9, self.game.platformer.level10, self.game.platformer.level11,
                self.game.platformer.level12
            ]
            self.game.platformer.levelparse(level_map[self.current_sel])

    def return_to_start(self):
        """Clears current active state layers and safely moves memory focus back to the title screen."""
        self.exit()
        pygame.mixer.music.stop()
        self.musicplaying = False

        # Flush control inputs dictionary array entries to bypass instant firing frames
        for action in list(self.game.actions.keys()):
            self.game.actions[action] = False

        self.game.start.enter()

    def update(self):
        if self.input_delay > 0:
            self.input_delay -= 1

        # 1. Process Hardware Cursor Interaction Loops
        self.handle_mouse_navigation()

        # 2. Keyboard Navigation Fallback Loops (Only checks if mouse isn't on the back button)
        if self.input_delay == 0 and not self.mouse_over_back:
            if self.game.actions["up"] and self.current_sel < 11 and self.pressedonce == False:
                self.current_sel += 1
                self.pressedonce = True
                if self.movesound:
                    self.movesound.play()
            elif self.game.actions["down"] and self.current_sel > 0 and self.pressedonce == False:
                self.current_sel -= 1
                self.pressedonce = True
                if self.movesound:
                    self.movesound.play()

            if not self.game.actions["up"] and not self.game.actions["down"]:
                self.pressedonce = False

            if self.game.actions["a"]:
                self.input_delay = 20
                self.launch_level()

        # Continuous audio checker setup
        if not self.musicplaying:
            pygame.mixer.music.load(os.path.join("data", "music", "levelsel.ogg"))
            pygame.mixer.music.play(-1)
            self.musicplaying = True

    def render(self):
        self.game.screen.blit(pygame.transform.scale(self.mapimage, (self.game.screen_width, self.game.screen_height)),
                              (0, 0))

        # 1. Dynamically select text color profile depending on active hover flag statuses
        if self.mouse_over_back:
            self.game.screen.blit(self.back_text_hover, self.back_rect)
        else:
            self.game.screen.blit(self.back_text_normal, self.back_rect)

        # 2. Render Level Node Graph lines matrices
        pygame.draw.lines(self.game.screen, (25, 25, 25), False, self.points, 6)
        pygame.draw.lines(self.game.screen, (255, 255, 255), False, self.points, 3)

        at = 0
        for i in self.points:
            pygame.draw.circle(self.game.screen, (25, 25, 25), i, 14)
            pygame.draw.circle(self.game.screen, (255, 255, 255), i, 10)
            if self.levellock[at] == 1:
                pygame.draw.circle(self.game.screen, (255, 25, 25), i, 8)
            if self.levellock[at] == 2:
                pygame.draw.circle(self.game.screen, (25, 255, 25), i, 8)
            at += 1

        # Draw current coordinate selector pointer highlight bubble
        pygame.draw.circle(self.game.screen, (2, 2, 255), self.points[self.current_sel], 9)
