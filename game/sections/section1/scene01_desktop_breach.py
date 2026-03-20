import math
import random
import string
from collections import deque

import pygame


class Section1Scene1DesktopBreach:
    name = "Section 1 / Scene 1 - Desktop Breach Intro"
    ALLOWED_EXTRA_KEYS = "-_/.:"
    MOVEMENT_KEYS = {
        pygame.K_UP,
        pygame.K_DOWN,
        pygame.K_LEFT,
        pygame.K_RIGHT,
        pygame.K_HOME,
        pygame.K_END,
        pygame.K_PAGEUP,
        pygame.K_PAGEDOWN,
    }
    MODIFIER_KEYS = {
        pygame.K_LSHIFT,
        pygame.K_RSHIFT,
        pygame.K_LCTRL,
        pygame.K_RCTRL,
        pygame.K_LALT,
        pygame.K_RALT,
        pygame.K_LGUI,
        pygame.K_RGUI,
    }

    def __init__(self) -> None:
        self.stage = 0
        self.stage_key_count = 0
        self.keys_needed = 30
        self.is_complete = False

        self.total_letter_keys = 0
        self.raw_key_stream = ""
        self.raw_key_stream_max = 56
        self.last_gameplay_key = ""
        self.number_key_count = 0
        self.symbol_key_count = 0

        self.rng = random.Random(401)

        self.button_flash_timer = 0.0
        self.button_flash_duration = 0.24

        self.key_popup_text = ""
        self.key_popup_timer = 0.0

        self.input_activity = 0.0
        self.shake_timer = 0.0
        self.cursor_pos = [926.0, 178.0]
        self.cursor_target = [926.0, 178.0]
        self.cursor_click_timer = 0.0
        self.cursor_pause_timer = 0.0
        self.last_cursor_target = (int(self.cursor_target[0]), int(self.cursor_target[1]))

        self.toast_lifetime = 2.4
        self.toast_events = []
        self.live_alerts = []
        self.live_alert_lifetime = 3.0

        self.key_times = deque(maxlen=140)
        self.typing_wpm = 0.0
        self.reveal_budget = 0.0
        self.reveal_momentum = 0.0
        self.reveal_channel_cursor = 0
        self.stage_flash_timer = 0.0
        # Combo prompts should stay rare so free typing remains the default flow.
        self.combo_prompt = ""
        self.future_combo_prompt = "Combo hint: Ctrl+L then Enter to clear the terminal pane"
        self.combo_rules = [
            {
                "name": "clear_terminal",
                "keys": ("Ctrl+L", "Enter"),
                "prompt": self.future_combo_prompt,
                "enabled": False,
            }
        ]

        self.terminal_prompt = "parrot@kidgame:~$ "
        self.terminal_buffer = deque(
            [
                "$ booting parrot os desktop...",
                "$ loading scene_01 assets",
                "$ keyboard entropy detected",
                "$ syslog watcher attached to local mail relay",
            ],
            maxlen=14,
        )
        self.terminal_steps = [
            {
                "min_stage": 0,
                "command": "sudo htop --sort-key=PERCENT_CPU",
                "outputs": [
                    "[htop] cpu 18%  mem 42%  tasks 167",
                    "[htop] suspicious process mail_syncd(pid 4128) spikes on key bursts",
                    "[htop] watcher note: perimeter service drift detected",
                ],
                "alert": ("Resource Alert", "mail_syncd spikes whenever typing velocity rises"),
            },
            {
                "min_stage": 0,
                "command": "nmap -sV 127.0.0.1 --top-ports 20",
                "outputs": [
                    "Starting Nmap 7.94 scan report for kidgame (127.0.0.1)",
                    "PORT    STATE SERVICE  VERSION",
                    "25/tcp  open  smtp     masked-relay",
                    "443/tcp open  https    unknown-cert (CN=void-gateway)",
                    "Nmap done: 1 host up, 20 ports probed",
                ],
                "alert": ("Port Warning", "Untrusted relay services detected on critical ports"),
            },
            {
                "min_stage": 1,
                "command": "tshark -i lo -a duration:5 -q",
                "outputs": [
                    "Capturing on loopback: burst mode enabled",
                    "tcp syn flood signatures observed -> source masked",
                    "decoded stream phrase: warning they are coming",
                ],
                "alert": ("Traffic Surge", "Loopback capture found hidden warning payload"),
            },
            {
                "min_stage": 2,
                "command": "burpsuite --project-file incident_trace.burp --passive",
                "outputs": [
                    "[burp] passive scan started for internal mail UI",
                    "[burp] issue: response headers expose breach fingerprints",
                    "[burp] issue: hidden note field references breach-all-ports",
                ],
                "alert": ("Mail UI Alert", "Passive scan surfaced hidden breach markers"),
            },
            {
                "min_stage": 2,
                "command": "msfconsole -q",
                "outputs": [
                    "msf6 > workspace -a incident_scene1",
                    "msf6 > notes add \"warning they are coming\"",
                    "msf6 > banner monitor: hostile foothold confirmed",
                ],
                "alert": ("Console Signal", "Incident workspace synced with breach evidence"),
            },
            {
                "min_stage": 3,
                "command": "python3 trace_intrusion.py --hunt clown-route",
                "outputs": [
                    "[trace] route marker resolved: carnival-grid/void",
                    "[trace] hostile message mirrored to local desktop",
                    "[trace] response path pending user continuation",
                ],
                "alert": ("Endpoint Alert", "Malware taunt synchronized with trace pipeline"),
            },
        ]
        self.terminal_step_index = 0
        self.terminal_mode = "typing_command"
        self.terminal_command_progress = 0
        self.terminal_output_line_index = 0
        self.terminal_output_char_progress = 0
        self.terminal_pause_timer = 0.0
        self.terminal_progress_units = 0.0
        self.terminal_pending_alert = None

        self.stage_names = [
            "Parrot OS desktop",
            "Email alert popup",
            "Email opened",
            "Malware popup",
        ]

        self.script_channels = {
            "decoded": {
                "text": (
                    "filter> random keys accepted\n"
                    "filter> entropy reduced to signal\n"
                    "filter> warning they are coming\n"
                    "filter> breach all ports\n"
                    "filter> hostile foothold confirmed"
                ),
                "revealed": 8,
            },
            "alert": {
                "text": "Subject: WARNING - they are coming",
                "revealed": 0,
            },
            "email": {
                "text": (
                    "WARNING: they are coming.\n"
                    "BREACH ALL PORTS!!\n"
                    "They are not knocking. They are already inside.\n"
                    "Follow the traces before they vanish."
                ),
                "revealed": 0,
            },
            "malware": {
                "text": (
                    "UNAUTHORIZED ACCESS ACTIVE.\n"
                    "remote operator session detected\n"
                    "route marker: carnival-grid/void"
                ),
                "revealed": 0,
            },
        }

        self.title_font = pygame.font.SysFont("dejavusans", 34, bold=True)
        self.subhead_font = pygame.font.SysFont("dejavusans", 24, bold=True)
        self.body_font = pygame.font.SysFont("dejavusans", 20)
        self.small_font = pygame.font.SysFont("dejavusans", 17)
        self.mono_font = pygame.font.SysFont("dejavusansmono", 18)
        self.tiny_font = pygame.font.SysFont("dejavusansmono", 14)

    def handle_event(self, event: pygame.event.Event) -> None:
        key_char = self._extract_gameplay_input(event)
        if key_char is None:
            return

        self._register_gameplay_press(key_char)
        self.stage_key_count += 1
        if self.stage_key_count >= self.keys_needed:
            self.stage_key_count = 0
            if self.stage < 3:
                self.stage += 1
                self.stage_flash_timer = 1.0
                self.cursor_pause_timer = 0.12
                self._push_toast(f"state transition: {self.stage_names[self.stage]}")
                self._push_live_alert("Stage Update", f"Scene escalated to {self.stage_names[self.stage]}")
                self._retarget_cursor("stage_change")
            else:
                self.is_complete = True
                self._push_toast("Scene 1 complete -> syncing loopback capture")

    def update(self, delta_seconds: float) -> None:
        self.button_flash_timer = max(0.0, self.button_flash_timer - delta_seconds)
        self.key_popup_timer = max(0.0, self.key_popup_timer - delta_seconds)
        self.input_activity = max(0.0, self.input_activity - delta_seconds * 0.95)
        self.shake_timer = max(0.0, self.shake_timer - delta_seconds * 2.6)
        self.cursor_click_timer = max(0.0, self.cursor_click_timer - delta_seconds * 3.8)
        self.cursor_pause_timer = max(0.0, self.cursor_pause_timer - delta_seconds)
        self.stage_flash_timer = max(0.0, self.stage_flash_timer - delta_seconds * 1.2)

        active_toasts = []
        for toast in self.toast_events:
            toast["timer"] -= delta_seconds
            if toast["timer"] > 0:
                active_toasts.append(toast)
        self.toast_events = active_toasts

        active_alerts = []
        for alert in self.live_alerts:
            alert["timer"] -= delta_seconds
            if alert["timer"] > 0:
                active_alerts.append(alert)
        self.live_alerts = active_alerts

        self.reveal_momentum = max(0.0, self.reveal_momentum - delta_seconds * 3.8)
        self._trim_old_key_times()
        self._advance_terminal_story(delta_seconds)
        self._advance_script_from_rhythm(delta_seconds)
        self._update_cursor(delta_seconds)

    def render(self, surface: pygame.Surface) -> None:
        self._draw_desktop(surface)

        if self.stage >= 1:
            self._draw_email_alert(surface)
        if self.stage >= 2:
            self._draw_email_window(surface)
        if self.stage >= 3:
            self._draw_malware_popup(surface)

        self._draw_live_alerts(surface)
        self._draw_toasts(surface)
        self._draw_cursor(surface)

    @classmethod
    def _extract_gameplay_input(cls, event: pygame.event.Event) -> str | None:
        if event.type != pygame.KEYDOWN:
            return None
        if event.key in cls.MODIFIER_KEYS or event.key in cls.MOVEMENT_KEYS:
            return None
        if not event.unicode:
            return None
        key_char = event.unicode.lower()
        allowed_chars = string.ascii_lowercase + string.digits + cls.ALLOWED_EXTRA_KEYS
        if len(key_char) != 1 or key_char not in allowed_chars:
            return None
        return key_char

    @staticmethod
    def _format_gameplay_key(key_char: str) -> str:
        special_names = {
            "-": "DASH",
            "_": "UNDERSCORE",
            "/": "SLASH",
            ".": "DOT",
            ":": "COLON",
        }
        return special_names.get(key_char, key_char.upper())

    def _register_gameplay_press(self, key_char: str) -> None:
        now_seconds = pygame.time.get_ticks() / 1000.0
        self.key_times.append(now_seconds)
        instant_wpm = self._compute_instant_wpm()
        self.typing_wpm = self.typing_wpm * 0.74 + instant_wpm * 0.26

        speed_factor = max(0.65, min(2.5, self.typing_wpm / 42.0 if self.typing_wpm > 0 else 0.65))

        self.total_letter_keys += 1
        self.last_gameplay_key = key_char
        if key_char in string.digits:
            self.number_key_count += 1
        elif key_char in self.ALLOWED_EXTRA_KEYS:
            self.symbol_key_count += 1
        self.button_flash_timer = max(self.button_flash_duration, 0.14 + 0.1 * speed_factor)
        self.key_popup_text = f"[{self._format_gameplay_key(key_char)}] -> {self._terminal_input_hint()}"
        self.key_popup_timer = max(0.18, 0.44 - min(0.2, speed_factor * 0.1))
        self.input_activity = min(1.0, self.input_activity + 0.16 + 0.05 * speed_factor)
        self.shake_timer = min(1.0, self.shake_timer + 0.22 + 0.1 * speed_factor)
        self.cursor_click_timer = 0.8
        move_interval = 7
        if self.stage == 1:
            move_interval = 5
        elif self.stage == 2:
            move_interval = 4
        elif self.stage >= 3:
            move_interval = 3
        if self.typing_wpm > 110:
            move_interval = max(2, move_interval - 1)
        if self.total_letter_keys % move_interval == 0:
            self._retarget_cursor("typing")

        self.raw_key_stream += key_char
        if len(self.raw_key_stream) > self.raw_key_stream_max:
            self.raw_key_stream = self.raw_key_stream[-self.raw_key_stream_max :]

        self.reveal_momentum = min(17.0, self.reveal_momentum + 1.0 * speed_factor)
        self.reveal_budget += 0.8 + 0.6 * speed_factor

        if self.total_letter_keys % 6 == 0:
            event_messages = [
                "Filter daemon: parsed input cluster",
                "Threat monitor: pattern confidence up",
                "Mail client: hidden draft expanded",
                "Popup manager: warning stack updated",
            ]
            message_index = (self.total_letter_keys // 6 - 1) % len(event_messages)
            self._push_toast(f"{event_messages[message_index]} ({int(self.typing_wpm)} wpm)")
            if self.total_letter_keys % 12 == 0:
                self._push_live_alert("Input Signal", event_messages[message_index])

    def _compute_instant_wpm(self) -> float:
        if len(self.key_times) < 2:
            return 0.0
        span_seconds = max(0.25, self.key_times[-1] - self.key_times[0])
        keys_per_second = (len(self.key_times) - 1) / span_seconds
        wpm = keys_per_second * 12.0
        return max(0.0, min(180.0, wpm))

    def _trim_old_key_times(self) -> None:
        if not self.key_times:
            return
        now_seconds = pygame.time.get_ticks() / 1000.0
        while self.key_times and now_seconds - self.key_times[0] > 4.0:
            self.key_times.popleft()

        if len(self.key_times) >= 2:
            instant_wpm = self._compute_instant_wpm()
            self.typing_wpm = self.typing_wpm * 0.88 + instant_wpm * 0.12
        else:
            self.typing_wpm = max(0.0, self.typing_wpm - 22.0 / 60.0)

    def _advance_terminal_story(self, delta_seconds: float) -> None:
        if self.terminal_step_index >= len(self.terminal_steps):
            return

        if self.terminal_mode.startswith("pause"):
            pause_speed = 0.7 + self.input_activity * 2.1
            self.terminal_pause_timer -= delta_seconds * pause_speed
            if self.terminal_pause_timer > 0:
                return
            if self.terminal_mode == "pause_before_output":
                self.terminal_mode = "typing_output"
            elif self.terminal_mode == "pause_between_lines":
                self.terminal_mode = "typing_output"
            elif self.terminal_mode == "pause_after_step":
                self.terminal_mode = "typing_command"
                self.terminal_step_index += 1
                self.terminal_command_progress = 0
                self.terminal_output_line_index = 0
                self.terminal_output_char_progress = 0
                if self.terminal_pending_alert:
                    alert = self.terminal_pending_alert
                    self._push_live_alert(alert[0], alert[1])
                    self.terminal_pending_alert = None

        if self.terminal_step_index >= len(self.terminal_steps):
            return

        active_step = self.terminal_steps[self.terminal_step_index]
        if self.stage < active_step["min_stage"]:
            return

        self.terminal_progress_units += self._terminal_reveal_speed() * delta_seconds
        reveals = int(self.terminal_progress_units)
        if reveals <= 0:
            return

        self.terminal_progress_units -= reveals
        for _ in range(reveals):
            if self.terminal_mode == "typing_command":
                command = active_step["command"]
                if self.terminal_command_progress < len(command):
                    self.terminal_command_progress += 1
                else:
                    self._append_terminal_line(f"{self.terminal_prompt}{command}")
                    self.terminal_mode = "pause_before_output"
                    self.terminal_pause_timer = max(0.08, 0.28 - self.input_activity * 0.15)
                    break
            elif self.terminal_mode == "typing_output":
                output_lines = active_step["outputs"]
                if self.terminal_output_line_index >= len(output_lines):
                    self._complete_terminal_step()
                    break

                current_output = output_lines[self.terminal_output_line_index]
                if self.terminal_output_char_progress < len(current_output):
                    self.terminal_output_char_progress += 1
                else:
                    self._append_terminal_line(current_output)
                    self.terminal_output_line_index += 1
                    self.terminal_output_char_progress = 0
                    if self.terminal_output_line_index >= len(output_lines):
                        self._complete_terminal_step()
                        break
                    self.terminal_mode = "pause_between_lines"
                    self.terminal_pause_timer = max(0.04, 0.14 - self.input_activity * 0.08)
                    break
            else:
                break

    def _terminal_reveal_speed(self) -> float:
        if self.input_activity < 0.03 and self.typing_wpm < 6.0 and self.reveal_momentum < 0.4:
            return 0.0
        speed_floor = 0.04 + self.input_activity * 0.65
        typing_speed = (self.typing_wpm / 8.5) * (0.2 + 0.8 * self.input_activity)
        momentum_speed = self.reveal_momentum * 0.35
        return speed_floor + typing_speed + momentum_speed

    def _complete_terminal_step(self) -> None:
        step = self.terminal_steps[self.terminal_step_index]
        self.terminal_pending_alert = step.get("alert")
        self._push_toast(f"command complete: {step['command'].split(' ')[0]}")
        self._retarget_cursor("command_done")
        self.terminal_mode = "pause_after_step"
        self.terminal_pause_timer = max(0.12, 0.24 - self.input_activity * 0.1)

    def _append_terminal_line(self, text: str) -> None:
        self.terminal_buffer.append(text)

    def _terminal_overlay_line(self) -> str:
        if self.terminal_step_index >= len(self.terminal_steps):
            return f"{self.terminal_prompt}awaiting next scene..."
        step = self.terminal_steps[self.terminal_step_index]
        if self.stage < step["min_stage"]:
            return f"{self.terminal_prompt}waiting_for_stage_{step['min_stage'] + 1}..."

        if self.terminal_mode == "typing_command":
            command = step["command"][: self.terminal_command_progress]
            cursor = "_" if pygame.time.get_ticks() % 1000 < 520 else " "
            return f"{self.terminal_prompt}{command}{cursor}"

        if self.terminal_mode == "typing_output":
            output = step["outputs"][self.terminal_output_line_index]
            return output[: self.terminal_output_char_progress]

        return ""

    def _terminal_input_hint(self) -> str:
        if self.terminal_step_index >= len(self.terminal_steps):
            return "scene_sync"

        step = self.terminal_steps[self.terminal_step_index]
        command_head = step["command"].split(" ")[0]

        if self.stage < step["min_stage"]:
            return f"unlock_stage_{step['min_stage'] + 1}"
        if self.terminal_mode == "typing_command":
            return f"type_{command_head}"
        if self.terminal_mode == "typing_output":
            return f"read_{command_head}_output"
        return f"sync_{command_head}"

    def _advance_script_from_rhythm(self, delta_seconds: float) -> None:
        base_chars = 0.08 * self.input_activity
        speed_chars = min(8.5, self.typing_wpm / 11.0) * (0.22 + 0.78 * self.input_activity)
        momentum_chars = self.reveal_momentum * 0.52
        self.reveal_budget += (base_chars + speed_chars + momentum_chars) * delta_seconds

        reveal_units = int(self.reveal_budget)
        if reveal_units <= 0:
            return

        revealed_count = self._reveal_chars(reveal_units)
        self.reveal_budget = max(0.0, self.reveal_budget - revealed_count)

    def _reveal_chars(self, count: int) -> int:
        channels = self._active_channels()
        if not channels:
            return 0

        revealed = 0
        guard = 0
        max_attempts = count * 8

        while revealed < count and guard < max_attempts:
            guard += 1
            channel = channels[self.reveal_channel_cursor % len(channels)]
            self.reveal_channel_cursor += 1
            revealed += self._reveal_chars_in_channel(channel, count - revealed)

        return revealed

    def _reveal_chars_in_channel(self, channel_name: str, remaining_budget: int) -> int:
        channel = self.script_channels[channel_name]
        if channel["revealed"] >= len(channel["text"]):
            return 0

        chars_to_reveal = 1
        if channel_name == "alert":
            chars_to_reveal = 2

        chars_to_reveal = min(chars_to_reveal, remaining_budget, len(channel["text"]) - channel["revealed"])
        channel["revealed"] += chars_to_reveal
        return chars_to_reveal

    def _active_channels(self) -> list[str]:
        if self.stage == 0:
            return ["decoded"]
        if self.stage == 1:
            return ["decoded", "alert"]
        if self.stage == 2:
            return ["decoded", "alert", "email"]
        return ["decoded", "alert", "email", "malware"]

    def _channel_visible(self, channel_name: str) -> str:
        channel = self.script_channels[channel_name]
        return channel["text"][: channel["revealed"]]

    def _push_toast(self, text: str) -> None:
        self.toast_events.append({"text": text, "timer": self.toast_lifetime})
        if len(self.toast_events) > 5:
            self.toast_events = self.toast_events[-5:]

    def _push_live_alert(self, title: str, body: str) -> None:
        self.live_alerts.append({"title": title, "body": body, "timer": self.live_alert_lifetime})
        if len(self.live_alerts) > 3:
            self.live_alerts = self.live_alerts[-3:]

    def _retarget_cursor(self, reason: str = "typing") -> None:
        candidates = [
            (431, 343, 1.8),  # terminal input line
            (362, 174, 1.1),  # terminal title bar
        ]

        if self.stage >= 1:
            candidates.extend(
                [
                    (1113, 210, 1.5),  # open-mail button zone
                    (1006, 88, 1.1),  # alert popup title
                ]
            )
        if self.stage >= 2:
            candidates.extend(
                [
                    (670, 316, 1.7),  # email body
                    (842, 426, 1.2),  # email confidence/status row
                    (527, 352, 1.0),  # sidebar alerts folder
                ]
            )
        if self.stage >= 3:
            candidates.extend(
                [
                    (649, 252, 2.0),  # malware popup header
                    (739, 406, 1.4),  # malware body text
                ]
            )

        if reason == "stage_change":
            for index, point in enumerate(candidates):
                boost = 1.25 if point[0] > 760 else 1.0
                candidates[index] = (point[0], point[1], point[2] * boost)
        elif reason == "command_done":
            for index, point in enumerate(candidates):
                boost = 1.35 if point[0] < 760 else 1.0
                candidates[index] = (point[0], point[1], point[2] * boost)

        total_weight = sum(point[2] for point in candidates)
        pick_value = self.rng.uniform(0.0, total_weight)
        chosen_x = 431
        chosen_y = 343
        running = 0.0
        for point_x, point_y, weight in candidates:
            running += weight
            if pick_value <= running:
                chosen_x = point_x
                chosen_y = point_y
                break

        distance = math.hypot(chosen_x - self.last_cursor_target[0], chosen_y - self.last_cursor_target[1])
        if distance < 24 and len(candidates) > 1:
            farthest = max(candidates, key=lambda p: math.hypot(p[0] - self.last_cursor_target[0], p[1] - self.last_cursor_target[1]))
            chosen_x, chosen_y = farthest[0], farthest[1]

        jitter_scale = 2 + int(self.input_activity * 7)
        chosen_x += self.rng.randint(-jitter_scale, jitter_scale)
        chosen_y += self.rng.randint(-jitter_scale, jitter_scale)

        self.cursor_target[0] = float(chosen_x)
        self.cursor_target[1] = float(chosen_y)
        self.last_cursor_target = (int(chosen_x), int(chosen_y))

    def _update_cursor(self, delta_seconds: float) -> None:
        if self.cursor_pause_timer > 0:
            return
        catchup_speed = 5.4 + min(11.0, self.typing_wpm / 12.0)
        lerp_amount = min(1.0, delta_seconds * catchup_speed)
        self.cursor_pos[0] += (self.cursor_target[0] - self.cursor_pos[0]) * lerp_amount
        self.cursor_pos[1] += (self.cursor_target[1] - self.cursor_pos[1]) * lerp_amount

    def _draw_desktop(self, surface: pygame.Surface) -> None:
        width, height = surface.get_size()

        surface.fill((34, 73, 104))
        pygame.draw.rect(surface, (23, 44, 72), (0, 0, width, height // 2))
        pygame.draw.circle(surface, (44, 93, 133), (width - 120, 120), 250)
        pygame.draw.circle(surface, (18, 39, 61), (220, height - 100), 340)
        pygame.draw.circle(surface, (54, 112, 152), (width // 2, height + 80), 420)
        for x_pos in range(-120, width, 110):
            pygame.draw.line(surface, (28, 58, 84), (x_pos, 48), (x_pos + 180, height), 1)
        horizon_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(horizon_overlay, (9, 16, 24, 52), (0, height - 140, width, 140))
        pygame.draw.rect(horizon_overlay, (134, 192, 232, 18), (0, 42, width, 2))
        surface.blit(horizon_overlay, (0, 0))

        top_bar = pygame.Rect(0, 0, width, 42)
        pygame.draw.rect(surface, (19, 24, 31), top_bar)
        pygame.draw.line(surface, (53, 66, 79), (0, 41), (width, 41), 1)
        self._blit_text(surface, self.small_font, "Activities", (16, 12), (222, 228, 235))
        self._blit_text(surface, self.small_font, self._clock_label(), (width // 2 - 38, 12), (222, 228, 235))

        net_label = "net secure"
        if self.stage >= 1:
            net_label = "net monitoring"
        if self.stage >= 2:
            net_label = "net unstable"
        alert_count = min(9, len(self.toast_events) + self.stage)
        self._blit_text(
            surface,
            self.small_font,
            f"{net_label}   bat 62%   notif {alert_count}",
            (width - 270, 12),
            (199, 215, 224),
        )

        meter_rect = pygame.Rect(width - 128, 27, 98, 8)
        meter_fill = int((meter_rect.w - 2) * (0.16 + 0.84 * self.input_activity))
        meter_pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.015)
        meter_glow = int(self.input_activity * 34 * meter_pulse)
        pygame.draw.rect(surface, (44, 54, 67), meter_rect, border_radius=4)
        pygame.draw.rect(
            surface,
            (111 + meter_glow // 2, 186 + meter_glow, 136 + meter_glow // 3),
            (meter_rect.x + 1, meter_rect.y + 1, meter_fill, meter_rect.h - 2),
            border_radius=3,
        )

        dock_bg = pygame.Rect(12, 66, 62, height - 156)
        pygame.draw.rect(surface, (20, 27, 35), dock_bg, border_radius=12)
        dock_pulse = int(self.stage_flash_timer * 42)
        for index in range(7):
            icon_rect = pygame.Rect(17, 74 + index * 74, 52, 52)
            active = index == 1 or (self.stage >= 2 and index == 3)
            fill = (72, 106, 138) if active else (43, 54, 66)
            pygame.draw.rect(surface, fill, icon_rect, border_radius=11)
            pygame.draw.circle(surface, (136, 170, 196), icon_rect.center, 12)
            if active:
                pygame.draw.rect(
                    surface,
                    (168 + dock_pulse // 3, 216 + dock_pulse // 2, min(255, 238 + dock_pulse)),
                    icon_rect,
                    2,
                    border_radius=11,
                )

        terminal = pygame.Rect(122, 110, 610, 352)
        shadow = terminal.move(8, 9)
        pygame.draw.rect(surface, (10, 14, 20), shadow, border_radius=7)
        pygame.draw.rect(surface, (22, 22, 26), terminal, border_radius=6)
        pygame.draw.rect(surface, (53, 56, 62), (terminal.x, terminal.y, terminal.w, 34), border_radius=6)
        pygame.draw.rect(surface, (53, 56, 62), (terminal.x, terminal.y + 28, terminal.w, 8))
        pygame.draw.circle(surface, (228, 101, 92), (terminal.x + 18, terminal.y + 17), 5)
        pygame.draw.circle(surface, (232, 188, 81), (terminal.x + 34, terminal.y + 17), 5)
        pygame.draw.circle(surface, (116, 198, 112), (terminal.x + 50, terminal.y + 17), 5)
        pygame.draw.rect(surface, (37, 45, 54), (terminal.x + 12, terminal.y + 46, 2, terminal.h - 60), border_radius=1)
        self._blit_text(
            surface,
            self.small_font,
            "parrot-terminal - parrot@kidgame",
            (terminal.x + 70, terminal.y + 8),
            (220, 220, 226),
        )

        terminal_lines = list(self.terminal_buffer)[-7:]
        overlay_line = self._terminal_overlay_line()
        if overlay_line:
            terminal_lines.append(overlay_line)
        terminal_lines = terminal_lines[-8:]
        for index, line in enumerate(terminal_lines):
            if line.startswith(self.terminal_prompt):
                color = (122, 216, 125)
            elif line.startswith("["):
                color = (159, 212, 242)
            else:
                color = (122, 216, 125)
            self._blit_text(
                surface,
                self.mono_font,
                self._fit_text_to_width(self.mono_font, line, terminal.w - 34),
                (terminal.x + 20, terminal.y + 52 + index * 36),
                color,
            )

        panel = pygame.Rect(748, 108, 426, 244)
        panel_shadow = panel.move(6, 8)
        pygame.draw.rect(surface, (17, 26, 35), panel_shadow, border_radius=8)
        pygame.draw.rect(surface, (19, 31, 43), panel, border_radius=8)
        pygame.draw.rect(surface, (68, 105, 142), panel, 1, border_radius=8)
        pygame.draw.rect(surface, (35, 58, 82), (panel.x, panel.y, panel.w, 38), border_radius=8)
        pygame.draw.rect(surface, (35, 58, 82), (panel.x, panel.y + 30, panel.w, 8))
        pygame.draw.rect(surface, (88, 162, 198), (panel.x + 14, panel.y + 56, panel.w - 28, 28), border_radius=14)
        self._blit_text(surface, self.small_font, "Signal Processor", (panel.x + 12, panel.y + 10), (237, 242, 247))
        self._blit_text(surface, self.small_font, "filter stream aligned", (panel.x + 26, panel.y + 63), (16, 39, 54))

        self._blit_text(surface, self.small_font, "Decoded narrative:", (panel.x + 16, panel.y + 102), (198, 216, 232))
        decoded_lines = self._channel_visible("decoded").split("\n")[-3:]
        for index, line in enumerate(decoded_lines):
            self._blit_text(
                surface,
                self.tiny_font,
                line if line else "...",
                (panel.x + 16, panel.y + 128 + index * 22),
                (178, 201, 220),
            )

        self._blit_wrapped_text(
            surface,
            self.small_font,
            "Status: entropy stream reduced to readable warning text.",
            pygame.Rect(panel.x + 16, panel.y + 194, panel.w - 32, 40),
            (198, 216, 232),
            max_lines=2,
        )

        if self.stage >= 1:
            self._draw_scanlines(surface)

    def _draw_email_alert(self, surface: pygame.Surface) -> None:
        width, _ = surface.get_size()
        alert = pygame.Rect(width - 404, 62, 372, 176)
        alert_shadow = alert.move(6, 8)
        pygame.draw.rect(surface, (13, 22, 36), alert_shadow, border_radius=8)
        pygame.draw.rect(surface, (242, 247, 255), alert, border_radius=8)
        pygame.draw.rect(surface, (74, 105, 158), (alert.x, alert.y, alert.w, 34), border_radius=8)
        pygame.draw.rect(surface, (74, 105, 158), (alert.x, alert.y + 26, alert.w, 8))
        pygame.draw.circle(surface, (224, 235, 249), (alert.x + 28, alert.y + 84), 18)
        pygame.draw.circle(surface, (84, 118, 176), (alert.x + 28, alert.y + 84), 11)

        self._blit_text(surface, self.small_font, "Email Alert", (alert.x + 12, alert.y + 8), (239, 246, 255))
        self._blit_text(surface, self.body_font, "1 New Message", (alert.x + 56, alert.y + 48), (20, 30, 44))
        self._blit_wrapped_text(
            surface,
            self.small_font,
            self._channel_visible("alert") or "Subject: ...",
            pygame.Rect(alert.x + 56, alert.y + 74, 170, 38),
            (42, 55, 72),
            max_lines=2,
        )
        self._blit_wrapped_text(
            surface,
            self.small_font,
            "Priority: review message before relay state changes again",
            pygame.Rect(alert.x + 14, alert.y + 116, 214, 36),
            (42, 55, 72),
            max_lines=2,
        )

        open_button = pygame.Rect(alert.x + 242, alert.y + 132, 112, 30)
        hot_strength = min(1.0, self.input_activity + self.button_flash_timer * 1.4)
        hot = hot_strength > 0.1
        button_fill = (
            int(84 + 22 * hot_strength),
            int(132 + 18 * hot_strength),
            int(204 + 22 * hot_strength),
        )
        button_border = (200, 226, 255) if hot else (141, 183, 242)
        pygame.draw.rect(surface, button_fill, open_button, border_radius=6)
        pygame.draw.rect(surface, button_border, open_button, 2, border_radius=6)
        self._blit_text(surface, self.small_font, "Open Mail", (open_button.x + 18, open_button.y + 7), (236, 246, 255))

    def _draw_email_window(self, surface: pygame.Surface) -> None:
        width, height = surface.get_size()
        mail = pygame.Rect(width // 2 - 432, height // 2 - 216, 864, 432)
        mail_shadow = mail.move(8, 10)
        pygame.draw.rect(surface, (13, 18, 24), mail_shadow, border_radius=10)
        pygame.draw.rect(surface, (247, 248, 251), mail, border_radius=10)
        pygame.draw.rect(surface, (229, 233, 240), (mail.x, mail.y, mail.w, 48), border_radius=10)
        pygame.draw.rect(surface, (229, 233, 240), (mail.x, mail.y + 35, mail.w, 13))
        pygame.draw.circle(surface, (227, 101, 92), (mail.x + 20, mail.y + 24), 5)
        pygame.draw.circle(surface, (233, 188, 84), (mail.x + 36, mail.y + 24), 5)
        pygame.draw.circle(surface, (117, 197, 111), (mail.x + 52, mail.y + 24), 5)

        self._blit_text(surface, self.small_font, "Inbox", (mail.x + 76, mail.y + 15), (39, 48, 59))

        gmail_chip = pygame.Rect(mail.x + 88, mail.y + 11, 78, 26)
        aol_chip = pygame.Rect(mail.x + 173, mail.y + 11, 63, 26)
        pygame.draw.rect(surface, (213, 226, 252), gmail_chip, border_radius=13)
        pygame.draw.rect(surface, (221, 232, 242), aol_chip, border_radius=13)
        self._blit_text(surface, self.small_font, "Gmail", (gmail_chip.x + 16, gmail_chip.y + 5), (26, 39, 56))
        self._blit_text(surface, self.small_font, "AOL", (aol_chip.x + 15, aol_chip.y + 5), (26, 39, 56))

        sidebar = pygame.Rect(mail.x + 14, mail.y + 56, 176, 360)
        pygame.draw.rect(surface, (240, 243, 248), sidebar, border_radius=7)
        self._blit_text(surface, self.small_font, "Folders", (sidebar.x + 12, sidebar.y + 12), (59, 72, 88))
        folder_rows = ["Inbox", "Alerts", "Starred", "Drafts", "Spam", "Trash"]
        for index, row in enumerate(folder_rows):
            color = (26, 44, 66) if row == "Alerts" else (77, 94, 114)
            prefix = "> " if row == "Alerts" else "  "
            if row == "Alerts" and self.input_activity > 0.06:
                pulse_width = int(6 + self.input_activity * 18)
                pygame.draw.rect(
                    surface,
                    (220, 234, 252),
                    (sidebar.x + 8, sidebar.y + 40 + index * 28, pulse_width, 19),
                    border_radius=4,
                )
            self._blit_text(
                surface,
                self.small_font,
                f"{prefix}{row}",
                (sidebar.x + 12, sidebar.y + 44 + index * 28),
                color,
            )

        content = pygame.Rect(mail.x + 204, mail.y + 56, 646, 360)
        pygame.draw.rect(surface, (252, 253, 255), content, border_radius=7)

        self._blit_text(
            surface,
            self.body_font,
            "From: unknown@shadowmail.net",
            (content.x + 20, content.y + 16),
            (54, 68, 83),
        )
        self._blit_text(
            surface,
            self.body_font,
            "To: parrot@kidgame",
            (content.x + 20, content.y + 44),
            (54, 68, 83),
        )
        pygame.draw.line(
            surface,
            (220, 227, 236),
            (content.x + 20, content.y + 74),
            (content.x + content.w - 20, content.y + 74),
            1,
        )

        email_lines = self._channel_visible("email").split("\n")
        body_y = content.y + 98
        for line in email_lines[:5]:
            color = (141, 27, 32) if "BREACH" in line else (33, 42, 56)
            font = self.subhead_font if "BREACH" in line else self.body_font
            body_y = self._blit_wrapped_text(
                surface,
                font,
                line,
                pygame.Rect(content.x + 20, body_y, content.w - 40, 72),
                color,
                max_lines=2,
            ) + 10

        self._blit_wrapped_text(
            surface,
            self.small_font,
            "Mailbox status: suspicious local relay activity.",
            pygame.Rect(content.x + 20, content.y + 312, content.w - 40, 34),
            (72, 89, 109),
            max_lines=2,
        )

    def _draw_malware_popup(self, surface: pygame.Surface) -> None:
        width, height = surface.get_size()
        jitter_amplitude = int(self.shake_timer * 7 + min(3.0, self.typing_wpm / 65.0))
        if self.stage >= 3:
            jitter_amplitude += int(self.shake_timer * 5 + min(3.0, self.typing_wpm / 60.0))
        jitter = 0
        if jitter_amplitude > 0:
            jitter = int(math.sin(pygame.time.get_ticks() * 0.07) * jitter_amplitude)
        popup = pygame.Rect(width // 2 - 268 + jitter, height // 2 - 144, 536, 288)
        popup_shadow = popup.move(9, 11)
        pygame.draw.rect(surface, (22, 8, 8), popup_shadow, border_radius=10)
        pygame.draw.rect(surface, (252, 242, 242), popup, border_radius=9)
        pygame.draw.rect(surface, (142, 24, 24), popup, 3, border_radius=9)
        for stripe_index in range(6):
            stripe_x = popup.x + 164 + stripe_index * 38
            pygame.draw.line(surface, (239, 206, 114), (stripe_x, popup.y + 40), (stripe_x + 22, popup.y + 18), 3)

        header = pygame.Rect(popup.x, popup.y, popup.w, 38)
        pygame.draw.rect(surface, (167, 26, 26), header, border_radius=9)
        pygame.draw.rect(surface, (167, 26, 26), (header.x, header.y + 28, header.w, 10))
        self._blit_text(surface, self.small_font, "malware.exe", (popup.x + 12, popup.y + 10), (255, 236, 236))

        face_center = (popup.x + 95, popup.y + 142)
        pygame.draw.circle(surface, (255, 242, 228), face_center, 44)
        pygame.draw.circle(surface, (29, 29, 29), (face_center[0] - 15, face_center[1] - 8), 5)
        pygame.draw.circle(surface, (29, 29, 29), (face_center[0] + 15, face_center[1] - 8), 5)
        pygame.draw.circle(surface, (200, 38, 38), (face_center[0], face_center[1] + 6), 8)
        pygame.draw.arc(surface, (29, 29, 29), (face_center[0] - 19, face_center[1] + 10, 38, 26), 0.2, 2.9, 3)
        pygame.draw.circle(surface, (214, 12, 12), (face_center[0], face_center[1] - 49), 18)

        malware_lines = self._channel_visible("malware").split("\n")
        for index, line in enumerate(malware_lines):
            if not line:
                continue
            color = (125, 22, 22) if index == 0 else (44, 30, 30)
            font = self.subhead_font if index == 0 else self.body_font
            self._blit_text(surface, font, line, (popup.x + 170, popup.y + 86 + index * 42), color)

        self._blit_text(
            surface,
            self.small_font,
            self._fit_text_to_width(
                self.small_font,
                "Session unstable. Unauthorized activity is still active on this host.",
                popup.w - 52,
            ),
            (popup.x + 26, popup.y + 228),
            (76, 52, 52),
        )
        self._blit_text(
            surface,
            self.small_font,
            "Capture source: loopback relay mirror",
            (popup.x + 26, popup.y + 250),
            (76, 52, 52),
        )

    def _draw_live_alerts(self, surface: pygame.Surface) -> None:
        if not self.live_alerts:
            return

        width, _ = surface.get_size()
        for index, alert in enumerate(self.live_alerts[-2:]):
            box = pygame.Rect(width - 432, 428 + index * 86, 402, 76)
            alpha_scale = max(0.18, min(1.0, alert["timer"] / self.live_alert_lifetime))
            fill = (
                int(28 + self.input_activity * 24),
                int(30 + self.input_activity * 20),
                int(38 + self.input_activity * 18),
            )
            pygame.draw.rect(surface, fill, box, border_radius=8)
            pygame.draw.rect(surface, (98, 128, 166), box, 1, border_radius=8)

            self._blit_text(
                surface,
                self.small_font,
                alert["title"],
                (box.x + 12, box.y + 8),
                (234, 242, 251),
            )
            self._blit_text(
                surface,
                self.small_font,
                self._fit_text_to_width(self.small_font, alert["title"], box.w - 24),
                (box.x + 12, box.y + 8),
                (234, 242, 251),
            )
            self._blit_wrapped_text(
                surface,
                self.small_font,
                alert["body"],
                pygame.Rect(box.x + 12, box.y + 30, box.w - 24, 28),
                (192, 212, 230),
                max_lines=2,
            )

            bar_width = int((box.w - 16) * alpha_scale)
            pygame.draw.rect(
                surface,
                (126, 174, 218),
                (box.x + 8, box.y + box.h - 7, bar_width, 3),
                border_radius=1,
            )

    def _draw_toasts(self, surface: pygame.Surface) -> None:
        if not self.toast_events:
            return

        width, _ = surface.get_size()
        recent = self.toast_events[-3:]
        for index, toast in enumerate(recent):
            toast_rect = pygame.Rect(width - 404, 236 + index * 62, 374, 54)
            pygame.draw.rect(surface, (26, 35, 48), toast_rect, border_radius=8)
            pygame.draw.rect(surface, (84, 115, 152), toast_rect, 1, border_radius=8)
            self._blit_wrapped_text(
                surface,
                self.small_font,
                toast["text"],
                pygame.Rect(toast_rect.x + 12, toast_rect.y + 8, toast_rect.w - 24, 32),
                (218, 231, 244),
                max_lines=2,
            )
            progress = max(0.0, min(1.0, toast["timer"] / self.toast_lifetime))
            bar_width = int((toast_rect.w - 16) * progress)
            pygame.draw.rect(
                surface,
                (110, 167, 208),
                (toast_rect.x + 8, toast_rect.y + toast_rect.h - 8, bar_width, 4),
                border_radius=2,
            )

    def _draw_cursor(self, surface: pygame.Surface) -> None:
        cx = int(self.cursor_pos[0])
        cy = int(self.cursor_pos[1])
        points = [
            (cx, cy),
            (cx, cy + 24),
            (cx + 7, cy + 18),
            (cx + 13, cy + 30),
            (cx + 17, cy + 28),
            (cx + 11, cy + 16),
            (cx + 24, cy + 16),
        ]
        pygame.draw.polygon(surface, (241, 245, 250), points)
        pygame.draw.polygon(surface, (22, 27, 34), points, 1)

        if self.cursor_click_timer > 0:
            ripple = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            ring_radius = int(8 + (1.0 - min(1.0, self.cursor_click_timer)) * 14)
            alpha = int(170 * min(1.0, self.cursor_click_timer))
            pygame.draw.circle(ripple, (175, 220, 255, alpha), (cx + 8, cy + 8), ring_radius, 2)
            surface.blit(ripple, (0, 0))

    def _draw_scanlines(self, surface: pygame.Surface) -> None:
        width, height = surface.get_size()
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        intensity = int((2 if self.stage >= 1 else 0) + self.input_activity * 30 + self.shake_timer * 26)
        intensity = min(24, intensity)
        if intensity <= 1:
            return
        spacing = 4 if self.typing_wpm < 72 else 3
        for y_pos in range(0, height, spacing):
            overlay.fill((12, 15, 19, intensity), (0, y_pos, width, 1))
        surface.blit(overlay, (0, 0))

    @staticmethod
    def _clock_label() -> str:
        seconds = pygame.time.get_ticks() // 1000
        minute = 3 + (seconds // 10) % 57
        second = seconds % 60
        return f"Thu 21:{minute:02d}:{second:02d}"

    @staticmethod
    def _blit_text(
        surface: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        position: tuple[int, int],
        color: tuple[int, int, int],
    ) -> None:
        rendered = font.render(text, True, color)
        surface.blit(rendered, position)

    @staticmethod
    def _fit_text_to_width(font: pygame.font.Font, text: str, max_width: int) -> str:
        if font.size(text)[0] <= max_width:
            return text
        trimmed = text
        while trimmed and font.size(f"{trimmed}...")[0] > max_width:
            trimmed = trimmed[:-1]
        return f"{trimmed}..." if trimmed else "..."

    def _blit_wrapped_text(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        rect: pygame.Rect,
        color: tuple[int, int, int],
        line_spacing: int = 4,
        max_lines: int | None = None,
    ) -> int:
        y_pos = rect.y
        lines_drawn = 0
        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            words = paragraph.split()
            if not words:
                y_pos += font.get_height() + line_spacing
                continue

            current = words[0]
            for word in words[1:]:
                trial = f"{current} {word}"
                if font.size(trial)[0] <= rect.w:
                    current = trial
                else:
                    if max_lines is not None and lines_drawn >= max_lines:
                        return y_pos
                    surface.blit(font.render(current, True, color), (rect.x, y_pos))
                    y_pos += font.get_height() + line_spacing
                    lines_drawn += 1
                    current = word

            if max_lines is not None and lines_drawn >= max_lines:
                return y_pos
            line_text = current
            if max_lines is not None and lines_drawn == max_lines - 1:
                line_text = self._fit_text_to_width(font, current, rect.w)
            surface.blit(font.render(line_text, True, color), (rect.x, y_pos))
            y_pos += font.get_height() + line_spacing
            lines_drawn += 1

            if max_lines is not None and lines_drawn >= max_lines:
                return y_pos

        return y_pos
