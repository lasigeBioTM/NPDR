"""
@author: horta-trc

The phenotype_annotations, *_disease_annotations, *_gene_annotations, *_disease_abbreviation_annotations, *_disease_synonym_annotations and
relations_annotations functions were adapted from annotations.py available here:
https://github.com/lasigeBioTM/PGR/tree/master/src
"""

import os

############################################
#      NEGATION SENTENCES ANNOTATIONS      #
############################################

def detect_negation(corpus_path, destination_path):
    """ Creates a file with sentences containing negations or the word 'normal' for each article in the corpus

    :param corpus_path: file corpus path
    :param destination_path: destination path
    :return: negation sentence file for each article in the corpus
    """

    # negation tokens from the NPDR dataset
    negation_list = [' no ', 'negative', 'none ', 'not ', 'absence', 'absent ', 'without', 'impaired', 'impairment' \
                     'denied', 'excluded', 'free of', 'lack of', 'present exclusively', 'rules out', 'normal']

    for (root, dir_path, files) in os.walk(corpus_path):
        for filename in files:

            article_file = open(corpus_path + filename, 'r', encoding='utf-8')
            article = article_file.readlines()
            article_file.close()

            annotation_negation = []

            for sentence in article:
               for word in negation_list:
                    if word in sentence:
                        annotation_negation.append(sentence)

            # no need to write files where there is no negation token
            if len(annotation_negation) != 0:
            	# removing duplicate sentences
                annotation_negation = [i for n, i in enumerate(annotation_negation) if i not in annotation_negation[:n]]
                output = open(destination_path + filename, 'w', encoding = 'utf-8')

                for line in annotation_negation:
                    output.write(line)
                output.close()

    return


###########################################
#          PHENOTYPE ANNOTATIONS          #
###########################################

def phenotype_annotations(corpus_path, annotation_path, synonym_path, mer_path):
    """ Creates a phenotype and phenotype synonym annotation file for each negation sentence annotation file in the corpus

    :param corpus_path: article corpus path
    :param mer_path: mer data path
    :param destination_path: destination path
    :return: phenotype and phenotype synonym annotation file for each negation sentence annotation file in the corpus
    """

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:

            negation_file = open(corpus_path + filename, 'r', encoding='utf-8')
            negation_sentences = negation_file.readlines()
            negation_file.close()

            annotations = []
            synonyms = []

            for sentence in negation_sentences:
                annotations_phenotypes = os.popen('./' + mer_path + ' ' + '\'' + sentence + '\'' + ' hp').readlines()
                # print (annotations_phenotypes)
                annotations_synonyms = os.popen('./' + mer_path + ' ' + '\'' + sentence + '\'' + ' hpsynonym').readlines()
                # print (annotations_synonyms)

                for annotations_phenotype in annotations_phenotypes:
                    phenotype_index_1 = annotations_phenotype.split('\t')[0]  
                    phenotype_index_2 = annotations_phenotype.split('\t')[1]
                    phenotype_name = annotations_phenotype.split('\t')[2]
                    phenotype_id = annotations_phenotype.split('\t')[3][:-2]

                    annotations.append((phenotype_index_1, phenotype_index_2, phenotype_name, phenotype_id))

                for annotations_synonym in annotations_synonyms:
                    phenotype_index_1 = annotations_synonym.split('\t')[0]  
                    phenotype_index_2 = annotations_synonym.split('\t')[1]
                    phenotype_name = annotations_synonym.split('\t')[2]
                    phenotype_id = annotations_synonym.split('\t')[3][:-1]

                    synonyms.append((phenotype_index_1, phenotype_index_2, phenotype_name, phenotype_id))

            annotations = sorted(annotations, key=lambda position: int(position[0]))
            unique_annotations = list(set(annotations))
            annotation_file = open(annotation_path + filename, 'w', encoding = 'utf-8')

            synonyms = sorted(synonyms, key=lambda position: int(position[0]))
            unique_synonyms = list(set(synonyms))
            synonyms_file = open(synonym_path + filename, 'w', encoding = 'utf-8')

            for annotation in unique_annotations:
                if 'HP' in annotation[3]:
                    annotation_file.write(annotation[0] + '\t' + annotation[1] + '\t' + annotation[2] + '\t' + annotation[3] + '\n')

            for synonym in unique_synonyms:
                synonyms_file.write(synonym[0] + '\t' + synonym[1] + '\t' + synonym[2] + '\t' + synonym[3] + '\n')

            annotation_file.close()

    return


##########################################
#            GENE ANNOTATIONS            #
##########################################

### ABSTRACTS GENE ANNOTATIONS ###

def abstract_gene_annotations(corpus_path, annotation_path, mer_path):
    """ Creates a gene annotation file for each abstract in the corpus

    :param corpus_path: abstract corpus path
    :param mer_path: mer data path
    :param destination_path: destination path
    :return: gene annotation file for each abstract in the corpus
    """

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:
            annotations = []
            gene_annotations = []
            save_line = None

            abstract_file = open(corpus_path + filename, 'r', encoding = 'utf-8')
            abstract = str(abstract_file.read().encode('utf-8'))
            abstract_file.close()

            annotations_genes = os.popen('./' + mer_path + ' ' + abstract + ' genes').readlines()
            # print (annotations_genes)

            for annotations_gene in annotations_genes:
                annotations_gene = annotations_gene.split('\t')
                # annotation line with index, entity name and id
                if len(annotations_gene) == 4:  
                    save_line = annotations_gene[0] + '\t' + annotations_gene[1] + '\t' + annotations_gene[2]
                    gene_annotations.append(str(annotations_gene).replace('[', '').replace('\'', '').replace(']', '').replace(',', '\t').replace('\\', ''))

                # annotation with id only
                elif len(annotations_gene) == 1:   
                    extra_id = annotations_gene[0].strip('\n')
                    if save_line:
                        gene_annotations.append(save_line + '\t' + extra_id + '\n')

            for annotations_gene in gene_annotations:
                gene_index_1 = annotations_gene.split('\t')[0] 
                gene_index_2 = annotations_gene.split('\t')[1]
                gene_name = annotations_gene.split('\t')[2]
                gene_id = annotations_gene.split('\t')[3][:-1]
                
                annotations.append((gene_index_1, gene_index_2, gene_name, gene_id))

            # sort by position in text
            annotations = sorted(annotations, key=lambda position: int(position[0]))
            annotation_file = open(annotation_path + filename, 'w', encoding='utf-8')

            for annotation in annotations:
                annotation_file.write(annotation[0] + '\t' + annotation[1] + '\t' + annotation[2] + '\t' + annotation[3] + '\n')

            annotation_file.close()

    return


### ARTICLES GENE ANNOTATIONS ###

def article_gene_annotations(corpus_path, annotation_path, mer_path):
    """ Creates a gene annotation file for each article in the corpus

    :param corpus_path: article corpus path
    :param mer_path: mer data path
    :param destination_path: destination path
    :return: gene annotation file for each article in the corpus
    """

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:
            annotations = []
            gene_annotations = []
            save_line = None

            article_file = open(corpus_path + filename, 'r', encoding='utf-8')
            article = str(article_file.read().encode('utf-8'))
            article_file.close()

            annotations_genes = os.popen('./' + mer_path + ' ' + article + ' genes').readlines()
            # print (annotations_genes)

            for annotations_gene in annotations_genes:
                annotations_gene = annotations_gene.split('\t')
                # annotation line with index, entity name and id
                if len(annotations_gene) == 4: 
                    save_line = annotations_gene[0] + '\t' + annotations_gene[1] + '\t' + annotations_gene[2]
                    gene_annotations.append(str(annotations_gene).replace('[', '').replace('\'', '').replace(']', '').replace(',', '\t').replace('\\', ''))

                # annotation with id only 
                elif len(annotations_gene) == 1:  
                    extra_id = annotations_gene[0].strip('\n')
                    if save_line:
                        gene_annotations.append(save_line + '\t' + extra_id + '\n')

            for annotations_gene in gene_annotations:
                gene_index_1 = annotations_gene.split('\t')[0] 
                gene_index_2 = annotations_gene.split('\t')[1]
                gene_name = annotations_gene.split('\t')[2]
                gene_id = annotations_gene.split('\t')[3][:-1]
                
                annotations.append((gene_index_1, gene_index_2, gene_name, gene_id))

            # sort by position in text
            annotations = sorted(annotations, key=lambda position: int(position[0]))
            annotation_file = open(annotation_path + filename, 'w', encoding='utf-8')

            for annotation in annotations:
                annotation_file.write(annotation[0] + '\t' + annotation[1] + '\t' + annotation[2] + '\t' + annotation[3] + '\n')

            annotation_file.close()

    return


###########################################
#           DISEASE ANNOTATIONS           #
###########################################

### ABSTRACT DISEASE ANNOTATIONS ###

def abstract_disease_annotations(corpus_path, annotation_path, mer_path):
    """ Creates a disease annotation file for each abstract in the corpus

    :param corpus_path: abstract corpus path
    :param mer_path: mer data path
    :param destination_path: destination path
    :return: disease annotation file for each abstract in the corpus
    """

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:
            annotations = []

            abstract_file = open(corpus_path + filename, 'r', encoding = 'utf-8')
            abstract = str(abstract_file.read().encode('utf-8'))
            abstract_file.close()

            annotations_diseases = os.popen('./' + mer_path + ' ' + abstract + ' diseases').readlines()
            # print (annotations_diseases)

            for annotations_disease in annotations_diseases:
                disease_index_1 = annotations_disease.split('\t')[0]
                disease_index_2 = annotations_disease.split('\t')[1]
                disease_name = annotations_disease.split('\t')[2]
                disease_id = annotations_disease.split('\t')[3][:-1]

                annotations.append((disease_index_1, disease_index_2, disease_name, disease_id))

            annotations = sorted(annotations, key=lambda position: int(position[0]))  # sort by position in text
            unique_annotations = list(set(annotations))
            annotation_file = open(annotation_path + filename, 'w', encoding = 'utf-8')  

            for annotation in unique_annotations:
                annotation_file.write(annotation[0] + '\t' + annotation[1] + '\t' + annotation[2] + '\t' + annotation[3] +'\n')

            annotation_file.close()

    return


### ARTICLE DISEASE ANNOTATIONS ###

def article_disease_annotations(corpus_path, annotation_path, mer_path):
    """ Creates a disease annotation file for each article in the corpus

    :param corpus_path: article corpus path
    :param mer_path: mer data path
    :param destination_path: destination path
    :return: disease annotation file for each article in the corpus
    """

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:
            annotations = []

            article_file = open(corpus_path + filename, 'r', encoding='utf-8')
            article = str(article_file.read().encode('utf-8'))
            article_file.close()

            annotations_diseases = os.popen('./' + mer_path + ' ' + article + ' diseases').readlines()
            # print (annotations_diseases)

            for annotations_disease in annotations_diseases:
                disease_index_1 = annotations_disease.split('\t')[0]
                disease_index_2 = annotations_disease.split('\t')[1]
                disease_name = annotations_disease.split('\t')[2]
                disease_id = annotations_disease.split('\t')[3][:-1]

                annotations.append((disease_index_1, disease_index_2, disease_name, disease_id))

            # sort by position in text
            annotations = sorted(annotations, key=lambda position: int(position[0]))  
            unique_annotations = list(set(annotations))
            annotation_file = open(annotation_path + filename, 'w', encoding = 'utf-8')  

            for annotation in unique_annotations:
                annotation_file.write(annotation[0] + '\t' + annotation[1] + '\t' + annotation[2] + '\t' + annotation[3] +'\n')

            annotation_file.close()

    return


### ABSTRACT DISEASE ABBREAVIATION ANNOTATIONS ###

def abstract_abbreviation_annotations(corpus_path, annotation_path, mer_path):
    """ Creates a disease abbreviation annotation file for each abstract in the corpus

    :param corpus_path: abstract corpus path
    :param mer_path: mer data path
    :param destination_path: destination path
    :return: disease abbreviation annotation file for each abstract in the corpus
    """

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:
            annotations = []
            abbreviation_annotations = []
            save_line = None

            abstract_file = open(corpus_path + filename, 'r', encoding = 'utf-8')
            abstract = str(abstract_file.read().encode('utf-8'))
            abstract_file.close()

            annotations_disease_abbreviations = os.popen('./' + mer_path + ' ' + abstract + ' diseaseabbreviation').readlines()
            # print (annotations_disease_abbreviations)

            for annotations_disease_abbreviation in annotations_disease_abbreviations:
                annotations_disease_abbreviation = annotations_disease_abbreviation.split('\t')
                # annotation line with index, entity name and id
                if len(annotations_disease_abbreviation) == 4: 
                    save_line = annotations_disease_abbreviation[0] + '\t' + annotations_disease_abbreviation[1] + '\t' + annotations_disease_abbreviation[2]
                    abbreviation_annotations.append(str(annotations_disease_abbreviation).replace('[', '').replace('\'', '').replace(']', '').replace(',', '\t').replace('\\', ''))

                # annotation with id only 
                elif len(annotations_disease_abbreviation) == 1:  
                    extra_id = annotations_disease_abbreviation[0].strip('\n')
                    if save_line:
                        abbreviation_annotations.append(save_line + '\t' + extra_id + '\n')

            for annotations_disease_abbreviation in abbreviation_annotations:
                abbreviation_index_1 = annotations_disease_abbreviation.split('\t')[0] 
                abbreviation_index_2 = annotations_disease_abbreviation.split('\t')[1]
                abbreviation_name = annotations_disease_abbreviation.split('\t')[2]
                abbreviation_id = annotations_disease_abbreviation.split('\t')[3][:-1]
                
                annotations.append((abbreviation_index_1, abbreviation_index_2, abbreviation_name, abbreviation_id))

            # sort by position in text
            annotations = sorted(annotations, key=lambda position: int(position[0]))
            unique_annotations = list(set(annotations))
            annotation_file = open(annotation_path + filename, 'w', encoding='utf-8')

            for annotation in unique_annotations:
                annotation_file.write(annotation[0] + '\t' + annotation[1] + '\t' + annotation[2] + '\t' + annotation[3] + '\n')

            annotation_file.close()

    return


### ARTICLE DISEASE ABBREVIATION ANNOTATIONS ###

def article_abbreviation_annotations(corpus_path, annotation_path, mer_path):
    """ Creates a disease abbreviation annotation file for each article in the corpus

    :param corpus_path: article corpus path
    :param mer_path: mer data path
    :param destination_path: destination path
    :return: disease abbreviation annotation file for each article in the corpus
    """

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:
            annotations = []
            abbreviation_annotations = []
            save_line = None

            article_file = open(corpus_path + filename, 'r', encoding='utf-8')
            article = str(article_file.read().encode('utf-8'))
            article_file.close()

            annotations_disease_abbreviations = os.popen('./' + mer_path + ' ' + article + ' diseaseabbreviation').readlines()
            # print (annotations_disease_abbreviations)

            for annotations_disease_abbreviation in annotations_disease_abbreviations:
                annotations_disease_abbreviation = annotations_disease_abbreviation.split('\t')
                # annotation line with index, entity name and id
                if len(annotations_disease_abbreviation) == 4:  
                    save_line = annotations_disease_abbreviation[0] + '\t' + annotations_disease_abbreviation[1] + '\t' + annotations_disease_abbreviation[2]
                    abbreviation_annotations.append(str(annotations_disease_abbreviation).replace('[', '').replace('\'', '').replace(']', '').replace(',', '\t').replace('\\', ''))

                # annotation with id only 
                elif len(annotations_disease_abbreviation) == 1:   
                    extra_id = annotations_disease_abbreviation[0].strip('\n')
                    if save_line:
                        abbreviation_annotations.append(save_line + '\t' + extra_id + '\n')

            for annotations_disease_abbreviation in abbreviation_annotations:
                abbreviation_index_1 = annotations_disease_abbreviation.split('\t')[0] 
                abbreviation_index_2 = annotations_disease_abbreviation.split('\t')[1]
                abbreviation_name = annotations_disease_abbreviation.split('\t')[2]
                abbreviation_id = annotations_disease_abbreviation.split('\t')[3][:-1]
                
                annotations.append((abbreviation_index_1, abbreviation_index_2, abbreviation_name, abbreviation_id))

            # sort by position in text
            annotations = sorted(annotations, key=lambda position: int(position[0]))
            unique_annotations = list(set(annotations))
            annotation_file = open(annotation_path + filename, 'w', encoding='utf-8')

            for annotation in unique_annotations:
                annotation_file.write(annotation[0] + '\t' + annotation[1] + '\t' + annotation[2] + '\t' + annotation[3] + '\n')

            annotation_file.close()

    return


### ABSTRACT DISEASE SYNONYM ANNOTATIONS ####

def abstract_synonym_annotations(corpus_path, annotation_path, mer_path):
    """ Creates a disease synonym annotation file for each abstract in the corpus

    :param corpus_path: abstract corpus path
    :param mer_path: mer data path
    :param destination_path: destination path
    :return: disease synonym annotation file for each abstract in the corpus
    """

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:
            annotations = []
            synonyms_annotations = []
            save_line = None

            abstract_file = open(corpus_path + filename, 'r', encoding = 'utf-8')
            abstract = str(abstract_file.read().encode('utf-8'))
            abstract_file.close()

            annotations_disease_synonyms = os.popen('./' + mer_path + ' ' + abstract + ' diseasesynonyms').readlines()
            # print (annotations_disease_synonyms)

            for annotations_disease_synonym in annotations_disease_synonyms:
                annotations_disease_synonym = annotations_disease_synonym.split('\t')
                # annotation line with index, entity name and id
                if len(annotations_disease_synonym) == 4:
                    save_line = annotations_disease_synonym[0] + '\t' + annotations_disease_synonym[1] + '\t' + annotations_disease_synonym[2]
                    synonyms_annotations.append(str(annotations_disease_synonym).replace('[', '').replace('\'', '').replace(']', '').replace(',', '\t').replace('\\', ''))

                # annotation with id only 
                elif len(annotations_disease_synonym) == 1:  
                    extra_id = annotations_disease_synonym[0].strip('\n')
                    if save_line:
                        synonyms_annotations.append(save_line + '\t' + extra_id + '\n')

                for annotation_synonym in synonyms_annotations:
                    synonym_index_1 = annotation_synonym.split('\t')[0] 
                    synonym_index_2 = annotation_synonym.split('\t')[1]
                    synonym_name = annotation_synonym.split('\t')[2]
                    synonym_id = annotation_synonym.split('\t')[3][:-1]
                    
                    annotations.append((synonym_index_1, synonym_index_2, synonym_name, synonym_id))

            # sort by position in text
            annotations = sorted(annotations, key=lambda position: int(position[0]))
            unique_annotations = list(set(annotations))
            annotation_file = open(annotation_path + filename, 'w', encoding='utf-8')

            for annotation in unique_annotations:
                annotation_file.write(annotation[0] + '\t' + annotation[1] + '\t' + annotation[2] + '\t' + annotation[3] + '\n')

            annotation_file.close()

    return


### ARTICLE DISEASE SYNONYM ANNOTATIONS ####

def article_synonym_annotations(corpus_path, annotation_path, mer_path):
    """ Creates a disease synonym annotation file for each article in the corpus

    :param corpus_path: article corpus path
    :param mer_path: mer data path
    :param destination_path: destination path
    :return: disease synonym annotation file for each article in the corpus
    """

    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:
            annotations = []
            synonyms_annotations = []
            save_line = None

            article_file = open(corpus_path + filename, 'r', encoding='utf-8')
            article = str(article_file.read().encode('utf-8'))
            article_file.close()

            annotations_disease_synonyms = os.popen('./' + mer_path + ' ' + article + ' diseasesynonyms').readlines()
            # print (annotations_disease_synonyms)

            for annotations_disease_synonym in annotations_disease_synonyms:
                annotations_disease_synonym = annotations_disease_synonym.split('\t')
                # annotation line with index, entity name and id
                if len(annotations_disease_synonym) == 4:  
                    save_line = annotations_disease_synonym[0] + '\t' + annotations_disease_synonym[1] + '\t' + annotations_disease_synonym[2]
                    synonyms_annotations.append(str(annotations_disease_synonym).replace('[', '').replace('\'', '').replace(']', '').replace(',', '\t').replace('\\', ''))

                # annotation with id only 
                elif len(annotations_disease_synonym) == 1:   
                    extra_id = annotations_disease_synonym[0].strip('\n')
                    if save_line:
                        synonyms_annotations.append(save_line + '\t' + extra_id + '\n')

            for annotation_synonym in synonyms_annotations:
                synonym_index_1 = annotation_synonym.split('\t')[0] 
                synonym_index_2 = annotation_synonym.split('\t')[1]
                synonym_name = annotation_synonym.split('\t')[2]
                synonym_id = annotation_synonym.split('\t')[3][:-1]
                
                annotations.append((synonym_index_1, synonym_index_2, synonym_name, synonym_id))

            # sort by position in text
            annotations = sorted(annotations, key=lambda position: int(position[0]))
            unique_annotations = list(set(annotations))
            annotation_file = open(annotation_path + filename, 'w', encoding='utf-8')

            for annotation in unique_annotations:
                annotation_file.write(annotation[0] + '\t' + annotation[1] + '\t' + annotation[2] + '\t' + annotation[3] + '\n')

            annotation_file.close()

    return


#########################################
#           FINAL ANNOTATIONS           #
#########################################

def sort_annotations_files(abstract_disease_abbreviations_path, abstract_disease_synonyms_path, abstract_diseases_path, \
                           abstract_genes_path, article_disease_abbreviations_path, article_disease_synonyms_path, \
                           article_diseases_path, article_genes_path, phenotypes_path, phenotype_synonyms_path, \
                           final_annotations_path):
    """ Merges all annotations files into one file for each article in the corpus

	:param abstract_disease_abbreviations_path: abstract disease abbreviations annotations path
	:param abstract_disease_synonyms_path: abstract disease annotations path
	:param abstract_diseases_path: abstract disease annotations path
	:param abstract_genes_path: abstract genes annotations path
	:param article_disease_abbreviations_path: article disease abbreviations annotations path
	:param article_disease_synonyms_path: article disease synonyms annotations path
	:param article_diseases_path: article diseases annotations path
	:param article_genes_path: article genes annotations path
	:param phenotypes_path: phenotypes annotations path
	:param phenotype_synonyms_path: phenotype synonyms annotations path
	:param final_annotations_path: final annotations path
    :return: file with phenotype, gene and disease annotations from the same article
    """

    for (dir_path, dir_names, file_names) in os.walk(diseases_path):
        for filename in file_names:

            abstract_disease_abbreviations_file = open(abstract_disease_abbreviations_path + filename, 'r', encoding='utf-8')
            abstract_disease_abbreviations = abstract_disease_abbreviations_file.readlines()
            abstract_disease_abbreviations_file.close()

            try: 
                abstract_disease_synonyms_file = open(abstract_disease_synonyms_path + filename, 'r', encoding='utf-8')
                abstract_disease_synonyms = abstract_disease_synonyms_file.readlines()
                abstract_disease_synonyms_file.close()

            except FileNotFoundError:
                continue 

            try: 
	            abstract_diseases_file = open(diseases_path + filename, 'r', encoding='utf-8')
	            diseases = abstract_diseases_file.readlines()
	            abstract_diseases_file.close()

            except FileNotFoundError:
                continue 

            try: 
                abstract_genes_file = open(genes_path + filename, 'r', encoding='utf-8')
                genes = abstract_genes_file.readlines()
                abstract_genes_file.close()

            except FileNotFoundError:
                continue 

            try: 
                article_disease_abbreviations_file = open(article_disease_abbreviations_path + filename, 'r', encoding='utf-8')
                article_disease_abbreviations = article_disease_abbreviations_file.readlines()
                article_disease_abbreviations_file.close()

            except FileNotFoundError:
                continue 

            try: 
                article_disease_synonyms_file = open(article_disease_synonyms_path + filename, 'r', encoding='utf-8')
                article_disease_synonyms = article_disease_synonyms_file.readlines()
                article_disease_synonyms_file.close()

            except FileNotFoundError:
                continue 

            try: 
                article_diseases_file = open(article_diseases_path + filename, 'r', encoding='utf-8')
                article_diseases = article_diseases_file.readlines()
                article_diseases_file.close()

            except FileNotFoundError:
                continue 

            try: 
                article_genes_file = open(article_genes_path + filename, 'r', encoding='utf-8')
                article_genes = article_genes_file.readlines()
                article_genes_file.close()

            except FileNotFoundError:
                continue 

            try: 
                phenotypes_file = open(phenotypes_path + filename, 'r', encoding='utf-8')
                phenotypes = phenotypes_file.readlines()
                phenotypes_file.close()

            except FileNotFoundError:
                continue 

            try: 
                phenotype_synonyms_file = open(phenotype_synonyms_path + filename, 'r', encoding='utf-8')
                phenotype_synonyms = phenotype_synonyms_file.readlines()
                phenotype_synonyms_file.close()

            except FileNotFoundError:
                continue 

            final_annotations = open(final_annotations_path + filename, 'w', encoding='utf-8')
	
            for phenotype in phenotypes:
                final_annotations.write(phenotype)

            for phenotype in phenotype_synonyms:
                final_annotations.write(phenotype)

            for disease in abstract_disease_abbreviations:
                final_annotations.write(disease)

            for disease in abstract_disease_synonyms:
                final_annotations.write(disease)

            for disease in abstract_diseases:
                final_annotations.write(disease)

            for gene in abstract_genes:
                final_annotations.write(disease)

            for disease in article_disease_abbreviations:
                final_annotations.write(disease)

            for disease in article_disease_synonyms:
                final_annotations.write(disease)

    final_annotations.close()

    return


################################################
#  HPO GOLD STANDARD NEGATION FILE DICTIONARY  #
################################################

def hpo_dict(hpo_file, dict_type = None):
    """Creates a dictionary of type {disease1:[phenotype1, phenotype2, ...], }

    :param hpo_file: hpo gold standard file with negative relations disease to phenotype
    :param dict_type: dict_type to create a dict with the names (default) or ids of the diseases and respective phenotypes
    :return: dict with the names or ids of type {disease1:[phenotype1, phenotype2, ...], }
    """

    disease2phenotype = open(file_d2p, 'r')
    disease2phenotype.readline()
    relations_d2p = disease2phenotype.readlines()
    relations_d2p.pop()
    disease2phenotype.close()

    if not dict_type:
        dict_diseaseID_phenotypeID = {}

    for line in relations_d2p:
        line = line.split('\t')
        diseaseID = line[1]
        disease_name = line[2].lower()
        phenotypeID = line[4].replace(':', '_')

        if diseaseID not in dict_diseaseID_phenotypeID:
                dict_diseaseID_phenotypeID[diseaseID] = []
                dict_diseaseID_phenotypeID[diseaseID].append(phenotypeID)

        if disease_name not in dict_diseaseID_phenotypeID:
                dict_diseaseID_phenotypeID[disease_name] = []
                dict_diseaseID_phenotypeID[disease_name].append(phenotypeID)   

        else:
            dict_diseaseID_phenotypeID[diseaseID].append(phenotypeID)

    return dict_diseaseID_phenotypeID


#########################################
#         RELATIONS ANNOTATIONS         #
#########################################

def relations_annotations(negation_path, gold_standard_file, annotations_path, destination_path):
    """Creates a file with the relations between disease and phenotype annotations for each negation sentence in each article of the corpus
       and counts the number of true and false relations between disease and phenotype annotations

    :param negation_path: negation sentences corpus path
    :param gold_standard_file: hpo gold standard file with negative relations disease to phenotype
    :param annotations_path: final annotations path
    :param destination_file_path: destination file path
    :return: file with the relations between disease and phenotype annotations for each negation sentence in each article of the corpus
             and a string with the number of true and false relations between disease and phenotype annotations
    """

    dict_hpo = hpo_dict(gold_standard_file)

    relations_file = open(destination_path, 'w', encoding = 'utf-8')
    relations_file.write('FILE_ID\tSENTENCE\tDISEASE\tPHENOTYPE\tDISEASE_ID\tPHENOTYPE_ID\tDISEASE_START_POSITION\tDISEASE_END_POSITION\tPHENOTYPE_START_POSITION\tPHENOTYPE_END_POSITION\tRELATION\n')

    for (dir_path, dir_names, file_names) in os.walk(annotations_path):
        for filename in file_names:

            try:  
                negation_file = open(negation_path + filename, 'r', encoding='utf-8') 
                negation_sentences = negation_file.readlines()
                negation_file.close()

            except FileNotFoundError:
                continue 

            final_annotations = open(annotations_path + filename, 'r', encoding='utf-8')
            list_annotations = final_annotations.readlines()
            final_annotations.close()

            for annotation in list_annotations:
                disease_annotations_list = []

                if 'omim' in annotation:
                    disease_first = annotation.split('\t')[0]
                    disease_last = annotation.split('\t')[1]
                    disease_name = annotation.split('\t')[2]
                    disease_id = annotation.split('https://www.omim.org/entry/')[1][:-1]

                    disease_annotations_list.append((disease_name, disease_id, disease_first, disease_last))

            for sentence in negation_sentences:
                sentence_position_count = sentence
                phenotype_annotations_list = []
                length = len(sentence[:-1])

                for annotation in list_annotations:
                    first_position = str(len(sentence_position_count.split(annotation.split('\t')[2], 1)[0]))
                    last_position = str(len(sentence_position_count.split(annotation.split('\t')[2], 1)[0]) + len(annotation.split('\t')[2]))
                    sentence_position_count = sentence_position_count.replace(annotation.split('\t')[2], len(annotation.split('\t')[2]) * 'A')

                    if int(last_position) < length:
                        if 'HP' in annotation:
                            phenotype_annotations_list.append((annotation.split('\t')[2], annotation.split('\t')[3][:-1].strip('http://purl.obolibrary.org/obo/'), \
                                                                first_position, last_position))

                if phenotype_annotations_list != [] and disease_annotations_list != []:

                    for phenotype_name, phenotype_id, phenotype_first, phenotype_last in phenotype_annotations_list:

                        for disease_name, disease_id, disease_first, disease_last in disease_annotations_list:

                            if disease_id in dict_hpo and phenotype_id in dict_hpo[disease_id]:

                                relation = 'True'

                            else:
                                relation = 'False'
				
                            relations_file.write(filename + '\t' + sentence[:-1] + '\t' + disease_name + '\t' + phenotype_name + \
                                                '\t' + disease_id + '\t' + phenotype_id + '\t' + disease_first + '\t' + disease_last + '\t' \
                                                + phenotype_first + '\t' + phenotype_last + '\t' + relation + '\n')


    relations_file.close()

    return


###############################
#            RUN              #
###############################

def main():
    """Creates a directory with a file for each retrieved abstract and full body
       article with their respective disease and human phenotype annotations 

    :return: directory with a file for each retrieved abstract and full body article with their respective disease and human
             phenotype annotations, and a file with negative relations between the annotated diseases and human phenotype
    """

    os.system('mkdir -p corpora/corpus_A/phenotypes || true')
    os.system('mkdir -p corpora/corpus_A/phenotype_synonyms || true')
    os.system('mkdir -p corpora/corpus_A/abstract_genes || true')
    os.system('mkdir -p corpora/corpus_A/article_genes || true')
    os.system('mkdir -p corpora/corpus_A/abstract_diseases || true')
    os.system('mkdir -p corpora/corpus_A/article_diseases || true')
    os.system('mkdir -p corpora/corpus_A/abstract_disease_abbreviations || true')
    os.system('mkdir -p corpora/corpus_A/article_disease_abbreviations || true')
    os.system('mkdir -p corpora/corpus_A/abstract_disease_synonyms || true')
    os.system('mkdir -p corpora/corpus_A/article_disease_synonyms || true')
    os.system('mkdir -p corpora/corpus_A/final_annotations || true')
    os.system('mkdir -p corpora/corpus_A/negation_in_articles || true')

    os.chdir('../bin/MER/')
    os.system('cd data; wget http://purl.obolibrary.org/obo/hp.owl')
    os.system('cd data; ../produce_data_files.sh hp.owl')
    os.system('cd data; ../produce_data_files.sh hpsynonym.txt')
    os.system('cd data; ../produce_data_files.sh diseases.txt')
    phenotype_annotations('../../corpus_A/negation_in_articles/', '../../corpus_A/phenotypes/', '../../corpus_A/phenotype_synonyms/', 'get_entities.sh')
    abstract_disease_annotations('../../corpus_A/abstracts/', '../../corpus_A/abstract_diseases/', 'get_entities.sh')
    article_disease_annotations('../../corpus_A/articles/', '../../corpus_A/article_diseases/', 'get_entities.sh')

    # MER directory where the get_entities.sh file is adapted to annotate up to 10 ids for the same entity
    os.chdir('../../corpora/MER/') 
    os.chdir('mv ../../data/get_entities.sh .')
    os.system('cd data; ../produce_data_files.sh genes.txt')
    os.system('cd data; ../produce_data_files.sh diseaseabbreviations.txt')
    os.system('cd data; ../produce_data_files.sh diseasesynonyms.txt')
    abstract_gene_annotations('../corpus_A/abstracts/', '../corpus_A/abstract_genes/', 'get_entities.sh')
    abstract_abbreviation_annotations('../corpus_A/abstracts/', '../corpus_A/abstract_disease_abbreviations/', 'get_entities.sh')
    abstract_synonym_annotations('../corpus_A/abstracts/', '../corpus_A/abstract_disease_synonyms/', 'get_entities.sh')
    article_gene_annotations('../corpus_A/articles/', '../corpus_A/article_genes/', 'get_entities.sh')
    article_abbreviation_annotations('../corpus_A/articles/', '../corpus_A/article_disease_abbreviations/', 'get_entities.sh')
    article_synonym_annotations('../corpus_A/articles/', '../corpus_A/article_disease_synonyms/', 'get_entities.sh')

    os.chdir('../corpus_A/') 
    sort_annotations_files('abstract_disease_abbreviations/', 'abstract_disease_synonyms/', 'abstract_diseases/', 'abstract_genes/', 'article_disease_abbreviations/', \
                           'article_disease_synonyms/', 'article_diseases/', 'article_genes/', 'phenotype_synonyms/', 'phenotypes/', 'final_annotations/')
    relations_annotations('negation_in_articles/', 'data/phenotype_annotation_negated.txt', 'final_annotations/', 'relations_corpus_A.tsv')

    return


if __name__ == "__main__":
    main()

