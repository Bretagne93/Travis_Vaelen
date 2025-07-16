import sys
import os
import random

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
            "Half-empty bag of sour diesel",
            "Bag of deer jerky",
        ]
        self.flags = {}
        self.flags["travis_stats"] = {
            "flex": 2,
            "flirt": 3,
            "yeehaw": 1,
        }
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
        print("Pit Viper sunglasses and a mustache so nice, it's your mom's favorite ride.")
        print(
            "A flamingo tattoo on his right bicep with the words \u201cSaeva Venia\u201d inked beneath it"
        )
        print("A lat spread so glorious, Macho Man sheds a single tear in Valhalla and whispers, 'Ohhh yeahhh.'")
        

    trailer = Scene(
        "trailer",
        (
            "Travis jolts awake in his sacred single-wide, air thick with mosquito fog and last night\u2019s regret. "
            "The walls are paper-thin, adorned with gator jawbones, fan-blown NASCAR posters, and a deer skull "
            "wearing a camo trucker hat that reads 'Freedom Ain't Free.'\n\n"
            "The floor creaks under his boots as he steps past a tipped-over beer can pyramid and the Dude's rug "
            "stained with bong water and maybe something unholy. A shrine of jars filled with sharks teeth rests beneath "
            "a faded Polaroid of him and Saeva\u2014her lipstick smudged on his cheek, his eyes full of feral devotion.\n\n"
            "A folded note lies on the counter, held down by a bottle of hot sauce and a shell casing.\n\n"
            "Outside, the swamp buzzes like a live wire. Travis\u2019s Toyota glows red in the morning sun, jacked and ready, "
            "but almost outta gas.\n\n"
            "A gator sunbathes on the bank, eyeing him like a potential snack."
        ),
        {
            "step outside": "dirt_road",
            "leave": "dirt_road",
            "look in fridge": lambda state: print(
                "The fridge hums like a dying possum. Inside: 2 hot dogs, 1 bottle of Bud, a jar of pickled eggs, "
                "and an enormous joint in a butter dish labeled 'emergency.'"
            ),
            "read note": lambda state: print(
    "The note is written in eyeliner on a crumpled Taco Bell napkin. It reads:\n\n"
    "\"Memorial Day. Ginnie Springs. Bring the ducky float, the doobies, and that sinful tongue. I’ll be waiting.\"\n\n"
    "- Saeva"
),

            "look in mirror": look_in_mirror,
            "inventory": show_inventory,
        },
    )

    dirt_road = Scene(
        "dirt_road",
        (
            "The road outside is nothing but sun-baked mud and palmettos leading back toward civilization. "
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
                "gap-toothed fella stacks cigarettes and blunts with a grin."
            )
            state.flags["visited_gas_station"] = True

    def buy_jerky(state):
        print("Travis tosses a few crumpled bills on the counter for some Moon Pies.")
        state.inventory.append("Moon Pies")

    def talk_cashier(state):
        if not state.flags.get("heard_shortcut"):
            print(
                "The cashier leans in close, whisperin' about a dirt trail that'll "
                "get you to Ginnie Springs quicker than a gator on ice skates."
            )
            state.flags["heard_shortcut"] = True
        else:
            print("The cashier just nods, his secret already spilled.")

    def lot_lizard_fight(state):
        print(
            "A raspy giggle echoes through the aisles as a woman in leopard print leggings and a crop top that says 'Daddy\u2019s Lil Toe Sucker' slinks into view.\n"
            "Her nails click like acrylic claws on the chip rack.\n"
            "The Lot Lizard is here."
        )

        boss_hp = 3
        travis_hp = 3
        stats = state.flags["travis_stats"]

        while boss_hp > 0 and travis_hp > 0:
            print("\nWhat\u2019s your move?")
            print("- flex (STR)")
            print("- flirt (CHA)")
            print("- yeehaw (WTF)")
            move = input(">").strip().lower()

            if move not in ("flex", "flirt", "yeehaw"):
                print("Travis just stands there scratchin\u2019 his ass. That ain\u2019t a move.")
                continue

            roll = random.randint(1, 20)
            mod = stats.get(move, 0)
            total = roll + mod

            print(f"You rolled a {roll} + {mod} = {total}!")

            if total >= 12:
                print("Direct hit! Lot Lizard hisses, knocking over a Mountain Dew display as she stumbles.")
                boss_hp -= 1
            else:
                print("She licks her thumb and touches your forehead. You feel *unholy.*")
                travis_hp -= 1

        if boss_hp <= 0:
            print("\nWith a final shriek, she flees through the automatic doors, leaving behind a trail of fake lashes and shame.")
            print("You find a gas can and a snack cooler where she once stood.")
            state.inventory.append("Gas Can")
            state.inventory.append("Cooler of Snacks")
            state.flags["beat_lizard"] = True
            state.move_to("gas_station_after_lizard")
        else:
            print("\nTravis drops to one knee, overwhelmed by the sheer chaotic thirst.")
            print("He needs to regroup before tryin' that again.")
            state.move_to("dirt_road")

    gas_station = Scene(
        "gas_station",
        (
            "The air inside the Fill-'Er-Up is thick with burnt coffee and years of nicotine. "
            "Lotto tickets peel off the counter like dying leaves.\n"
            "A wall of expired jerky dares you to bite. Something shifts near the energy drink fridge…"
        ),
        {
            "approach snacks": lambda state: lot_lizard_fight(state),
            "inventory": show_inventory,
            "leave": "dirt_road",
        },
        on_enter=gas_station_enter,
    )

    gas_station_after_lizard = Scene(
        "gas_station_after_lizard",
        (
            "The gas station is quiet now. The cashier peeks over the counter, impressed.\n"
            '"Shortcut to Ginnie? Dirt trail past the old bait shop. Only Malus ever drove it faster."\n'
            "You feel his gaze in the gator jerky aisle."
        ),
        {
            "talk to cashier": talk_cashier,
            "go to walmart": "walmart",
            "leave": "dirt_road",
            "inventory": show_inventory,
        },
    )

    def walmart_enter(state):
        if not state.flags.get("beat_meth_zombies"):
            print(
                "The parking lot is cracked and steaming. Weed smoke and meth vapor hang in the air like chemical fog."
            )
            print(
                "Discarded carts roll on their own. The entrance is barricaded with pallets."
            )
            print('Travis adjusts his Pit Vipers. "Time to chomp or be chomped."')
            print('A zombified greeter shuffles up: "Welcome to Hellmart. No returns. No mercy."')
        else:
            print(
                "The lot is littered with twitching corpses. A ranger waits by the opened barricade, tipping his hat."
            )

    def meth_zombie_fight(state):
        stats = state.flags["travis_stats"]
        travis_hp = 3
        for wave in range(1, 4):
            zombie_hp = 2
            print(f"\nWave {wave}! A meth zombie lurches from the smoke.")
            while zombie_hp > 0 and travis_hp > 0:
                print("\nWhat's your move?")
                print("- flex (STR)")
                print("- flirt (CHA)")
                print("- yeehaw (WTF)")
                move = input("> ").strip().lower()

                if move not in ("flex", "flirt", "yeehaw"):
                    print("Travis just stares through the haze. That ain't a move.")
                    continue

                roll = random.randint(1, 20)
                mod = stats.get(move, 0)
                total = roll + mod

                print(f"You rolled a {roll} + {mod} = {total}!")

                if total >= 12:
                    print(
                        random.choice(
                            [
                                "Zombie staggers back, dropping a half-smoked Marlboro.",
                                "You knock the fiend into a cart return with a wet crunch.",
                                "It screeches and reels, smacking into a broken Prius.",
                            ]
                        )
                    )
                    zombie_hp -= 1
                else:
                    print(
                        random.choice(
                            [
                                "Y'ain't got no teeth, you ain't got no power!",
                                "Where's ma baby?! Where's MA BABY?!",
                                "Y'all ever drank Baylees from a shoe?",
                            ]
                        )
                    )
                    travis_hp -= 1

            if travis_hp <= 0:
                print("\nTravis collapses under a pile of twitching bodies and crawls back to the road.")
                state.move_to("dirt_road")
                return
            else:
                print("The zombie crumples to the asphalt.")

        print("\nAll three zombies lie motionless.")
        print("Inside the store, Travis finds a Rubber duck floaty and a cheetah print fanny pack.")
        state.inventory.append("Rubber duck floaty")
        state.inventory.append("Cheetah print fanny pack")
        print("Travis does the Gator Chomp to celebrate.")
        print('A park ranger approaches: "You that boy what saved them folks durin\u2019 Hurricane Andrew. Go on. Ginnie\'s waitin\'."')
        state.flags["beat_meth_zombies"] = True
        state.move_to("walmart_after_zombies")

    walmart = Scene(
        "walmart",
        "A smoking Walmart parking lot full of rolling carts and chaos.",
        {
            "fight zombies": meth_zombie_fight,
            "leave": "dirt_road",
            "inventory": show_inventory,
        },
        on_enter=walmart_enter,
    )

    walmart_after_zombies = Scene(
        "walmart_after_zombies",
        "The barricade is open and the ranger waits to guide you toward the springs.",
        {
            "go to springs": "ginnie_springs",
            "head to ginnie": "ginnie_springs",
            "inventory": show_inventory,
            "leave": "dirt_road",
        },
        on_enter=walmart_enter,
    )

    def mud_hole_enter(state):
        if not state.flags.get("visited_mud_hole"):
            print(
                "Travis steps into the Mud Hole. A sun-scorched pit of beer cans, flip-flops, and lost dignity.\n"
                "The air is thick with humidity and gnat swarms. A busted boombox plays Kid Rock on loop, its battery held in with duct tape."
            )
            state.flags["visited_mud_hole"] = True


    def mole_cricket_fight(state):
        print(
            "Out from the passenger seat of a jacked up truck crawls the Mole Cricket, her eyes bloodshot and wild.\n"
            "She wears cut-off overalls, a bikini top, and Crocs covered in mud. A blunt the size of a kielbasa dangles from her lips."
        )
        print(
            "\n\"Wanna hit this, sugar?\" she purrs, exhaling a cloud so thick it makes the cicadas cough."
        )

        stats = state.flags["travis_stats"]
        boss_hp = 5
        travis_hp = 3
        bogged = False

        while boss_hp > 0 and travis_hp > 0:
            if bogged:
                print("\nTravis is disoriented from that righteous rip and loses this turn!")
                bogged = False
                travis_hp -= 1
                print("He coughs violently.\n\"Is you the police!?\" Mole Cricket shrieks.")
            else:
                print("\nWhat’s your move?")
                print("- flex (STR)")
                print("- flirt (CHA)")
                print("- yeehaw (WTF)")
                move = input("> ").strip().lower()

                if move not in ("flex", "flirt", "yeehaw"):
                    print("Travis hesitates. The Mole Cricket narrows her eyes. That ain't no move.")
                    continue

                roll = random.randint(1, 20)
                mod = stats.get(move, 0)
                total = roll + mod

                print(f"You rolled a {roll} + {mod} = {total}!")

                if total >= 14:
                    print("Boom! Mole Cricket stumbles backward into a kiddie pool full of Natty Light cans.")
                    boss_hp -= 1
                elif total >= 8:
                    print("You land a glancing blow, but she shrugs it off with a giggle and another rip.")
                else:
                    print("She exhales a monstrous bong rip right into your face. You've been BOGGED!")
                    bogged = True

        if boss_hp <= 0:
            print(
                "\nWith a dramatic flop, she falls onto a deflated pool float."
            )
            print("\"Alright alright, you earned it...\" she wheezes, tossing Travis a crusty Crown Royal bag.")
            print("Inside: the *Bag of Doobies*.")
            state.inventory.append("Bag of Doobies")
            state.flags["beat_mole_cricket"] = True
            state.move_to("town")
        else:
            print("\nTravis stumbles away, hacking and humiliated. He'll need to come back stronger.")
            state.move_to("dirt_road")

print(
    "Travis grabs the Bag of Doobies and hears tires screech in the distance. "
    "A voice echoes from a megaphone:\n\n"
    "\"TRAVIS VAELEN, STEP AWAY FROM THE STASH AND PUT YOUR HANDS WHERE I CAN SEE 'EM!\"\n"
)

print(
    "Sheriff Clovis appears, less man than legal liability, careening through the palmettos with righteous rage. "
    "Travis vaults a beer cooler, flips the bird, and sprints toward the Toyota.\n"
)

print(
    "With a roar of the engine and a cloud of vape smoke, Travis hauls ass down the dirt road. "
    "Sirens wail. A possum screams. A Bible page flies through the air.\n"
)

print(
    "He jerks the wheel hard right, catching a ditch ramp and *airborne Yeehaws* his way outta sight.\n"
)

print(
    "The cruiser crashes into a port-a-john. Blue goo sprays everywhere.\n"
    "Clovis emerges, dripping and furious: \"DAMN IT, VAELEN! THIS AIN'T OVER!\"\n"
)

print(
    "Minutes later, Travis strolls into the strip club parking lot like he didn’t just reenact all of *Smokey and the Bandit*."
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
        "I'M NOT GUNNA LIE",
        "I'LL NOT BE A GENTLEMAN",
        "BEHIND THE BOATHOUSE",
        "I'LL SHOW YOU MY DARK SECRET",
        "MAKE UP YOUR MIND",
        "AND I'LL PROMISE YOU",
        "I WILL TREAT YOU WELL",
        "MY SWEET ANGEL",
        "SO HELP ME JESUS",
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
            "go to ginnie springs": "ginnie_springs",
        },
    )

    ginnie_throne_desc = (
        "Travis reaches the base of a massive cypress tree draped in Spanish moss. "
        "Saeva Venia is trapped at the top, held hostage by a stinking, muscular cryptid: the Skunk Ape.\n"
        "The air reeks of sweat, cologne, and Mountain Dew.\n"
        "The Skunk Ape grunts and shows off his \"swamp bride\" to the frogs."
    )

    def look_around_ginnie(state):
        print(ginnie_throne_desc)

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
                "Saeva isn't here yet, but the Skunk Ape scampers off, leaving a trail straight toward Ginnie Springs."
            )
            state.move_to("ginnie_springs")
        else:
            print(
                "The Skunk Ape roars and beats his chest with swamp-soaked confidence."
            )
            print("You ain\u2019t ready for this fight, son.")

    ginnie_throne = Scene(
        "ginnie_throne",
        ginnie_throne_desc,
        {
            "fight": fight_skunk_ape,
            "look around": look_around_ginnie,
            "inventory": show_inventory,
        },
    )

    ginnie_springs_desc = (
        "Travis steps to the edge of Ginnie Springs, the water glistening under the moon. "
        "A bloated shadow rises from the depths—a seductive, unhinged Water Bug ready to strike."
    )


    def water_bug_fight(state):
        print("The Water Bug sways from the shallows, wings dripping. She eyes Travis with filthy intent.")
        boss_hp = 4
        travis_hp = 3
        stats = state.flags["travis_stats"]
        confused = 0
        while boss_hp > 1 and travis_hp > 0:
            if confused:
                print("\nTravis is woozy from the Toxic Twerk! -2 to his next move.")
            print("\nWhat's your move?")
            print("- flex (STR)")
            print("- flirt (CHA)")
            print("- yeehaw (WTF)")
            move = input("> ").strip().lower()
            if move not in ("flex", "flirt", "yeehaw"):
                print("Travis fumbles, unsure what that even was.")
                continue
            roll = random.randint(1, 20)
            mod = stats.get(move, 0)
            if confused:
                mod -= 2
                confused = 0
            total = roll + mod
            print(f"You rolled a {roll} + {mod} = {total}!")
            if total >= 13:
                print("Direct hit! Water Bug screeches, slime flying.")
                boss_hp -= 1
            else:
                if random.random() < 0.5:
                    print("She unleashes a Toxic Twerk, rattling the swamp!")
                    confused = 1
                else:
                    print("She slaps Travis with a slick limb.")
                    travis_hp -= 1
        if travis_hp <= 0:
            print("Travis tumbles into the spring, choking on defeat. He'll have to regroup back at the road.")
            state.move_to("dirt_road")
            return
        water_bug_cutscene(state)

    ginnie_springs = Scene(
        "ginnie_springs",
        ginnie_springs_desc,
        {
            "fight": water_bug_fight,
            "look around": lambda state: print(ginnie_springs_desc),
            "inventory": show_inventory,
        },
    )

    return {
        scene.name: scene
        for scene in [
            trailer,
            dirt_road,
            gas_station,
            gas_station_after_lizard,
            mud_hole,
            strip_club,
            mole_cricket_showdown,
            stage_backroom,
            club_exit,
            walmart,
            walmart_after_zombies,
            ginnie_throne,
            ginnie_springs,
        ]
    }


def water_bug_cutscene(state):
    print("\nSaeva Venia bursts from the treeline. \"Don’t touch my man, BITCH!\"")
    print("With a devastating judo kick, she yeets the Water Bug into the woods.")
    print("The Skunk Ape lumbers out, catching the bug mid-air before disappearing into the swamp.")
    print("The skies clear and the cicadas sing. Travis is stunned.")
    print("\nTravis and Saeva spark up some doobies from their stash.")
    print("Floating down the river on the Rubber Duck and Flamingo floaties, they snack on gas station goodies.")
    print('Saeva whispers, "Took you long enough, swamp god."')

    print("\n🌊💋  THE END – Together Forever, Memorial Day 2025 💋🌊\n")
    print("=== CREDITS ===")
    print("Code, Chaos & Carnage: You & Codex")
    print("Lead Character: Travis Vaelen, Florida's Swamp God")
    print("Boss Fights & Bad Bitches: Lot Lizard, Mole Cricket, Water Bug")
    print("Final Boss Assist: Saeva Venia (Certified Menace)")
    print("Special Thanks: The State of Florida, Pit Viper™, and You")

    while True:
        choice = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if choice in ("yes", "y"):
            os.execv(sys.executable, [sys.executable] + sys.argv)
        elif choice in ("no", "n"):
            print("Later, gator. May the river always carry you home.")
            sys.exit(0)
        else:
            print("Didn’t catch that, swamp cowboy. Type 'yes' or 'no'.")


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
