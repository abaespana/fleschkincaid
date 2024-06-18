import re
import csv

def count_syllables(word):
    count = 0
    vowels = "aeiouy"
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        count += 1
    if count == 0:
        count += 1
    return count

def flesch_kincaid_grade_level(words, sentences):
    total_words = len(words)
    total_sentences = len(sentences)
    average_words_per_sentence = total_words / total_sentences
    total_syllables = sum(count_syllables(word) for word in words)
    average_syllables_per_word = total_syllables / total_words
    grade_level = 0.39 * average_words_per_sentence + 11.8 * average_syllables_per_word - 15.59
    return grade_level

def process_text_file(file_path):
    paragraphs = []
    with open(file_path, 'r') as file:
        text = file.read()
        raw_paragraphs = re.split(r'\n\n', text)
        for idx, raw_paragraph in enumerate(raw_paragraphs):
            words = re.findall(r'\b\w+\b', raw_paragraph)
            sentences = re.split(r'[.!?]', raw_paragraph)
            sentences = [sentence.strip() for sentence in sentences if len(sentence.strip()) > 0]
            if len(words) > 100:
                first_three_words = ' '.join(words[:3])
                paragraph_info = [idx+1, first_three_words, ' '.join(words), sentences, len(words) / len(sentences)]
                average_syllables_per_word = sum(count_syllables(word) for word in words) / len(words)
                paragraph_info.append(average_syllables_per_word)
                grade_level = flesch_kincaid_grade_level(words, sentences)
                paragraph_info.append(grade_level)
                paragraphs.append(paragraph_info)
    return paragraphs

def write_to_csv(paragraphs, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Paragraph Number', 'First Three Words', 'Words', 'Sentences', 'Average Words per Sentence', 'Average Syllables per Word', 'Flesch-Kincaid Grade Level'])
        for paragraph in paragraphs:
            writer.writerow(paragraph)

def main():
    file_path = "example.txt"  # Change this to the path of your text file
    output_file = "output.csv"
    paragraphs = process_text_file(file_path)
    write_to_csv(paragraphs, output_file)

if __name__ == "__main__":
    main()
