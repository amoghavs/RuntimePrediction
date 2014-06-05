 #!/usr/bin/python

#### Pending items:
# * To allocate stride*limit number of elements. -  Done
# * To write allocated elements into a file. - Done
#

import sys, getopt,re,math


def usage():
	print "\n\t Usage: StrideBenchmarks.py -c/--config -d \n\t\t -c: file with all the configuration.\n\t\t -d: Debug option, 1 for printing debug messages and 0 to forego printing debug statements. \n "
	sys.exit()

def WhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output
	
# CAUTION: Following subrotuine is written/modified to work only for the last dimension.
def InitIndirArray(A,VarNum,InitExp,ConfigParams,debug):

	ThisLoop=[]
	#tmp=' This is the variable I am using: '+str(A)
	NumForLoops=ConfigParams['Dims']
    	LHSindices=''
    	RHSindices=''
    
	ThisForLoop=''
    	#for j in range(NumForLoops):
    	#	if(j==NumForLoops-1): # If you need to loop over, remove commented code and tab the for loop-code-gen twice
    	j=NumForLoops-1
	#ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['size'][j])+' * '+str(ConfigParams['maxstride'][VarNum])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
	ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['size'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'	
		#else:
		#	ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['size'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'		
		

	# If you need to loop over, remove commented code refer to below methods in case something does not work
	TabSpace='\t'
	#for k in range(j):
		#TabSpace+='\t'
	ThisForLoop=TabSpace+ThisForLoop
	ThisLoop.append(ThisForLoop)
	ThisLoop.append(TabSpace+'{')
	#print "\n\t ThisForLoop: "+ThisForLoop+" and For-loop index: "+str(j)
	LHSindices+='['+str(ConfigParams['indices'][NumForLoops-1])+']'

    	TabSpace='\t'
    	#for k in range(NumForLoops):
	#	TabSpace+='\t'
    	eqn="\t"+TabSpace+str(A)+LHSindices+' = '+str(InitExp)+';'
    	#print "\n So, the equation is: "+str(eqn)	
	ThisLoop.append(eqn)
    	#for k in range(NumForLoops):
    	TabSpace='' #\t'
    	#for l in range(NumForLoops-k):
    	TabSpace+="\t"
	ThisLoop.append(TabSpace+'}')
     
	return ThisLoop



def InitVar(A,VarNum,StreamNum,ConfigParams,debug):

	ThisLoop=[]
	tmp=' This is the variable I am using: '+str(A)
	NumForLoops=ConfigParams['Dims']
    	LHSindices=''
    	RHSindices=''
    
	
    	for j in range(NumForLoops):
    		if(j==NumForLoops-1):
			ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['size'][j])+' * '+str(ConfigParams['StrideinStream'][VarNum][StreamNum])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
		else:
			ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['size'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'		
		
		TabSpace='\t'
		for k in range(j):
			TabSpace+='\t'
		ThisForLoop=TabSpace+ThisForLoop
		ThisLoop.append(ThisForLoop)
		ThisLoop.append(TabSpace+'{')
		#print "\n\t ThisForLoop: "+ThisForLoop+" and For-loop index: "+str(j)
		LHSindices+='['+str(ConfigParams['indices'][j])+']'

    	TabSpace=''
    	for k in range(NumForLoops):
		TabSpace+='\t'
    	eqn="\t"+TabSpace+str(A)+LHSindices+' = '+str(ConfigParams['init'][VarNum])+';'
    	#print "\n So, the equation is: "+str(eqn)	
	ThisLoop.append(eqn)
    	for k in range(NumForLoops):
    		TabSpace='' #\t'
    		for l in range(NumForLoops-k):
    			TabSpace+="\t"
	    	ThisLoop.append(TabSpace+'}')
     
	return ThisLoop


def StridedLoopInFunction(Stride,StrideDim,A,VarNum,ConfigParams,debug):
    if( (StrideDim > ConfigParams['Dims']) or (StrideDim < 0) ):
      print "\n\t ERROR: For variaable "+str(A)+" a loop with stride access: "+str(StrideDim)+" has been requested, which is illegal!"
      sys.exit(0)

    if debug:	
	    print "\n\t In StrideLoop: Variable: "+str(A)+" dimension: "+str(StrideDim)+" and requested stride is "+str(Stride)
	    

    VarFuncDeclString=''
    VarDeclString=''
    for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
    	VarFuncDeclString+=ConfigParams['VarDecl'][VarNum][CurrStream]+','
    	VarDeclString+='Var'+str(VarNum)+'_Stream'+str(CurrStream)+','
 
    FuncName='Func'+str(A)+'Stride'+str(Stride)+"Dim"+str(StrideDim)	 
    FuncCall='Sum='+str(FuncName)+'('+VarDeclString+str(Stride)+',Sum'+');'	    
    ThisLoop=[]
    PopCode=0	
    ThisLoop.append('Sum=2;')
    ThisLoop.append('gettimeofday(&start,NULL);')
    ThisLoop.append(FuncCall) 
    ThisLoop.append('gettimeofday(&end,NULL);')
    ThisLoop.append('currtime=(end.tv_sec+end.tv_usec/1000000.0 )-(start.tv_sec+start.tv_usec/1000000.0);') 
    ThisLoop.append('printf("\\n\\t Run-time for function- '+str(FuncName)+': %lf ",currtime);')
    PrintResult='printf("\\n\\t Sum: %ld ",Sum);'
    ThisLoop.append(PrintResult)
    PopCode+=7
    
    if(ConfigParams['alloc'][VarNum]=='d' or ConfigParams['alloc'][VarNum]=='dynamic'):
	    FuncDecl='long int Func'+str(A)+'Stride'+str(Stride)+"Dim"+str(StrideDim)+'('+VarFuncDeclString+' long int Stride, int Sum )'
    else:
    	    FuncDecl='long int Func'+str(A)+'Stride'+str(Stride)+"Dim"+str(StrideDim)+'('+VarFuncDeclString+' long int Stride, int Sum )'
    ThisLoop.append(FuncDecl)
    ThisLoop.append('{')
    ThisLoop.append(str(ConfigParams['indices'][len(ConfigParams['indices'])-1]))
    ThisLoop.append('long int AnotherIndex=0;')
    NumDims=ConfigParams['Dims']
    LHSindices=''
    RHSindices=''
    
    if debug:
    	print "\n\t I need to generate following number of streams: "+str(ConfigParams['NumStreaminVar'][VarNum])
    LargestIndexNotFound=1
    IndicesForStream=[]
    BoundsForStream=[]
    IndexIncr=''
    IndexDecl=''
    StrideIndex=[]
    AccumVar=[]
    IndexInit=''
    CurrAccumVarDecl=''
    if debug:
    	print "\n\t Maxstride: "+str(ConfigParams['maxstride'][VarNum]) +' for VarNum: '+str(VarNum)
    for i in range(ConfigParams['NumStreaminVar'][VarNum]):
    	CurrAccumVar=str('Accum')+str(i)
 	AccumVar.append(CurrAccumVar)
 	CurrAccumVarDecl+='long int '+str(CurrAccumVar)+'='+str(i+1)+';'
    	
    	if(LargestIndexNotFound and (ConfigParams['StrideinStream'][VarNum][i]==ConfigParams['maxstride'][VarNum]) ):
	    	LargestIndexNotFound=0
	    	
	   	bounds= '((' + str(ConfigParams['size'][StrideDim])+' * '+str(ConfigParams['StrideinStream'][VarNum][i] )+' )- '  + str(ConfigParams['StrideinStream'][VarNum][i])+')'   	
	   	BoundsForStream.insert(0,str(bounds))
	   	CurrIndexIncr=str(ConfigParams['indices'][StrideDim])+'+= '+str(ConfigParams['StrideinStream'][VarNum][i])
	   	IndexIncr=str(CurrIndexIncr)+str(IndexIncr)    	
	    	if debug:
	    		print "\n\t The boss is here!! Bound: "+str(bounds)+' IndexIncr: '+str(CurrIndexIncr)
	    	StrideIndex.append(str(ConfigParams['indices'][StrideDim]))
	else:
	   	index=str('StreamIndex'+str(i))
	   	IndicesForStream.append(index)
	   	#bounds= '( (' + str(ConfigParams['size'][VarNum]) +' * '+ str(ConfigParams['maxstride'][VarNum] )+' ) - '  + str(ConfigParams['StrideinStream'][VarNum][i])+')'      	
	   	#BoundsForStream.append(str(bounds))
	   	CurrIndexIncr=','+str(index)+'+= '+str(ConfigParams['StrideinStream'][VarNum][i])
	   	IndexIncr+=CurrIndexIncr
	   	IndexDecl+='long int '+str(index)+'=0;'
	   	IndexInit+=','+str(index)+'=0'
	   	if debug:
	   		print "\n\t The minnions are here!! Bound: "+str(bounds)+' IndexIncr: '+str(CurrIndexIncr)
	   	StrideIndex.append(str(index))

    ThisLoop.append(CurrAccumVarDecl)		   	
    if debug:
    	print "\n\t IndexDecl: "+str(IndexDecl)+' Bounds: '+str(BoundsForStream[0])
    if(ConfigParams['NumStreaminVar'][VarNum] > 1):
    	ThisLoop.append(IndexDecl)
    
    LoopIter='LoopIter'	
    ThisLoop.append('long int '+str(LoopIter)+'=0;')
    TabSpace='\t'
    ThisForLoop=TabSpace+'for('+str(LoopIter)+'=0; '+str(LoopIter)+' < '+str(ConfigParams['NumIters'])+' ; '+str(LoopIter)+'+=1)'
    ThisLoop.append(ThisForLoop)
    ThisLoop.append(TabSpace+'{')
    
    #AccumInit=TabSpace+'\t'
    #for k in range(ConfigParams['NumStreaminVar'][VarNum]):
    #	    AccumInit+=AccumVar[k]+'=0;'
    #print "\n\t AccumInit: "  
    #ThisLoop.append(AccumInit)
    for j in range(NumDims):
		if(j==StrideDim):
			#RHSindices+='['+str(ConfigParams['indices'][j])+']'
			ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 '+str(IndexInit)+';'+str(ConfigParams['indices'][j])+'<='+str(BoundsForStream[0])+';'+str(IndexIncr)+')'
		elif(j!=StrideDim):
			#RHSindices+='['+str(ConfigParams['indices'][j])+']'	
			ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+	str(ConfigParams['indices'][j])+' < '+str(ConfigParams['size'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
		
		TabSpace='\t\t'
		for k in range(j):
			TabSpace+='\t'
		ThisForLoop=TabSpace+ThisForLoop
		ThisLoop.append(ThisForLoop)
		ThisLoop.append(TabSpace+'{')


    TabSpace='\t'
    for k in range(NumDims):
		TabSpace+='\t'
    MaxstrideDimNotFound=1	
    eqn=''
    for k in range(ConfigParams['NumStreaminVar'][VarNum]):
	    #eqn="\t"+TabSpace+str(A)+LHSindices+' = '+'Sum'+' + '+str(A)+RHSindices+';'
	    LHSindices=''
	    RHSindices=''
	    indices=''
	    for j in range(NumDims):
		if(j==StrideDim):
			#RHSindices+='['+str(ConfigParams['IndirVar'][VarNum][k])+'['+str(ConfigParams['indices'][j])+'] ]'
			#RHSindices+='['+str(ConfigParams['indices'][j])+']'	
			RHSindices+='['+str(StrideIndex[k])+']'
		else:
			#LHSindices+='['+str(ConfigParams['indices'][j])+']'
			RHSindices+='['+str(ConfigParams['indices'][j])+']'

		
		#print "\n\t LHS: "+str(LHSindices)+" RHS: "+str(RHSindices)
		
	    #for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
	    StreamVar='Var'+str(VarNum)+'_Stream'+str(k)
	    eqn="\t"+TabSpace+str(StreamVar)+RHSindices+' = '+AccumVar[k]+' + '+str(StreamVar)+RHSindices+';'
	    #eqn="\t"+TabSpace+AccumVar[k]+'+='+str(StreamVar)+RHSindices+';'
	    #print "\n\t eqn: "+str(eqn)
	    if debug:
	    	print "\n So, the equation is: "+str(eqn)	
    	    ThisLoop.append(eqn)
    	    
    for k in range(NumDims+1): # NumDims+1 since we are looping over the loops! 
    	TabSpace='\t'
    	for l in range(NumDims-k):
    		TabSpace+="\t"
    	ThisLoop.append(TabSpace+'}')
    ThisLoop.append('printf(" ");')
    AccumEqn=' Sum+=(';
    for k in range(ConfigParams['NumStreaminVar'][VarNum]-1):
    	    AccumEqn+=AccumVar[k]+'+'
    AccumEqn+=AccumVar[ConfigParams['NumStreaminVar'][VarNum]-1]+');'
    ThisLoop.append(AccumEqn) 
    ThisLoop.append('return Sum;')
    ThisLoop.append('}')
    ThisLoop.append(PopCode)
    return ThisLoop

def WriteArray(Array,File):
	File.write("\n\n")
	for i in range(len(Array)):
		File.write("\n\t "+str(Array[i])+"\n")
		
	File.write("\n")	


def main(argv):
	config=''
	debug=0
	try:
	   opts, args = getopt.getopt(sys.argv[1:],"c:d:h:v",["config","deubg","help","verbose"])
	except getopt.GetoptError:
		#print str(err) # will print something like "option -a not recognized"
	   usage()
	   sys.exit(2)
	verbose=False   
	for opt, arg in opts:
	   if opt == '-h':
	      print 'test.py -i <inputfile> -o <outputfile>'
	      sys.exit()
	   elif opt in ("-c", "--config"):
	      config=arg
	      print "\n\t Config file is "+str(config)+"\n";
	   elif opt in ("-d", "--debug"):
	      debug=int(arg)
	      print "\n\t Debug option is "+str(debug)+"\n";	      
           else:
   		usage()

	# If execution has come until this point, the script should have already identified the config file.
	if(config==''):
		usage()
	ConfigHandle=open(config)
	ConfigContents=ConfigHandle.readlines()
	ConfigHandle.close()
	
	# At this point the config should be read completely.
	ConfigParams={}
	ConfigParams['size']=[]
	ConfigParams['maxstride']=[]
	ConfigParams['alloc']=[]
	ConfigParams['datastructure']=[]	
	ConfigParams['Dims']=0
	ConfigParams['NumVars']=0
	ConfigParams['NumStreams']=0
	ConfigParams['NumIters']=[]
	ConfigParams['init']=[]	
	ConfigParams['NumStreaminVar']=[]
	ConfigParams['StrideinStream']=[]
	
	LineCount=0;
	DimNotFound=1;
	SizeNotFound=1;
	NumStreamsNotFound=1;
	StrideNotFound=1;
	AllocNotFound=1;
	DSNotFound=1;
	InitNotFound=1;
	ThisArray=[]
	NumVars=0
	NumVarNotFound=1
	NumStreamsDimsNotFound=1
	StrideForAllDimsNotFound=1
	FoundStrideForDims=0
	LoopIterationsNotFound=1
	
	# Tabs: 1
	for CurrLine in ConfigContents:
		LineCount+=1;
		LineNotProcessed=1
		# Tabs: 2
		if DimNotFound:
			MatchObj=re.match(r'\s*\#dims',CurrLine)
			if MatchObj:
				DimsLine=re.match(r'\s*\#dims\s*(\d+)*',CurrLine)
				if DimsLine:
					Dims=int(DimsLine.group(1))
					if debug:
						print "\n\t Number of dims is "+str(Dims)+"\n"
					ConfigParams['Dims']=Dims
					LineNotProcessed=0
					DimNotFound=0
		if NumVarNotFound:
			MatchObj=re.match(r'\s*\#vars',CurrLine)
			if MatchObj:
				DimsLine=re.match(r'\s*\#vars\s*(\d+)*',CurrLine)
				if DimsLine:
					NumVars=int(DimsLine.group(1))
					ConfigParams['NumVars']=NumVars
					if debug:
						print "\n\t Number of variables is "+str(ConfigParams['NumVars'])+"\n"	
					LineNotProcessed=0
					NumVarNotFound=0			
					
		if NumStreamsDimsNotFound:
			MatchObj=re.match(r'\s*\#StreamDims',CurrLine)
			if MatchObj:
				tmp=re.split(' ',CurrLine)
				NumStreaminVar=re.split(',',tmp[1])
				if NumStreaminVar:
					LineNotProcessed=0
					CurrDim=0;
					for CurrStreamDim in NumStreaminVar:
						CheckSpace=re.match(r'^\s*$',CurrStreamDim)
					        if(CheckSpace):
					       		if debug:
					       			print "\n\t For StreamDim parameter, the input is not in the appropriate format. Please check! \n"
					       		sys.exit(0)
					       	else:
							CurrStreamDim=re.sub(r'^\s*','',CurrStreamDim)
							CurrStreamDim=re.sub(r'\s*$','',CurrStreamDim)						       	
							ConfigParams['NumStreaminVar'].append( int(CurrStreamDim))
							CurrDim+=1				
							if debug:
					       			print "\n\t #Streams for dim "+str(CurrDim)+" is "+str(CurrStreamDim)+"\n" 
					if(CurrDim != ConfigParams['NumVars']):
						#if debug:
						print "\n\t The StreamDim parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions speciied is "+str(ConfigParams['Dims'])+"\n";
						sys.exit(0)
					else:
						NumStreamsDimsNotFound=0	
		if LoopIterationsNotFound: #loop_iterations	
			MatchObj=re.match(r'\s*\#loop\_iterations',CurrLine)
			if MatchObj:
				#LoopLine=re.match(r'\s*\#loop\_iterations_dim(\d+)*\s+(\d+)*',CurrLine)
				LoopLine=re.match(r'\s*\#loop\_iterations(.*)',CurrLine)
				if LoopLine:
					Iters=re.split(',',LoopLine.group(1))
					if Iters:
						for i in range(len(Iters)):
							ConfigParams['NumIters'].append(int(WhiteSpace(Iters[i])))
							if debug:
								print "\n\t Var: "+str(i)+" Loop-iterations: "+str(Iters[i])+"\n"	
					if(len(ConfigParams['NumIters'])!=ConfigParams['NumVars']):
						print "\n\t Number of iterations for nested loops is specified for "+str(len(ConfigParams['NumIters']))+" variables, expected for "+str(ConfigParams['NumVars'])
						sys.exit()
					else:
						LineNotProcessed=0
						LoopIterationsNotFound=0
						sys.exit()
				else:
					print "\n\t Unable to process loop_iterations parameter! "
					sys.exit()	
					
		else:
	
			if SizeNotFound:
				MatchObj=re.match(r'\s*\#size',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Sizes=re.split(',',tmp[1])
					if Sizes:
						LineNotProcessed=0
						CurrDim=0;
						for CurrSize in Sizes:
							CheckSpace=re.match(r'^\s*$',CurrSize)
						        if(CheckSpace):
						       		if debug:
						       			print "\n\t For size parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)
						       	else:
								CurrSize=re.sub(r'^\s*','',CurrSize)
								CurrSize=re.sub(r'\s*$','',CurrSize)						       	
								ConfigParams['size'].append( CurrSize)
								CurrDim+=1				
								if debug:
						       			print "\n\t Size for dim "+str(CurrDim)+" is "+str(CurrSize)+"\n" 
						if(CurrDim != ConfigParams['Dims']):
							#if debug:
							print "\n\t The size parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(ConfigParams['Dims'])+"\n";
							sys.exit(0)
						else:
							SizeNotFound=0

			if StrideForAllDimsNotFound:
				MatchObj=re.match(r'\s*\#stride',CurrLine)
				if MatchObj:
					FindDim=re.match(r'\s*\#stride(\d+)+',CurrLine)
					SearchingDim=0
					if FindDim:
						if debug:
							print "\n\t Found this dim: "+str(FindDim.group(1))
						SearchingDim=int(FindDim.group(1))
						tmp=re.split(' ',CurrLine)
						Strides=re.split(',',tmp[1])
						if Strides:
							LineNotProcessed=0
							Count=0;
							StrideInThisDim=[]
							for CurrStride in Strides:
								CheckSpace=re.match(r'^\s*$',CurrStride)
								if(CheckSpace):
							       		if debug:
							       			print "\n\t For size parameter, the input is not in the appropriate format. Please check! \n"
							       		sys.exit(0)						
								else:
									CurrStride=re.sub(r'^\s*','',CurrStride)
									CurrStride=re.sub(r'\s*$','',CurrStride)							
									StrideInThisDim.append(int(CurrStride));
									Count+=1				
									if debug:
							       			print "\n\t Stride for stream "+str(Count) +' in dim '+str(SearchingDim)+" "+str(Count)+" is "+str(CurrStride)+"\n" 
							if(Count != ConfigParams['NumStreaminVar'][SearchingDim]):
								print "\n\t The stride parameter is not specified for specified number of streams in "+str(ConfigParams['NumStreaminVar'][SearchingDim])+" in variable "+str(SearchingDim)+", it is specified only for "+str(Count)+ " streams. "
								sys.exit(0)
							else:
								ConfigParams['StrideinStream'].append(StrideInThisDim)
								FoundStrideForDims+=1
								if(FoundStrideForDims==ConfigParams['NumVars']):
									StrideNotFound=0	
									StrideForAllDimsNotFound=0
									if debug:
										print "\n\t Required stride for each stream in each dimension has been found!!! \n"
							
			if AllocNotFound:
				MatchObj=re.match(r'\s*\#alloc',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Allocs=re.split(',',tmp[1])
					if Allocs:
						LineNotProcessed=0
						CurrDim=0;
						for CurrAlloc in Allocs:
							CheckSpace=re.match(r'^\s*$',CurrAlloc)
						        if(CheckSpace):
						       		if debug:
						       			print "\n\t For size parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)						
							else:	
								CurrAlloc=re.sub(r'^\s*','',CurrAlloc)
								CurrAlloc=re.sub(r'\s*$','',CurrAlloc)					
								ConfigParams['alloc'].append(CurrAlloc);
								CurrDim+=1				
								if debug:
						       			print "\n\t Alloc for dim "+str(CurrDim)+" is "+str(CurrAlloc)+"\n" 					
						if(CurrDim != ConfigParams['NumVars']):
							print "\n\t The allocation parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit(0)
							
						else:
							AllocNotFound=0	

			if DSNotFound:
				MatchObj=re.match(r'\s*\#datastructure',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					DS=re.split(',',tmp[1])
					if DS:
						LineNotProcessed=0
						CurrDim=0;
						for CurrDS in DS:
							CheckSpace=re.match(r'^\s*$',CurrDS)
						        if(CheckSpace):
						       		if debug:
						       			print "\n\t For datastructure parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)						
							else:
								CurrDS=re.sub(r'\s*$','',CurrDS)
								ConfigParams['datastructure'].append( CurrDS);
								CurrDim+=1				
								if debug:
						       			print "\n\t Alloc for dim "+str(CurrDim)+" is "+str(CurrDS)+"\n" 					
						if(CurrDim != ConfigParams['NumVars']):
							print "\n\t The data structure parameter is not specified for each variable. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit(0)
						else:
							DSNotFound=0		

			if InitNotFound:
				MatchObj=re.match(r'\s*\#init',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Init=re.split(',',tmp[1])
					if Init:
						LineNotProcessed=0
						CurrDim=0;
						for CurrInit in Init:
							CheckSpace=re.match(r'^\s*$',CurrInit)
						        if(CheckSpace):
						       		if debug:
						       			print "\n\t For init parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)						
							else:
								CurrInit=re.sub(r'\s*$','',CurrInit)
								ConfigParams['init'].append( CurrInit);
								CurrDim+=1				
								if debug:
						       			print "\n\t Alloc for dim "+str(CurrDim)+" is "+str(CurrInit)+"\n" 					
						if(CurrDim != ConfigParams['NumVars']):
							print "\n\t The init expression is not specified for each variable. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit(0)
						else:
							InitNotFound=0		




		if LineNotProcessed:
			if debug:
				print "\n\t Info is not processed in line: "+str(LineCount)+"\n";
		
	
	#Tabs: 1		
	if( (NumVarNotFound==0) and (DimNotFound==0) and (SizeNotFound==0) and (StrideNotFound==0) and (AllocNotFound==0) and (DSNotFound==0) and (InitNotFound==0) and (NumStreamsDimsNotFound==0) and (LoopIterationsNotFound==0)):
		print "\n\t The config file has all the required info: #dims, size and allocation and initialization for all the dimensions "	
		InitAlloc=[]
		LibAlloc=[]
		ConfigParams['indices']=[]
		tmp='#include<stdio.h>'
		LibAlloc.append(tmp)
		tmp='#include<stdlib.h>'
		LibAlloc.append(tmp)
		tmp='#include <time.h>'
		LibAlloc.append(tmp)
		
			
		tmp='int main()'	
		InitAlloc.append(tmp)
		InitAlloc.append('\n\t{')				
		for i in range(ConfigParams['Dims']):
			ConfigParams['indices'].append('index'+str(i))
				
		tmp=' long int '
		for i in range(ConfigParams['Dims']-1):
			tmp+=ConfigParams['indices'][i]+','	
		tmp+=ConfigParams['indices'][len(ConfigParams['indices'])-1]+';'
		if debug:
			print "\n\t This is how the indices will look: "+tmp+" \n";		
		
		ConfigParams['indices'].append(tmp) # Need to insert this in the function. Lazily adding this here to avoid declaring another key for this hash.					
		InitAlloc.append(tmp);	
		DynAlloc=[]	
		ConfigParams['VarDecl']=[]	
		
		for CurrDim in range(ConfigParams['NumVars']):
			largest=0
			for j in range(ConfigParams['NumStreaminVar'][CurrDim]):
				if(largest < ConfigParams['StrideinStream'][CurrDim][j]):
					largest=ConfigParams['StrideinStream'][CurrDim][j]
			ConfigParams['maxstride'].append(largest)
			if debug:
				print "\n\t For dim "+str(CurrDim)+" largest stride requested for any stream is "+str(largest)
		
		#sys.exit()
		
		for index in range(ConfigParams['NumVars']):
				VarDeclStmt=[]
			
				VarDecl=''
				datatype=''
				if(ConfigParams['datastructure'][index]=='f' or ConfigParams['datastructure'][index]=='float'):
					VarDecl='float' 
					datatype=VarDecl
					if debug:
						print "\n\t Allocated float to variable "+str(index)
				elif(ConfigParams['datastructure'][index]=='d' or ConfigParams['datastructure'][index]=='double'):
					VarDecl='double' 
					datatype=VarDecl
					if debug:
						print "\n\t Allocated double to variable "+str(index)				
				elif(ConfigParams['datastructure'][index]=='i' or ConfigParams['datastructure'][index]=='integer'):
					VarDecl='int' 
					datatype=VarDecl
					if debug:
						print "\n\t Allocated integer to variable "+str(index)								
				else:
					print "\n\t Supported datastructure is only float, double, integer. Dimension "+str(index)+" requests one of the nonsupported datastructure: "+str(ConfigParams['datastructure'][index])+"\n"
					sys.exit(0)
				VarType=str(datatype)
				if( ConfigParams['alloc'][index]=='d' or ConfigParams['alloc'][index]=='dynamic'):
					for CurrStream in range(ConfigParams['NumStreaminVar'][index]):
						VarDecl=datatype
						var=' Var'+str(index)+'_Stream'+str(CurrStream)
						prefix=''
						suffix=''
						for CurrDim in range(ConfigParams['Dims']):
						   prefix+='*'
						for CurrDim in range(ConfigParams['Dims']-1):
						   suffix+='*'				   
						VarDecl+=prefix+var 
						VarDeclStmt.append(VarDecl)
						VarDecl+=';'
						if debug:
							print "\n\t This is the prefix: "+str(prefix)+" and this is the suffix: "+str(suffix)+" and this'd be the variable declaration: "+str(VarDecl)+ "\n "
						DynAlloc.append(VarDecl)
						if(ConfigParams['Dims']==1):
							tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['size'][0]+'*'+str(ConfigParams['StrideinStream'][index][CurrStream])+' * sizeof('+datatype+suffix+'))'+';'		
						else:
							tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['size'][0]+' * sizeof('+datatype+suffix+'))'+';'
				
						DynAlloc.append(tmp);
						  		
					if debug:
						print "\n\t This is how the first malloc statement look: "+str(tmp)+"\n"
				
					if(ConfigParams['Dims']>1):
						NumForLoops=''
						for i in range(ConfigParams['Dims']-1):
							NumForLoops=i+1
							MallocLHS=''
							for j in range(NumForLoops):
								ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+	str(ConfigParams['indices'][j])+' < '+str(ConfigParams['size'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
								if debug:
									print "\n\t ThisForLoop: "+ThisForLoop+" and For-loop index: "+str(j)
								DynAlloc.append(ThisForLoop);
								DynAlloc.append('{')
								MallocLHS+='['+str(ConfigParams['indices'][j])+']'
							prefix=''
							suffix=''
							for CurrDim in range(ConfigParams['Dims']-i-1):
							   prefix+='*'
							for CurrDim in range(ConfigParams['Dims']-i-2):
							   suffix+='*'	
							for CurrStream in range(ConfigParams['NumStreaminVar'][index]):  
								var=' Var'+str(index)+'_Stream'+str(CurrStream) 
								if(i==(ConfigParams['Dims']-2)): # Since the loop is going from 0 to ConfigParams['Dims']-2
									MallocEqn=var+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['size'][i+1]+' * '+str(ConfigParams['StrideinStream'][index][CurrStream])+' * sizeof('+datatype+suffix+'))'+';'		
								else:
									MallocEqn=var+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['size'][i+1]+' * sizeof('+datatype+suffix+'))'+';'		
								DynAlloc.append(MallocEqn)
						   		if debug:
									print "\t The malloc equation is: "+str(MallocEqn)+"\n"
							for j in range(NumForLoops):
								DynAlloc.append('}')
					
				else:
					
					VarDecl=''				
					for CurrDim in range(Dims-1):
						VarDecl+='['+str(ConfigParams['size'][CurrDim])+']'					
					for CurrStream in range(ConfigParams['NumStreaminVar'][index]):
						CurrStreamVar=' Var'+str(index)+'_Stream'+str(CurrStream)
						StreamVarDecl=datatype+' '+CurrStreamVar+VarDecl+'['+str(ConfigParams['size'][ConfigParams['Dims']-1])+' * '+str(ConfigParams['StrideinStream'][index][CurrStream])+']'
					#ConfigParams['VarDecl'].append(VarDecl)
						VarDeclStmt.append(StreamVarDecl)
						StreamVarDecl+=';'
						if debug:
							print "\n\t Variable declaration for variable "+str(index)+" is static and is as follows: "+str(StreamVarDecl)+"\n"
						
						LibAlloc.append(StreamVarDecl)
				ConfigParams['VarDecl'].append(VarDeclStmt)
	
			#InitAlloc[index]=[]


		SizeString=''
		for i in range(ConfigParams['Dims']-1):
			SizeString+=str(ConfigParams['size'][i])+'_'
		SizeString+=str(ConfigParams['size'][ConfigParams['Dims']-1])
		
		StrideString=''
		for index in range(ConfigParams['NumVars']-1):
			for CurrStream in range(ConfigParams['NumStreaminVar'][index]):
				StrideString+=str(ConfigParams['StrideinStream'][index][CurrStream])+'_'
		
		index=ConfigParams['NumVars']-1
		for CurrStream in range(ConfigParams['NumStreaminVar'][index]-1):
			StrideString+=str(ConfigParams['StrideinStream'][index][CurrStream])+'_'
		StrideString+=str(ConfigParams['StrideinStream'][index][(ConfigParams['NumStreaminVar'][index]-1)])
			
		print "\n\t StrideString: "+str(StrideString)
		#sys.exit()
			
		alloc_str=''
		for CurrAlloc in ConfigParams['alloc']:
			alloc_str+=str(CurrAlloc)
			
		StreamString=''
		for i in range(ConfigParams['NumVars']-1):
			StreamString+=str(ConfigParams['NumStreaminVar'][i])+'_'
		
		StreamString+=str(ConfigParams['NumStreaminVar'][ConfigParams['NumVars']-1])
		
		DSString=''
		for i in range(ConfigParams['NumVars']):
			DSString+=str(ConfigParams['datastructure'][i])
					
 		print "\n\t -- DSString: "+str(DSString)+" -- "				
	else:
		print "\n\t The config file has DOES NOT HAVE all the required info: #dims, size and allocation for all the dimensions. If this message is printed, there is a bug in the script, please report. "
		sys.exit(0)
	
	SrcFileName='StrideBenchmarks_Iters'+str(ConfigParams['NumIters'])+'_'+str(ConfigParams['NumVars'])+"vars"+"_DS_"+str(DSString)+'_alloc_'+alloc_str+"_"+str(ConfigParams['Dims'])+'dims_'+str(SizeString)+'_streams_'+str(StreamString)+'_stride_'+str(StrideString)+'.c'
	WriteFile=open(SrcFileName,'w')			
	InitLoop=[]
	for VarNum in range(ConfigParams['NumVars']):
		ThisVarInit=[]
		for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
			CurrVar='Var'+str(VarNum)+'_Stream'+str(CurrStream)		
			Temp=InitVar(CurrVar,VarNum,CurrStream,ConfigParams,debug)	
			ThisVarInit.append(Temp)
		InitLoop.append(ThisVarInit)


	ThisLoop=[]
	Comments=[]
	for VarNum in range(ConfigParams['NumVars']):
		FuncLoop=[]
		CurrVar='Var'+str(VarNum)
		CurrDim=ConfigParams['Dims']-1
		UseStride=ConfigParams['maxstride'][VarNum]
		#WriteFile.write("\n\t // The following loop should have stride "+str(UseStride)+" for variable "+str(CurrVar)+" in dimension "+str(CurrDim) )	
		ThisLoopComment="\n\t // The following loop should have stride "+str(UseStride)+" for variable "+str(CurrVar)+" in dimension "+str(CurrDim)			
		Comments.append(ThisLoopComment)
		FuncLoop=StridedLoopInFunction(UseStride,CurrDim,CurrVar,VarNum,ConfigParams,debug)
		ThisLoop.append(FuncLoop)
		PopCode=int(FuncLoop.pop(len(FuncLoop)-1))
		#Comments.append('//')
		for i in range(PopCode):
			Comments.append(ThisLoop[VarNum].pop(0))

		#WriteArray(ThisLoop,WriteFile)	
		


	print "\n\t Source file name: "+str(SrcFileName)+"\n"		
	
	WriteArray(LibAlloc,WriteFile)	
	for VarNum in range(ConfigParams['NumVars']):
		WriteArray(ThisLoop[VarNum],WriteFile)
	
	WriteArray(InitAlloc,WriteFile)
	WriteArray(DynAlloc,WriteFile)
	WriteFile.write("\n\t long int Sum=0;")
	WriteFile.write("\n\t struct timeval start,end;")
	WriteFile.write("\n\t double currtime;")
	
	for VarNum in range(ConfigParams['NumVars']):
		for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):	
			WriteArray(InitLoop[VarNum][CurrStream],WriteFile)	

 
	WriteArray(Comments,WriteFile)	


	WriteFile.write('\n\t printf("\\n");')
	WriteFile.write("\n\t return 0;")
	WriteFile.write("\n\t}")
	WriteFile.close()		
		
	
		
					



if __name__ == "__main__":
   main(sys.argv[1:])
