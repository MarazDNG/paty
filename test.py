# importing only those functions which
# are needed


with open('vocabulary_de.txt', 'r', encoding='utf-8') as f:
    lines = f.read()
lines = lines.split('\n')



with open('vocabulary_de.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        f.writelines(['-', line, '\n'])
