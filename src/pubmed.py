"""
@author: horta-trc

The get_pmcids, write_abstract, write_body and divided_by_sentences functions were adapted from pubmed_corpus.py available here:
https://github.com/lasigeBioTM/PGR/tree/master/src
"""

import os
import subprocess
import sys
from polyglot.detect import Detector
import re

############################################
#         PMID TO PMCID CONVERSION         #
############################################

def get_pmcids(pubmed_ids):
    """ Creates a list of pubmed central ids from a list of pubmed ids 

    :param pubmed_ids: file with pubmed ids
    :param destination_path: destination path
    :return: list of pubmed central ids that matches the list of pubmed ids and a dict of type {pubmed_id:pmc_id, }
    """

    pubmed_list = []

    with open (pubmed_ids) as pubmed_ids_file:

        for pubmed_id in pubmed_ids_file:
            pubmed_id = pubmed_id.strip()
            pubmed_list.append(pubmed_id)

    pmc_list = []
    dict_pubmed_id = {}

    for pubmed_id in pubmed_list:

        os.system('curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=' + pubmed_id + '&retmode=xml" > articles.xml')

        exit_file = open('articles.xml', 'r', encoding = 'utf-8')
        
        for line in exit_file:
            
            if "pmc" in line:
                pmc_id = line.split('<ArticleId IdType="pmc">')[-1].split('</ArticleId>')[0]
                final_pmc_id = pmc_id.strip('PMC')
                
                dict_pubmed_id[pubmed_id] = final_pmc_id
                pmc_list.append(final_pmc_id)

            dict_pubmed_id_file = open(destination_path + 'dict_pubmed_id', 'w', encoding = 'utf-8')
            dict_pubmed_id_file.write(dict_pubmed_id)

        dict_pubmed_id_file.close()
        exit_file.close()

    os.system('rm articles.xml')

    return pmc_list


#############################################
#     GETTING ARTICLE'S ABSTRACT & BODY     #
#############################################

### WRITING THE ABSTRACT ###

def write_abstract(pubmed_ids, destination_path):
    """Creates a file for each retrieved abstract

    :param pubmed_ids: file with pubmed ids
    :param destination_path: destination path
    :return: file for each retrieved abstract
    """
    
    pmc_list = get_pmcids(pubmed_ids)

    for pmc_id in pmc_list:
 
        number_requests = 0
        counter = 0

        os.system('curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=' + pmc_id + '&rettype=fulltext&retmode=xml" > abstract.xml')
        presence = subprocess.Popen("grep '<AbstractText>' 'abstract.xml'", shell = True)
        return_code = presence.wait()

        if return_code != 1:

            try:
                exit_file = open('abstract.xml', 'r', encoding = 'utf-8')
                abstract = exit_file.read().split('<abstract>', 1)[-1].split('</abstract>', 1)[0]

                save_language = ''

                try:
                    for language in Detector(abstract).languages:
                        save_language = str(language).split()[1]
                        break

                except:
                    pass

                if save_language == 'English':
                    output = open(destination_path + pmc_id, 'w', encoding = 'utf-8')
                    output.write(abstract)
                    output.close()

                    number_requests += 1

                else:
                    print(pmc_id, 'was discarded:', save_language)

                exit_file.close()

            except UnicodeDecodeError:
                pass

            except FileNotFoundError:
                pass

        counter += 1

    os.system('rm abstract.xml')

    return


### WRITING THE BODY ###

def write_body(pubmed_ids destination_path):
    """Creates a file for each retrieved article's body

    :param pubmed_ids: file with pubmed ids
    :param destination_path: destination path
    :return: file for each retrieved article's body
    """

    pmc_list = get_pmcids(pubmed_ids)

    for pmc_id in pmc_list:

        number_requests = 0
        counter = 0

        os.system('curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=' + pmc_id + '&rettype=fulltext&retmode=xml" > article.xml')
        presence = subprocess.Popen("grep '<body>' 'article.xml'", shell = True)
        return_code = presence.wait()

        if return_code != 1:

            try:
                exit_file = open('article.xml', 'r', encoding = 'utf-8')
                body = exit_file.read().split('<body>', 1)[-1].split('</body>', 1)[0]

                save_language = ''

                try:
                    for language in Detector(body).languages:
                        save_language = str(language).split()[1]
                        break

                except:
                    pass

                if save_language == 'English':
                    output = open(destination_path + pmc_id, 'w', encoding = 'utf-8')
                    output.write(body)
                    output.close()

                    number_requests += 1

                else:
                    print(pmc_id, 'was discarded:', save_language)

                exit_file.close()

            except UnicodeDecodeError:
                pass

            except FileNotFoundError:
                pass

        counter += 1

    os.system('rm article.xml')

    return


####################################
#           TEXT EDITING           #
####################################

### REMOVING UNWANTED CHARACTERS ###

def edited_text(corpus_path, destination_path):
    """Removes unwanted characters for each retrieved article's body

    :param corpus_path: edited corpus path
    :param geniass_path: GENIA Sentence Splitter path
    :param destination_path: destination path
    :return: file for each retrieved article's body
    """

    for (root, dir_path, files) in os.walk(corpus_path):
 
        for filename in files:

            article_file = open(corpus_path + filename, 'r', encoding = 'utf-8')
            text = []

            for line in article_file:
                line = re.sub(r'<.+?>', '', line)
                line = re.sub(']','', line)
                line = re.sub('\[','', line)
                line = re.sub('\)','', line)
                line = re.sub('\(','', line)
                line = re.sub('\'','', line)
                line = re.sub('\"','', line)
                line = re.sub('&gt','', line)
                line = re.sub('&#x', '', line)

                text.append(line)

            output = open(destination_path + filename, 'w', encoding = 'utf-8')
            
            for lines in text:
                output.write(lines)
            output.close()

    return


#### DIVIDED BY SENTENCES ABSTRACTS ####

def divided_by_sentences(corpus_path, geniass_path, destination_path):  # needs to be run from directory bin/geniass/
    """Creates a file for each divided by sentences abstract

    :param corpus_path: edited abstracts path
    :param geniass_path: GENIA Sentence Splitter path
    :param destination_path: destination path
    :return: file for each divided by sentences abstract
    """

    os.system('rm -rf ' + destination_path + '* || true')

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:
            os.system('./' + geniass_path + ' ' + corpus_path + filename + ' ' + destination_path + filename)

    return


#### RUN ####

def main():
    """Creates a directory with a file for each retrieved abstract divided by sentences and article's body

    :return: directory with a file for each retrieved article's abstract and body
    """

    os.system('mkdir -p corpus_A/articles || true')
    os.system('mkdir -p corpus_A/abstracts || true')
    os.system('mkdir -p corpus_A/intermediary_corpus_abstracts || true')
    os.system('mkdir -p corpus_A/edited_corpus_articles || true')

    write_article('data/pmids.txt', 'corpus_A/articles/')
    os.system('cp corpus_A/articles/* corpus_A/intermediary_corpus_articles/')
    edited_text('corpus_A/intermediary_corpus_articles/', 'corpus_A/articles/')
    os.system('rm -rf corpus_A/intermediary_corpus_articles/')

    write_abstract('data/pmids.txt', 'corpus_A/abstracts/')
    os.system('cp corpus_A/abstracts/* corpus_A/edited_corpus_abstracts/')
    os.chdir('bin/geniass/')
    divided_by_sentences('../../corpus_A/edited_corpus_abstracts/', 'geniass', '../../corpus_A/abstracts/')
    os.chdir('../..')
    os.system('rm -rf corpus_A/edited_corpus_abstracts/')


    return
    

if __name__ == "__main__":
    main()

