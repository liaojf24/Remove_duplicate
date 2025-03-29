# background
In bioinformatics and Deep learning research, there are too much work that requires us to remove duplicates and similiar DNA/RNA sequence. Otherwise, some severe problems, 
such as data leak will occur, reuslting a significant decrease in model performance. Here, I give a pipeline to teach bioinformatics/DL beginners how to remove similar DNA 
sequences before training DL model.

# Preparations
you should install bedtools.
# pipeline
For example, you have a dataset with 10,000 DNA fragemnts, you need to remove similar fragemnts. The file is: raw.fasta

Firstly, you need to blast the whole sequence, the threshold of similar is set 95%.
```
# create a db
 makeblastdb -in raw.fasta -dbtype nucl -out raw_db
# use blastn to align raw.fasta to raw_db database
blastn -query  raw.fasta -db raw_db -outfmt 6 -out blast_results.txt -evalue 1e-5 -perc_identity 95
```

Then, you need to remove sequences from the raw.fasta
```
cd src
python remove_duplicate.py \
--raw_data ../data/raw.fasta \
--blast ../data/blast_results.txt\
--output ../results/filtered.fasta
```

# Example
see example/example.ipynb

# LICENSE
his project is licensed under the MIT License - see the LICENSE file for details.


