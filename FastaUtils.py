#!/usr/bin/python
################################################################################
#
# Wenchaolin, 2015 @ Tianjin Biochip
# 
# Module with a Class to represent a Fasta sequence, 
# and methods to load Fasta-formatted sequences from a file.
#
################################################################################
from __future__ import print_function, division, absolute_import, with_statement
import re
from abc import ABC
from abc import abstractmethod

def say(*args, indent = 40, decimal = 2):
    """format output in left aligned table"""
    out_fmt = ''
    for v in args:
        if isinstance(v , float):
            out_fmt += '{:<%s.%sf}' % (indent, decimal)
        else:
            out_fmt += '{:<%s}' % indent
    print(out_fmt.format(*args))



def seq_gc_content(sequence):
    """return gc content"""
    gc_content = (sequence.upper().count('G') + sequence.upper().count('C')) / len(sequence) * 100
    return gc_content


def seq_gc_skew(sequence):
    """return: gc skew in percent"""
    gc_content = seq_gc_content(sequence)
    if gc_content == 0:
        gc_skew = 0
    else:
        gc_skew = (sequence.upper().count('G') - sequence.upper().count('C')) / (sequence.count('G') + sequence.count('C')) * 100
    return gc_skew


def Nx0(listOfNumbers, x = 50):
    """
    x is the Nx0 to be calculated, e.g. x = 50 for N50
    return Nx0 of an given list of numbers
    """
    listOfNumbers.sort(reverse=1)  # sort the list in descending order
    theorNx0 = sum(listOfNumbers) * x / 100  # calculate the theoretical Nx0
    
    tot = 0
    Nx0 = 0
    CNx0 = 0
    
    for num in listOfNumbers:
        tot += num
        CNx0 += 1
        if tot >= theorNx0:  # if the total is greater than or equal to the theoretical Nx0
            Nx0 = num
            break
    return (Nx0, CNx0)



def SimpleFastaParser(handle):
    """Iterate over Fasta records as string tuples.
    Arguments:
     - handle - input stream opened in text mode
    For each record a tuple of two strings is returned, the FASTA title
    line (without the leading '>' character), and the sequence (with any
    whitespace removed). The title line is not divided up into an
    identifier (the first word) and comment or description.
    >>> with open("Fasta/dups.fasta") as handle:
    ...     for values in SimpleFastaParser(handle):
    ...         print(values)
    ...
    ('alpha', 'ACGTA')
    ('beta', 'CGTC')
    ('gamma', 'CCGCC')
    ('alpha (again - this is a duplicate entry to test the indexing code)', 'ACGTA')
    ('delta', 'CGCGC')
    """
    # Skip any text before the first record (e.g. blank lines, comments)
    for line in handle:
        if line[0] == ">":
            title = line[1:].rstrip()
            break
    else:
        # no break encountered - probably an empty file
        return

    lines = []
    for line in handle:
        if line[0] == ">":
            yield title, "".join(lines).replace(" ", "").replace("\r", "")
            lines = []
            title = line[1:].rstrip()
            continue
        lines.append(line.rstrip())

    yield title, "".join(lines).replace(" ", "").replace("\r", "")



class FastaIO:
    """Base class for building SeqRecord iterators.
    You should write a parse method that returns a SeqRecord generator.  You
    may wish to redefine the __init__ method as well.
    """

    def __init__(self, source):
        """Create a SequenceIterator object.
        Arguments:
        - source - input file stream, or path to input file
        """

        try:
            self.stream = open(source, "r" )
            self.should_close_stream = True
        except Exception:
            "Open file error."

        try:
            self.records = self.parse(self.stream)
        except Exception:
            if self.should_close_stream:
                self.stream.close()
            raise

    def __next__(self):
        """Return the next entry."""
        try:
            return next(self.records)
        except Exception:
            if self.should_close_stream:
                self.stream.close()
            raise

    def __iter__(self):
        """Iterate over the entries as a SeqRecord objects.
        Example usage for Fasta files::
            with open("example.fasta","r") as myFile:
                myFastaReader = FastaIterator(myFile)
                for record in myFastaReader:
                    print(record.id)
                    print(record.seq)
        This method SHOULD NOT be overridden by any subclass. It should be
        left as is, which will call the subclass implementation of __next__
        to actually parse the file.
        """
        return self
    

    def parse(self, handle):
        """Start parsing the file, and return a SeqRecord generator."""
        records = self.iterate(handle)
        return records

    def iterate(self, handle):
        """Parse the file and generate SeqRecord objects."""

        for title, sequence in SimpleFastaParser(handle):
            try:
                first_word = title.split(None, 1)[0]
            except IndexError:
                assert not title, repr(title)
                first_word = ""
            yield SeqRecord(sequence, id=first_word, name=first_word, description=title
            )
    

class SeqRecord:
    """A SeqRecord object holds a sequence and information about it.
    Main attributes:
     - id          - Identifier such as a locus tag (string)
     - seq         - The sequence itself (Seq object or similar)

    Additional attributes:
     - description - Additional text (string)
    """
    
    def __init__(self, sequence,id = None, name = None, description = None):

        """Create a SeqRecord.
        Arguments:
         - sequence      - Sequence, required
         - id            - Sequence id, (first word after >)
         - name          - Sequence name, (first word after >)
         - description   - Sequence description
        """
       
        self.id = id
        self.name = name
        self.seq = sequence
        self.description = description


    @property
    def length(self):
        """return length."""
        return len(self.seq)
    
    @property
    def gcCount(self):
        """return: The GC count of the string"""

        return self.seq.count('C') + self.seq.count('c')+self.seq.count('G')+self.seq.count('g')
    

    def __len__(self):
        """ Return the length of the sequence"""
        return self.length 
        
    def __str__(self):
        """Output FASTA format of sequence when 'print' method is called"""
        s = []
        for i in range(0, len(self), 80):
            s.append(self.seq[i:i+80])

        return ">%s\n%s" % (self.description, "\n".join(s))
    
    @staticmethod
    def rev_comp(self):
        """return: The reverse complement of the string"""
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
        return ''.join([complement[base] for base in self.seq[::-1]])



if __name__ == "__main__":
    
    test = [10,20,30,40,50]
    m = Nx0(test, 50)
    print(m)