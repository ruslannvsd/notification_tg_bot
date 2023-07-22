from constants import constants


def set_enable_disable(user_id):
    with open(f"{constants.PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        time_period = lines[0].strip()
        new_status = "disabled" if lines[2].strip() == "enabled" else "enabled"
        keywords = lines[1].strip()
        print(new_status)
        with open(f"{constants.PATH}/{user_id}.txt", "w", encoding="utf-8") as f:
            f.write(f"{time_period}\n{new_status}\n{keywords}")
