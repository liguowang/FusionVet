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


def bam2bed(bam_file, bed_file, track_header, q_cut):
	'''
	Convert BAM file into standard BED file. The alignment blocks of paired-end reads will be
	merged into a single BED entry (row).
	
	
	Parameters
	----------
	bam_file : str
		Name of input BAM file.
		
	bed_file : str
		Name of input BED file.
	
	track_header : bool
		If True, add track header line to the bed file. 
		
	q_cut : int
		Mapping quality score cutoff. 
	'''   
	
	#key is read_id, value is list of "aligned gapless blocks"
	block_list = {}	
	OUT = open(bed_file,'w')
	if track_header:
		print ('track name="Gene fusion supporting reads" description="Gene fusion supporting reads. Alignment blocks from the paired-end reads were combined into a single BED row" visibility=2 itemRgb="On"', file=OUT)
	samfile = pysam.Samfile(bam_file,'rb')
	strandness = collections.defaultdict(list)
	try:
		while(1):
			aligned_read = next(samfile)	
			read_id = aligned_read.query_name
			chrom = aligned_read.reference_name
			
			if aligned_read.is_reverse:
				s = '-'
			else:
				s = '+'
				
			if read_id.endswith('/1') or read_id.endswith('/2'):
				read_id = read_id[:-2]	#remove last 2 chars
			
			key = read_id + ' ' + chrom
			strandness[key].append(s)
			if key not in block_list:
				block_list[key] = aligned_read.get_blocks()	#[(46650521, 46650555), (46650631, 46650645)]; chr1    46650522        66      34M76N14M  
			else:
				block_list[key].extend(aligned_read.get_blocks())
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
	
	# convert sorted block list into BED 
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
		thickStart = chromStart
		thickEnd = chromEnd
		itemRgb = '255,0,0'
		blockCount = len(blocks)
		blockSizes = ','.join([str(i[1] - i[0]) for i in blocks])
		blockStarts = ','.join([str(i[0] - chromStart) for i in blocks])
		
		bed_blocks = [chrom, chromStart, chromEnd, name, score, strand, thickStart, thickEnd, itemRgb, blockCount, blockSizes, blockStarts]
		print ("\t".join([str(i) for i in bed_blocks]), file=OUT)
		
	
if __name__=='__main__':
	bam2bed('Tumor_RNA_TCGA-HC-7819-01A-11R-2118-07.sorted.bam', 'bb')

