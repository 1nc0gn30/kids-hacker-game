from __future__ import annotations

import math
from dataclasses import dataclass

from ursina import (
    AmbientLight,
    Button,
    Entity,
    Sky,
    Text,
    Ursina,
    Vec3,
    camera,
    color,
    curve,
    destroy,
    held_keys,
    invoke,
    time,
    window,
)


@dataclass
class Objective:
    title: str
    prompt: str
    detail: str
    action: str
    success: str


class DroneController(Entity):
    def __init__(self) -> None:
        super().__init__(model="cube", color=color.azure, scale=(0.7, 0.25, 1.1), position=(0, 0.5, -7))
        self.speed = 4.8
        self.bounds_x = 4.5
        self.bounds_z = (-15.5, -2.5)
        self.bob_phase = 0.0
        self.pulse = 0.0
        self.core = Entity(parent=self, model="sphere", color=color.cyan, scale=0.6, y=0.1)
        self.shadow = Entity(parent=self, model="quad", scale=(1.4, 0.6), rotation_x=90, y=-0.22, color=color.rgba(20, 30, 40, 120))

    def update(self) -> None:
        move_x = held_keys["d"] - held_keys["a"] + held_keys["right arrow"] - held_keys["left arrow"]
        move_z = held_keys["w"] - held_keys["s"] + held_keys["up arrow"] - held_keys["down arrow"]
        self.x = max(-self.bounds_x, min(self.bounds_x, self.x + move_x * time.dt * self.speed))
        self.z = max(self.bounds_z[0], min(self.bounds_z[1], self.z + move_z * time.dt * self.speed))
        self.bob_phase += time.dt * (2.2 + abs(move_x) * 0.8 + abs(move_z) * 0.8)
        self.y = 0.5 + math.sin(self.bob_phase) * 0.06
        self.rotation_z = -move_x * 8
        self.rotation_x = move_z * 4
        self.pulse = max(0.0, self.pulse - time.dt * 2.0)
        glow = 180 + int(60 * self.pulse)
        self.core.color = color.rgba(90, glow, 255, 255)

    def boost(self) -> None:
        self.pulse = 1.0


class LoopbackRaid3D:
    def __init__(self) -> None:
        self.app = Ursina(borderless=False, development_mode=False)
        window.title = "KidGame3 - Scene 2 3D Raid"
        window.color = color.rgb(6, 10, 18)
        window.exit_button.visible = False
        window.fps_counter.enabled = False

        camera.position = (0, 7.5, -23)
        camera.rotation_x = 16
        camera.fov = 70

        Sky(color=color.rgb(6, 12, 20))
        AmbientLight(color=color.rgba(180, 200, 255, 0.7))

        self.objectives = [
            Objective(
                title="Lock the relay filter",
                prompt="Fly to the blue filter gate and press 2.",
                detail="Only the SMTP+TLS filter reveals the fake-local relay.",
                action="2",
                success="Correct filter locked in. The attack corridor is now visible.",
            ),
            Objective(
                title="Collect the mirrored packet",
                prompt="Fly through the packet shard and press E to scan it.",
                detail="The shard contains the mirrored warning payload.",
                action="e",
                success="Packet shard scanned. MIRROR signature confirmed.",
            ),
            Objective(
                title="Quarantine the hostile relay",
                prompt="Move into the red quarantine ring and press Q.",
                detail="Retrying the connection is too dangerous.",
                action="q",
                success="Relay quarantined. Hostile traffic is losing momentum.",
            ),
            Objective(
                title="Upload the route map",
                prompt="Dock at the command uplink and press R to upload the route.",
                detail="This finalizes the path for the next scene.",
                action="r",
                success="Route map uploaded. Scene 2 complete.",
            ),
        ]
        self.current_objective = 0
        self.status_text = "Launch into the breach tunnel and follow the mission prompts."
        self.feedback_text = ""
        self.feedback_until = 0.0
        self.completed = False

        self.drone = DroneController()
        self.progress_bar = Entity(parent=camera.ui, model="quad", color=color.azure, scale=(0.0, 0.03), origin=(-0.5, 0), position=(-0.42, -0.46))
        Entity(parent=camera.ui, model="quad", color=color.rgba(255, 255, 255, 35), scale=(0.84, 0.036), position=(0, -0.46))
        self.title_text = Text(parent=camera.ui, text="Loopback Tunnel Raid", position=(-0.86, 0.44), scale=1.4, color=color.azure)
        self.objective_text = Text(parent=camera.ui, text="", position=(-0.86, 0.34), origin=(0, 0), scale=0.98)
        self.detail_text = Text(parent=camera.ui, text="", position=(-0.86, 0.24), origin=(0, 0), scale=0.82, color=color.light_gray)
        self.status_ui = Text(parent=camera.ui, text=self.status_text, position=(-0.86, -0.39), origin=(0, 0), scale=0.85, color=color.rgb(210, 228, 255))
        self.feedback_ui = Text(parent=camera.ui, text="", position=(-0.2, 0.44), origin=(0, 0), scale=1.0, color=color.yellow)
        self.control_text = Text(
            parent=camera.ui,
            text="Move: WASD / Arrows   |   Interact: 2, E, Q, R   |   Esc: Quit",
            position=(-0.3, -0.46),
            scale=0.75,
            color=color.rgba(200, 220, 255, 200),
        )

        self.filter_gate = self._make_gate(position=(-3.8, 0.8, -4.8), tint=color.azure, label="FILTER 2")
        self.packet_shard = self._make_packet(position=(0.0, 1.3, -8.5))
        self.quarantine_ring = self._make_ring(position=(2.8, 0.15, -11.9), tint=color.red, label="QUARANTINE")
        self.uplink_pad = self._make_uplink(position=(0.0, 0.15, -14.8))
        self.finish_button = Button(parent=camera.ui, text="Close Scene", scale=(0.16, 0.06), position=(0.74, -0.42), color=color.rgb(46, 72, 112), visible=False)
        self.finish_button.on_click = self.app.userExit

        self.tunnel_segments = []
        self._build_tunnel()
        self._sync_ui()
        self.app.update = self.update
        self.app.input = self.input

    def _build_tunnel(self) -> None:
        for index in range(14):
            z_pos = -2 - index * 1.15
            ring = Entity(model="torus", scale=(8.5, 8.5, 0.18), position=(0, 2.4, z_pos), rotation_x=90, color=color.rgba(60, 120 + index * 6, 220, 90))
            self.tunnel_segments.append(ring)
            Entity(model="cube", scale=(10.5, 0.1, 1.0), position=(0, -0.05, z_pos), color=color.rgb(12, 20 + index * 2, 30 + index * 4))
            Entity(model="cube", scale=(0.12, 4.6, 1.0), position=(-5.2, 2.2, z_pos), color=color.rgb(20, 35, 48))
            Entity(model="cube", scale=(0.12, 4.6, 1.0), position=(5.2, 2.2, z_pos), color=color.rgb(20, 35, 48))

    def _make_gate(self, position: tuple[float, float, float], tint, label: str) -> Entity:
        gate = Entity(position=position)
        Entity(parent=gate, model="cube", scale=(1.6, 2.4, 0.2), color=tint)
        Text(parent=gate, text=label, y=1.35, billboard=True, scale=6, color=color.white)
        return gate

    def _make_packet(self, position: tuple[float, float, float]) -> Entity:
        shard = Entity(position=position)
        for angle in (0, 45, 90):
            Entity(parent=shard, model="cube", scale=(0.22, 1.4, 0.22), rotation_z=angle, color=color.cyan)
        Text(parent=shard, text="PACKET", y=1.1, billboard=True, scale=5, color=color.rgb(210, 250, 255))
        return shard

    def _make_ring(self, position: tuple[float, float, float], tint, label: str) -> Entity:
        ring = Entity(position=position)
        Entity(parent=ring, model="torus", scale=(2.4, 2.4, 0.18), rotation_x=90, color=tint)
        Text(parent=ring, text=label, y=1.1, billboard=True, scale=5, color=color.white)
        return ring

    def _make_uplink(self, position: tuple[float, float, float]) -> Entity:
        uplink = Entity(position=position)
        Entity(parent=uplink, model="cylinder", scale=(1.7, 0.28, 1.7), color=color.rgb(80, 170, 255))
        Entity(parent=uplink, model="sphere", y=1.25, scale=0.6, color=color.rgb(180, 230, 255))
        Text(parent=uplink, text="UPLINK", y=1.9, billboard=True, scale=5, color=color.white)
        return uplink

    def _distance_to(self, entity: Entity) -> float:
        return (self.drone.world_position - entity.world_position).length()

    def _objective_progress(self) -> float:
        return self.current_objective / len(self.objectives)

    def _set_feedback(self, message: str, tint=color.yellow) -> None:
        self.feedback_text = message
        self.feedback_ui.text = message
        self.feedback_ui.color = tint
        self.feedback_until = time.time() + 1.8

    def _sync_ui(self) -> None:
        objective = self.objectives[min(self.current_objective, len(self.objectives) - 1)]
        self.objective_text.text = f"Objective: {objective.title}\n{objective.prompt}"
        self.detail_text.text = objective.detail
        self.status_ui.text = self.status_text
        self.progress_bar.scale_x = 0.84 * self._objective_progress()

    def _complete_objective(self) -> None:
        objective = self.objectives[self.current_objective]
        self.status_text = objective.success
        self._set_feedback(objective.success, color.lime)
        self.drone.boost()
        self.current_objective += 1
        if self.current_objective >= len(self.objectives):
            self.completed = True
            self.objective_text.text = "Objective: Tunnel cleared\nYou mapped the loopback route and secured the relay."
            self.detail_text.text = "Press the button to close Scene 2 and return to the terminal."
            self.progress_bar.scale_x = 0.84
            self.finish_button.visible = True
            self.status_ui.text = self.status_text
            return
        self._sync_ui()

    def update(self) -> None:
        self.drone.update()
        now = time.time()
        if self.feedback_ui.text and now > self.feedback_until:
            self.feedback_ui.text = ""

        self.packet_shard.rotation_y += 36 * time.dt
        self.filter_gate.rotation_y += 12 * time.dt
        self.quarantine_ring.rotation_z += 20 * time.dt
        self.uplink_pad.rotation_y += 14 * time.dt
        for index, ring in enumerate(self.tunnel_segments):
            ring.rotation_z += (6 + index * 0.5) * time.dt

        camera.x = self.drone.x * 0.16
        camera.z = -23 + self.drone.z * 0.05

    def input(self, key: str) -> None:
        if key == "escape":
            self.app.userExit()
            return
        if self.completed:
            return

        objective = self.objectives[self.current_objective]
        if key != objective.action:
            return

        targets = [self.filter_gate, self.packet_shard, self.quarantine_ring, self.uplink_pad]
        target = targets[self.current_objective]
        if self._distance_to(target) > 2.2:
            self._set_feedback("Get closer to the active objective marker first.", color.orange)
            self.status_text = "Fly into the highlighted objective zone before interacting."
            self._sync_ui()
            return

        self._complete_objective()

    def run(self) -> None:
        self.app.run()


def run_scene() -> None:
    LoopbackRaid3D().run()


if __name__ == "__main__":
    run_scene()
