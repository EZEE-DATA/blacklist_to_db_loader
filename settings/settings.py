from os import getcwd, listdir
from typing import TypeAlias

environment_variable_name: TypeAlias = str


def get_list_of_settings(settings_dir: str) -> list[environment_variable_name]:
    all_files = listdir(settings_dir)
    set_names: list[environment_variable_name] = []
    for file_name in all_files:
        if str(file_name[-5:]) != '.list':
            continue
        set_names.append(file_name.replace('.list', ''))
    return set_names


def main():
    """
    debug sake function
    :return: exit code
    """
    print(*get_list_of_settings(getcwd()))
    return 0


if __name__ == '__main__':
    main()
