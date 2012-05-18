
k = 12
k_list = [3,7,12,21]

LOAD_ROWS_FROM_FILE = 2000 #ile wierszy wczytac z pliku
CAST_METHOD = 'float' #do jakiego formatu rzutujemy liczby z pliku

DEV_FRACTION = 0.0 #ulamek danych w zbiorze DEV
TRAINING_FRACTION = 0.8 #ulamek danych w zbiorze TRAIN


###############################################################################

REDUCE_DATA_TO_SIZE = 2000 #do ilu probek obciac dane

FINALTEST = True
FINALTEST_START = 1600
FINALTEST_END = 2000
FINAL_RESULT_PATH = '/tmp/final_labels.txt'

ADJUSTING = False #czy wykonywac procedure filtrowania zbioru train
ADJ_DEFAULT_REMOVE = False #czy domyslnym krokiem czy filtrowaniu jest usuwanie
