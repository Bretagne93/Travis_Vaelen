class Scene:
    """A single location in the game world."""

    def __init__(self, name, description, choices, on_enter=None):
        self.name = name
        self.description = description
        # mapping of command -> next scene name or callable
        self.choices = choices
        # optional function called when the scene is entered
        self.on_enter = on_enter or (lambda state: None)

    def perform_action(self, command, state):
        """Run an action for the given command if available."""
        if command in self.choices:
            action = self.choices[command]
            if callable(action):
                result = action(state)
            else:
                result = action
            return True, result
        return False, None


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
        # run the starting scene's enter hook
        self.current_scene.on_enter(self)

    def move_to(self, scene_name):
        self.current_scene = self.scenes[scene_name]
        self.current_scene.on_enter(self)


def create_scenes():
    """Build all scenes and their behaviors."""

    def show_inventory(state):
        print("Travis checks his pockets:")
        for item in state.inventory:
            print(f"- {item}")

    def dirt_road_enter(state):
        if not state.flags.get("saw_gator"):
            print(
                "A mysterious gator crawls from the ditch, gives Travis a wink, "
                "and coughs up a shiny tooth before disappearing back into the mud."
            )
            state.flags["saw_gator"] = True
            state.flags["tooth_on_ground"] = True

    def pick_up_tooth(state):
        if state.flags.get("tooth_on_ground"):
            print(
                "Travis snatches the Mysterious Gator Tooth. Probably cursed, "
                "definitely awesome."
            )
            state.inventory.append("Mysterious Gator Tooth")
            state.flags["tooth_on_ground"] = False
        else:
            print("There ain't no tooth lyin' around here.")

    def look_in_mirror(state):
        print("A golden mullet, gleaming like sunrise on the Suwannee")
        print("Pit Viper sunglasses and a mustache sharp enough to slice jerky")
        print(
            "A flamingo tattoo on his right bicep with the words \u201cSaeva Venia\u201d inked beneath it"
        )
        print("A lat spread so glorious, it was carved by ancient fanboat spirits")

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
            "inventory": show_inventory,
            "look in mirror": look_in_mirror,
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
            "pick up tooth": pick_up_tooth,
            "inventory": show_inventory,
            "go to gas station": "gas_station",
        },
        on_enter=dirt_road_enter,
    )

    def gas_station_enter(state):
        if not state.flags.get("visited_gas_station"):
            print(
                "Travis pushes open the smeared glass door of the Fill-'Er-Up. The "
                "air reeks of burnt coffee and diesel fumes. Behind the counter, a "
                "gap-toothed fella hawks lotto tickets and gator jerky with a grin."
            )
            state.flags["visited_gas_station"] = True

    def buy_jerky(state):
        print("Travis tosses a few crumpled bills on the counter for some Slim Jims.")
        state.inventory.append("Slim Jims")

    def talk_cashier(state):
        if not state.flags.get("heard_shortcut"):
            print(
                "The cashier leans in close, whisperin' about a dirt trail that'll "
                "get you to Ginnie Springs quicker than a gator on ice skates."
            )
            state.flags["heard_shortcut"] = True
        else:
            print("The cashier just nods, his secret already spilled.")

    gas_station = Scene(
        "gas_station",
        (
            "Dusty aisles of the local gas station stretch before Travis, lit by "
            "flickering fluorescent tubes."
        ),
        {
            "buy jerky": buy_jerky,
            "talk to cashier": talk_cashier,
            "leave": "dirt_road",
            "inventory": show_inventory,
        },
        on_enter=gas_station_enter,
    )

    return {scene.name: scene for scene in [trailer, dirt_road, gas_station]}


def main():
    scenes = create_scenes()
    state = GameState(scenes, "trailer")

    print("Type 'quit' to leave the swamp.")
    while True:
        scene = state.current_scene
        print(f"\n=== {scene.name.upper()} ===")
        print(scene.description)
        print("What now? You can:")
        for cmd in scene.choices:
            print(f"- {cmd}")
        choice = input("What now? ").strip().lower()

        if choice == "quit":
            print("Even swamp gods need their beauty rest. Later, gator!")
            break

        handled, next_scene = scene.perform_action(choice, state)
        if not handled:
            print("Travis scratches his head, wonderin' what that even means.")
        elif next_scene:
            state.move_to(next_scene)


if __name__ == "__main__":
    main()
