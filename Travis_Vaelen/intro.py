def main():
    inventory = [
        "A half-empty flask labeled \"'shine\"",
        "A bag of gator jerky",
        "An empty can of bug spray",
        "A VHS tape labeled \"Raise Hell- Praise Dale '98 – DO NOT ERASE\"",
        "A folded-up love note from Saeva Venia 💋",
    ]
    print("Welcome to Travis Vaelen's world of gator-gut glory.")
    print("Travis jolts awake in his rusty trailer after dreamin' of HOA demons.")
    print(
        "Around him: dusty gator heads on the walls, beer cans stacked like a shrine, "
        "and his trusty shotgun restin' across an altar made from old hubcaps."
    )

    choice = input("Do ya wanna 'step outside', 'check the fridge', 'look in the mirror', or 'inventory'? ").strip().lower()

    if 'step' in choice or 'outside' in choice:
        print(
            "Travis kicks open the screen door and steps into the muggy mornin'. "
            "The neighbor's cat hisses from under the porch, and the sweet stank of "
            "swamp tells him today's gonna be a doozy."
        )
    elif 'fridge' in choice or 'check' in choice:
        print(
            "He yanks open the fridge, findin' leftover possum stew next to a jar of "
            "glowin' moonshine. Breakfast of champions!"
        )
    elif 'mirror' in choice:
        print(
            "Travis catches a glimpse of himself in the cracked bathroom mirror and can't help but sport a mustachioed grin."
        )
        print(
            "Golden mullet flowing like swamp water at sunset, crowned by Pit Vipers that could blind a gator."
        )
        print(
            "His right bicep flexes, showin' off a flamingo tattoo that reads 'Saeva Venia' in hot-pink glory."
        )
        print(
            "He spreads his lats wide enough to block out the trailer door, a god among men in a single-wide."
        )
        print(
            "With Florida-man swagger dialed up to eleven, Travis winks at himself, absolutely unhinged and lovin' it."
        )
    elif 'inventory' in choice:
        print("Travis pats his pockets and rummages through his stash:")
        for item in inventory:
            print(f"- {item}")
    else:
        print(
            "Travis scratches his head, wonderin' how you even managed that choice. "
            "He shrugs and decides maybe he oughta hit snooze again."
        )


if __name__ == '__main__':
    main()