import constants


def set_enable_disable(user_id):
    with open(f"{constants.PATH}/{user_id}.txt") as file:
        lines = file.readlines()
        keywords = lines[1].strip()
        time_period = lines[2].strip()
        new_status = "disabled" if lines[3].strip() == "enabled" else "enabled"
        print(new_status)
        with open(f"{constants.PATH}/{user_id}.txt", "w") as f:
            f.write(f"{str(user_id).strip()}\n{keywords}\n{time_period}\n{new_status}")
