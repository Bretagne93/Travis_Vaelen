import sys
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
            "Half-empty flask of 'shine",
            "Bag of gator jerky",
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
                '\"Memorial Day. Ginnie Springs. Bring the ducky float, the shine, and that sinful tongue. I\u2019ll be waiting.\"\n\n'
                "- Saeva \ud83d\udc8b"
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
            "go to mud hole": "mud_hole",
            "leave": "dirt_road",
            "inventory": show_inventory,
        },
    )

    def walmart_enter(state):
        if not state.flags.get("beat_meth_zombies"):
            print("Travis slips through the sliding doors and heads straight for the Halloween aisle.")
            print(
                "Wedged between plastic pumpkins sits the RED-Neckronomicon, bound in denim and reeking of Axe body spray."
            )
            print("When he cracks it open, an unholy banjo chord summons meth zombies from every checkout lane.")
        else:
            print(
                "Stacks of corpses block the clearance racks. A ranger nods respectfully by the exit."
            )

    def meth_zombie_fight(state):
        stats = state.flags["travis_stats"]
        travis_hp = 3
        florida_man_lines = [
            "Florida Man wrestles gator for beer money!",
            "Florida Man drives lawnmower to courthouse on dare!",
            "Florida Man robs Wendy's with live iguana!",
        ]
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
                if move == "yeehaw":
                    print(random.choice(florida_man_lines))

                roll = random.randint(1, 20)
                mod = stats.get(move, 0)
                total = roll + mod

                print(f"You rolled a {roll} + {mod} = {total}!")

                if total >= 12:
                    print(
                        random.choice(
                            [
                                "Zombie slips on a puddle of nacho cheese and faceplants.",
                                "Your strike sends it tumbling into the clearance DVDs.",
                                "The undead cashier explodes in a shower of cheap cologne.",
                            ]
                        )
                    )
                    zombie_hp -= 1
                else:
                    print(
                        random.choice(
                            [
                                "Zombie chomps back, breath reeking of expired Mountain Dew.",
                                "It screeches, 'Cleanup on aisle YOU,' and slashes wildly.",
                                "The fiend spits a tooth and cackles about rollbacks.",
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
        print(
            "Among the scattered limbs Travis grabs a rubber duck floaty, a cheetah-print fanny pack, and a coupon for Slim Jims."
        )
        print("Saeva’s gonna lose her mind when she sees this floaty.")
        state.inventory.append("Rubber duck floaty")
        state.inventory.append("Cheetah-print fanny pack")
        state.inventory.append("Slim Jim coupon")
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
        "The ranger tips his hat, impressed by the carnage. It's time to hit the road before the sirens roll in.",
        {
            "go to springs": "cop_chase",
            "head to ginnie": "cop_chase",
            "inventory": show_inventory,
            "leave": "dirt_road",
        },
        on_enter=walmart_enter,
    )

    cop_chase = Scene(
        "cop_chase",
        "Blue lights flash in the rearview as Travis floors it. Sirens wail just behind the tailgate.",
        {
            "keep running": "ditch_the_cops",
            "floor it": "ditch_the_cops",
            "inventory": show_inventory,
        },
    )

    def ditch_the_cops_enter(state):
        print(
            "Travis spots a dirt mound and punches it. The truck launches like a mud-drenched comet into a nearby field."
        )
        print("Blue lights vanish behind him. Far ahead, neon letters spell out Melrose Hoes.")
        state.move_to("strip_club")

    ditch_the_cops = Scene(
        "ditch_the_cops",
        "The truck lands with a crunch of metal and weeds.",
        {},
        on_enter=ditch_the_cops_enter,
    )

    def mud_hole_enter(state):
        if not state.flags.get("visited_mud_hole"):
            print(
                "Travis steps into the Mud Hole—a sun-scorched pit of beer cans, flip-flops, and lost dignity.\n"
                "The air is thick with weed smoke and gnat swarms. A busted boombox plays Kid Rock on loop, its battery held in with duct tape."
            )
            state.flags["visited_mud_hole"] = True


    def mole_cricket_fight(state):
        print(
            "Out from a camo-tarp tent crawls the Mole Cricket, her eyes bloodshot and wild.\n"
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
            state.move_to("walmart")
        else:
            print("\nTravis stumbles away, hacking and humiliated. He'll need to come back stronger.")
            state.move_to("dirt_road")


    mud_hole = Scene(
        "mud_hole",
        (
            "A wretched swamp-side gathering of lawn chairs, broken coolers, and permanent regret.\n"
            "You hear hacking coughs and the sound of someone trying to light a wet joint."
        ),
        {
            "approach tent": lambda state: mole_cricket_fight(state),
            "inventory": lambda state: print("Inventory: " + ', '.join(state.inventory)),
            "leave": "dirt_road",
        },
        on_enter=mud_hole_enter,
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

    def strip_club_enter(state):
        if "Cheetah-print fanny pack" in state.inventory and not state.flags.get("fanny_pack_buff"):
            print("Travis tightens the cheetah-print fanny pack, feelin' slick as an oil spill.")
            state.flags["fanny_pack_buff"] = True
            state.flags["travis_stats"]["flirt"] += 1

    def talk_dancer(state):
        if not state.flags.get("heard_bug_queen"):
            print("A dancer leans close and whispers, \"There's a shortcut through the springs, but watch for the bug queen.\"")
            state.flags["heard_bug_queen"] = True
        else:
            print("She just winks, already spilled the secret.")

    strip_club = Scene(
        "strip_club",
        (
            "Neon signs flicker above sticky floors while the bass rattles Travis's ribs. Half-interested dancers twirl as the crowd hollers."
        ),
        {
            "approach stage": attempt_stage,
            "talk to dancer": talk_dancer,
            "leave": "dirt_road",
            "inventory": show_inventory,
        },
        on_enter=strip_club_enter,
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
            "DO YOU WANNA DIE?",
            "MAKE UP YOUR MIND",
            "DO YOU WANNA HOLD HER?",
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
                "Saeva isn't here yet, but the Skunk Ape scampers off, leaving a trail straight toward Cypress Springs."
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
        "Bass rattles the trees as Travis wades into Cypress Springs. Neon lights flicker off the water "
        "and clouds of vape mist swirl across the surface. "
        "A glitter-soaked shape rises from the depths—a deranged Water Bug part stripper, part toxic ex, "
        "all nightmare."
    )

    def water_bug_cutscene(state):
        print('"Don\u2019t touch my man, BITCH!"')
        print("Suddenly, Saeva Venia descends from the cypress canopy.")
        print("With glowing eyes and bare feet slapping water, she launches a judo kick.")
        print("The Water Bug is sent flying into the woods.")
        print(
            "A huge hairy arm bursts from the brush\u2014Skunk Ape catches her mid-air and vanishes into the trees with his new bride."
        )
        state.move_to("ginnie_celebration")

    def water_bug_fight(state):
        required = ["Rubber duck floaty", "Cheetah-print fanny pack", "Slim Jim coupon"]
        if not all(item in state.inventory for item in required):
            print("Travis ain't properly kitted out for this throwdown. Best gather more gear.")
            state.move_to("dirt_road")
            return

        print("The Water Bug sways from the shallows, wings dripping. She eyes Travis with filthy intent.")
        boss_hp = 4
        travis_hp = 3
        stats = state.flags["travis_stats"]
        confused = 0
        while boss_hp > 1 and travis_hp > 0:
            if confused:
                auto_move = random.choice(["flex", "flirt", "yeehaw"])
                print(f"\nTravis reels from the Toxic Twerk and accidentally performs '{auto_move}'.")
                move = auto_move
                confused = 0
            else:
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
            print("Travis tumbles into the spring, choking on defeat. A faint neon glimmer beckons from the treeline.")
            print("He limps along a hidden trail and somehow ends up back at Melrose Hoes.")
            if not state.flags.get("got_dancer_charm"):
                print("A dancer takes pity on him and slips a Rhinestone Dancer Charm into his palm.")
                state.inventory.append("Rhinestone Dancer Charm")
                state.flags["got_dancer_charm"] = True
            state.move_to("strip_club")
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

    def ginnie_celebration_enter(state):
        print("Travis lights a doobie with Saeva as they drift along on the Rubber Duck Floaty.")
        print("They pass a jar of 'shine back and forth under the moonlight.")
        print('Travis cackles, "Ain\'t no meth zombie strong enough to keep me from my girl."')
        print("The spring water sparkles. The cicadas scream. All is right in Florida.")
        print("\n--- THE END ---\n")
        print("Together Forever. Memorial Day 2025.")
        sys.exit(0)

    ginnie_celebration = Scene(
        "ginnie_celebration",
        "The springs flow lazy and bright.",
        {},
        on_enter=ginnie_celebration_enter,
    )

    return {
        scene.name: scene
        for scene in [
            trailer,
            dirt_road,
            gas_station,
            gas_station_after_lizard,
            mud_hole,
            walmart,
            walmart_after_zombies,
            cop_chase,
            ditch_the_cops,
            strip_club,
            mole_cricket_showdown,
            stage_backroom,
            club_exit,
            ginnie_throne,
            ginnie_springs,
            ginnie_celebration,
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
