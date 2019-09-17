.. FusionVet documentation master file, created by
   sphinx-quickstart on Thu Sep  5 00:17:09 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Introduction
=============
Gene fusion is one of the most common somatic alterations that plays an important role in
tumorgenesis. Well-known examples include the intra-chromosomal TMPRSS2-ERG fusions
in prostate cancer, and the inter-chromosomal BCR-ABL fusions in chronic myelogenous
leukemia (CML). With the advent of next generation sequencing technologies especially RNA-seq
and the development of dozens of fusion detection tools, most recurrent
gene fusions in common cancers have been identified. These fusion are cataloged in databases 
such as `COSMIC <https://cancer.sanger.ac.uk/cosmic/fusion>`_ , 
`FusionGDB <https://ccsm.uth.edu/FusionGDB>`_
, `FusionHub <https://fusionhub.persistent.co.in>`_, 
`ChimerDB <http://203.255.191.229:8080/chimerdbv31/mhelp.cdb>`_ 
and `TumorFusions <https://tumorfusions.org>`_ ).

To facilitate molecular testing, we developed FusionVet (Fusion Visualization and
Evaluation Tool) to quickly (and accurately) examine if a gene fusion with clinical
significance exists in a particular sample.

Input files
===========
FusionVet needs two input files: one is `BAM <https://en.wikipedia.org/wiki/SAM_(file_format)>`_
file (must be sorted and indexed), another one is gene fusion file. The gene fusion file is a
plain text file with 8 columns separated by space or tab (The first 4 columns describe
the "chrom", "transcription_start" and "transcription_end" of gene-1, the other 4 columns
describe the same information for gene-2). Below example file defines two fusions:

::

 chr21   39739182        40033704        ERG     chr21   42836477        42880085        TMPRSS2
 chr14   38033152        38033701        EST14         chr7    13930855        14031050        ETV1 

Output files
============

Performance
=============
FusionVet takes *less than 2 seconds* to scan a gene fusion from a typical
`TCGA <https://www.cancer.gov/about-nci/organization/ccg/research/structural-genomics/tcga>`_
RNA-seq `BAM <https://en.wikipedia.org/wiki/SAM_(file_format)>`_ file. 