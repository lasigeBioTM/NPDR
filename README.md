# NPDR: A Dataset of Negative Human Phenotype-Disease Relations

The Negative Phenotype-Disease Relations (NPDR) dataset describes a subset of negative disease­-phenotype relations from a [gold-standard knowledge base](http://purl.obolibrary.org/obo/hp/hpoa/phenotype_annotation_negated.tab) made available by the Human Phenotype Ontology. 
The NPDR dataset was constructed by analysing 177 medical documents, and consists of 347 manually annotated at the document-level relations, from which 222 are inferred from the HPO gold-standard knowledge base, and 125 are new annotated relations. 

In order to automatically annotate the entities mentioned in the NPDR dataset and extract their negative relations, an automatic extraction system was developed. If you intend to annotate entities using the lexica generated from the NPDR dataset and extract negative relations from biomedical documents, you can follow the below guidelines.

## Dependencies

* Python >= 3.8

* Pre-processing:
    * [PDFMiner](https://github.com/pdfminer/pdfminer.six)
    * [Genia Sentence Splitter](http://www.nactem.ac.uk/y-matsu/geniass/)
    
* Term Recognition:
    * [MER (Minimal Named-Entity Recognizer)](https://github.com/lasigeBioTM/MER) (Phenotype, Disease and Gene Entities)
        
* Relation Extraction:
    * [Human Phenotype Ontology Gold Standard Negative Relations](http://purl.obolibrary.org/obo/hp/hpoa/phenotype_annotation_negated.tab) (Knowledge Base)
    
## Getting Started

````
cd bin/
git clone https://github.com/lasigeBioTM/MER 

cd ../corpora/
git clone https://github.com/pdfminer/pdfminer.six
git clone https://github.com/lasigeBioTM/MER 
````

## Preparing the Biomedical Documents

There are two approaches that can be used to gather the biomedical documents:
1. By automatically retrieving PubMed articles using the [Entrez Programming Utilities (E-utilities) program](https://www.ncbi.nlm.nih.gov/books/NBK25501/) ([Corpus A](./corpora/corpus_A/)). 
2. By converting PDF articles into machine-readable text format using the [PDFMiner text converter tool](https://github.com/pdfminer/pdfminer.six) ([Corpus B](./corpora/corpus_B/)).

If you intend to automatically retrieve the biomedical documents run:
````
 python3 src/pubmed.py
````
* Creates: 
    * **corpora/corpus_A/articles**
    * **corpora/corpus_A/abstracts**    

If you intend to convert PDF documents, place the documents in the [PDF_files](corpora/PDF_files/) directory and run:
````
 python3 src/pdf2text.py
````

## Annotating Genes, Diseases, Human Phenotypes and Relations

1. If using Corpus A run:
````
 python3 src/annotations_corpus_A.py
````
* Creates: 
    * **corpora/corpus_A/phenotypes/** 
    * **corpora/corpus_A/phenotype_synonyms/** 
    * **corpora/corpus_A/abstract_genes/** 
    * **corpora/corpus_A/article_genes/** 
     * **corpora/corpus_A/abstract_diseases/** 
     * **corpora/corpus_A/article_diseases/** 
     * **corpora/corpus_A/abstract_disease_abbreviations/**
     * **corpora/corpus_A/article_disease_abbreviations/**
     * **corpora/corpus_A/abstract_disease_synonyms/**
     * **corpora/corpus_A/article_disease_synonyms/**
     * **corpora/corpus_A/final_annotations/**
     * **corpora/corpus_A/negation_in_articles/**
    * __corpora/corpus_A/relations_corpus_A.tsv__
    
2. If using Corpus B run:
````
 python3 src/annotations_corpus_B.py
````
* Creates: 
    * **corpora/corpus_B/phenotypes/** 
    * **corpora/corpus_B/phenotype_synonyms/** 
    * **corpora/corpus_B/genes/** 
    * **corpora/corpus_B/diseases/** 
    * **corpora/corpus_B/disease_abbreviations/**
    * **corpora/corpus_B/disease_synonyms/**
    * **corpora/corpus_B/final_annotations_corpus_B/**
    * __corpora/corpus_B/relations_corpus_A.tsv__

## Configuration

* ### bin/
    * **MER/**
        * **data/**
            * __diseases.txt__
            * __diseases_links.tsv__
            * __hpsynonym.txt__
            * __hpsynonym_links.tsv__
            * __hp.owl__
            * __hp_links.tsv__
    * **geniass/**
    
* ### corpora/

    * **MER/**
        * **data/**
            * __diseaseabbreviations.txt__
            * __diseaseabbreviations_links.tsv__
            * __diseasesynonyms.txt__
            * __diseasesynonyms_links.tsv__
            * __genes.txt__
            * __genes_links.tsv__
    * **corpus_A/**
        * **abstract_disease_abbreviations/**
        * **abstract_disease_synonyms/**
        * **abstract_diseases/**
        * **abstract_genes/**
        * **abstracts/**
        * **article_disease_abbreviations/**
        * **article_disease_synonyms/**
        * **article_diseases**
        * **article_genes** 
        * **articles/**
        * **final_annotations/**
        * **negation_in_articles/**
        * **phenotype_synonyms/**
        * **phenotypes/**
    * **corpus_B/**
        * **articles/**
        * **disease_abbreviations/**
        * **disease_synonyms/**
        * **diseases/**
        * **final_annotations/**          
        * **genes/**
        * **negation_in_articles/**
        * **phenotype_synonyms/**
        * **phenotypes/**

* ### data/
    * __get_entities.sh__
    * __phenotype_annotation_negated.txt__
    * __pmids.txt__
    
* ### src/
    * **annotations_corpus_A.py**
    * **annotations_corpus_B.py**
    * **pdf2text.py**
    * **pubmed.py**
