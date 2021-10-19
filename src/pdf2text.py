
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage

import os
import re

#################################
#      CONVERT PDF TO TEXT      #
#################################

def get_pdf_file_content(pdf_path, final_path):
    """ Creates a file for each PDF article
    :param pdf_path: pdf articles path
    :param final_path: final destination path
    :return: file for each article
    """

    for (dir_path, dir_names, file_names) in os.walk(pdf_path):
        for file_name in file_names:
            
            path_to_pdf = pdf_path + file_name

            resource_manager = PDFResourceManager(caching=True)
            out_text = StringIO()
            codec = 'utf-8'
            laParams = LAParams()
            text_converter = TextConverter(resource_manager, out_text, laparams=laParams)
            fp = open(path_to_pdf, 'rb')
            interpreter = PDFPageInterpreter(resource_manager, text_converter)

            for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
                try:
                    interpreter.process_page(page)
                except OverflowError:
                    continue

            text = out_text.getvalue()

            out_file = open(final_path + file_name[:-4], 'w', encoding = 'utf-8')
            out_file.write(text)

            out_file.close()
            fp.close()
            text_converter.close()
            out_text.close()

    return 


#################################
#           EDIT TEXT           #
#################################

def edit_text(corpus_path, final_path):
    """ Removes unwanted characters from text files converted from PDF
    :param corpus_path: articles corpus path
    :param final_path: final destination path
    :return: file for each article
    """

    for (root, dir_path, files) in os.walk(corpus_path):
        for filename in files:

            article_file = open(corpus_path + filename, 'r', encoding = 'utf-8')
            article = str(article_file.read().encode('utf-8'))
            article_file.close()

            out_file = open(final_path + filename, 'w', encoding = 'utf-8')

            # splitting the text into sentences 
            text = article.split('.')

            for line in text:

                line = line.replace('\\x0', '')
                line = re.sub(r'\\n', ' ', line)
                line = re.sub('- ', '', line)
                line = re.sub(r'\\xef\\xac\\x81', 'fi', line)
                line = re.sub(r'\\xe2\\x80\\x9d', '', line)
                line = re.sub(r'\\xe2\\x80\\x9c', '', line)
                line = re.sub(r'\\xe2\\x80\\x99', '\'', line)
                line = re.sub(r'\\xe2\\x80\\x98', '\'', line)
                line = re.sub(r'\\xe2\\x80\\x93', '–', line)
                line = re.sub(r'\\xe2\\x88\\x92', '–', line)
                line = re.sub(r'\\xe2\\x80\\x94', '–', line)
                line = re.sub(r'\\xef\\xac\\x82', 'fl', line)
                line = re.sub(r'\\xe2\\x80\\xa6', '', line)
                line = re.sub(r'\\xe2\\x80\\xa0', '', line)   
                line = re.sub(r'\\xe2\\x80\\xa6', '', line)   # …
                line = re.sub(r'\\xe2\\xac\\x9a', '', line)   # ⬚
                line = re.sub(r'\\xe2\\xab\\xb9', '', line)   # ⫹
                line = re.sub(r'\\xe4\\xab\\xb9', '', line)   # 䫹
                line = re.sub(r'\\xe2\\x88\\x97', '', line)   # ∗
                line = re.sub(r'\\xe2\\x88\\xbc', '', line)   # ~
                line = re.sub(r'\\xe2\\x80\\xb2', '', line)   # ´
                line = re.sub(r'\\xe2\\x86\\x92', '', line)   # →
                line = re.sub(r'\\xe4\\x89\\xb7', '', line)   # 䉷
                line = re.sub(r'\\xce.+', '', line)
                line = re.sub(r'\\xc2.+', '', line)
                line = re.sub(r'\\xc3.+', '', line)
                line = re.sub(r'\\xcb.+', '', line)
                line = re.sub(r'\\x[0-9][0-9].+', '', line)

                out_file.write(line + '\n')

            out_file.close()

    return


def main():
    """Creates a directory with a file for each article

    :return: directory with a file for each article
    """

    os.system('mkdir -p intermediary_corpus || true')
    get_pdf_file_content('PDF_files/', 'intermediary_corpus/')
    edit_text('intermediary_corpus/', 'corpus_B/')
    os.system('rm -rf intermediary_corpus/')

    return


if __name__ == "__main__":
    main()
