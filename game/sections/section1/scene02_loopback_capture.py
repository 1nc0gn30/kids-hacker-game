import math
import string

import pygame


class Section1Scene2LoopbackCapture:
    name = "Section 1 / Scene 2 - Loopback Capture Review"
    ALLOWED_KEYS = string.ascii_lowercase + string.digits + "-_/.:"

    def __init__(self) -> None:
        self.is_complete = False
        self.keys_seen = 0
        self.keys_needed = 36
        self.input_activity = 0.0
        self.wave_phase = 0.0
        self.visible_rows = 3
        self.status_line = "Capture loaded. Type to reconstruct the loopback flow."

        self.capture_rows = [
            ("21:14:07.110", "127.0.0.1:40214", "127.0.0.1:587", "SMTP", "EHLO desktop.local"),
            ("21:14:07.348", "127.0.0.1:587", "127.0.0.1:40214", "SMTP", "250-STARTTLS relay-ready"),
            ("21:14:08.021", "127.0.0.1:40214", "127.0.0.1:443", "TLS", "Client Hello SNI=void-gateway"),
            ("21:14:08.406", "127.0.0.1:443", "127.0.0.1:40214", "TLS", "Server Hello certificate mismatch"),
            ("21:14:09.004", "127.0.0.1:40214", "127.0.0.1:587", "SMTP", "AUTH probe failed relay policy"),
            ("21:14:09.552", "127.0.0.1:587", "127.0.0.1:40214", "SMTP", "warning payload mirrored to inbox"),
        ]

        self.title_font = pygame.font.SysFont("dejavusans", 34, bold=True)
        self.subhead_font = pygame.font.SysFont("dejavusans", 22, bold=True)
        self.body_font = pygame.font.SysFont("dejavusans", 18)
        self.small_font = pygame.font.SysFont("dejavusans", 16)
        self.tiny_font = pygame.font.SysFont("dejavusansmono", 14)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN or not event.unicode:
            return

        key_char = event.unicode.lower()
        if len(key_char) != 1 or key_char not in self.ALLOWED_KEYS:
            return

        self.keys_seen += 1
        self.input_activity = min(1.0, self.input_activity + 0.14)
        self.visible_rows = min(len(self.capture_rows), 3 + self.keys_seen // 5)

        if self.keys_seen >= 12:
            self.status_line = "Flow reconstruction in progress. Hidden relay path is stabilizing."
        if self.keys_seen >= 24:
            self.status_line = "Warning confirmed: the local mail relay is behaving like an external host."
        if self.keys_seen >= self.keys_needed:
            self.is_complete = True
            self.status_line = "Capture review complete. Loopback route mapped for the next scene."

    def update(self, delta_seconds: float) -> None:
        self.input_activity = max(0.0, self.input_activity - delta_seconds * 0.65)
        self.wave_phase += delta_seconds * (1.2 + self.input_activity * 4.0)

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
            "Triage the packet trail left by the mirrored warning email.",
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

        for index, row in enumerate(self.capture_rows[: self.visible_rows]):
            row_y = table_rect.y + 54 + index * 54
            if index % 2 == 0:
                pygame.draw.rect(surface, (244, 248, 252), (table_rect.x + 8, row_y - 6, table_rect.w - 16, 42), border_radius=6)
            time_text, source, destination, proto, info = row
            self._blit_text(surface, self.tiny_font, time_text, (table_rect.x + 14, row_y), (67, 82, 98))
            self._blit_text(surface, self.tiny_font, source, (table_rect.x + 138, row_y), (37, 49, 64))
            self._blit_text(surface, self.tiny_font, destination, (table_rect.x + 328, row_y), (37, 49, 64))
            self._blit_text(surface, self.tiny_font, proto, (table_rect.x + 548, row_y), (73, 99, 136))
            self._blit_text(surface, self.tiny_font, info, (table_rect.x + 644, row_y), (37, 49, 64))

        side_rect = pygame.Rect(panel.x + 930, panel.y + 124, 236, 414)
        pygame.draw.rect(surface, (21, 30, 40), side_rect, border_radius=8)
        pygame.draw.rect(surface, (72, 100, 132), side_rect, 1, border_radius=8)
        self._blit_text(surface, self.small_font, "System Load", (side_rect.x + 14, side_rect.y + 14), (224, 234, 244))

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

        self._blit_text(surface, self.small_font, f"Keys processed: {self.keys_seen}/{self.keys_needed}", (side_rect.x + 14, side_rect.y + 194), (208, 223, 238))
        self._blit_text(surface, self.small_font, f"Packets visible: {self.visible_rows}/{len(self.capture_rows)}", (side_rect.x + 14, side_rect.y + 224), (208, 223, 238))
        self._blit_text(surface, self.small_font, "Typing raises capture detail and system pressure.", (side_rect.x + 14, side_rect.y + 266), (155, 190, 216))

        footer = pygame.Rect(panel.x + 18, panel.y + panel.h - 52, panel.w - 36, 34)
        pygame.draw.rect(surface, (224, 232, 241), footer, border_radius=6)
        self._blit_text(
            surface,
            self.small_font,
            "Interface: lo  |  Display filter: tcp.port == 587 or tcp.port == 443  |  Status: packet triage active",
            (footer.x + 12, footer.y + 9),
            (58, 76, 98),
        )

        self._blit_text(surface, self.small_font, self.status_line, (54, 646), (202, 220, 236))

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
