import sys

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

    def check_truck(state):
        print(
            "Travis slaps the hood of his red Toyota, chipped paint gleaming in the sun.\n"
            "\"Shoot! Truck's outta gas… Better go get some.\"\n"
            "He scratches his jaw, thinks for a beat, then grins.\n"
            "\"I'll grab some jerky for Saeva too. Girl gets real ornery without her protein.\""
        )
        state.flags["checked_truck"] = True

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
            "Travis jolts awake in his sacred single-wide, air thick with mosquito fog and last night\u2019s regret. "
            "The walls are paper-thin, adorned with gator jawbones, fan-blown NASCAR posters, and a deer skull "
            "wearing a camo trucker hat that reads 'Born to Mullet.'\n\n"
            "The floor creaks under his boots as he steps past a tipped-over beer can pyramid and an ancient rug "
            "stained with pork grease and maybe something unholy. A shrine of empty Slim Jim wrappers rests beneath "
            "a faded Polaroid of him and Saeva\u2014her lipstick smudged on his cheek, his eyes full of feral devotion.\n\n"
            "A folded note lies on the counter, held down by a bottle of hot sauce and a shell casing.\n\n"
            "Outside, the swamp buzzes like a live wire. Travis\u2019s Toyota glows red in the morning sun, jacked and ready, "
            "but almost outta gas.\n\n"
            "Somewhere in the ether, his cousin Malus growls with pride.\n"
        ),
        {
            "step outside": "dirt_road",
            "leave": "dirt_road",
            "look in fridge": lambda state: print(
                "The fridge hums like a dying possum. Inside: 2 hot dogs, 1 open Bud Heavy, a jar of expired pickled okra, "
                "and a half-smoked joint in a butter dish labeled 'emergency.'"
            ),
            "read note": lambda state: print(
            "The note is written in lipstick on crumpled receipt paper. It reads:\n\n"
            "\"Memorial Day. Ginnie Springs. Bring the ducky float, the shine, and that sinful tongue. I’ll be waiting.\"\n\n"
            "- Saeva (kiss mark)"
   ),

            "look in mirror": look_in_mirror,
            "inventory": show_inventory,
        },
    )

    dirt_road = Scene(
        "dirt_road",
        (
            "The road outside is nothing but sun-baked mud leading back toward civilization. "
            "Mosquitoes buzz like chainsaws in the air. Travis’s truck squats in the driveway, thirsty."
        ),
        {
            "go back": "trailer",
            "return": "trailer",
            "pick up tooth": pick_up_tooth,
            "inventory": show_inventory,
            "check truck": check_truck,
            "go to gas station": lambda state: (
                "gas_station" if state.flags.get("checked_truck") else print(
                    "Travis ain't about to walk off before checking the truck. Man’s got priorities."
                )
            ),
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
            "go to strip club": "strip_club",
        },
        on_enter=gas_station_enter,
    )

    def mole_cricket_enter(state):
        print(
            "The lights dim and a shadow slinks from the fog machine. Mole Cricket steps into view\u2014mud-slicked thighs, rhinestone flip-flops, daisy dukes from 2008, a bikini top made of fishing net, and a vape cloud that smells like watermelon and shame."
        )
        rounds = 0
        while rounds < 3:
            choice = input("Your move? ").strip().lower()
            if choice in ("flex lat spread", "quote saeva"):
                rounds += 1
            elif choice == "offer jerky":
                rounds += 1
            elif choice in ("run", "say 'who\u2019s dale?'", "say 'who's dale?'", "bite lip"):
                if "Bag of gator jerky" in state.inventory:
                    state.inventory.remove("Bag of gator jerky")
                print("Travis moans her name in his sleep now. Saeva\u2019s gonna be pissed.")
                state.move_to("mole_cricket_showdown")
                return
            else:
                if "Bag of gator jerky" in state.inventory:
                    state.inventory.remove("Bag of gator jerky")
                print("Travis moans her name in his sleep now. Saeva\u2019s gonna be pissed.")
                state.move_to("mole_cricket_showdown")
                return

        print("Mole Cricket snarls: 'You ain\u2019t even worth suckin\u2019 the soul out of.'")
        state.inventory.append("Blood-Slicked Lip Gloss")
        state.flags["beat_mole_cricket"] = True
        state.move_to("stage_backroom")

    def attempt_stage(state):
        if not state.flags.get("beat_mole_cricket"):
            return "mole_cricket_showdown"
        return "stage_backroom"

    strip_club = Scene(
        "strip_club",
        (
            "Neon signs flicker above sticky floors while the bass rattles Travis's ribs. Half-interested dancers twirl as the crowd hollers."
        ),
        {
            "approach stage": attempt_stage,
            "leave": "dirt_road",
            "inventory": show_inventory,
        },
    )

    mole_cricket_showdown = Scene(
        "mole_cricket_showdown",
        "Mole Cricket blocks the path to the stage, eyes glittering with menace.",
        {},
        on_enter=mole_cricket_enter,
    )

    def stage_backroom_intro(state):
        print(
            "The backstage reeks of spilled beer, sweat, and something that might be regret. "
            "Bubba Slim is tuning his bass, dressed in a sleeveless tee that reads ‘WAP = Whiskey And Pickles.’"
        )
        print(
            "Bubba tells Travis he can get the lighter, but only if Travis plays “Possum Kingdom” by the Toadies with the band."
        )
        lyrics = [
            "I'm not gonna lie",
            "I'll not be a gentleman",
            "Behind the boathouse",
            "I'll show you my dark secret"
        ]
        for line in lyrics:
            reply = input(f"{line} ").strip().upper()
            if reply != line:
                print(
                    "Travis hits a sour note. Bubba frowns like a man betrayed by his own blood."
                )
                return
        print(
            "The final chord rings out and Bubba whoops with pride, handing Travis a Zippo lighter with a naked lady on it."
        )
        state.inventory.append("Zippo lighter with a naked lady on it")
        state.move_to("club_exit")

    stage_backroom = Scene(
        "stage_backroom",
        "Heavy curtains close behind Travis as he slips into the backstage haze of cheap perfume and spilled beer.",
        {
            "leave": "strip_club",
            "inventory": show_inventory,
        },
        on_enter=stage_backroom_intro,
    )

    club_exit = Scene(
        "club_exit",
        "With the lighter in hand and the crowd still roaring, Travis steps into the muggy night behind the club.",
        {
            "leave": "dirt_road",
            "inventory": show_inventory,
            "go to cypress tree": "cypress_throne",
        },
    )

    cypress_throne_desc = (
        "Travis reaches the base of a massive cypress tree draped in Spanish moss. "
        "Saeva Venia is trapped at the top, held hostage by a stinking, muscular cryptid: the Skunk Ape.\n"
        "The air reeks of sweat, cologne, and Mountain Dew.\n"
        "The Skunk Ape grunts and shows off his \"swamp bride\" to the frogs."
    )

    def look_around_cypress(state):
        print(cypress_throne_desc)

    def fight_skunk_ape(state):
        has_lighter = any("Zippo lighter" in item for item in state.inventory)
        has_jerky = "Bag of gator jerky" in state.inventory
        has_floaty = "Rubber duck floaty" in state.inventory
        if has_lighter and has_jerky and has_floaty:
            print(
                "Travis cracks his neck, lights the Zippo, and throws gator jerky like a damn grenade."
            )
            print("The Skunk Ape sniffs, distracted.")
            print(
                "With a mighty yell, Travis belly flops off a cypress root, floaty deployed, and dropkicks the horny bastard into the mud."
            )
            print(
                "Saeva leaps into his arms, and they descend like trashy angels from a moss-draped heaven."
            )
            print('"Got my girl, got my floaty, got my shine. Let\u2019s fuckin\u2019 go."')
            import sys
            sys.exit(0)
        else:
            print(
                "The Skunk Ape roars and beats his chest with swamp-soaked confidence."
            )
            print("You ain\u2019t ready for this fight, son.")

    cypress_throne = Scene(
        "cypress_throne",
        cypress_throne_desc,
        {
            "fight": fight_skunk_ape,
            "look around": look_around_cypress,
            "inventory": show_inventory,
        },
    )

    return {
        scene.name: scene
        for scene in [
            trailer,
            dirt_road,
            gas_station,
            strip_club,
            mole_cricket_showdown,
            stage_backroom,
            club_exit,
            cypress_throne,
        ]
    }


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
