SIZE = 5000  # Veľkosť pola pre generovanie bodov. pre hodnotu 5000 sa vygeneruje pole 10 000 * 10 000
WIN_SCALE = 0.05

GENERATE_BY_SEED = True  # Z rovnakého seedu je rovnaký output
SEED = 11

FILL_EMPTY_SPACE = True  # Pred vizualizáciou zaplní prázdny priestor novými bodmi,
                         # pri menších hodnotách POINTS_TO_GENERATE neodporúčam, zaplnený priestor potom je celý červený

POINTS_TO_GENERATE = 10000  # Skutočný počet vygenerovaných bodov je POINTS_TO_GENERATE*4 (ak má hodnotu 10
                            # vygenereje sa 10 pre každú farbu dokopy 40)
K = 15  # Nemeniť!!

K_Values = {  # Pre ktoré K hodnoty má program zobraziť výsledok
    1: True,
    3: True,
    7: True,
    15: True
}


