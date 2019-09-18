Usage
======

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -b INPUT_BAM, --bam=INPUT_BAM
                        Input BAM file. The BAM file should be sorted and
                        indexed using SAMtools
                        (http://samtools.sourceforge.net/). (mandatory)
  -c INPUT_CHIMERAS, --chimeras=INPUT_CHIMERAS
                        Fusion file. This file can be 6 columns (chr1 start1
                        end1 chr2 start2 end2) or 8 columns (chr1 start1 end1
                        name1 chr2 start2 end2 name2) separated by Tab or
                        Space. Lines starting with '#' will be ignored.
                        (mandatory)
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        Prefix of output files. Four files will be created
                        including "prefix.fusion.sorted.bam",
                        "prefix.fusion.bed", "prefix.fusion.interact.bed" and
                        "prefix.fusion.summary.txt". (mandatory)
  -q MAP_QUAL, --mapq=MAP_QUAL
                        Mapping quality cutoff. default=30
  -t, --track-header    If set, add "track line" to the BED file.
  -k, --keep-unknown-mapq
                        If set, keep alignments with unknown mapping quality
                        (i.e., MAPQ = 255).