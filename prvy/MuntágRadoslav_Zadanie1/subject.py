import copy


class Subject:
    def __init__(self, id: int, memory_cells: dict[int, int]):
        self.id = id
        self.memory_cells_count: int = len(memory_cells)
        self.memory_cells = memory_cells
        self.memory_cells_backup = copy.deepcopy(memory_cells)
        # backup slúži na udržanie pôvodných buniek pre ďalšie možné testovanie

        self.position: tuple[int, int] = (0, 0)
        self.has_visited = []

        self.memory_pointer: int = 0  # ukazovateľ na aktuálnu bunku

        self.movement = ""
        self.fitness = 0
        self.found_treasures = []
        self.step_counter = 0

        self.operations = [
            self.increment,
            self.decrement,
            self.jump_to,
            self.move
        ]  # lookup table aby som nemusel pre každú funkciu robiť if statement

    def set_position(self, position: tuple[int, int]):
        self.position = position

    def reset_self(self):
        """resets the subject for new test"""
        self.memory_cells = copy.deepcopy(self.memory_cells_backup)  # deepcopy backupu buniek

        self.position = (0, 0)
        self.has_visited = []

        self.memory_pointer: int = 0

        self.movement = ""
        self.fitness = 0
        self.found_treasures = []
        self.step_counter = 0

    def increment_mem_pointer(self):
        self.memory_pointer += 1

        if self.memory_pointer >= len(self.memory_cells):  # zabezpečujé cyklenie pointera
            self.memory_pointer = 0

    def check_for_treasures(self, treasure_coordinates: list[tuple[int, int]]):
        """removes a treasure from list of treasures if subject founds it"""
        for treasure in treasure_coordinates:
            if self.position == treasure and treasure not in self.found_treasures:
                self.found_treasures.append(treasure)
                break

    def increment(self, pointer: int):
        """increment operation"""
        self.memory_cells[pointer] += 1

        if self.memory_cells[pointer] > 255:
            self.memory_cells[pointer] = 0

        self.increment_mem_pointer()

    def decrement(self, pointer: int):
        """decrement operation"""
        self.memory_cells[pointer] -= 1

        if self.memory_cells[pointer] < 0:
            self.memory_cells[pointer] = 255

        self.increment_mem_pointer()

    def jump_to(self, pointer: int):
        """jump operation"""
        self.memory_pointer = pointer

    def move(self, pointer: int):
        """move operation"""
        bit_count: int = bin(self.memory_cells[pointer]).count("1")
        # spočíta bity v hodnote v bunke na ktorú ukazuje pointer

        if bit_count <= 3:
            self.movement += "H"
            self.set_position((self.position[0], self.position[1] - 1))
        elif bit_count <= 4:
            self.movement += "D"
            self.set_position((self.position[0], self.position[1] + 1))
        elif bit_count <= 5:
            self.movement += "P"
            self.set_position((self.position[0] + 1, self.position[1]))
        elif bit_count <= 8:
            self.movement += "L"
            self.set_position((self.position[0] - 1, self.position[1]))
        else:
            print("Something went wrong, bit count in movement exceeds 8. (Oprav to!!!!!!!)")
            exit(-1)
        # V dokumentácií som vysvetloval prečo som zvolil takéto hodnoty pre podmienku počítania bitov, viď 3.2.5.

        if self.position in self.has_visited:
            self.fitness -= 0.01 # zníženie fitness ak sa vrátil subjekt na pole kde už bol

        self.has_visited.append(self.position)

        self.increment_mem_pointer()

    def start_test(self, treasure_count: int, treasure_coordinates: list[tuple[int, int]], map_size: tuple[int, int], extended_print: bool):
        """start test returns true if subject founds all treasures, else false"""
        while True:

            if (self.position[0] < 0 or self.position[1] < 0 or
                    self.position[0] >= map_size[0] or self.position[1] >= map_size[1]):  # subjekt vyšiel z mapy
                if extended_print:
                    print("Subject id: " + str(self.id) + " is out of bounds at position: " + str(self.position))
                break

            if self.step_counter > 500:  # subjekt prekročil hranicu krokov
                if extended_print:
                    print("Subject id: " + str(self.id) + " is out of steps")
                break

            if treasure_count == len(self.found_treasures):  # subjekt našiel všetky poklady
                print("Subject id: " + str(self.id) + " Found all treasures!!!")
                print("Found treasures count: " + str(len(self.found_treasures)) +
                      ". Treasures found at location: " + str(self.found_treasures))
                print("Its movement is: " + self.movement)

                self.fitness += len(self.found_treasures) + (1/(len(self.movement) + 1))
                return True

            cell_data: int = self.memory_cells[self.memory_pointer]
            # hodnota v bunke na ktorú ukazuje hlavný pointer
            operation_id: int = cell_data >> 6  # extrakcia indexu operácie bitovým posunom
            self.operations[operation_id](cell_data % 64)  # spustenie operácie pomocou lookup table

            if operation_id == 3:  # ak bola operácia move, zisti či objekt nenašiel poklad
                self.check_for_treasures(treasure_coordinates)

            self.step_counter += 1



        #self.fitness = len(self.found_treasures)
        movement_bonus = len(self.movement)/200 if len(self.found_treasures) < 3 else (1 / (len(self.movement) + 1))
        # udelenie movement bonusu podľa počtu vykonaných pohybov, opačný výsledok vzhľadom na počet nájdených pokladov
        self.fitness += len(self.found_treasures) + movement_bonus

        if extended_print:
            print("Found treasures count: " + str(len(self.found_treasures)) +
                  ". Treasures found at location: " + str(self.found_treasures))
            print("Its movement is: " + self.movement)
            print("Its fitness is: " + str(self.fitness))
            print("")

        return False
