
k = 12

LOAD_ROWS_FROM_FILE = 10000 #ile wierszy wczytac z pliku
CAST_METHOD = 'float' #do jakiego formatu rzutujemy liczby z pliku

REDUCE_DATA_TO_SIZE = 20000 #do ilu probek obciac dane

DEV_FRACTION = 0.0 #ulamek danych w zbiorze DEV
TRAINING_FRACTION = 1.0 #ulamek danych w zbiorze TRAIN

FINALTEST = True
FINALTEST_START = 10000
FINALTEST_END = 20000
FINAL_RESULT_PATH = 'final_labels.txt'

ADJUSTING = False #czy wykonywac procedure filtrowania zbioru train
ADJ_DEFAULT_REMOVE = False #czy domyslnym krokiem czy filtrowaniu jest usuwanie
