import pysam
import collections
import os,sys
from time import strftime

from vetmodule.Overlap import is_overlap
from vetmodule.ReadFusion import get_coord

def get_aberrant_reads(bam_file, coord_file, out_file, q_cut):
	'''
	Extract reads supporting gene fusions and save them into separate BAM and BED files.
	Two type of reads will be identified including "split read" and "read pairs". A "split
	read" will be identified if, after split mapping, one end is mappped to gene A, and another
	end is mapped to gene B. A "read pair" will be identified if read-1 is mapped to gene
	A and read-2 is mapped to gene B. A "split read" (one read) and a "read pairs" 
	(two reads) are *equivalent* in identifying gene fusions, thus they are all called a "
	supporting RNA fragment".  
	
	
	Parameters
	----------
	bam_file : str
		Name of input BAM file
	coord_file : str
		Name of input file containing gene fusions. This file can be 6 columns (chr1	
		start1	end1	chr2	start2	end2) or 8 columns (chr1	start1	end1	
		name1	chr2	start2	end2	name2) separated by Tab. lines starting with '#'
		will be skipped.
	out_file : str
		Prefix of output files. "out_file.fusion.bam" will be created.
	q_cut : int
		Mapping quality score cutoff. 	
	
	Notes
	------
	
	* Input BAM file must be sorted and indexed. 
	* In the output BAM file, two tags are added to each alignment record: "SR" (supporting read): 
	  and "FZ" (fusion check).
	  "SR" takes three values:
	  	SR = 1: fusion is only supported by a split read
	  	SR = 2: fusion is only supported by a read pair
		SR = 3: fusion is supported by bot split read and read pair
	  "FZ" takes one string value indicating fusion (such as "ERG-TMPRSS2") 
	'''
	
	print("@ " + strftime("%Y-%m-%d %H:%M:%S") + ": Extracting fusion supporting alignments from \"%s\""  % bam_file, file=sys.stderr)
	
	samfile = pysam.Samfile(bam_file,'rb')
	read_names = {}	#read ids supporting fusion transcripts
	support_Frag = collections.defaultdict(int)	# including supporting split read and read-pairs
	for (Achr, Ast, Aend, Aname, Bchr, Bst, Bend,Bname) in get_coord(coord_file):

		fusion_name = Aname + "-" + Bname
		split_read = 0	#split read only + split/paired
		pair_read = 0	#pair only
		
		# alignments from gene A
		for aligned_read in samfile.fetch(Achr, Ast, Aend):
			if aligned_read.is_qcfail: continue
			if aligned_read.is_secondary: continue
			if aligned_read.is_unmapped: continue
			if aligned_read.mapping_quality < q_cut: continue
			if aligned_read.mapping_quality == 255: continue
			if aligned_read.is_duplicate: continue
			
			read_name = aligned_read.query_name
			if read_name.endswith('/1') or read_name.endswith('/2'):
				read_name = read_name[:-2]	#remove last char
			
			# genomic span of query read
			read_map_chr = aligned_read.reference_name		# chrom
			read_map_start = aligned_read.reference_start	# start (0-based)
			read_map_end = aligned_read.reference_end		# end
			
			# genomic span of mate
			mate_map_chr = 'chr1000'
			mate_map_start = 0
			mate_map_end = 0
			if aligned_read.is_paired:
				if not aligned_read.mate_is_unmapped:
					mate_map_chr = aligned_read.next_reference_name
					mate_map_start = aligned_read.next_reference_start
					mate_map_end = mate_map_start + aligned_read.query_length	#putative next_reference_end! suppose the mate is not split.
			
			# *genomic span of query read* vs gene B
			if is_overlap(read_map_chr, read_map_start, read_map_end, Bchr, Bst, Bend):
				
				#support by both split-read and read-pair
				if is_overlap(mate_map_chr, mate_map_start, mate_map_end, Bchr, Bst, Bend):
					if read_name not in read_names:
						split_read += 1
						read_names[read_name] = [("SR", 3, "i"),("FC", fusion_name,'Z')]
				#support only by split-read
				else:
					if read_name not in read_names:
						split_read += 1
						read_names[read_name] = [("SR", 1, "i"),("FC", fusion_name,'Z')]
			else:
				#support only by read-pair
				if is_overlap(mate_map_chr, mate_map_start, mate_map_end, Bchr, Bst, Bend):
					if read_name not in read_names:
						pair_read += 1
						read_names[read_name] = [("SR", 2, "i"),("FC", fusion_name,'Z')]
				else:
					pass		
		
		# alignments from gene B
		for aligned_read in samfile.fetch(Bchr, Bst, Bend):
			if aligned_read.is_qcfail: continue
			if aligned_read.is_secondary: continue
			if aligned_read.is_unmapped: continue
			if aligned_read.mapping_quality < q_cut: continue
			if aligned_read.mapping_quality == 255: continue
			if aligned_read.is_duplicate: continue

			read_name = aligned_read.query_name
			if read_name.endswith('/1') or read_name.endswith('/2'):
				read_name = read_name[:-2]	#remove last char
						
			# genomic span of query read
			read_map_chr = aligned_read.reference_name		# chrom
			read_map_start = aligned_read.reference_start	# start (0-based)
			read_map_end = aligned_read.reference_end		# end
			
			# genomic span of mate
			mate_map_chr = 'chr1000'
			mate_map_start = 0
			mate_map_end = 0
			if aligned_read.is_paired:
				if not aligned_read.mate_is_unmapped:
					mate_map_chr = aligned_read.next_reference_name
					mate_map_start = aligned_read.next_reference_start
					mate_map_end = mate_map_start + aligned_read.query_length	#putative next_reference_end! suppose the mate is not split.
			
			
			if is_overlap(read_map_chr, read_map_start, read_map_end, Achr, Ast, Aend):
				#support by both split-read and read-pair
				if is_overlap(mate_map_chr, mate_map_start, mate_map_end, Achr, Ast, Aend):
					if read_name not in read_names:
						split_read += 1
						read_names[read_name] = [("SR", 3, "i"),("FC", fusion_name,'Z')]
				#support only by split-read
				else:
					if read_name not in read_names:
						split_read += 1
						read_names[read_name] = [("SR", 1, "i"),("FC", fusion_name,'Z')]
			else:
				#support only by read-pair
				if is_overlap(mate_map_chr, mate_map_start, mate_map_end, Achr, Ast, Aend):
					if read_name not in read_names:
						pair_read += 1
						read_names[read_name] = [("SR", 2, "i"),("FC", fusion_name,'Z')]
				else:
					pass
		support_Frag[fusion_name] = split_read + pair_read		
	
	# write support read to another BAM file
	print("@ " + strftime("%Y-%m-%d %H:%M:%S") + ": Writing fusion supporting alignments to \"%s\"" % (out_file + '.fusion.bam'), file=sys.stderr)
	OUT_BAM = pysam.Samfile(out_file + '.fusion.bam', 'wb',template=samfile)
	for aligned_read in samfile.fetch(Achr, Ast, Aend):
		if aligned_read.is_qcfail: continue
		if aligned_read.is_secondary: continue
		if aligned_read.is_unmapped: continue
		if aligned_read.mapping_quality < q_cut: continue
		if aligned_read.mapping_quality == 255: continue
		if aligned_read.is_duplicate: continue

		read_id = aligned_read.query_name
		if read_id.endswith('/1') or read_id.endswith('/2'):
			read_id = read_id[:-2]	#remove last char
		
		
		if read_id in read_names.keys():
			#print (read_id)
			aligned_read.tags = aligned_read.tags + read_names[read_id]
			OUT_BAM.write(aligned_read)

	for aligned_read in samfile.fetch(Bchr, Bst, Bend):
		if aligned_read.is_qcfail: continue
		if aligned_read.is_secondary: continue
		if aligned_read.is_unmapped: continue
		if aligned_read.mapping_quality < q_cut: continue
		if aligned_read.mapping_quality == 255: continue
		if aligned_read.is_duplicate: continue

		read_id = aligned_read.query_name
		if read_id.endswith('/1') or read_id.endswith('/2'):
			read_id = read_id[:-2]	#remove last char
		
		if read_id in read_names.keys():
			#print (read_id)
			aligned_read.tags = aligned_read.tags + read_names[read_id]
			OUT_BAM.write(aligned_read)
	
	OUT_BAM.close()
	
	print("@ " + strftime("%Y-%m-%d %H:%M:%S") + ": Sorting and indexing \"%s\"" % (out_file + '.fusion.bam'), file=sys.stderr)
	pysam.sort("-o", out_file + '.fusion.sorted.bam', out_file + '.fusion.bam')
	pysam.index(out_file + '.fusion.sorted.bam')
	
	print("@ " + strftime("%Y-%m-%d %H:%M:%S") + ": Remove \"%s\". Sorted alignments save to \"%s\"" % (out_file + '.fusion.bam', out_file + '.fusion.sorted.bam'), file=sys.stderr)
	if os.path.exists(out_file + '.fusion.sorted.bam') and os.path.getsize(out_file + '.fusion.sorted.bam') > 0:
		os.remove(out_file + '.fusion.bam')
	return (support_Frag)


def count_fragment(bam_file,q_cut = 30):
	'''
	Return total fragment (read pairs) and properly mapped read pairs.
	'''
        
	total_frag = 0    #total splicing reads
	proper_frag = 0
	samfile = pysam.Samfile(bam_file,'rb')
	try:
		while(1):
			aligned_read = next(samfile)
			if not aligned_read.is_paired:
				if aligned_read.is_qcfail: continue
				if aligned_read.is_secondary: continue
				if aligned_read.is_unmapped: continue
				if aligned_read.mapq < q_cut: continue
				if aligned_read.mapping_quality == 255: continue
				total_frag += 1
			else:
			
				if aligned_read.is_read2:
					if aligned_read.is_qcfail: continue
					if aligned_read.is_secondary: continue
					if aligned_read.is_unmapped: continue
					if aligned_read.mapq < q_cut: continue
					if aligned_read.mate_is_unmapped:
						total_frag 
				if aligned_read.is_read1:
					if aligned_read.is_qcfail: continue
					if aligned_read.is_secondary: continue
					if aligned_read.is_unmapped: continue
					if aligned_read.mapq < q_cut: continue
					if aligned_read.mapping_quality == 255: continue
					if aligned_read.is_proper_pair: proper_frag += 1
					total_frag += 1
	except StopIteration:
		print("Done", file=sys.stderr)
		samfile.seek(0)
	return (total_frag, proper_frag)
	
