class Scene:
    """A single location in the game world."""
    def __init__(self, name, description, choices):
        self.name = name
        self.description = description
        self.choices = choices  # mapping of command -> next scene name


class GameState:
    """Tracks the player's progress."""
    def __init__(self, scenes, start):
        self.scenes = scenes
        self.current_scene = scenes[start]
        self.inventory = [
            "Half-empty flask of 'shine",
            "Bag of gator jerky",
        ]
        self.flags = {}

    def move_to(self, scene_name):
        self.current_scene = self.scenes[scene_name]


def create_scenes():
    trailer = Scene(
        "trailer",
        (
            "Travis jolts awake in his single-wide temple, walls plastered with "
            "gator jaws and NASCAR posters. The swamp hums like a choir of "
            "mosquitoes outside."
        ),
        {
            "step outside": "dirt_road",
            "leave": "dirt_road",
        },
    )

    dirt_road = Scene(
        "dirt_road",
        (
            "The road outside is nothing but sun-baked mud leading back toward "
            "civilization. The air tastes like fried humidity."
        ),
        {
            "go back": "trailer",
            "return": "trailer",
        },
    )

    return {scene.name: scene for scene in [trailer, dirt_road]}


def main():
    scenes = create_scenes()
    state = GameState(scenes, "trailer")

    print("Type 'quit' to leave the swamp.")
    while True:
        scene = state.current_scene
        print(f"\n=== {scene.name.upper()} ===")
        print(scene.description)
        choice = input("What now? ").strip().lower()

        if choice == "quit":
            print("Even swamp gods need their beauty rest. Later, gator!")
            break

        next_scene = scene.choices.get(choice)
        if next_scene:
            state.move_to(next_scene)
        else:
            print("Travis scratches his head, wonderin' what that even means.")


if __name__ == "__main__":
    main()
