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

# transliterate for reverse complement
try:
    import string
    trans = string.maketrans('ACGTacgt', 'TGCAtgca')
except AttributeError:
    trans = str.maketrans('ACGTacgt', 'TGCAtgca')
# re for fasta header
r = re.compile("^>(?P<name>\S+)(\s(?P<desc>.*))?")


class Fasta(object):
    """ Simple class to store a fasta formatted sequence """
    
    def __init__(self, name, desc, seq):
        self.name = name
        self.desc = desc
        self.seq = seq
        #self.gc = gcContent(self.seq)
        self.length = len(seq)
        
    def __str__(self):
        """ Output FASTA format of sequence when 'print' method is called """
        s = []
        for i in range(0, self.length, 80):
            s.append(self.seq[i:i+80])
        if self.desc:
            return ">%s %s\n%s" % (self.name, self.desc, "\n".join(s))
        else:
            return ">%s\n%s" % (self.name, "\n".join(s))
    
    def reverse_complement(self):
        """ Reverse complement sequence, return new Fasta object """
        rcseq = self.seq[::-1].translate(trans)
        return Fasta(self.name, self.desc, rcseq)


def gcContent(seq):
    """return gc content"""
    gc = seq.count('G') + seq.count('g')+ seq.count('c')+ seq.count('C')
    gcContent = float(gc) / len(seq)
    return gcContent


def Nx0(listOfNumbers, x = 50):
    """return Nx0 of an given list of numbers"""
    listOfNumbers.sort(reverse=1)
    theorNx0 = sum(listOfNumbers) * x / 100
    
    tot = 0
    Nx0 = 0
    CNx0 = 0
    
    for num in listOfNumbers:
        tot += num
        CNx0 += 1
        if tot >= theorNx0:
            Nx0 = num
            break
    return (Nx0, CNx0)


def load(f):
    """ Parameter: HANDLE to input in Fasta format
        e.g. sys.stdin, or open(<file>)
        Returns array of Fasta objects."""
    name, desc, seq = '', '', ''
    seqs = []
    while True:
        line = f.readline()
        if not line:
            break
        
        if line[0] == '>' and (line[1:].find(">") == -1):
            if seq != '':
                seqs.append(Fasta(name, desc, seq))

            seq = r''
            m = r.match(line)
            name = m.group("name")
            desc = m.group("desc")
        else:
            seq += line.strip()

    seqs.append(Fasta(name, None, seq))
    return seqs


if __name__ == "__main__":
    
    test = [10,20,30,40,50]
    m = Nx0(test, 50)
    print(m)