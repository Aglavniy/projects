def log_plagiat_check(func):
    def wrapper(*args):
        w1,w2 = args
        result = func(*args)
        print(f"Check '{w1}' vs '{w2}' -> {result}")
    return wrapper


@log_plagiat_check
def is_plagiat(word1, word2):

    word1=word1.lower()
    word2=word2.lower()

    # если входит в множетсво
    if (set(word1) & set(word2)) == set(word2):
        return True

    # есть 1 дополнительная буква
    if len(set(word1) & set(word2)) == len(set(word2)) - 1:
        return True

    return False

# Открытие файла для чтения
with open("words.txt", "r") as file:
    while True:
        # Чтение одной строки
        line = file.readline()
        if not line:  # Если строка пустая, конец файла
            break

        is_plagiat(*line.split())

# is_plagiat(*line.split())