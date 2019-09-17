import pysam
import sys
import collections

def consec(lst):
	'''
	Merge consecutive regions.
	
	Parameters
	----------
	lst : List of list
		List of list containing regions [start, end]. 
		
	Notes
	-----
	* List of list must be sorted by the "start" position.
	* Cannot be "list of tuple". 
	
	Return
	------
	This function returns a generator. 
	
	Examples
	--------
	::
	
		>>> regions = [[1, 2], [2, 3], [5, 8], [8,10], [17, 22]]
		>>> list(consec(regions))
		[[1, 3], [5, 10], [17, 22]]	
	'''
	
	it = iter(lst)
	prev = next(it)
	tmp = prev
	for ele in it:
		if ele[0] > prev[1]:
			yield tmp
			tmp = ele
		else:
			tmp[1] = ele[1]
		prev = ele
	yield tmp


def bam2bed(bam_file, bed_file, track_header, interact_file, q_cut):
	'''
	Convert BAM file into standard BED file. The alignment blocks of paired-end reads will be
	merged into a single BED entry (row).
	
	
	Parameters
	----------
	bam_file : str
		Name of input BAM file.
		
	bed_file : str
		Name of output BED file.
	
	interact_file : str
		Name of the output Interact file.
		
	track_header : bool
		If True, add track header line to the bed file. 
		
	q_cut : int
		Mapping quality score cutoff. 
	'''   
	
	#key is read_id, value is list of "aligned gapless blocks"
	block_list = {}	
	samfile = pysam.Samfile(bam_file,'rb')
	strandness = collections.defaultdict(list)
	interChrom_IDs = set()
	try:
		while(1):
			aligned_read = next(samfile)	
			read_type = aligned_read.get_tag(tag="SR")   #1 : only supported by split read; 2: only supported by read pair; 3: supported by both 
			fusion_name = aligned_read.get_tag(tag="FN")			
			
			chrom = aligned_read.reference_name
			if aligned_read.is_paired:
				mate_chrom = aligned_read.next_reference_name				

			if aligned_read.is_reverse:
				s = '-'
			else:
				s = '+'
			
			read_id = aligned_read.query_name
			if read_id.endswith('/1') or read_id.endswith('/2'):
				read_id = read_id[:-2]	#remove last 2 chars
			# In the output BED file
			# for intra chrom fusions, pair reads will be merged into a single bed record
			# for inter chrom fusions, pair reads will each has its own separated record
			key = fusion_name + '_@_' + read_id + ' ' + chrom
			strandness[key].append(s)
			if key not in block_list:
				block_list[key] = aligned_read.get_blocks()	#[(46650521, 46650555), (46650631, 46650645)]; chr1    46650522        66      34M76N14M  
			else:
				block_list[key].extend(aligned_read.get_blocks())
			
			if chrom != mate_chrom:
				interChrom_IDs.add(fusion_name + '_@_' + read_id)
	except StopIteration:
		print("Done", file=sys.stderr)
		samfile.seek(0)
	
	#key is read_id, value is list of sorted, non-consecutive "aligned gapless blocks"
	sorted_block_list = {}	
	for k,v in block_list.items():
		#print (k + '\t' + str(v))
		tmp = sorted( list(set(v)), key = lambda tup: tup[0])	#remove redundancy; sort coordinates (small to large)
		tmp = [list(i) for i in tmp]	#tuple list to list list
				
		sorted_block_list[k] = list(consec(tmp))		#combine consecutive regions
	
	#####################################
	# convert sorted block list into BED 
	#####################################
	OUT = open(bed_file,'w')
	if track_header:
		print ('track name="Supporting reads of Intra-Chrom gene fusion" description="Alignment blocks from the paired reads were combined" visibility=2 itemRgb="On"', file=OUT)
	for id,blocks in sorted_block_list.items():
		(name,chrom) = id.split(' ')
		chromStart = blocks[0][0]
		chromEnd = blocks[-1][-1]
		score = 0
		
		if id in strandness:
			tmp = list(set(strandness[id]))
			if len(tmp) == 1:
				strand = tmp[0]
			else:
				strand = '.'
		else:
			strand = '.'
        
		#split read : orange
		if read_type == 1:		
			itemRgb = '255,128,0'
		#paired read : blue
		elif read_type == 2:	   
			itemRgb = '0,102,204'
		#both : red
		elif read_type == 3:
			itemRgb = '255,0,0'
		else:
			itemRgb = '0,0,0'
		
		thickStart = chromStart
		thickEnd = chromEnd
		
		blockCount = len(blocks)
		blockSizes = ','.join([str(i[1] - i[0]) for i in blocks])
		blockStarts = ','.join([str(i[0] - chromStart) for i in blocks])
		
		bed_blocks = [chrom, chromStart, chromEnd, name, score, strand, thickStart, thickEnd, itemRgb, blockCount, blockSizes, blockStarts]
		print ("\t".join([str(i) for i in bed_blocks]), file=OUT)
	OUT.close()

	#####################################
	# convert BED into Interact 
	#####################################
	OUT2 = open(interact_file,'w')
	print ('track type=interact name="Supporting reads of gene fusions" description="Connection map of gene fusion reads" maxHeightPixels=200:200:50 visibility=full', file=OUT2)
	InterChrom_list = collections.defaultdict(list)	#k is read_id, value is list of tuples (chrom, st, end, name, score, strand)
	for line in open(bed_file,'r'):
		if line.startswith('#'):continue
		if line.startswith('track'):continue
		if line.startswith('browser'):continue 
	
		exon_blocks = []
		f = line.strip().split()
		chrom = f[0]
		chrom_start = int(f[1])
		name = f[3]
		#sourceName,targetName = name.split('_@_')[0].split('--')
		score = f[4]
		strand = f[5]
		blockSizes = [ int(i) for i in f[10].strip(',').split(',') ]
		blockStarts = [ chrom_start + int(i) for i in f[11].strip(',').split(',') ]
		for base,offset in zip( blockStarts, blockSizes ):		
			exon_blocks.append ([chrom, base, base+offset, strand])
			
		if name not in interChrom_IDs:
			for indx in range(0, len(exon_blocks)-1):
				block1 = exon_blocks[indx]
				block2 = exon_blocks[indx+1]
				chrom = chrom
				chromStart = min(block1[1], block2[1])
				chromEnd = max(block1[2], block2[2])
				name = name
				score = 100
				value = 100.0
				exp = 'Intra_Chrom_fusion'
				color = 'blue'
				sourceChrom, sourceStart,sourceEnd,sourceStrand = block1
				sourceName = sourceChrom + ':' + str(sourceStart) + '-' + str(sourceEnd)
				
				targetChrom, targetStart,targetEnd,targetStrand = block2
				targetName = targetChrom + ':' + str(targetStart) + '-' + str(targetEnd)
				
				print ("\t".join([str(i) for i in (chrom, chromStart, chromEnd, name, score, value, exp, color, sourceChrom, sourceStart,sourceEnd,sourceName, sourceStrand, targetChrom, targetStart,targetEnd,targetName, targetStrand)]), file=OUT2)
		
		else:
			InterChrom_list[name].append(exon_blocks)
		
	for k,v in InterChrom_list.items():
	
		name = k
		#print (name)
		score = 100
		value = 100.0
		exp = 'Inter_Chrom_fusion'
		color = 'red'
		
		if len(v) !=2:	#paired reads must have two block_list
			continue
		for block1 in v[0]:
			sourceChrom, sourceStart,sourceEnd,sourceStrand = block1
			sourceName = sourceChrom + ':' + str(sourceStart) + '-' + str(sourceEnd)
			for block2 in v[1]:
				targetChrom, targetStart,targetEnd,targetStrand = block2
				targetName = targetChrom + ':' + str(targetStart) + '-' + str(targetEnd)
				print ("\t".join([str(i) for i in (sourceChrom, sourceStart, sourceEnd, name, score, value, exp, color, sourceChrom, sourceStart,sourceEnd,sourceName, sourceStrand, targetChrom, targetStart,targetEnd,targetName, targetStrand)]), file=OUT2)
				
	OUT2.close()
	
if __name__=='__main__':
	bam2bed('Tumor_RNA_TCGA-HC-7819-01A-11R-2118-07.sorted.bam', 'bb')

