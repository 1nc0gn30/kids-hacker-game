import math
import string

import pygame


class Section1Scene2LoopbackCapture:
    name = "Section 1 / Scene 2 - Loopback Capture Review"
    ALLOWED_KEYS = string.ascii_lowercase + string.digits + "-_/.:"

    def __init__(self) -> None:
        self.is_complete = False
        self.keys_seen = 0
        self.input_activity = 0.0
        self.wave_phase = 0.0
        self.visible_rows = 3
        self.status_line = "Capture loaded. Follow the analyst prompts to reconstruct the loopback flow."
        self.feedback_timer = 0.0
        self.feedback_tone = "info"
        self.feedback_text = ""
        self.last_action = "Awaiting analyst input"
        self.progress_ratio = 0.0
        self.scan_sweep = 0.0
        self.packet_focus = 0
        self.evidence_flash = 0.0

        self.capture_rows = [
            ("21:14:07.110", "127.0.0.1:40214", "127.0.0.1:587", "SMTP", "EHLO desktop.local"),
            ("21:14:07.348", "127.0.0.1:587", "127.0.0.1:40214", "SMTP", "250-STARTTLS relay-ready"),
            ("21:14:08.021", "127.0.0.1:40214", "127.0.0.1:443", "TLS", "Client Hello SNI=void-gateway"),
            ("21:14:08.406", "127.0.0.1:443", "127.0.0.1:40214", "TLS", "Server Hello certificate mismatch"),
            ("21:14:09.004", "127.0.0.1:40214", "127.0.0.1:587", "SMTP", "AUTH probe failed relay policy"),
            ("21:14:09.552", "127.0.0.1:587", "127.0.0.1:40214", "SMTP", "warning payload mirrored to inbox"),
        ]

        self.sequence_steps = [
            {
                "title": "Choose the best display filter",
                "instruction": "Press 1, 2, or 3 to lock the filter onto the suspicious relay path.",
                "detail": "2 is the strongest lead because it watches SMTP and TLS together.",
                "kind": "choice",
                "options": [
                    "1  http.port == 80",
                    "2  tcp.port == 587 or tcp.port == 443",
                    "3  udp.port == 53",
                ],
                "correct": "2",
                "success": "Filter locked onto the mirrored mail relay.",
                "failure": "That filter misses the suspicious relay traffic.",
                "rows_visible": 4,
                "focus_row": 1,
            },
            {
                "title": "Decode the anomaly label",
                "instruction": "Type MIRROR to mark the warning payload as a mirrored local attack.",
                "detail": "The payload is looping through localhost while pretending to be external.",
                "kind": "token",
                "token": "mirror",
                "success": "Mirrored payload signature confirmed.",
                "failure": "Keep typing the anomaly label exactly as prompted.",
                "rows_visible": 5,
                "focus_row": 5,
            },
            {
                "title": "Decide the response lane",
                "instruction": "Press Q to quarantine the relay before the route mutates again.",
                "detail": "Quarantine is safer than retrying the suspicious host.",
                "kind": "choice",
                "options": [
                    "Q  Quarantine relay",
                    "R  Retry handshake",
                    "I  Ignore warning",
                ],
                "correct": "q",
                "success": "Relay quarantine requested.",
                "failure": "Unsafe response. Contain the relay instead.",
                "rows_visible": 6,
                "focus_row": 4,
            },
            {
                "title": "Write the route summary",
                "instruction": "Type MAP to finalize the loopback route for the next scene.",
                "detail": "A short action word finishes the packet review cleanly.",
                "kind": "token",
                "token": "map",
                "success": "Route summary exported for incident response.",
                "failure": "Finish the report with the requested action word.",
                "rows_visible": 6,
                "focus_row": 2,
            },
        ]
        self.current_step_index = 0
        self.current_prompt_progress = ""
        self.completed_steps = 0
        self.correct_actions = 0

        self.title_font = pygame.font.SysFont("dejavusans", 34, bold=True)
        self.subhead_font = pygame.font.SysFont("dejavusans", 22, bold=True)
        self.body_font = pygame.font.SysFont("dejavusans", 18)
        self.small_font = pygame.font.SysFont("dejavusans", 16)
        self.tiny_font = pygame.font.SysFont("dejavusansmono", 14)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN or not event.unicode or self.is_complete:
            return

        key_char = event.unicode.lower()
        if len(key_char) != 1 or key_char not in self.ALLOWED_KEYS:
            return

        self.keys_seen += 1
        self.input_activity = min(1.0, self.input_activity + 0.14)
        self.scan_sweep = min(1.0, self.scan_sweep + 0.18)

        active_step = self.sequence_steps[self.current_step_index]
        if active_step["kind"] == "choice":
            self._handle_choice_step(key_char, active_step)
        else:
            self._handle_token_step(key_char, active_step)

    def update(self, delta_seconds: float) -> None:
        self.input_activity = max(0.0, self.input_activity - delta_seconds * 0.65)
        self.wave_phase += delta_seconds * (1.2 + self.input_activity * 4.0)
        self.feedback_timer = max(0.0, self.feedback_timer - delta_seconds)
        self.evidence_flash = max(0.0, self.evidence_flash - delta_seconds * 1.8)
        self.scan_sweep = max(0.0, self.scan_sweep - delta_seconds * 0.2)

    def render(self, surface: pygame.Surface) -> None:
        width, height = surface.get_size()

        surface.fill((16, 24, 34))
        pygame.draw.rect(surface, (10, 16, 24), (0, 0, width, height // 2))
        pygame.draw.circle(surface, (26, 52, 78), (width - 140, 110), 220)
        pygame.draw.circle(surface, (18, 38, 54), (210, height - 30), 280)

        self._blit_text(surface, self.title_font, "Loopback Capture Review", (52, 30), (226, 237, 248))
        self._blit_text(
            surface,
            self.small_font,
            "Play through the packet triage steps instead of free-typing to advance.",
            (54, 72),
            (151, 186, 214),
        )

        panel = pygame.Rect(48, 100, 1184, 520)
        shadow = panel.move(10, 12)
        pygame.draw.rect(surface, (8, 12, 18), shadow, border_radius=12)
        pygame.draw.rect(surface, (232, 239, 246), panel, border_radius=12)
        pygame.draw.rect(surface, (41, 63, 88), (panel.x, panel.y, panel.w, 42), border_radius=12)
        pygame.draw.rect(surface, (41, 63, 88), (panel.x, panel.y + 30, panel.w, 12))
        self._blit_text(
            surface,
            self.small_font,
            "Capture Window - tshark follow stream on lo",
            (panel.x + 14, panel.y + 12),
            (234, 242, 249),
        )

        warning_rect = pygame.Rect(panel.x + 18, panel.y + 58, panel.w - 36, 48)
        pygame.draw.rect(surface, (250, 241, 221), warning_rect, border_radius=8)
        pygame.draw.rect(surface, (194, 146, 44), warning_rect, 1, border_radius=8)
        self._blit_text(
            surface,
            self.small_font,
            "Warning: the local mail relay is answering like an external host.",
            (warning_rect.x + 14, warning_rect.y + 15),
            (106, 72, 14),
        )

        table_rect = pygame.Rect(panel.x + 18, panel.y + 124, 892, 414)
        pygame.draw.rect(surface, (248, 251, 254), table_rect, border_radius=8)
        pygame.draw.rect(surface, (214, 223, 234), table_rect, 1, border_radius=8)

        headers = [("Time", 14), ("Source", 138), ("Destination", 328), ("Proto", 548), ("Info", 644)]
        for label, x_pos in headers:
            self._blit_text(surface, self.small_font, label, (table_rect.x + x_pos, table_rect.y + 14), (73, 88, 106))

        pygame.draw.line(surface, (218, 226, 236), (table_rect.x + 12, table_rect.y + 42), (table_rect.x + table_rect.w - 12, table_rect.y + 42), 1)

        current_step = self.sequence_steps[self.current_step_index]
        focus_row = current_step["focus_row"]
        for index, row in enumerate(self.capture_rows[: self.visible_rows], start=1):
            row_y = table_rect.y + 54 + (index - 1) * 54
            if index % 2 == 1:
                pygame.draw.rect(surface, (244, 248, 252), (table_rect.x + 8, row_y - 6, table_rect.w - 16, 42), border_radius=6)
            if index == focus_row:
                pulse = int(18 * (0.5 + 0.5 * math.sin(self.wave_phase * 4.0)))
                highlight = (255, 236 - pulse // 3, 186)
                pygame.draw.rect(surface, highlight, (table_rect.x + 8, row_y - 6, table_rect.w - 16, 42), 2, border_radius=6)
            time_text, source, destination, proto, info = row
            self._blit_text(surface, self.tiny_font, time_text, (table_rect.x + 14, row_y), (67, 82, 98))
            self._blit_text(surface, self.tiny_font, source, (table_rect.x + 138, row_y), (37, 49, 64))
            self._blit_text(surface, self.tiny_font, destination, (table_rect.x + 328, row_y), (37, 49, 64))
            self._blit_text(surface, self.tiny_font, proto, (table_rect.x + 548, row_y), (73, 99, 136))
            self._blit_text(surface, self.tiny_font, info, (table_rect.x + 644, row_y), (37, 49, 64))

        side_rect = pygame.Rect(panel.x + 930, panel.y + 124, 236, 414)
        pygame.draw.rect(surface, (21, 30, 40), side_rect, border_radius=8)
        pygame.draw.rect(surface, (72, 100, 132), side_rect, 1, border_radius=8)
        self._blit_text(surface, self.small_font, "Analyst Console", (side_rect.x + 14, side_rect.y + 14), (224, 234, 244))

        graph_rect = pygame.Rect(side_rect.x + 14, side_rect.y + 48, side_rect.w - 28, 124)
        pygame.draw.rect(surface, (12, 18, 25), graph_rect, border_radius=6)
        pygame.draw.rect(surface, (53, 74, 100), graph_rect, 1, border_radius=6)

        points = []
        for x_pos in range(graph_rect.w):
            wave = math.sin(self.wave_phase * 2.1 + x_pos * 0.08) * (10 + self.input_activity * 24)
            baseline = graph_rect.y + graph_rect.h // 2
            points.append((graph_rect.x + x_pos, int(baseline + wave)))
        if len(points) > 1:
            pygame.draw.lines(surface, (117, 205, 168), False, points, 2)

        sweep_x = graph_rect.x + int((graph_rect.w - 8) * min(1.0, self.scan_sweep))
        pygame.draw.rect(surface, (195, 235, 255), (sweep_x, graph_rect.y + 8, 8, graph_rect.h - 16), border_radius=3)

        self._blit_text(surface, self.small_font, f"Stage: {self.current_step_index + 1}/{len(self.sequence_steps)}", (side_rect.x + 14, side_rect.y + 194), (208, 223, 238))
        self._blit_text(surface, self.small_font, f"Correct actions: {self.correct_actions}", (side_rect.x + 14, side_rect.y + 224), (208, 223, 238))
        self._blit_text(surface, self.small_font, self._fit_text_to_width(self.small_font, self.last_action, side_rect.w - 28), (side_rect.x + 14, side_rect.y + 254), (155, 190, 216))

        progress_box = pygame.Rect(side_rect.x + 14, side_rect.y + 294, side_rect.w - 28, 94)
        pygame.draw.rect(surface, (13, 21, 29), progress_box, border_radius=8)
        pygame.draw.rect(surface, (65, 91, 120), progress_box, 1, border_radius=8)
        self._blit_text(surface, self.small_font, "Prompt Progress", (progress_box.x + 12, progress_box.y + 10), (225, 235, 245))
        typed_text = self.current_prompt_progress.upper() or "..."
        target_text = current_step.get("token", current_step.get("correct", "")).upper()
        self._blit_text(surface, self.tiny_font, f"typed  {typed_text}", (progress_box.x + 12, progress_box.y + 38), (174, 205, 232))
        self._blit_text(surface, self.tiny_font, f"target {target_text}", (progress_box.x + 12, progress_box.y + 60), (174, 205, 232))

        footer = pygame.Rect(panel.x + 18, panel.y + panel.h - 52, panel.w - 36, 34)
        pygame.draw.rect(surface, (224, 232, 241), footer, border_radius=6)
        self._blit_text(
            surface,
            self.small_font,
            "Interface: lo  |  Display filter: tcp.port == 587 or tcp.port == 443  |  Status: guided packet triage active",
            (footer.x + 12, footer.y + 9),
            (58, 76, 98),
        )

        mission_rect = pygame.Rect(48, 636, 1184, 58)
        pygame.draw.rect(surface, (14, 20, 28), mission_rect, border_radius=10)
        pygame.draw.rect(surface, (66, 93, 118), mission_rect, 1, border_radius=10)
        fill_width = int((mission_rect.w - 24) * self.progress_ratio)
        pygame.draw.rect(surface, (91, 175, 231), (mission_rect.x + 12, mission_rect.y + mission_rect.h - 16, fill_width, 8), border_radius=4)
        self._blit_text(surface, self.small_font, self.status_line, (mission_rect.x + 16, mission_rect.y + 10), (202, 220, 236))

        prompt_panel = pygame.Rect(930, 548, 236, 146)
        pygame.draw.rect(surface, (21, 30, 40), prompt_panel, border_radius=8)
        pygame.draw.rect(surface, (72, 100, 132), prompt_panel, 1, border_radius=8)
        self._blit_text(surface, self.small_font, current_step["title"], (prompt_panel.x + 14, prompt_panel.y + 12), (228, 237, 245))
        self._blit_wrapped_text(surface, self.small_font, current_step["instruction"], pygame.Rect(prompt_panel.x + 14, prompt_panel.y + 40, prompt_panel.w - 28, 46), (178, 205, 226), max_lines=3)
        if current_step["kind"] == "choice":
            option_y = prompt_panel.y + 88
            for option in current_step["options"]:
                self._blit_text(surface, self.tiny_font, option, (prompt_panel.x + 14, option_y), (210, 224, 237))
                option_y += 18
        else:
            self._blit_text(surface, self.tiny_font, f"Keyword: {current_step['token'].upper()}", (prompt_panel.x + 14, prompt_panel.y + 102), (210, 224, 237))
            self._blit_text(surface, self.tiny_font, current_step["detail"], (prompt_panel.x + 14, prompt_panel.y + 122), (146, 178, 202))

        if self.feedback_timer > 0:
            self._draw_feedback(surface)

    def _handle_choice_step(self, key_char: str, active_step: dict) -> None:
        self.current_prompt_progress = key_char
        if key_char == active_step["correct"]:
            self.correct_actions += 1
            self._complete_step(active_step["success"])
            return
        if key_char in {"1", "2", "3", "q", "r", "i"}:
            self._set_feedback(active_step["failure"], "warn")
            self.last_action = f"Rejected option: {key_char.upper()}"

    def _handle_token_step(self, key_char: str, active_step: dict) -> None:
        token = active_step["token"]
        candidate = (self.current_prompt_progress + key_char)[-len(token):]
        self.current_prompt_progress = candidate
        self.last_action = f"Building token: {self.current_prompt_progress.upper()}"
        if token.startswith(candidate):
            if candidate == token:
                self.correct_actions += 1
                self._complete_step(active_step["success"])
            return
        self.current_prompt_progress = key_char if token.startswith(key_char) else ""
        self._set_feedback(active_step["failure"], "warn")

    def _complete_step(self, success_text: str) -> None:
        active_step = self.sequence_steps[self.current_step_index]
        self.completed_steps += 1
        self.progress_ratio = self.completed_steps / len(self.sequence_steps)
        self.visible_rows = max(self.visible_rows, active_step["rows_visible"])
        self.packet_focus = active_step["focus_row"]
        self.evidence_flash = 1.0
        self.last_action = success_text
        self.current_prompt_progress = ""
        self._set_feedback(success_text, "ok")

        if self.current_step_index < len(self.sequence_steps) - 1:
            self.current_step_index += 1
            next_step = self.sequence_steps[self.current_step_index]
            self.status_line = f"Step cleared. {next_step['instruction']}"
            self.visible_rows = max(self.visible_rows, next_step["rows_visible"])
        else:
            self.is_complete = True
            self.status_line = "Capture review complete. Loopback route mapped for the next scene."

    def _set_feedback(self, text: str, tone: str) -> None:
        self.feedback_text = text
        self.feedback_tone = tone
        self.feedback_timer = 1.6

    def _draw_feedback(self, surface: pygame.Surface) -> None:
        color = (90, 171, 122) if self.feedback_tone == "ok" else (196, 146, 54)
        box = pygame.Rect(690, 30, 500, 40)
        pygame.draw.rect(surface, (18, 28, 38), box, border_radius=8)
        pygame.draw.rect(surface, color, box, 2, border_radius=8)
        self._blit_text(surface, self.small_font, self._fit_text_to_width(self.small_font, self.feedback_text, box.w - 24), (box.x + 12, box.y + 11), (233, 240, 248))

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
