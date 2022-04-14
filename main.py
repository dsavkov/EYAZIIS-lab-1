import io
import os
import sys

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from word import Word

symbols_black_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                      '.', ',', '!', ';', ':', '?', '-', '№', '(', ')', '"', '«', '»',
                      '\t', '\n', '\x0b', '\x0c', '\r', '\'']


def dict_for_quantity(tmp: list) -> dict:
    d = {}
    for i in tmp:
        if i not in d.keys():
            d[i] = 1
        else:
            d[i] = d.get(i) + 1
    return d


def extract_text_by_page(pdf_path: str) -> list:
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()


def extract_words_from_pdf(pdf_path: str) -> list:
    words_list = []
    for page in extract_text_by_page(pdf_path):
        for word in page.split(' '):
            if not symbols_black_list.__contains__(word):
                words_list.append(word)
    for i in range(len(words_list)):
        for j in symbols_black_list:
            if words_list[i].count(j):
                words_list[i] = words_list[i].replace(f"{j}", "")
    words_list.remove("")
    return words_list


def all_to_lower_case(words_list: list) -> None:
    for i in range(len(words_list)):
        words_list[i] = words_list[i].lower()


def create_vocabulary(pdf_file_path):
    words_list = extract_words_from_pdf(pdf_file_path)
    all_to_lower_case(words_list)
    words_dict = dict_for_quantity(sorted(words_list))
    pdf_file_name = pdf_file_path.split(os.sep)[-1].split(".")[0]

    output_file = open(f'{pdf_file_name}_morph.txt', 'tw', encoding='utf-8')
    output_file.write(f'Количество слов в словаре: {len(words_dict)}\n\n')
    for key in words_dict:
        word = Word(key)
        output_file.write('\n')
        output_file.write(f'{key} ({word.get_lexeme()}) - {words_dict.get(key)}\n')
        output_file.write(word.get_full_characteristics())
    output_file.close()


if __name__ == '__main__':
    create_vocabulary(sys.argv[1])
