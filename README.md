Synopsis
========

A simple program for evaluate the assembly of a give genome. Shows simple statistics about a fasta file containing many sequences. The result includes the name, N50, N90, GC Content, N rate, number of sequences etc., as well as various other information both in large scaffolds (>1000 bp) and in all sequences. 

USAGE
-----


```
Usage: assemblyStatics.py [options] -f INPUT.fasta

Options:
  -h, --help            show this help message and exit
  -f FILE, --fasta=FILE
                        input fasta file
  -L LARGE, --large=LARGE
                        Threshold of LARGE sequence [default = 1000]


```



```
python assemblyStatics.py -f duixia.SSPACE2.final.scaffolds_new.fasta
```

Sample output
-------------
```

All scaffold sequences summary:
-----------------------------------
  Counts of scaffold sequences:	16551
  Length of scaffold sequences:	1413526492
         Largest scaffold name:	scaffold229_size1132254|ref0002838
       Largest scaffold length:	1132254
                  Scaffold N50:	154152
                 Counts of N50:	2599
                  Scaffold N90:	40011
                 Counts of N90:	9491
                 GC content(%):	35.88%
                 N content (%):	4.018%

LARGE (>1000bp) sequences summary:
-----------------------------------
     Counts of LARGE sequences:	16549
     Length of LARGE sequences:	1413524983
            LARGE scaffold N50:	154152
           Counts of LARGE N50:	2599
            LARGE scaffold N90:	40011
           Counts of LARGE N90:	9491
                 GC content(%):	35.88%
                 N content (%):	56805%

contigs summary:
-----------------------------------
             Counts of contigs:	36707
     Maximum length of contigs:	848414
                    contig N50:	59299
          Counts of contig N50:	6486
                    contig N90:	16287
          Counts of contig N90:	23604

```
