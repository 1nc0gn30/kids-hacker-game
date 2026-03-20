from .scene01_desktop_breach import Section1Scene1DesktopBreach
from .scene02_loopback_capture import Section1Scene2LoopbackCapture

PLANNED_SCENE_COUNT = 10


def create_scenes():
    return [Section1Scene1DesktopBreach(), Section1Scene2LoopbackCapture()]
