import subprocess
import sys

import pygame

from game.sections import load_section

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
SCENE_TRANSITION_DURATION = 1.0


def launch_scene2_3d() -> None:
    subprocess.run([sys.executable, '-m', 'game.sections.section1.scene02_loopback_3d'], check=False)


def draw_completion_banner(surface: pygame.Surface, font: pygame.font.Font) -> None:
    width, height = surface.get_size()
    banner_rect = pygame.Rect(0, height - 42, width, 42)
    pygame.draw.rect(surface, (17, 20, 24), banner_rect)
    pygame.draw.line(surface, (74, 96, 125), (0, height - 42), (width, height - 42), 2)
    text = font.render(
        "Latest built scene complete. More Section 1 scenes are still in progress.",
        True,
        (188, 234, 193),
    )
    surface.blit(text, (14, height - 30))


def _ease_out_cubic(value: float) -> float:
    return 1.0 - pow(1.0 - value, 3)


def draw_scene_transition(
    surface: pygame.Surface,
    from_scene: pygame.Surface,
    to_scene: pygame.Surface,
    progress: float,
    title_font: pygame.font.Font,
    body_font: pygame.font.Font,
    next_scene_name: str,
) -> None:
    width, height = surface.get_size()
    eased = _ease_out_cubic(progress)

    surface.blit(from_scene, (0, 0))

    fade_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    fade_overlay.fill((4, 8, 14, int(160 * eased)))
    surface.blit(fade_overlay, (0, 0))

    incoming = to_scene.copy()
    incoming.set_alpha(int(255 * min(1.0, max(0.0, (progress - 0.12) / 0.88))))
    incoming_y = int((1.0 - eased) * 70)
    surface.blit(incoming, (0, incoming_y))

    bands = pygame.Surface((width, height), pygame.SRCALPHA)
    for index in range(6):
        band_y = int(height * (progress * 0.85 + index * 0.16)) - 120
        pygame.draw.rect(bands, (78, 168, 248, 18), (0, band_y, width, 18))
    surface.blit(bands, (0, 0))

    sweep_x = int(width * eased)
    pygame.draw.rect(surface, (170, 224, 255), (max(0, sweep_x - 4), 0, 8, height))

    panel = pygame.Rect(width // 2 - 280, height // 2 - 70, 560, 140)
    panel_surface = pygame.Surface((panel.w, panel.h), pygame.SRCALPHA)
    panel_surface.fill((8, 14, 20, 205))
    surface.blit(panel_surface, panel.topleft)
    pygame.draw.rect(surface, (94, 152, 212), panel, 1, border_radius=10)
    pygame.draw.rect(
        surface,
        (94, 152, 212),
        (panel.x + 18, panel.y + panel.h - 18, int((panel.w - 36) * eased), 4),
        border_radius=2,
    )

    title = title_font.render("SYNCING NEXT SCENE", True, (229, 240, 249))
    subtitle = body_font.render(next_scene_name, True, (153, 194, 228))
    caption = body_font.render("Loopback capture interface coming online", True, (193, 218, 238))
    surface.blit(title, (panel.x + 24, panel.y + 22))
    surface.blit(subtitle, (panel.x + 24, panel.y + 60))
    surface.blit(caption, (panel.x + 24, panel.y + 92))


def main() -> None:
    pygame.init()
    pygame.display.set_caption("KidGame3 - Section 1")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    ui_font = pygame.font.SysFont("dejavusans", 20)
    transition_font = pygame.font.SysFont("dejavusansmono", 24, bold=True)

    scenes = load_section(1)
    scene_index = 0
    running = True
    transition_timer = 0.0
    transition_from_index = 0
    transition_to_index = 0

    while running:
        delta_seconds = clock.tick(FPS) / 1000.0
        active_scene = scenes[scene_index]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif transition_timer <= 0.0:
                active_scene.handle_event(event)

        if transition_timer > 0.0:
            transition_timer = max(0.0, transition_timer - delta_seconds)
            from_scene = scenes[transition_from_index]
            to_scene = scenes[transition_to_index]
            to_scene.update(delta_seconds)

            from_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            to_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            from_scene.render(from_surface)
            to_scene.render(to_surface)

            progress = 1.0 - (transition_timer / SCENE_TRANSITION_DURATION)
            draw_scene_transition(
                screen,
                from_surface,
                to_surface,
                progress,
                transition_font,
                ui_font,
                to_scene.name,
            )

            if transition_timer <= 0.0:
                scene_index = transition_to_index

            pygame.display.flip()
            continue

        active_scene.update(delta_seconds)

        if active_scene.is_complete and scene_index == 0 and len(scenes) > 1:
            pygame.quit()
            launch_scene2_3d()
            return

        if active_scene.is_complete and scene_index < len(scenes) - 1:
            transition_from_index = scene_index
            transition_to_index = scene_index + 1
            transition_timer = SCENE_TRANSITION_DURATION

        active_scene.render(screen)

        if scene_index == len(scenes) - 1 and active_scene.is_complete:
            draw_completion_banner(screen, ui_font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
