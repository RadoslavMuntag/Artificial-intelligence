import random

from subject import Subject
from virtual_machine import VirtualMachine
import json


def init_subjects(subject_count: int) -> dict[int, Subject]:
    return {
        subject: Subject(
            subject,
            {i: random.randint(0, 255) for i in range(64)}
        ) for subject in range(subject_count)
    }


def get_default_map_config():
    config = {
        "size": (7, 7),
        "start_position": (3, 6),
        "treasure_count": 5,
        "treasure_coordinates": [(4, 1), (2, 2), (6, 3), (1, 4), (4, 5)]
    }
    return config


def get_default_machine_config():
    config = {
        "population_size": 30,
        "elitism_size": 3,
        "roulette_size": 5,
        "tournament_size": 2,
        "mutation_rate": 0.05, 
        "mutation_rate_all_bits": 0.01,  # mala by byť nižšia ako mutation rate
        "dynamic_mutation": True,  # dynamická mutácia - k šanci mutácie sa pripočíta inverzná funkcia best_fitness
        # v kóde reprezentované ako random.random() < mutation_rate + 1 / (best_fitness * dynamic_mutation_constant + 1)
        # je to veľmi experimentálne a snaži sa aby mutácie nastávali menej, keď jedinci nachádzajú veľa pokladov
        "dynamic_mutation_constant": 4,  # väčšie hodnoty konštanty znižujú vpliv dynamickej mutácie

        "winner_vizualization": True,
        "end_program_when_winner": True,
        "extended_data_print": False,
        "generations_count_limit": 1000
    }
    return config


if __name__ == '__main__':
    map_config = {}
    machine_config = {}

    print("0 - Default config")
    print("1 - Load custom config from file")
    config_choice: int = int(input("Input 0 or 1: "))

    if config_choice == 0:  # Načítaj default config
        map_config = get_default_map_config()
        machine_config = get_default_machine_config()

    elif config_choice == 1:  # Načítaj custom config
        with open('map_config.json', 'r') as file:
            map_config = json.load(file)
            map_config["size"] = tuple(map_config["size"])
            map_config["start_position"] = tuple(map_config["start_position"])
            for i, treasure in enumerate(map_config["treasure_coordinates"]):
                map_config["treasure_coordinates"][i] = tuple(treasure)

        with open("machine_config.json", "r") as file1:
            machine_config = json.load(file1)

    if map_config == {} or machine_config == {}:
        print("Invalid input or missing config file")
        print("If 1 was chosen, loading config may have been unsuccessful, try 0 for default config")
        exit(-1)

    subjects: dict[int, Subject] = init_subjects(machine_config["population_size"])  # Vytvor populáciu s náhodnými hodnotami a daj ju do slovníka
    virtual_machine: VirtualMachine = VirtualMachine(map_config, machine_config, subjects)

    for _ in range(machine_config["generations_count_limit"]):  # Mian loop
        virtual_machine.start()
        virtual_machine.init_new_generation()
