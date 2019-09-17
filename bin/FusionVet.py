#!/usr/bin/env python3

import sys
from time import strftime
from os.path import basename
from optparse import OptionParser
#from subprocess import call
from vetmodule.ReadFusion import get_coord
from vetmodule.AberrantRead import get_aberrant_reads
from vetmodule.BamToBed import bam2bed

__author__ = "Liguo Wang"
__contributor__="Liguo Wang"
__copyright__ = "Copyright 2019, Mayo Clinic"
__credits__ = []
__license__ = "GPL"
__version__="1.0.1"
__maintainer__ = "Liguo Wang"
__email__ = "wang.liguo@mayo.edu"
__status__ = "4 - Beta"


if __name__=='__main__':
        
    usage="%prog [options]" + '\n'
    parser = OptionParser(usage,version="%prog " + __version__)
    parser.add_option("-b","--bam",action="store",type="string",dest="input_bam",help="Input BAM file. The BAM file should be sorted and indexed using SAMtools (http://samtools.sourceforge.net/). (mandatory)")
    parser.add_option("-c","--chimeras",action="store",type="string",dest="input_chimeras",help="Fusion file. This file can be 6 columns (chr1 start1 end1 chr2 start2 end2) or 8 columns (chr1 start1 end1 name1 chr2 start2 end2 name2) separated by Tab or Space. Lines starting with '#' will be ignored. (mandatory)")
    parser.add_option("-o","--output",action="store",type="string",dest="output_file",help="Prefix of output files. Four files will be created including \"prefix.fusion.sorted.bam\", \"prefix.fusion.bed\", \"prefix.fusion.interact.bed\" and \"prefix.fusion.summary.txt\". (mandatory)")
    parser.add_option("-q","--mapq",action="store",type="int",dest="map_qual",default=30,help="Mapping quality cutoff. default=%default")
    parser.add_option("-t","--track-header",action="store_true",default=False,dest="header",help="If set, add \"track line\" to the BED file.")
    parser.add_option("-k","--keep-unknown-mapq",action="store_true",default=False,dest="keep",help="If set, keep alignments with unknown mapping quality (i.e., MAPQ = 255).")
    (options,args)=parser.parse_args()
    
    #print (options.keep)
    #sys.exit()
    if not (options.input_bam and options.input_chimeras and options.output_file):
        parser.print_help()
        sys.exit(0)
    
    
    
    candidate_list = []
    print("@ " + strftime("%Y-%m-%d %H:%M:%S") + ": Get genome coordinates of fusion genes from file \"%s\" ... "  % options.input_chimeras, file=sys.stderr)
    for (chr1, st1, end1,name1,chr2, st2, end2,name2) in get_coord(options.input_chimeras):
        candidate_list.append(name1 + '--' + name2)  


    STAT = open(options.output_file + '.fusion.summary.txt', 'w')
    print("Sample_ID\t" + '\t'.join(candidate_list), file=STAT)
    
    (RF) = get_aberrant_reads(options.input_bam, options.input_chimeras,  options.output_file, q_cut = options.map_qual, keep_unknown = options.keep)
    print(basename(options.input_bam)  + '\t' + '\t'.join([str(RF[k]) for k in candidate_list]), file = STAT)
    print("@ " + strftime("%Y-%m-%d %H:%M:%S") + ": Save results to file \"%s\" "  % (options.output_file + '.fusion.summary.txt'), file=sys.stderr)
    STAT.close()
    
    print("@ " + strftime("%Y-%m-%d %H:%M:%S") + ": Convert and consolidate fusion supporting reads into BED format file \"%s\" and Intersection format file \"%s\""  % (options.output_file + '.fusion.bed', options.output_file + '.fusion.interact.bed'), file=sys.stderr)
    bam2bed(options.output_file + '.fusion.sorted.bam', options.output_file + '.fusion.bed',track_header = options.header, interact_file = options.output_file + '.fusion.interact.bed', q_cut = options.map_qual)
    
    
    		
		
		
		
