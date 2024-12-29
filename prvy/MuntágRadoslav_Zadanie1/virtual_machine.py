import random

from subject import Subject
from end_vizualization import Visualization


def get_better_subject(subject1: Subject, subject2: Subject):
    """From two subjects returns them in order from better to worse"""
    if subject1.fitness > subject2.fitness:
        return subject1, subject2
    else:
        return subject2, subject1


def tournament(subjects: dict[int, Subject]):
    """(Obsolete) Returns winner of tournament from all
    subjects (it literally just returned the best, no possible use here)"""
    shuffle_arr = list(subjects.keys())

    while len(subjects) != 1:
        winners = shuffle_arr
        random.shuffle(shuffle_arr)
        while len(shuffle_arr) > len(subjects) % 2:
            contestant1 = shuffle_arr.pop(0)
            contestant2 = shuffle_arr.pop(0)
            winner_2_loser = get_better_subject(subjects[contestant1], subjects[contestant2])
            subjects.pop(winner_2_loser[1].id)
            winners.append(winner_2_loser[0].id)
        shuffle_arr = winners

    return subjects[shuffle_arr[0]]


def tournament_v2(subjects: dict[int, Subject]):
    """Returns winner from two subjects"""
    shuffle_arr = list(subjects.values())
    random.shuffle(shuffle_arr)

    contestant1 = shuffle_arr.pop(0)
    contestant2 = shuffle_arr.pop(0)

    return get_better_subject(contestant1, contestant2)[0]


def flip_bits(n, bit_width):
    """flips a bit at n position"""
    return ~n & ((1 << bit_width) - 1)


def flip_a_random_bit(n):
    """flips all bits with n length"""
    position = random.randint(0, 7)
    return n ^ (1 << position)


class VirtualMachine:
    def __init__(self, map_config, machine_config, subjects: dict[int, Subject]):
        self.map_config = map_config
        self.size = map_config['size']
        self.start_position = map_config['start_position']
        self.treasure_count = map_config['treasure_count']
        self.treasure_coordinates = map_config['treasure_coordinates']

        self.machine_config = machine_config

        self.subjects: dict[int, Subject] = subjects
        self.id_counter = len(self.subjects) - 1  # slúži na priraďovanie ID subjektom

        self.best_fitness = 0

        self.generation_counter = 0

    def end_with_success(self, subject: Subject):
        """ends when a subject founds all treasures if config is set to do"""
        print("Generácia číslo " + str(self.generation_counter))
        if self.machine_config["winner_vizualization"]:  # vizualizácia ak je tak nastavené v configu
            Visualization(self.map_config.copy()).start_simulation(subject.movement)
        if self.machine_config["end_program_when_winner"]:
            exit(1)

    def start(self):
        """starts testing of subjects"""
        self.generation_counter += 1
        print("----------------------- Generation number: " + str(self.generation_counter) + " -----------------------")
        for subject in self.subjects.values():
            self.test_room(subject)

    def test_room(self, subject: Subject):
        """tests one subject"""
        subject.set_position(self.start_position)
        if subject.start_test(self.treasure_count, self.treasure_coordinates, self.size, self.machine_config["extended_data_print"]):
            self.end_with_success(subject)

    def cross_breed(self, subject1: Subject, subject2: Subject):
        """cross-breeds two subjects and evaluates mutation"""
        newborn_memory_cells = {}
        temp_queue = [subject1, subject2]
        random.shuffle(temp_queue)  # náhodné zamiešanie subjektov

        gen_offset = random.randint(10, 53)  # pridelenie hranice pre mutáciu

        for i in range(64):
            new_cell = 0
            if i < gen_offset:
                new_cell = temp_queue[0].memory_cells_backup[i]
            else:
                new_cell = temp_queue[1].memory_cells_backup[i]

            if random.random() < self.machine_config["mutation_rate_all_bits"]:
                new_cell = flip_bits(new_cell, 8)  # mutácia všetkých bitov

            dynamic_mutation = (
                (1 / (self.best_fitness * self.machine_config["dynamic_mutation_constant"] + 1))
                if self.machine_config["dynamic_mutation"] else 0
                # ak je zapnutá dynamická mutácia pričíta hodnotu podla inverznú k najlepšiemu doterajšiemu subjektu
            )

            if random.random() < self.machine_config["mutation_rate"] + dynamic_mutation:
                new_cell = flip_a_random_bit(new_cell)  # mutácia náhodného jedného bitu

            newborn_memory_cells[i] = new_cell

        self.id_counter += 1
        return Subject(self.id_counter, newborn_memory_cells)

    def fill_newborns(self, subjects: dict[int, Subject], lesser_subjects: dict[int, Subject]):
        """fills a new generation with newborns"""
        parents = list(subjects.values())
        parents.extend(list(lesser_subjects.values()))
        # parents list z elite_subjects a survived_suvjects

        while len(subjects) != self.machine_config["population_size"]:
            # cyklus vytvára nových jedincov kým sa nenaplní populácia
            subject1 = random.choice(parents)
            subject2 = random.choice(parents)
            while subject1 == subject2:  # zabezpečenie aby neboli dva subjekty rovnaké
                subject2 = random.choice(parents)

            newborn = self.cross_breed(subject1, subject2)
            subjects[newborn.id] = newborn

        self.subjects = subjects

    def init_new_generation(self):
        """initializes the new generation"""
        elite_subjects = {}
        survived_subjects = {}
        sorted_by_fitness = dict(sorted(self.subjects.items(),
                                        key=lambda subject: subject[1].fitness,
                                        reverse=True))  # zoradenie subjektov podľa fitness

        self.best_fitness = list(sorted_by_fitness.values())[0].fitness
        for i in range(self.machine_config["elitism_size"]):  # výber elitizmom
            best_subject = list(sorted_by_fitness.values()).pop(0)
            best_subject.reset_self()
            sorted_by_fitness.pop(best_subject.id)
            elite_subjects[best_subject.id] = best_subject

        for i in range(self.machine_config["roulette_size"]):  # výber ruletov
            lucky_subject = random.choice(list(sorted_by_fitness.values()))
            lucky_subject.reset_self()
            sorted_by_fitness.pop(lucky_subject.id)
            survived_subjects[lucky_subject.id] = lucky_subject

        for i in range(self.machine_config["tournament_size"]): # výber turnamentom
            survivor = tournament_v2(sorted_by_fitness.copy())
            survivor.reset_self()
            sorted_by_fitness.pop(survivor.id)
            elite_subjects[survivor.id] = survivor

        # print(survived_subjects)
        self.fill_newborns(elite_subjects, survived_subjects)
