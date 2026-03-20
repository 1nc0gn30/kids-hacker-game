from .section1 import create_scenes as create_section1_scenes

PLANNED_SECTION_COUNT = 10
PLANNED_SCENES_PER_SECTION = 10


def load_section(section_number: int):
    if section_number == 1:
        return create_section1_scenes()
    raise NotImplementedError(
        f"Section {section_number} is not built yet. Planned total sections: "
        f"{PLANNED_SECTION_COUNT}."
    )

