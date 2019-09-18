Input files
===========
FusionVet needs two types of input files. 

BAM file
--------
`BAM <https://en.wikipedia.org/wiki/SAM_(file_format)>`_ file must be sorted and indexed using `samtools <http://samtools.sourceforge.net/>`_

gene fusion file
----------------
The gene fusion file is a
plain text file with 8 columns separated by space or tab (The first 4 columns describe
the "chrom", "transcription_start", "transcription_end" and "symbol" of gene-1, the other 4 columns
describe the same information for gene-2. Below example file defines two fusions:

::

 chr21   39739182        40033704        ERG     chr21   42836477        42880085        TMPRSS2
 chr14   38033152        38033701        EST14         chr7    13930855        14031050        ETV1 
