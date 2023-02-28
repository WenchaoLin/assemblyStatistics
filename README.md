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
  -l LARGE, -L LARGE, --large=LARGE
                        Threshold of LARGE sequence [default = 1000]
```



```
python assemblyStatics.py -f test.fasta -l 100
```

Sample output
-------------
```

All scaffold sequences summary:
--------------------------------------------------
Counts of scaffold sequences            3                                       
Length of scaffold sequences            490                                     
Largest scaffold name                   seq1                                    
Largest scaffold length                 210                                     
Scaffold N50                            210                                     
Counts of N50                           2                                       
Scaffold N90                            70                                      
Counts of N90                           3                                       
GC content(%)                           42.86                                   
N Length                                141                                     
N content (%)                           28.78                                   

LARGE (> 100 bp) sequences summary:
--------------------------------------------------
Counts of LARGE sequences               2                                       
Length of LARGE sequences               420                                     
LARGE scaffold N50                      210                                     
Counts of LARGE N50                     1                                       
LARGE scaffold N90                      210                                     
Counts of LARGE N90                     2                                       
GC content(%)                           33.33                                   
N Length                                141                                     
N content (%)                           33.57                                   

contigs summary:
--------------------------------------------------
Counts of contigs                       7                                       
Maximum length of contigs               70                                      
contig N50                              70                                      
Counts of contig N50                    3                                       
contig N90                              36                                      
Counts of contig N90                    5     
```
