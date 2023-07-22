from constants import constants


def change_keywords(user_id, keywords_list):
    with open(f"{constants.PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        keywords = list_to_string(keywords_list)
        time_period = lines[0].strip()
        status = lines[2].strip()
        print(f"{user_id} {lines}\n{keywords} {time_period} {status}")
        with open(f"{constants.PATH}/{user_id}.txt", "w", encoding="utf-8") as f:
            f.write(f"{time_period}\n{keywords}\n{status}")
        message = f"You subscribed for {keywords}"
        if status == "disabled":
            message += "\nYou need to Enable the subscription to receive news."
    return message


def list_to_string(words):
    string = ""
    for word in words:
        string += word + " "
    return string.strip()
