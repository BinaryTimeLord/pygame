import os.path
import pygame
import state
import utilities


class Settings(state.State):
    def __init__(self, game):
        state.State.__init__(self, game)
        self.background = utilities.loadImage(os.path.join("data", "images"), "skygrad.png")

        # Track active navigation layout index rules
        # Index 0: Master Volume slider
        # Indices 1-8: Action keybind entries
        # Index 9: Reset to Default Keybinds
        # Index 10: Back Button
        self.selected_index = 0
        self.input_delay = 0

        # Remap state tracker toggles
        self.remapping_mode = False
        self.remap_target_action = None

        # Build list of configurable tracking actions to mirror game.py mapping structure
        self.bindable_actions = ["a", "b", "up", "down", "left", "right", "start", "select"]

        # Default key dictionary setup matching original game.py initialization
        self.default_mapping = {
            "a": pygame.K_SPACE,
            "b": pygame.K_BACKSPACE,
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "start": pygame.K_RETURN,
            "select": pygame.K_RIGHTBRACKET
        }

        # Volume configuration range parameters (0.0 to 1.0)
        self.volume_level = 0.5

        # UI Text/Rect definitions
        self.title_text = self.game.large_font.render("Settings Menu", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(self.game.screen_width / 2, 50))
        self.hint_text = self.game.tiny_font.render("Press Enter/Click to edit action keybinds", True, (200, 200, 200))
        self.hint_rect = self.hint_text.get_rect(center=(self.game.screen_width / 2, 100))

        self.option_rects = []
        # Store the exact coordinates of the slider graphic separately for precise dragging math
        self.slider_bar_rect = pygame.Rect(300, 160, 400, 15)

    def handle_mouse_input(self):
        """Processes screen-space mouse hover selections and clicks over active rows fields."""
        if self.input_delay > 0 or self.remapping_mode or not self.option_rects:
            return

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]  # Left Click Snapping

        for idx, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                if self.selected_index != idx:
                    self.selected_index = idx

                # Check for direct selections
                if mouse_clicked:
                    self.input_delay = 20
                    self.confirm_selection()
                    break

    def handle_event(self, event):
        """Processes events passed directly from the main engine loop to prevent queue starvation."""
        if not self.remapping_mode:
            return

        if event.type == pygame.KEYDOWN:
            # Ignore Escape key as a hardware binding backup escape
            if event.key == pygame.K_ESCAPE:
                self.remapping_mode = False
                self.input_delay = 15
                return

            # Overwrite action map indices directly inside core dictionary reference layout
            self.game.action_mapping[self.remap_target_action] = event.key
            self.remapping_mode = False
            self.input_delay = 20

    def confirm_selection(self):
        """Runs menu execution commands or flags binding locks active."""
        if self.selected_index == 0:
            pass
        elif 1 <= self.selected_index <= 8:
            # Selected an action row box to rebind
            self.remapping_mode = True
            self.remap_target_action = self.bindable_actions[self.selected_index - 1]
        elif self.selected_index == 9:
            # Reset to Default Keybinds triggered
            self.reset_to_defaults()
        elif self.selected_index == 10:
            # Back Button triggered
            self.return_to_title()

    def reset_to_defaults(self):
        """Safely rolls back action mapping structures to native engine constants."""
        for action, key_code in self.default_mapping.items():
            self.game.action_mapping[action] = key_code
        self.input_delay = 20

    def return_to_title(self):
        """Saves current engine configs and steps context backward."""
        self.exit()

        # Clean structural actions array to break instant-trigger loops
        for action in list(self.game.actions.keys()):
            self.game.actions[action] = False

        self.game.start.enter()

    def update(self):
        if self.input_delay > 0:
            self.input_delay -= 1

        # Skip logic updating completely while waiting for a key press bind
        if self.remapping_mode:
            return

        # 1. Process Hardware Cursor Hover Selections
        self.handle_mouse_input()

        # 2. Continuous Volume Slider Dragging Math
        mouse_buttons = pygame.mouse.get_pressed()[0]
        if mouse_buttons:  # If holding down left-click
            mouse_pos = pygame.mouse.get_pos()
            if self.selected_index == 0 or self.slider_bar_rect.inflate(20, 20).collidepoint(mouse_pos):
                self.selected_index = 0  # Force index focus onto slider

                # Clamp mouse horizontal values between the start and end coordinates of the bar
                relative_x = mouse_pos[0] - self.slider_bar_rect.x
                self.volume_level = max(0.0, min(1.0, relative_x / self.slider_bar_rect.width))

                # Apply adjustments directly into Pygame mixers
                pygame.mixer.music.set_volume(self.volume_level)

        # 3. Keyboard Backup Adjustments (Left/Right taps)
        if self.selected_index == 0:
            if self.game.actions["right"]:
                self.volume_level = min(1.0, self.volume_level + 0.02)
                pygame.mixer.music.set_volume(self.volume_level)
            elif self.game.actions["left"]:
                self.volume_level = max(0.0, self.volume_level - 0.02)
                pygame.mixer.music.set_volume(self.volume_level)

        # 4. Vertical Keyboard Grid Navigation Fallbacks (Modded to include index up to 10)
        if self.input_delay == 0:
            if self.game.actions["down"]:
                self.selected_index = (self.selected_index + 1) % 11
                self.input_delay = 12
            elif self.game.actions["up"]:
                self.selected_index = (self.selected_index - 1) % 11
                self.input_delay = 12

            if self.game.actions["start"]:
                self.confirm_selection()

    def render(self):
        self.game.screen.blit(
            pygame.transform.scale(self.background, (self.game.screen_width, self.game.screen_height)), (0, 0))
        self.game.screen.blit(self.title_text, self.title_rect)
        self.game.screen.blit(self.hint_text, self.hint_rect)

        self.option_rects = []
        start_y = 140
        spacing_y = 38

        self.slider_bar_rect.y = start_y + 10

        # ---- 1. RENDER VOLUME SLIDER BAR ----
        v_color = (255, 255, 0) if self.selected_index == 0 else (255, 255, 255)
        v_label = self.game.small_font.render("Master Volume:", True, v_color)
        self.game.screen.blit(v_label, (50, start_y))

        pygame.draw.rect(self.game.screen, (60, 60, 60), self.slider_bar_rect)

        fill_width = int(self.slider_bar_rect.width * self.volume_level)
        fill_rect = pygame.Rect(self.slider_bar_rect.x, self.slider_bar_rect.y, fill_width, self.slider_bar_rect.height)
        pygame.draw.rect(self.game.screen, (0, 255, 0), fill_rect)

        slider_hitbox = pygame.Rect(50, start_y, 700, 30)
        self.option_rects.append(slider_hitbox)

        # ---- 2. RENDER ACTION KEYBINDS ROWS FIELDS ----
        for idx, action in enumerate(self.bindable_actions):
            row_index = idx + 1
            r_color = (255, 255, 0) if self.selected_index == row_index else (255, 255, 255)

            y_pos = start_y + (row_index * spacing_y)

            key_code = self.game.action_mapping[action]
            key_name = pygame.key.name(key_code).upper()

            action_surf = self.game.small_font.render(f"Action [{action.upper()}]:", True, r_color)
            self.game.screen.blit(action_surf, (50, y_pos))

            if self.remapping_mode and self.remap_target_action == action:
                bind_surf = self.game.small_font.render("< PRESS ANY KEY >", True, (255, 50, 50))
            else:
                bind_surf = self.game.small_font.render(key_name, True, (150, 255, 150))

            self.game.screen.blit(bind_surf, (300, y_pos))

            row_hitbox = pygame.Rect(50, y_pos, 700, 30)
            self.option_rects.append(row_hitbox)

        # ---- 3. RENDER RESET TO DEFAULTS BUTTON ----
        reset_y = start_y + (9 * spacing_y) + 10
        reset_color = (255, 255, 0) if self.selected_index == 9 else (255, 150, 150)
        reset_text = "> Reset Keybinds to Default <" if self.selected_index == 9 else "Reset Keybinds to Default"
        reset_surf = self.game.small_font.render(reset_text, True, reset_color)
        reset_rect = reset_surf.get_rect(center=(self.game.screen_width / 2, reset_y))

        self.game.screen.blit(reset_surf, reset_rect)
        self.option_rects.append(reset_rect)

        # ---- 4. RENDER BACK BUTTON ----
        back_y = start_y + (10 * spacing_y) + 20
        b_color = (255, 255, 0) if self.selected_index == 10 else (200, 200, 200)
        b_text = "> Back to Title Menu <" if self.selected_index == 10 else "Back to Title Menu"
        back_surf = self.game.small_font.render(b_text, True, b_color)
        back_rect = back_surf.get_rect(center=(self.game.screen_width / 2, back_y))

        self.game.screen.blit(back_surf, back_rect)
        self.option_rects.append(back_rect)
