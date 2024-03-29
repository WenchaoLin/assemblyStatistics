#!/usr/bin/env python

import sys
import re
import json
from optparse import OptionParser
from src.FastaUtils import FastaIO, Nx0, say
from src import __version__


def run(options):
    """Main method for collecting all Fasta stats"""

    threshold = options.length
    outfmt = options.format

    largestScaffoldName = None
    largestScaffoldLength = 0
    all_seq_list = []
    large_seq_list = []
    contig_seq_list = []

    n_cnt, gc_cnt, lg_n_cnt, lg_gc_cnt = 0, 0, 0, 0

    seqObj = FastaIO(options.fasta)
    for seq in seqObj:
        name = seq.id
        length = seq.length
        sequence = seq.seq
        all_seq_list.append(length)
        contig_seq_list += map(len, re.split('[nN]+', sequence))
        n_cnt += sequence.upper().count('N')
        gc_cnt += seq.gcCount

        if length > largestScaffoldLength:
            largestScaffoldName = name
            largestScaffoldLength = length

        if length > threshold:
            large_seq_list.append(length)
            lg_gc_cnt += seq.gcCount
            lg_n_cnt += sequence.upper().count('N')
    res_dic = {}
    res_dic['All scaffolds'] = {}
    res_dic['LARGE sequences'] = {}
    res_dic['Contigs'] = {}
    res_dic['LARGE sequences']['threshold'] = threshold
    res_dic['All scaffolds']['Counts of scaffold sequences'] = len(all_seq_list)
    res_dic['All scaffolds']['Length of scaffold sequences'] = sum(all_seq_list)
    res_dic['All scaffolds']['Largest scaffold name'] = largestScaffoldName
    res_dic['All scaffolds']['Largest scaffold length'] = largestScaffoldLength
    res_dic['All scaffolds']['Scaffold N50'] = Nx0(all_seq_list, 50)[0]
    res_dic['All scaffolds']['Counts of N50'] = Nx0(all_seq_list, 50)[1]
    res_dic['All scaffolds']['Scaffold N90'] = Nx0(all_seq_list, 90)[0]
    res_dic['All scaffolds']['Counts of N90'] = Nx0(all_seq_list, 90)[1]
    res_dic['All scaffolds']['GC content(%)'] = gc_cnt / sum(all_seq_list) * 100.0
    res_dic['All scaffolds']['N Length'] = n_cnt
    res_dic['All scaffolds']['N content (%)'] = n_cnt / sum(all_seq_list) * 100.0
    if large_seq_list:
        res_dic['LARGE sequences']['Counts of LARGE sequences'] = len(large_seq_list)
        res_dic['LARGE sequences']['Length of LARGE sequences'] = sum(large_seq_list)
        res_dic['LARGE sequences']['LARGE N50'] = Nx0(large_seq_list, 50)[0]
        res_dic['LARGE sequences']['Counts of N50'] = Nx0(large_seq_list, 50)[1]
        res_dic['LARGE sequences']['LARGE N90'] = Nx0(large_seq_list, 90)[0]
        res_dic['LARGE sequences']['Counts of LARGE N90'] = Nx0(large_seq_list, 90)[1]
        res_dic['LARGE sequences']['GC content(%)'] = lg_gc_cnt / sum(large_seq_list) * 100.0
        res_dic['LARGE sequences']['N Length'] = lg_n_cnt
        res_dic['LARGE sequences']['N content (%)'] = lg_n_cnt / sum(large_seq_list) * 100.0
    else:
        res_dic['LARGE sequences']['Counts of LARGE sequences'] = 0
        res_dic['LARGE sequences']['Length of LARGE sequences'] = 0
    res_dic['Contigs']['Counts of contigs'] = len(contig_seq_list)
    res_dic['Contigs']['Maximum length'] = max(contig_seq_list)
    res_dic['Contigs']['contig N50'] = Nx0(contig_seq_list, 50)[0]
    res_dic['Contigs']['Counts of contig N50'] = Nx0(contig_seq_list, 50)[1]
    res_dic['Contigs']['contig N90'] = Nx0(contig_seq_list, 90)[0]
    res_dic['Contigs']['Counts of contig N90'] = Nx0(contig_seq_list, 90)[1]

    if outfmt.upper() == 'JSON':
        print(json.dumps(res_dic, indent=4))
    
    else:
        print('\nAll scaffold sequences summary:')
        print('-' * 50)
        say('Counts of scaffold sequences', len(all_seq_list))
        say('Length of scaffold sequences', sum(all_seq_list))
        say('Largest scaffold name', largestScaffoldName)
        say('Largest scaffold length', largestScaffoldLength)
        say('Scaffold N50 ', Nx0(all_seq_list, 50)[0])
        say('Counts of N50', Nx0(all_seq_list, 50)[1])
        say('Scaffold N90', Nx0(all_seq_list, 90)[0])
        say('Counts of N90', Nx0(all_seq_list, 90)[1])
        say('GC content(%)', gc_cnt / sum(all_seq_list) * 100.0)
        say('N Length', n_cnt)
        say('N content (%)',  n_cnt / sum(all_seq_list) * 100.0)
        print('\nLARGE (> %s bp) sequences summary:' % threshold)
        print('-' * 50)
        if large_seq_list:
            say('Counts of LARGE sequences', len(large_seq_list))
            say('Length of LARGE sequences', sum(large_seq_list))
            say('LARGE scaffold N50', Nx0(large_seq_list, 50)[0])
            say('Counts of LARGE N50', Nx0(large_seq_list, 50)[1])
            say('LARGE scaffold N90', Nx0(large_seq_list, 90)[0])
            say('Counts of LARGE N90', Nx0(large_seq_list, 90)[1])
            say('GC content(%)', lg_gc_cnt / sum(large_seq_list) * 100.0)
            say('N Length', lg_n_cnt)
            say('N content (%)', lg_n_cnt / sum(large_seq_list) * 100.0)
        else:
            say('Counts of LARGE sequences', 0)
            say('Length of LARGE sequences', 0)
        print('\ncontigs summary:')
        print('-'*50)
        say('Counts of contigs', len(contig_seq_list))
        say('Maximum length of contigs', max(contig_seq_list))
        say('contig N50', Nx0(contig_seq_list, 50)[0])
        say('Counts of contig N50', Nx0(contig_seq_list, 50)[1])
        say('contig N90', Nx0(contig_seq_list, 90)[0])
        say('Counts of contig N90', Nx0(contig_seq_list, 90)[1])

def main():

    """ parse options """
    usage = 'usage: %prog [options] -f INPUT.fasta'
    parser = OptionParser(prog='assemblyStatistics',
                          description='A script to evaluate the assembly of a given fasta.',
                          usage=usage,
                          version=__version__,
                          )
    parser.add_option('-f', '--fasta',
                      dest='fasta', metavar='FILE',
                      help='input fasta file'
                      )
    parser.add_option('-t', '--outfmt',
                      dest="format",
                      type='choice',
                      choices=['txt','json'],
                      default='txt',
                      help='format of the output, choices = [txt, json]'
                      )
    parser.add_option('-l', '-L', '--length',
                      dest='length', default=1000, type=int,
                      help='Threshold of length defined a sequence as Large [default = 1000]'
                      )

    (options, args) = parser.parse_args()
    if not options.fasta:
        try:
            options.fasta = args[0]
        except IndexError:
            parser.print_help()
            sys.exit()

    run(options)


if __name__ == "__main__":

    main()
