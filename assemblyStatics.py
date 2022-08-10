#!/usr/bin/python
__author__ = "Wenchao Lin"
__copyright__ = "Copyright 2015, TBC"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Wenchao Lin"
__email__ = "linwenchao@yeah.net"
__status__ = "Release"


import FastaUtils
import sys
import re
from optparse import OptionParser

def run(options):
    '''
    
    '''

    
    largeThreshold = options.large

    largestScaffoldName = ''
    largestScaffoldLength = 0
    countOfLargeSequence = 0
    totalGC = 0
    largeGC = 0
    lengthOfLargeSequence = 0
    countOfNs = 0
    allLenList = []
    largeLenList = []
    contigList = []
    largeN = 0
    totalN = 0
    
    
    obj = FastaUtils.load(open(options.fasta, 'r'))
    
    for fa in obj:

        name = fa.name
        length = fa.length
        seq = fa.seq
        contigList += map(len, re.split('N+', seq))
        if fa.length > largestScaffoldLength:
            largestScaffoldName = name
            largestScaffoldLength = length
        if fa.length > largeThreshold :
            largeLenList.append(length)
            largeGC += seq.count('G') + seq.count('g')+ seq.count('c')+ seq.count('C')
            largeN += seq.count('N') + seq.count('n')
            
        lengthOfLargeSequence = sum(largeLenList)
        countOfLargeSequence = len(largeLenList)
        allLenList.append(length)
        totalGC += seq.count('G') + seq.count('g')+ seq.count('c')+ seq.count('C')
        totalN += seq.count('N') + seq.count('n')
        
    totalLength = sum(allLenList)
    totalCount = len(allLenList)
        
    print '\nAll scaffold sequences summary:'
    print '-----------------------------------'
    say('Counts of scaffold sequences', totalCount)
    say('Length of scaffold sequences', sum(allLenList))
    say('Largest scaffold name', largestScaffoldName)    
    say('Largest scaffold length', largestScaffoldLength)    
    say('Scaffold N50', FastaUtils.Nx0(allLenList, 50)[0])
    say('Counts of N50', FastaUtils.Nx0(allLenList, 50)[1])
    say('Scaffold N90', FastaUtils.Nx0(allLenList, 90)[0])
    say('Counts of N90', FastaUtils.Nx0(allLenList, 90)[1])
    try:
        sayPercent('GC content(%)', float(totalGC) / lengthOfLargeSequence * 100)
        say('N Length', totalN)
        sayPercent('N content (%)',  float(totalN) / lengthOfLargeSequence * 100)
    except ZeroDivisionError:
        sayPercent('GC content(%)', 0)
        say('N Length', 0)
        sayPercent('N content (%)', 0)
        
    
    print '\nLARGE (> %sbp) sequences summary:' % (largeThreshold)
    print '-----------------------------------'
    say('Counts of LARGE sequences', countOfLargeSequence)
    say('Length of LARGE sequences', lengthOfLargeSequence)
    say('LARGE scaffold N50', FastaUtils.Nx0(largeLenList, 50)[0])
    say('Counts of LARGE N50', FastaUtils.Nx0(largeLenList, 50)[1])
    say('LARGE scaffold N90', FastaUtils.Nx0(largeLenList, 90)[0])
    say('Counts of LARGE N90', FastaUtils.Nx0(largeLenList, 90)[1])
    try:
        sayPercent('GC content(%)', float(largeGC) / lengthOfLargeSequence * 100)
        say('N Length', largeN)
        sayPercent('N content (%)', float(largeN) / lengthOfLargeSequence * 100)
    except ZeroDivisionError:
        sayPercent('GC content(%)', 0)
        say('N Length', 0)
        sayPercent('N content (%)', 0)        
        
    
    print '\ncontigs summary:'
    print '-----------------------------------'
    say('Counts of contigs',len(contigList))
    say('Maximum length of contigs',max(contigList))
    say('contig N50', FastaUtils.Nx0(contigList, 50)[0])
    say('Counts of contig N50', FastaUtils.Nx0(contigList, 50)[1])
    say('contig N90', FastaUtils.Nx0(contigList, 90)[0])
    say('Counts of contig N90', FastaUtils.Nx0(contigList, 90)[1])    
    


def say(notes, value):
    '''format output'''
    
    print('%30s:\t%s' % (notes, value))
    return 1

def sayPercent(notes, value):
    '''Percent format output'''
    
    print('%30s:\t%.5s%%' % (notes, value))
    return 1
    
    
def parseArgs():
    '''
    parse options
    '''
    usage = 'usage: %prog [options] -f INPUT.fasta'
    parser = OptionParser(usage = usage) 
    parser.add_option('-f', '--fasta', 
                      dest='fasta', metavar = 'FILE', 
                      help='input fasta file')
    parser.add_option('-L', '--large',
                      dest = 'large', default = 1000, type = int, 
                      help = 'Threshold of LARGE sequence [default = 1000]')
    
    (options, args) = parser.parse_args()
    if not options.fasta:
            parser.print_help()
            sys.exit()
    return options


if __name__ == '__main__':
    
    options = parseArgs()
    run(options)
