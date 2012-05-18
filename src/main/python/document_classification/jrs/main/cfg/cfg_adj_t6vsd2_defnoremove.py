
k = 12

LOAD_ROWS_FROM_FILE = 8000 #ile wierszy wczytac z pliku
CAST_METHOD = 'float' #do jakiego formatu rzutujemy liczby z pliku

REDUCE_DATA_TO_SIZE = 10000 #do ilu probek obciac dane

DEV_FRACTION = 0.6 #ulamek danych w zbiorze DEV
TRAINING_FRACTION = 0.2 #ulamek danych w zbiorze TRAIN

ADJUSTING = True #czy wykonywac procedure filtrowania zbioru train
ADJ_DEFAULT_REMOVE = False #czy domyslnym krokiem czy filtrowaniu jest usuwanie

FINALTEST = False
FINALTEST_START = 1000
FINALTEST_END = 1100
FINAL_RESULT_PATH = '/tmp/test_labels.txt'