def is_overlap(chr1, st1, end1, chr2, st2, end2):
	'''
	Check if two regios are overlap.
	
	Parameters
	----------
	chr1 : str
		Chromosome ID of the first genomic region
	st1 : int
		Start coordinate of the first genomic region
	end1 : int
		End coordinate of the first genomic region

	chr2 : str
		Chromosome ID of the second genomic region
	st2 : int
		Start coordinate of the second genomic region
	end2 : int
		End coordinate of the second genomic region
	
	Return
	------
		bool
	'''
	#genome coordinate is left-open, right-close. 
	st1 = st1 +1
	end1 = end1
	st2 = st2 +1
	end2 = end2
	
	overlap_size = []
	if chr1 != chr2:
		overlap_size = []
	else:
		overlap_size = range(max(st1, st2), min(end1, end2)+1)
	
	if len(overlap_size) > 0:
		return True
	else:
		return False