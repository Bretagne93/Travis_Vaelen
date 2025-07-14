def main():
    print("Howdy, y'all! Welcome to Travis Vaelen's world of gator-gut glory.")
    print("Travis jolts awake in his rusty trailer after dreamin' of HOA demons.")
    print(
        "Around him: dusty gator heads on the walls, beer cans stacked like a shrine, "
        "and his trusty shotgun restin' across an altar made from old hubcaps."
    )

    choice = input("Do ya wanna 'step outside' or 'check the fridge'? ").strip().lower()

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
    else:
        print(
            "Travis scratches his head, wonderin' how you even managed that choice. "
            "He shrugs and decides maybe he oughta hit snooze again."
        )


if __name__ == '__main__':
    main()