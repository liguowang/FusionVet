import sys
'''Read fusion file'''

def get_coord(infile):
	'''
	Get coordinates from input fusion file. 
	
	Parameters
	----------
	
	infile : str
		Name of input file containing gene fusions. This file can be 6 columns (chr1	
		start1	end1	chr2	start2	end2) or 8 columns (chr1	start1	end1	
		name1	chr2	start2	end2	name2) separated by Tab. lines starting with '#'
		will be skipped.

	'''
	for line in open(infile,'r'):
		line = line.strip()
		if line.startswith('#'):continue
		fields = line.split()
		if len(fields) == 6:
			chr1 = fields[0]
			start1 = int(fields[1])
			end1 = int(fields[2])
			name1 = fields[0] + ':' + fields[1] + '-' + fields[2]
			
			if start1 > end1:
				print("Start > End, skip %s" % line, file=sys.stderr)
			
			chr2 = fields[3]
			start2 = int(fields[4])
			end2 = int(fields[5])
			name2 = fields[3] + ':' + fields[4] + '-' + fields[5]
			if start2 > end2:
				print("Start > End, skip %s" % line, file=sys.stderr)
		
		elif len(fields) == 8:
			chr1 = fields[0]
			start1 = int(fields[1])
			end1 = int(fields[2])
			name1 = fields[3] 
			if start1 > end1:
				print("Start > End, skip %s" % line, file=sys.stderr)
			
			chr2 = fields[4]
			start2 = int(fields[5])
			end2 = int(fields[6])
			name2 = fields[7]
			if start2 > end2:
				print("Start > End, skip %s" % line, file=sys.stderr)

		else:
			print("Skip " + line, file=sys.stderr)
		
		if chr1 == chr2:
			if len((list(range(max(start1, start2), min(end1, end2)+1)))) > 0:
				print(sys.stderr, "input regions overlapped: " + line)
				continue
		yield ((chr1, start1, end1, name1,chr2, start2, end2, name2))
				
		
