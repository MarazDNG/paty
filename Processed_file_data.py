from random import *
import os


class Vocabulary_file_structure():
    left = 1
    right = 2
    streak = 3
    in_chunk = 4


SPLIT_CHARACTER = '-'
STREAK_LIMIT = 15
CHUNK_RANGE = 50


class Processed_line():
    unique_id = 0

    def __init__(self, file_line):
        temp = file_line.split(SPLIT_CHARACTER)
        self.left = temp[Vocabulary_file_structure.left]
        self.right = temp[Vocabulary_file_structure.right]
        self.streak = int(temp[Vocabulary_file_structure.streak])
        self.in_chunk = int(temp[Vocabulary_file_structure.in_chunk])
        self.id = Processed_line.unique_id
        Processed_line.unique_id += 1


class Processed_file_data():
    def __init__(self, file_lines):
        if len(file_lines[-1]) == 0:
            del file_lines[-1]
        self.file_lines = file_lines.copy()
        self.all_words_list = []
        self.practice_words_list = []
        self.chunk_words_list = []
        self.done_words_list = []
        self.nouns_list = []
        print('jsipica')

        for line in file_lines:
            temp = Processed_line(line)
            self.all_words_list.append(temp)
            temp_string = temp.right.lstrip()
            first_word = temp_string.split(' ')[0]
            #print(first_word)
            if first_word in ['der', 'die', 'das']:
                self.nouns_list.append(temp)
            if temp.in_chunk:
                self.chunk_words_list.append(temp)
            elif temp.streak >= STREAK_LIMIT:
                self.done_words_list.append(temp)
            else:
                self.practice_words_list.append(temp)
        print('Practice: ', len(self.practice_words_list),
              '\tIn chunk: ', len(self.chunk_words_list),
              '\tDone: ', len(self.done_words_list))

    def select_from_chunk_words(self, word_number):
        return sample(self.chunk_words_list, word_number)

    def select_from_all_words(self, word_number):
        return sample(self.all_words_list, word_number)

    def update_streaks_in_chunk(self, words_to_merge):
        """Takes Processed_line list."""
        for word in words_to_merge:
            for i in range(len(self.chunk_words_list)):
                if (word.left == self.chunk_words_list[i].left and
                        word.right == self.chunk_words_list[i].right):
                    self.chunk_words_list[i].streak = word.streak

    def update_chunk(self):
        self.remove_done_from_chunk()
        self.refill_chunk()

    def remove_done_from_chunk(self):
        for word in self.chunk_words_list:
            if word.streak >= STREAK_LIMIT:
                self.done_words_list.append(word)
                self.chunk_words_list.remove(word)

    def refill_chunk(self):
        to_fill_count = CHUNK_RANGE - len(self.chunk_words_list)
        selected_from_practice = sample(
                                    self.practice_words_list, to_fill_count)
        for word in selected_from_practice:
            self.chunk_words_list.append(word)
            self.practice_words_list.remove(word)

    def save_data(self):
        with open('next.txt', 'w', encoding='utf-8') as f:
            for i in range(len(self.chunk_words_list)):
                f.writelines([
                        self.chunk_words_list[i].left, '-',
                        self.chunk_words_list[i].right, '-',
                        str(self.chunk_words_list[i].streak), '-',
                        '1', '\n'])
            for i in range(len(self.practice_words_list)):
                f.writelines([
                        self.practice_words_list[i].left, '-',
                        self.practice_words_list[i].right, '-',
                        str(self.practice_words_list[i].streak), '-',
                        str(self.practice_words_list[i].in_chunk), '\n'])
            for i in range(len(self.done_words_list)):
                f.writelines([
                        self.done_words_list[i].left, '-',
                        self.done_words_list[i].right, '-',
                        str(self.done_words_list[i].streak), '-',
                        '0', '\n'])
        os.rename('vocabulary_de.txt', 'backup.txt')
        os.rename('next.txt', 'vocabulary_de.txt')
        os.rename('backup.txt', 'next.txt')
        print('Successfully saved!')
