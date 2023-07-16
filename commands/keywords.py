import constants


async def keywords_command(user_id):
    with open(f"{constants.PATH}/{user_id}.txt") as file:
        lines = file.readlines()
        second_line = lines[1].strip().split()
        print(second_line)
        fourth_line = lines[3].strip()
        status = "disabled" if fourth_line else "enabled"
        if not second_line:
            message = f"You've got no keywords. Notifications are {status}.\n" \
                      f"Enter words you want to monitor:"
            return message
        else:
            message = f"You've got keywords: {second_line}" \
                      f"Notifications are {fourth_line}"
            return message
