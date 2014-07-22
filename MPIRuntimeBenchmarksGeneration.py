 #!/usr/bin/python

#### Pending items:
# * To allocate stride*limit number of elements. -  Done
# * To write allocated elements into a file. - Done
#

import sys, getopt,re,math


def usage():
	print "\n\t Usage: StrideBenchmarks.py -c/--config -d \n\t\t -c: file with all the configuration.\n\t\t -d: Debug option, 1 for printing debug messages and 0 to forego printing debug statements. \n "
	sys.exit()

def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output
	
def IsNumber(s):
# Credits: StackExchange: DanielGoldberg: http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
	try:
		float(s)
		return True
	except ValueError:
		return False

def RemoveBraces(Input):
	temp=re.sub('^\s*\(','',Input)
	Output=re.sub('\)\s*$','',temp)
	#print "\n\t RemoveBraces--Input: "+str(Input)+" tmp: "+str(temp)+" Output "+str(Output)
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
	#ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' * '+str(ConfigParams['maxstride'][VarNum])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
	ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'	
		#else:
		#	ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'		
		

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


def InitVar(CurrVarName,VarNum,StreamNum,ConfigParams,WorkingVars,debug):

	ThisLoop=[]
	tmp=' This is the variable I am using: '+str(CurrVarName)
	NumForLoops=ConfigParams['Dims']
    	LHSindices=''
    	RHSindices=''
    
	if debug:
		print "\n\t Operand: "+str(VarNum)+" Stream: "+str(StreamNum)+" and I have "+str(ConfigParams['StrideVar'][VarNum][StreamNum]['NumOperands'])+" operands in me! "+" my random acess status is "+str(ConfigParams['RandomAccess'][VarNum])	
	
	FlushForLoop=[]	
	if(ConfigParams['RandomAccess'][VarNum]>0):
		TabSpace=''
		FlushVarName= 'FlushVar'+str(VarNum)+'_Stream'+str(StreamNum)	
	    	BoundVar=WorkingVars['BoundVar'] #'bound'
    		#BoundVarDecl=TabSpace+'long int '+BoundVar+' =0; '
    		#ThisLoop.append(BoundVarDecl);
    		InnerLoopVar=WorkingVars['InnerLoopVar']
    		#InnerLoopVarDecl=TabSpace+'long int '+InnerLoopVar+' =0;'
    		#ThisLoop.append(InnerLoopVarDecl)
    		#TempVar='temp'
    		#TempVarDecl=TabSpace+'long int '+str(TempVar)+';'
    		#ThisLoop.append(TempVarDecl);
    		NumOperandsVar=WorkingVars['NumOperandsVar']
    		NumOperandsVarDecl=TabSpace+' '+str(NumOperandsVar)+'= '+str(ConfigParams['StrideVar'][VarNum][StreamNum]['NumOperands'])+' ;'
    		ThisLoop.append(NumOperandsVarDecl)
     		PermuteArrayVar='PermuteArray'+str(VarNum)+'_'+str(StreamNum)
    		PermuteArrayVarDecl=TabSpace+'int* '+str(PermuteArrayVar)+';'
    		ThisLoop.append(PermuteArrayVarDecl)    
    		PermuteSizeVar='PermuteSize'+str(VarNum)+'_'+str(StreamNum)
    		PermuteSizeVarDecl=TabSpace+'int '+str(PermuteSizeVar)+';'
    		ThisLoop.append(PermuteSizeVarDecl)
    		LastDim=NumForLoops-1
    		PermuteSizeCalc=TabSpace+str(PermuteSizeVar)+' = (int) ( ( '+str(ConfigParams['GlobalVar']['DimsSize'][LastDim])+' * '+str(ConfigParams['GlobalVar']['Stream'][VarNum][StreamNum])+' ) / '+str(NumOperandsVar)+' );'
    		ThisLoop.append(PermuteSizeCalc)
    		CallPermuteFunc=TabSpace+str(PermuteArrayVar)+' = RandomPermutationGeneration( '+str(PermuteSizeVar)+' );'
    		ThisLoop.append(CallPermuteFunc)
		FlushForLoop.append(CallPermuteFunc)
    		PermuteIndexVar='PermuteIndex'
    		PermuteIndexVarInit=' PermuteIndex=0 ;'
    		CountVar=WorkingVars['CountVar']
    		ThisLoop.append(PermuteIndexVarInit)		

    	for j in range(NumForLoops):
		TabSpace='\t'
		for k in range(j):
			TabSpace+='\t'
    		DontSkip=1
    		if(j==NumForLoops-1):
	    		if(ConfigParams['RandomAccess'][VarNum]>0):
    				LoopStmt=[]
				LoopStmt.append(TabSpace+'for('+str(ConfigParams['indices'][j])+'=0 , '+str(PermuteIndexVar)+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(PermuteSizeVar)+' ; '+str(ConfigParams['indices'][j])+'+='+str(1)+' , '+str(PermuteIndexVar)+'+=1 )')
				LoopStmt.append(TabSpace+'{')
				LoopStmt.append(TabSpace+'\t '+str(BoundVar)+'= '+str(ConfigParams['indices'][j])+' + '+str(NumOperandsVar)+' ;')
				LoopStmt.append(TabSpace+'\t if( '+str(BoundVar)+' > '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' )')
				LoopStmt.append(TabSpace+'\t\t '+str(BoundVar)+' = '+str(ConfigParams['GlobalVar']['DimsSize'][j])+';')
				#LoopStmt.append(TabSpace+'\t '+str(TempVar)+' = (long int) ( rand() % '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' );')
				LoopStmt.append(TabSpace+'\t for('+str(InnerLoopVar)+'='+str(ConfigParams['indices'][j])+','+str(CountVar)+'='+str(ConfigParams['indices'][j])+' ; ( ( '+str(CountVar)+' < '+str(PermuteSizeVar)+' ) && ( '+ str(InnerLoopVar)+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ) ) ; '+str(CountVar)+'+=1,'+str(InnerLoopVar)+'+='+str(PermuteSizeVar)+')')
				for CurrLine in LoopStmt:
					ThisLoop.append(CurrLine)
					FlushForLoop.append(CurrLine)
				
				DontSkip=0
			else:
				ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' * '+str(ConfigParams['GlobalVar']['MaxStream'][VarNum])+' ; '+str(ConfigParams['indices'][j])+'+=1 )'
			
		else:
			ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'	
			if(ConfigParams['RandomAccess'][VarNum]>0):
				ThisFlushForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'	
				FlushForLoop.append(TabSpace+ThisFlushForLoop)
					
		if DontSkip:
			ThisForLoop=TabSpace+ThisForLoop
			ThisLoop.append(ThisForLoop)
			ThisLoop.append(TabSpace+'{')
			LHSindices+='['+str(ConfigParams['indices'][j])+']'
			if(ConfigParams['RandomAccess'][VarNum]>0):
				FlushForLoop.append(TabSpace+'{')
		else:
			LHSindices+='['+str(InnerLoopVar)+']'

    	TabSpace=''
    	for k in range(NumForLoops):
		TabSpace+='\t'
		
    	if(ConfigParams['RandomAccess'][VarNum]):
	    	#eqn="\t\t"+TabSpace+str(CurrVarName)+LHSindices+' = '+str(TempVar)+';' #+str(ConfigParams['init'][VarNum])+';'
	    	eqn="\t\t"+TabSpace+str(CurrVarName)+LHSindices+' = '+PermuteArrayVar+'['+str(PermuteIndexVar)+']'+';'
	    	FlushEqn="\t\t"+TabSpace+str(FlushVarName)+LHSindices+' = '+PermuteArrayVar+'['+str(PermuteIndexVar)+']'+';'
	    	FlushForLoop.append(FlushEqn)
	else:
		eqn="\t"+TabSpace+str(CurrVarName)+LHSindices+' = '+str(ConfigParams['init'][VarNum])+';'
    	
    	#print "\n So, the equation is: "+str(eqn)	
	ThisLoop.append(eqn)
    	for k in range(NumForLoops):
    		TabSpace='' #\t'
    		for l in range(NumForLoops-k):
    			TabSpace+="\t"
	    	ThisLoop.append(TabSpace+'}')
	    	if(ConfigParams['RandomAccess'][VarNum]>0):
	    		FlushForLoop.append(TabSpace+'}')
	
	for CurrLine in FlushForLoop:
		#print "\n\t FlushForLoop: "+str(CurrLine)
		ThisLoop.append(CurrLine)
     
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
    #FuncNamePrint='StrideBenchmarks_Iters'+str(ConfigParams['NumIters'])+'_'+str(ConfigParams['NumVars'])+"vars_"+alloc_str+"_"+str(ConfigParams['Dims'])+'dims_'+str(SizeString)+'_streams_'+str(StreamString)+'_stride_'+str(StrideString)
    FuncNamePrint='Func'+str(A)+'Stride'+str(Stride)+"Dim"+str(StrideDim)    #LAURA    
    ThisLoop=[]
    PopCode=0	
    ThisLoop.append('Sum=2;')
    #LAURA ThisLoop.append('gettimeofday(&start,NULL);')
    ThisLoop.append('MPI_Barrier(MPI_COMM_WORLD);');  #LAURA
    ThisLoop.append('stime=rtclock();')               #LAURA
    ThisLoop.append(FuncCall) 
    #LAURA ThisLoop.append('gettimeofday(&end,NULL);')
    #LAURA ThisLoop.append('currtime=(end.tv_sec+end.tv_usec/1000000.0 )-(start.tv_sec+start.tv_usec/1000000.0);') 
#LAURA ADD
    ThisLoop.append('etime=rtclock();')
    ThisLoop.append('currtime=etime-stime;')  
    #ThisLoop.append('double time_buf[MPI_Size];')
    ThisLoop.append('MPI_Gather(&currtime, 1, MPI_DOUBLE, time_buf, 1, MPI_DOUBLE,0,MPI_COMM_WORLD); ')
    ThisLoop.append('if(rank==0) { ')
    #AVS #ThisLoop.append('   printf("app ' +str(FuncNamePrint)+' time: "); ')
    ThisLoop.append(' printf("app '+str(FuncNamePrint)+' "); ');
    ThisLoop.append('   int ii; ')
    ThisLoop.append('   for(ii=0; ii<MPI_Size; ii++) ')
    #AVS # ThisLoop.append(' printf (" %f ",time_buf[ii]); ')
    ThisLoop.append('      printf("\t time: %f start: %lf end: %lf  ", time_buf[ii],stime,etime); ')
    ThisLoop.append('      printf("\\n"); ')
    ThisLoop.append('} ')
#LAURA END ADD
    #LAURA ThisLoop.append('printf("\\n\\t Run-time for function- '+str(FuncName)+': %lf from rank: %d",currtime,rank);')
    #LAURA PrintResult='printf("\\n\\t Sum: %ld ",Sum);'
    #LAURA ThisLoop.append(PrintResult)
    PopCode+=14  #LAURA was PopCode+=8
    
    if(ConfigParams['alloc'][VarNum]=='d' or ConfigParams['alloc'][VarNum]=='dynamic'):
	    FuncDecl='long int Func'+str(A)+'Stride'+str(Stride)+"Dim"+str(StrideDim)+'('+VarFuncDeclString+' long int Stride, int Sum )'
    else:
    	    FuncDecl='long int Func'+str(A)+'Stride'+str(Stride)+"Dim"+str(StrideDim)+'('+VarFuncDeclString+' long int Stride, int Sum )'
    ThisLoop.append(FuncDecl)
    ThisLoop.append('{')
    ThisLoop.append(str(ConfigParams['indices'][len(ConfigParams['indices'])-1]))
    #ThisLoop.append('long int AnotherIndex=0;')
    NumDims=ConfigParams['Dims']
    LHSindices=''
    RHSindices=''
    
    if debug:
    	print "\n\t I need to generate following number of streams: "+str(ConfigParams['NumStreaminVar'][VarNum])
    LargestIndexNotFound=1
    IndicesForStream=[]
    IndexIncr=''
    IndexDecl=''
    StrideIndex=[]
    AccumVar=[]
    IndexInit=''
    CurrAccumVarDecl=''
    if debug:
    	print "\n\t Maxstride: "+str(ConfigParams['maxstride'][VarNum]) +' for VarNum: '+str(VarNum)
	
    eqn=''
    BoundsChangePerStream={}
    RHSExprnPerStream={}
    ShouldDeclareVars=[]
    RandomAccessVarPerStream={}
    
    if(ConfigParams['RandomAccess'][VarNum]>0):
    	for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):	
     		Temp='RandomVar'+str(VarNum)+'_Stream'+str(CurrStream)
    		RandomAccessVarPerStream[CurrStream]=Temp
   		VarDecl='int '+str(Temp)+'=0;'
    		ShouldDeclareVars.append(VarDecl)
    		
    PermuteSizeVarforStream={}    		
    for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):	
	    #eqn="\t"+TabSpace+str(A)+LHSindices+' = '+'Sum'+' + '+str(A)+RHSindices+';'
	    LHSindices=''
	    RHSindices=''
	    indices=''
 
 	    LastDim=ConfigParams['Dims']-1
 	    PermuteSizeVar='PermuteSizeVar'+str(VarNum)+'_'+str(CurrStream)
 	    PermuteSizeVarforStream[CurrStream]=PermuteSizeVar
 	    NumOperandsVar='NumOperandsVar'+str(VarNum)+'_Stream'+str(CurrStream)
	    PermuteSizeCalc=' (int) ( ( '+str(ConfigParams['GlobalVar']['DimsSize'][LastDim])+' * '+str(ConfigParams['GlobalVar']['Stream'][VarNum][CurrStream])+' ) / '+str(NumOperandsVar)+' );'
	    PermuteSizeVarDecl='int '+str(PermuteSizeVar)+' = '+str(PermuteSizeCalc)+';'
	    ShouldDeclareVars.append(PermuteSizeVarDecl)
	    
 	    StreamVar='Var'+str(VarNum)+'_Stream'+str(CurrStream)
	
	    RHSExprnPerStream[CurrStream]=[]
	    IndexChangeForBound=[]
    	    RHSOperandsForStream=[]

	    for	CurrOperandIdx in range(ConfigParams['StrideVar'][VarNum][CurrStream]['NumOperands']):
	    	CurrOperands=ConfigParams['StrideVar'][VarNum][CurrStream]['Operands']
	    		        
	    	#IntraOperations=ConfigParams['StrideVar'][VarNum][CurrStream]['Operations']
	    	#IndexChangeforBoundforOperand=[]
	    	
	    	if debug:
	    		print "\n\t CurrVar: "+str(VarNum)+" CurrOperand: "+str(CurrOperandIdx)#+" which needs "+str(IntraOperands[CurrOperand]['NumOperands'])+" operands which have operations "+str(IntraOperands[CurrOperand]['Operations'])

	    	#NumOperations=len(IntraOperands[CurrOperand]['Operations'])
	    	#if(IntraOperands[CurrOperand]['NumOperands']==1):

		CurrOperandExprn=str(CurrOperands[CurrOperandIdx])	
		if debug:
			print "\n\t CurrOperand: "+str(CurrOperandExprn)  	
## ***********

	    	if(CurrOperandExprn[0]=='='):
	    		#if debug:
	    		RHSExprn='Const_Var'+str(VarNum)+'_Stream'+str(CurrStream)
	    		ExtractNumber=re.match('\s*\=(.*)',CurrOperandExprn)
	    		if debug:
	    			print "\n\t CurrOperandExprn: "+str(CurrOperandExprn)
	    		if ExtractNumber:
	    			NumberCheck=re.match('\s*(\d+)*\.(\d+)*',ExtractNumber.group(1))
	    			if NumberCheck:
	    				DeclareVar='double '+str(RHSExprn)+str(CurrOperandExprn)+';'
	    			else:
	    				IntCheck=re.match('\s*(\d+)*',ExtractNumber.group(1))
	    				if IntCheck:
	    					DeclareVar='long int '+str(RHSExprn)+str(CurrOperandExprn)+';'
	    				else:
	    					print "\n\t ERROR: Const-var does not have number! Use debug to locate the error! \n"
	    					sys.exit()
	    		else:
	    			print "\n\t ERROR: Const var does not have equal symbol! Use debug to locate the error! \n "
	    			sys.exit()

	    		if debug:
	    			print "\n\t ConstVar should be inserted!! "+str(CurrOperandExprn)+" RHSExprn: "+str(RHSExprn)

	    		RHSOperandsForStream.append(RHSExprn)
	    		ShouldDeclareVars.append(DeclareVar)
	    	else:
	    		if debug:
	    			print "\n\t Operand: "+str(CurrOperandExprn)
	    		BreakdownFromIdx=re.match('\s*([ijkl])(.*)',CurrOperandExprn)
	    		StreamDim=-1
	    		if BreakdownFromIdx:
	    			#print "\n\t Requesting indices "+str(BreakdownFromIdx.group(1))+" extra "+str(BreakdownFromIdx.group(2)) 
	    			IndexChange=RemoveWhiteSpace(BreakdownFromIdx.group(2))
	    			if(BreakdownFromIdx.group(1)=='i'):
	    					StreamDim=NumDims-1
	    			elif(BreakdownFromIdx.group(1)=='j'):
	    				if(ConfigParams['Dims']>1):
	    					StreamDim=NumDims-2
	    				else:
	    					print "\n\t ERROR: Requesting to manipulate (InnerMost_loop-1), where as #dimensions are "+str(ConfigParams['Dims'])
	    					sys.exit()
	    			elif(BreakdownFromIdx.group(1)=='k'):
	    				if(ConfigParams['Dims']>2):
	    					StreamDim=NumDims-3
	    				else:
	    					print "\n\t ERROR: Requesting to manipulate (InnerMost_loop-2), where as #dimensions are "+str(ConfigParams['Dims'])
	    					sys.exit()	    					
	    			elif(BreakdownFromIdx.group(1)=='l'):
	    				if(ConfigParams['Dims']>3):
	    					StreamDims=NumDims-4
	    				else:
	    					print "\n\t ERROR: Requesting to manipulate (InnerMost_loop-3), where as #dimensions are "+str(ConfigParams['Dims'])
	    					sys.exit()	

					if debug:
						print "\n\t Need to manipulate (InnerMost_loop- "+str(NumDims-StreamDim+1)+") and IndexChange: "+str(IndexChange)
	    			AppendIndexChange=''
	    			IndexChangeBreakdown={}
	    			if(IndexChange):
		    			BreakIndexChange=re.match('\s*([\+\-])\s*(\d+)*',IndexChange)
		    			if BreakIndexChange:
		    				AppendIndexChange=BreakIndexChange.group(1)+str(BreakIndexChange.group(2))	
		    				IndexChangeBreakdown['Sign']=BreakIndexChange.group(1)
		    				IndexChangeBreakdown['Delta']=int(BreakIndexChange.group(2))
		    				
		    				if(ConfigParams['RandomAccess'][VarNum]>0):
		    					#AppendIndexChange='+ ( '+str(ConfigParams['GlobalVar']['SuccessiveOperandDiff'][VarNum])+' * '+str(CurrOperandIdx)+')'
		    					AppendIndexChange='+ ( '+str(PermuteSizeVarforStream[CurrStream])+' * '+str(CurrOperandIdx)+')'
		    					IndexChangeParameterized=ConfigParams['OpDiff'][VarNum] * CurrOperandIdx
		    					if( IndexChangeParameterized == IndexChangeBreakdown['Delta'] ):
			    					if debug:
										print "\n\t Yaay Parameterized delta "+str(IndexChangeParameterized)+" is equal to specified delta: "+str(IndexChangeBreakdown['Delta'])
			    					#sys.exit()
		    					else:
		    						print "\n\t ERROR: Parameterized delta "+str(IndexChangeParameterized)+" is not equal to specified delta: "+str(IndexChangeBreakdown['Delta'])
		    						sys.exit()
		    				if debug:
		    					print "\n\t -- Sign: "+str(IndexChangeBreakdown['Sign'])+" Delta "+str(IndexChangeBreakdown['Delta'])
		    			else:
		    				print "\n\t ERROR: Unable to decode index change. Likely that the index change term was not of the form \"+-number\". Use debug to locate the source of error" 
		    				sys.exit()

	    	
    					OperandIndices=''
    					if( (ConfigParams['RandomAccess'][VarNum]>0) ):
		    				for i in range(NumDims-1):
			    				if(i==StreamDim):
			    					PushIndexChange=str(ConfigParams['indices'][i])+str(AppendIndexChange)	
			    					OperandIndices+='['+str(PushIndexChange)+']'	
			    				else:
			    					OperandIndices+='['+str(ConfigParams['indices'][i])+']'
			    			if(StreamDim==(NumDims-1)):
			    				PushIndexChange=str(RandomAccessVarPerStream[CurrStream])+str(AppendIndexChange)
			    				OperandIndices+='['+str(PushIndexChange)+']'	
			    			else:
			    				PushIndexChange=str(RandomAccessVarPerStream[CurrStream])
							OperandIndices+='['+str(PushIndexChange)+']'
							
	    				else:
		    				for i in range(NumDims):
			    				if(i==StreamDim):
			    					PushIndexChange=str(ConfigParams['indices'][i])+str(AppendIndexChange)	
			    					OperandIndices+='['+str(PushIndexChange)+']'	
			    				else:
			    					OperandIndices+='['+str(ConfigParams['indices'][i])+']'
	    				ThusOperand=str(StreamVar)+str(OperandIndices)
	    				if(AppendIndexChange==''):
	    					AppendIndexChange=0

	    				IndexChangeForBound.append((StreamDim,IndexChangeBreakdown))
	    				RHSOperandsForStream.append(ThusOperand)
	    				if debug:
	    					print "\n\t Hence the indices should be "+str(ThusOperand)+" push-indices: "+str(PushIndexChange)+" AppendIndexChange "+str(AppendIndexChange)
	    		else:
	    			print "\n\t ERROR: Operand requested is neither of 'ijkl'. Use debug for tracking the location of error "
	    			sys.exit()     					
	    iIter=0
	    RHSExprn=''	    	
	    for ThisOperand in range(len(RHSOperandsForStream)-1):
		RHSExprn+=' ('+RHSOperandsForStream[ThisOperand]+') '+str(ConfigParams['StrideVar'][VarNum][CurrStream]['ExprnOperations'][iIter]) #str(IntraOperands[CurrOperand]['Operations'][iIter])
		if debug:
			print "\n\t Operand "+str(RHSOperandsForStream[ThisOperand]) #+" Operation: "+str(IntraOperands[CurrOperand]['Operations'][iIter])
			print "\n\t -- RHSExprn: "+str(RHSExprn)
		iIter+=1
	    if(len(RHSOperandsForStream)):
		RHSExprn+=' ( '+str(RHSOperandsForStream[len(RHSOperandsForStream)-1])+' )'
	    #RHSExprnPerStream[CurrStream].append(RHSExprn)
	    RHSExprnPerStream[CurrStream]=(RHSExprn)
	    if debug:
		print "\n\t RHSExprn: "+str(RHSExprn)
		
## *********	    	
	    
	    #sys.exit()	
	    CurrStreamIndexChangeConsolidation={}
	    CurrStreamIndexChangeFinal={}
	    for CurrDim in range(NumDims):
			CurrStreamIndexChangeConsolidation[CurrDim]=[]
			CurrStreamIndexChangeFinal[CurrDim]={}

	    for CurrOperand in (IndexChangeForBound):
	    	if debug:
	    		print "\n\t CurrOperand: "+str(CurrOperand)
    		CurrStreamIndexChangeConsolidation[CurrOperand[0]].append(CurrOperand[1])
		
	    for CurrDim in range(NumDims):
	    	CurrStreamIndexChangeFinal[CurrDim]['Init']=0
	    	CurrStreamIndexChangeFinal[CurrDim]['Final']=0
	    	for CurrIndexChange in (CurrStreamIndexChangeConsolidation[CurrDim]):
	    		if debug:
	    			print "\n\t Dim: "+str(CurrDim)+" IndexChange: "+str(CurrIndexChange)#+" IndexChangeFinal: "+str(CurrStreamIndexChangeFinal[CurrDim]) 
	    		if(CurrIndexChange):
				if(CurrIndexChange['Sign']=='-'):
					if( CurrStreamIndexChangeFinal[CurrDim]['Init'] < CurrIndexChange['Delta'] ):
						CurrStreamIndexChangeFinal[CurrDim]['Init']=CurrIndexChange['Delta']
						#print "\n\t CurrStreamIndexChangeFinal[CurrDim]['Init']: "+str(CurrStreamIndexChangeFinal[CurrDim]['Init'])
				elif(CurrIndexChange['Sign']=='+'):
					if( CurrStreamIndexChangeFinal[CurrDim]['Final'] < CurrIndexChange['Delta'] ):
						CurrStreamIndexChangeFinal[CurrDim]['Final']=CurrIndexChange['Delta']
							#print "\n\t CurrStreamIndexChangeFinal[CurrDim]['Final']: "+str(CurrStreamIndexChangeFinal[CurrDim]['Final'])
	    
	    BoundsChangePerStream[CurrStream]=CurrStreamIndexChangeFinal
	    
	    #eqn="\t"+TabSpace+str(StreamVar)+RHSindices+' = '+AccumVar[CurrStream]+' + '+str(StreamVar)+RHSindices+';'
 	    #eqn="\t"+TabSpace+AccumVar[CurrStream]+'+='+str(StreamVar)+RHSindices+';'
	    #print "\n\t eqn: "+str(eqn)

	    	
	    if debug:
	    	print "\n So, the equation is: "+str(eqn)	


    FinalStreamIndexChange={} 	    
    if(ConfigParams['NumStreaminVar'][VarNum]>1):
    	for CurrDim in range(NumDims):
    		FinalStreamIndexChange[CurrDim]={}
    		FinalStreamIndexChange[CurrDim]['Init']=0
    		FinalStreamIndexChange[CurrDim]['Final']=0    		
    		
    	for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
	    	for CurrDim in range(NumDims):
	    		if(FinalStreamIndexChange[CurrDim]['Init'] < BoundsChangePerStream[CurrStream][CurrDim]['Init']):
	    			FinalStreamIndexChange[CurrDim]['Init'] = BoundsChangePerStream[CurrStream][CurrDim]['Init']
	    		if(FinalStreamIndexChange[CurrDim]['Final'] < BoundsChangePerStream[CurrStream][CurrDim]['Final']):
	    			FinalStreamIndexChange[CurrDim]['Final'] = BoundsChangePerStream[CurrStream][CurrDim]['Final']
	    		if debug:
	    			print "\n\t Dim: "+str(CurrDim)+" IndexChange "+str(BoundsChangePerStream[CurrStream][CurrDim])+" FinalStreamIndexChange[CurrDim] "+str(FinalStreamIndexChange[CurrDim])
    else:
    	FinalStreamIndexChange=BoundsChangePerStream[ConfigParams['NumStreaminVar'][VarNum]-1] #['Init'] #CAUTION: "ConfigParams['NumStreaminVar'][VarNum]=1, hence accessing CurrStream=0 here.
    
    for CurrStream in RHSExprnPerStream:
    	if debug:
    		print "\n\t CurrStream: "+str(CurrStream)+" RHS: "+str(RHSExprnPerStream[CurrStream])
    	
    for CurrDeclareVar in (ShouldDeclareVars):
        if debug:
        	print "\n\t ShouldDeclareVars: "+str(CurrDeclareVar)+" --"	    	    

    if debug:
    	for CurrDim in range(len(FinalStreamIndexChange)):
    		print "\n\t CurrDim: "+str(CurrDim)+" FinalStreamIndexChange "+str(FinalStreamIndexChange[CurrDim])
    #sys.exit()		
#########

    BoundForDim=[]
    InitForDim=[]

    LHSIndicesPerStream={}
    for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
		LHSIndicesPerStream[CurrStream]=[]
	
    for CurrDim in range(NumDims):
    	if (CurrDim!=StrideDim):
	    	InitForCurrDim='='+str(FinalStreamIndexChange[CurrDim]['Init'])
	    	InitForDim.append(InitForCurrDim)
    		BoundForThisDim='('+str(ConfigParams['GlobalVar']['DimsSize'][CurrDim])+'-'+str(FinalStreamIndexChange[CurrDim]['Final'])+')'
    		BoundForDim.append(BoundForThisDim)
    		for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
    			LHSIndicesPerStream[CurrStream].append(ConfigParams['indices'][CurrDim])
    	else:
	###
		
			for i in range(ConfigParams['NumStreaminVar'][VarNum]):
				CurrAccumVar=str('Accum')+str(i)
		 		AccumVar.append(CurrAccumVar)
			 	CurrAccumVarDecl+='long int '+str(CurrAccumVar)+'='+str(i+1)+';'
				
				if(LargestIndexNotFound and (ConfigParams['StrideinStream'][VarNum][i]==ConfigParams['maxstride'][VarNum]) ):
					LargestIndexNotFound=0
					if(ConfigParams['RandomAccess'][VarNum]>0):
						#bounds= '(' + str(ConfigParams['GlobalVar']['DimsSize'][StrideDim])+' - ('  + str(ConfigParams['GlobalVar']['Stream'][VarNum][i])+' + '+str(FinalStreamIndexChange[StrideDim]['Final'])+') )'  
						bounds= '( ( ' + str(ConfigParams['GlobalVar']['DimsSize'][StrideDim])+' * '+str(ConfigParams['GlobalVar']['NumItersLastDimVar'][VarNum])+' ) '+' - '+str(FinalStreamIndexChange[StrideDim]['Final'])+')' 		
					else:
						bounds= '((' + str(ConfigParams['GlobalVar']['DimsSize'][StrideDim])+' * '+str(ConfigParams['StrideinStream'][VarNum][i] )+' )- ('  + str(ConfigParams['GlobalVar']['Stream'][VarNum][i])+' + '+str(FinalStreamIndexChange[StrideDim]['Final'])+') )'  	
					BoundForDim.append(str(bounds))#BoundForDim.insert(0,str(bounds))
					CurrIndexIncr=str(ConfigParams['indices'][StrideDim])+'+= '+str(ConfigParams['GlobalVar']['Stream'][VarNum][i])
					IndexIncr=str(CurrIndexIncr)+str(IndexIncr)    	
					if debug:
						print "\n\t The boss is here!! Bound: "+str(bounds)+' IndexIncr: '+str(CurrIndexIncr)
					StrideIndex.append(str(ConfigParams['indices'][StrideDim]))
					LHSIndicesPerStream[i].append(ConfigParams['indices'][StrideDim])
				else:
					index=str('StreamIndex'+str(i))
					IndicesForStream.append(index)
					bounds= '( (' + str(ConfigParams['GlobalVar']['DimsSize'][CurrDim]) +' * '+ str(ConfigParams['maxstride'][VarNum] )+' ) - '  + str(ConfigParams['GlobalVar']['Stream'][VarNum][i])+')'      	
					#print "\n\t CurrStream: "+str(i)+" bounds: "+str(bounds)
				   	#BoundForDim.append(str(bounds))
					CurrIndexIncr=','+str(index)+'+= '+str(ConfigParams['GlobalVar']['Stream'][VarNum][i])
					IndexIncr+=CurrIndexIncr
					IndexDecl+='long int '+str(index)+'='+str(FinalStreamIndexChange[StrideDim]['Init'])+';'
					IndexInit+=','+str(index)+'=0'
					if debug:
						print "\n\t The minnions are here!! Bound: "+str(bounds)+' IndexIncr: '+str(CurrIndexIncr)+" IndexInit "+str(IndexInit)
					StrideIndex.append(str(index))
					LHSIndicesPerStream[i].append(index)
			#print "\n\t --*-- IndexInit "+str(IndexInit)
			InitForStrideDim='='+str(FinalStreamIndexChange[StrideDim]['Init'])+str(IndexInit)
			#print "\n\t InitForStrideDim: "+str(InitForStrideDim)
			InitForDim.append(InitForStrideDim)	    

	####    		
    	
    #sys.exit()	 
    ThisLoop.append(CurrAccumVarDecl)		   	
    if debug:
    	print "\n\t IndexDecl: "+str(IndexDecl)+' Bounds: '+str(BoundForDim[0])
    if(ConfigParams['NumStreaminVar'][VarNum] > 1):
    	ThisLoop.append(IndexDecl)
    
    LoopIter='LoopIter'	
    ThisLoop.append('long int '+str(LoopIter)+'=0;')

    for CurrDeclareVar in (ShouldDeclareVars):
        if debug:
        	print "\n\t ShouldDeclareVars: "+str(CurrDeclareVar)+" --"	    	    
        #VarDeclareExprn='long int'+str(CurrDeclareVar)
        ThisLoop.append(CurrDeclareVar)
    
    TabSpace='\t'
    # ConfigParams['GlobalVar']['NumItersDecl']
    ThisForLoop=TabSpace+'for('+str(LoopIter)+'=0; '+str(LoopIter)+' < '+str(ConfigParams['GlobalVar']['NumIters'][VarNum])+' ; '+str(LoopIter)+'+=1)'
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
			#ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 '+str(IndexInit)+';'+str(ConfigParams['indices'][j])+'<='+str(BoundForDim[j])+';'+str(IndexIncr)+')'
		        #if(ConfigParams['RandomAccess'][VarNum]>0):
		    	#	for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):	
		    	#		ThisLoop.append(TabSpace+str(RandomAccessVarPerStream[CurrStream])+' =0;')
			
			ThisForLoop='for('+str(ConfigParams['indices'][j])+str(InitForDim[j])+';'+str(ConfigParams['indices'][j])+'<='+str(BoundForDim[j])+';'+str(IndexIncr)+')'
		elif(j!=StrideDim):
			#RHSindices+='['+str(ConfigParams['indices'][j])+']'	
			#ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+	str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
			ThisForLoop='for('+str(ConfigParams['indices'][j])+str(InitForDim[j])+'; '+	str(ConfigParams['indices'][j])+' < '+str(BoundForDim[j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
		
		TabSpace='\t\t'
		for k in range(j):
			TabSpace+='\t'
		ThisForLoop=TabSpace+ThisForLoop
		ThisLoop.append(ThisForLoop)
		ThisLoop.append(TabSpace+'{')


    TabSpace='\t'
    for k in range(NumDims):
		TabSpace+='\t'

    
###########

    for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
		StreamVar='Var'+str(VarNum)+'_Stream'+str(CurrStream)
		LHSVariableCurrStream=str(StreamVar)
		if(ConfigParams['RandomAccess'][VarNum]>0):
			LHSVariableCurrStream=(RandomAccessVarPerStream[CurrStream])
		else:
			for CurrDim in range(NumDims):
				LHSVariableCurrStream+='['+str(LHSIndicesPerStream[CurrStream][CurrDim])+']'
		
		#print "\n\t CurrStream: "+str(CurrStream)+" Var: "+str(LHSVariableCurrStream)
		#print "\n\t RHSExprnPerOperand: "+str(RHSExprnPerStream[CurrStream])
		if(ConfigParams['RandomAccess'][VarNum]):
			#AccumExprn=str(AccumVar[VarNum])+' += '+str(RandomAccessVarPerStream[CurrStream])+';'
			#ThisLoop.append(AccumExprn)
			#StreamExprn=LHSVariableCurrStream+'= ('+'(int) ('+str(RHSExprnPerStream[CurrStream])+') ) % ( '+str(ConfigParams['GlobalVar']['DimsSize'][(NumDims-1)])+' - '+str(ConfigParams['GlobalVar']['NumOperandsVar'][VarNum][CurrStream])+' ) ;'
			StreamExprn=LHSVariableCurrStream+'= ('+'(int) ('+str(RHSExprnPerStream[CurrStream])+') ) % ( '+str(PermuteSizeVarforStream[CurrStream])+' ) ;'
		else:
			StreamExprn=LHSVariableCurrStream+'='+'('+str(RHSExprnPerStream[CurrStream])+') ;'
		if debug:
			print "\n\t StreamExprn: "+str(StreamExprn)
		ThisLoop.append(StreamExprn)
    
    
    for k in range(NumDims+1): # NumDims+1 since we are looping over the loops! 
    	TabSpace='\t'
    	for l in range(NumDims-k):
    		TabSpace+="\t"
    	ThisLoop.append(TabSpace+'}')
    if(ConfigParams['RandomAccess'][VarNum]>0):	
	    PrintStmt='printf("\\n\t '
	    PrintSuffix=''
	    for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
			PrintStmt+=str((RandomAccessVarPerStream[CurrStream]))+' :%d '
			PrintSuffix+=','+str((RandomAccessVarPerStream[CurrStream]))
	    PrintStmt+='"'+str(PrintSuffix)+');'
	    #ThisLoop.append('printf(" ");')
	    ThisLoop.append(PrintStmt)
    else:
	    PrintStmt='printf("\\n\t '
	    PrintSuffix=''
    	    for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
			StreamVar='Var'+str(VarNum)+'_Stream'+str(CurrStream)
			for CurrDim in range(NumDims):
				StreamVar+='[('+str(LHSIndicesPerStream[CurrStream][CurrDim])+'-1)]'
			PrintStmt+=str(StreamVar)+' :%'+str(ConfigParams['DSforPrintf'][VarNum])
			PrintSuffix+=','+str(StreamVar)
	    PrintStmt+='\\n"'+str(PrintSuffix)+');'
	    #ThisLoop.append('printf(" ");')
	    ThisLoop.append(PrintStmt)	    
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
	File.write("\n")
	for i in range(len(Array)):
		File.write("\n\t "+str(Array[i])+"\n")
		
	#File.write("\n")	


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
	ConfigParams['StrideVar']={}
	ConfigParams['RandomAccess']=[]
	ConfigParams['OpDiff']=[]
		
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
	StrideForAllVarsNotFound=1
	FoundStrideForDims=0
	LoopIterationsNotFound=1
	RandomAccessNotFound=1
	OpDiffNotFound=1
	RandomAccessExtracted=0
	StrideExtracted=[]

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
					for i in range(NumVars):
						StrideExtracted.append(0)
					if debug:
						print "\n\t Number of variables is "+str(ConfigParams['NumVars'])+"\n"	
					if RandomAccessExtracted:
						if( len(ConfigParams['RandomAccess']) == ConfigParams['NumVars']):
							if debug:
								print "\n\t 1. RandomAccess found for all variables "
							RandomAccessNotFound=0
						else:
							print "\n\t ERROR: RandomAccess found for "+str(len(ConfigParams['RandomAccess']))+" expected it for "+str(ConfigParams['NumVars'])
							sys.exit()
					LineNotProcessed=0
					NumVarNotFound=0	

		if RandomAccessNotFound:
			MatchObj=re.match(r'\s*\#RandomAccess',CurrLine)
			if MatchObj:
				DimsLine=re.match(r'\s*\#RandomAccess\s*(.*)',CurrLine)
				if DimsLine:
					Temp=RemoveWhiteSpace(DimsLine.group(1))
					RandomAccessString=re.split(',',Temp)
					if debug:
						print "\n\t RandomAccessString: "+str(RandomAccessString)
					for CurrRandomAccess in RandomAccessString:
						if(IsNumber(CurrRandomAccess)):
							ConfigParams['RandomAccess'].append(int(CurrRandomAccess))
					#if debug:
					if not(NumVarNotFound):
						if( len(ConfigParams['RandomAccess']) == ConfigParams['NumVars']):
							if debug:
								print "\n\t RandomAccess found for all variables "
							RandomAccessNotFound=0	
						else:
							print "\n\t ERROR: RandomAccess found for "+str(len(ConfigParams['RandomAccess']))+" expected it for "+str(ConfigParams['NumVars'])
							sys.exit()
					else:
						RandomAccessExtracted=1
						print "\n\t RandomAccessExtracted: "+str(RandomAccessExtracted)+" RandomAccessNotFound "+str(RandomAccessNotFound)
				if debug:
					print "\n\t RandomAccessNotFound: "+str(RandomAccessNotFound)
				LineNotProcessed=0
							
							
					
		if NumStreamsDimsNotFound:
			MatchObj=re.match(r'\s*\#StreamDims',CurrLine)
			if MatchObj:
				if NumVarNotFound:
					print "\n\t ERROR: Expected to determine the number of variables before extracting stream for different variables. "
					sys.exit()
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
							CurrStreamDim=RemoveWhiteSpace(CurrStreamDim)
							ConfigParams['NumStreaminVar'].append( int(CurrStreamDim))
							CurrDim+=1				
							if debug:
					       			print "\n\t #Streams for dim "+str(CurrDim)+" is "+str(CurrStreamDim)+"\n" 
					if(CurrDim != ConfigParams['NumVars']):
						#if debug:
						print "\n\t The StreamDim parameter is not specified for each dimension. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions speciied is "+str(ConfigParams['Dims'])+"\n";
						sys.exit(0)
					else:
						for CurrVar in range(ConfigParams['NumVars']):
							ThisArray=[]
							for i in range(ConfigParams['NumStreaminVar'][CurrVar]):
								ThisArray.append(0)
							if debug:
								print"\n\t Var: "+str(CurrVar)+" ThisArray: "+str(ThisArray)
							ConfigParams['StrideinStream'].append(ThisArray)	
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
							ConfigParams['NumIters'].append(int(RemoveWhiteSpace(Iters[i])))
							if debug:
								print "\n\t Var: "+str(i)+" Loop-iterations: "+str(Iters[i])+"\n"	
					if(len(ConfigParams['NumIters'])!=ConfigParams['NumVars']):
						print "\n\t Number of iterations for nested loops is specified for "+str(len(ConfigParams['NumIters']))+" variables, expected for "+str(ConfigParams['NumVars'])
						sys.exit()
					else:
						LineNotProcessed=0
						LoopIterationsNotFound=0
						#sys.exit()
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
								CurrSize=RemoveWhiteSpace(CurrSize)
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

			if StrideForAllVarsNotFound and (not RandomAccessNotFound):
				MatchObj=re.match(r'\s*\#stride',CurrLine)
				if MatchObj:
					FindDim=re.match(r'\s*\#stride(\d+)+',CurrLine)
					SearchingDim=0
					if(FindDim):
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
									CurrStride=RemoveWhiteSpace(CurrStride)
									StrideInThisDim.append(int(CurrStride));
									Count+=1				
									if debug:
							       			print "\n\t Stride for stream "+str(Count) +' in dim '+str(SearchingDim)+" "+str(Count)+" is "+str(CurrStride)+"\n" 
							if(Count != ConfigParams['NumStreaminVar'][SearchingDim]):
								print "\n\t The stride parameter is not specified for specified number of streams in "+str(ConfigParams['NumStreaminVar'][SearchingDim])+" in variable "+str(SearchingDim)+", it is specified only for "+str(Count)+ " streams. "
								sys.exit(0)
							else:
								#ConfigParams['StrideinStream'].append(StrideInThisDim)
								#print "WARNING: ConfigParams['StrideinStream'] is not updated in traditional method!! "
								FoundStrideForDims+=1
								if(FoundStrideForDims==ConfigParams['NumVars']):
									StrideNotFound=0	
									#StrideForAllVarsNotFound=0
									if debug:
										print "\n\t Required stride for each stream in each dimension has been found!!! \n"
					else:
						FindOperations=re.match(r'\s*\#strideoperations_var(\d+)*_(\d+)*\s*\<(.*)\>',CurrLine)
						if FindOperations:
							if debug:
								print "\n\t stride-operations detected for var: "+str(FindOperations.group(1))+" expression: "+str(FindOperations.group(3))					
							CurrVar=int(RemoveWhiteSpace(FindOperations.group(1)))	
							CurrStream=int(RemoveWhiteSpace(FindOperations.group(2)))
							CurrExprn=RemoveWhiteSpace(FindOperations.group(3))
							if not(CurrVar in (ConfigParams['StrideVar'])):
								ConfigParams['StrideVar'][CurrVar]={}
								
							if CurrStream in (ConfigParams['StrideVar'][CurrVar]):
								print "\n\t ERROR:Conflicting statement found for stride and it's operations for variable "+str(CurrVar)+" and stream is "+str(CurrStream)
								sys.exit()
							else:
								ConfigParams['StrideVar'][CurrVar][CurrStream]={}
							ExprnBreakdown=re.split(';',CurrExprn)
							if ExprnBreakdown:
								if debug:
									print "\n\t ExprnBreakdown -- "+str(ExprnBreakdown)
								ConfigParams['StrideVar'][CurrVar][CurrStream]['Stride']=int(RemoveWhiteSpace(ExprnBreakdown[0]))
								if( (ConfigParams['RandomAccess'][CurrVar]>0) and (ConfigParams['StrideVar'][CurrVar][CurrStream]['Stride']>1) ):
									print "\n\t ERROR: Variable: "+str(CurrVar)+" has conflicting configurations requested in stream "+str(CurrStream)+" . Random Acess is requested with a stride greater than 1. "
									print "\n\t RandomAccess[Var] "+str(ConfigParams['RandomAccess'][CurrVar])+" Stride: "+str(ConfigParams['StrideVar'][CurrVar][CurrStream]['Stride'])
									print "\n\t CurrExprn: "+str(CurrExprn)
									sys.exit()
								ConfigParams['StrideinStream'][CurrVar][CurrStream]=ConfigParams['StrideVar'][CurrVar][CurrStream]['Stride']
								ConfigParams['StrideVar'][CurrVar][CurrStream]['NumOperands']=int(RemoveWhiteSpace(ExprnBreakdown[1]))
								NumOperands=ConfigParams['StrideVar'][CurrVar][CurrStream]['NumOperands']
								OperationsIdx=2
								OperandsIdx=3

								ExprnOperations=re.split(',',ExprnBreakdown[OperationsIdx])
								if ExprnOperations:
									ConfigParams['StrideVar'][CurrVar][CurrStream]['ExprnOperations']=[]
									if debug:
										print "\n\t Number of operations "+str(len(ExprnOperations))
									if( len(ExprnOperations)!=(NumOperands-1) ):
										if(len(ExprnOperations)>1):
											print "\n\t ERROR: Expected "+str(NumOperands-1)+" operations, but could find only "+str(len(ExprnOperations))
											#print "\n\t ExprnOperations: "+str(ExprnOperations)
											sys.exit()
										else:
											CheckEmpty=re.match('^\s*$',(ExprnOperations[0]) )
											if(CheckEmpty):
												if debug:
													print "\n\t Found a one operand RHS "
											else:
												print "\n\t ERROR: Expected "+str(NumOperands-1)+" operations, but could find only "+str(len(ExprnOperations))
												#print "\n\t ExprnOperations: "+str(ExprnOperations)
												sys.exit()
												
											
											
									else:
									
										for CurrOperation in ExprnOperations:
											CurrOperation=RemoveBraces(CurrOperation)
											CheckOperation=re.match('\s*[\+\-\*\/]',CurrOperation)
											if CheckOperation:
												ConfigParams['StrideVar'][CurrVar][CurrStream]['ExprnOperations'].append(CurrOperation)
												if debug:
													print "\n\t stream "+str(CurrStream)+" and variable "+str(CurrVar)+" CurrOperation "+str(CurrOperation)
											elif(CurrOperation=='0'):
												ConfigParams['StrideVar'][CurrVar][CurrStream]['ExprnOperations'].append(0)
												if debug:
													print "\n\t stream "+str(CurrStream)+" and variable "+str(CurrVar)+" CurrOperation "+str(CurrOperation)
											
											
											else:
												print "\n\t ERROR: Expected one of \"+-*/\" as operation. Use debug to locate source of the error"
												print "\n\t CurrOperation "+str(CurrOperation)
												sys.exit()
								else:
									print "\n\t ERROR: Unable to extract operations b/n operands  of stream "+str(CurrStream)+" and variable "+str(CurrVar)
								
								ConfigParams['StrideVar'][CurrVar][CurrStream]['Operands']={}
								OperandsSet=RemoveBraces(ExprnBreakdown[OperandsIdx])
								OperandsBreakdown=re.split(',',OperandsSet)
								if OperandsBreakdown:
									FoundNumOperands=len(OperandsBreakdown)
									if(FoundNumOperands!=NumOperands):
										print "\n\t ERROR: Was expecting "+str(NumOperands)+" number of operands, but obtained "+str(FoundNumOperands)+" operands "
										sys.exit()
									else:
										for i in range(NumOperands):
											ConfigParams['StrideVar'][CurrVar][CurrStream]['Operands'][i]= (OperandsBreakdown[i])
											if debug:
												print "\n\t i: "+str(i)+" Operands: "+str(OperandsBreakdown[i])
								
								StrideExtracted[CurrVar]+=1
							else:
								print "\n\t Not able to extract the expression for var: "+str(CurrVar)+" and stream "+str(CurrStream)
								sys.exit()	
							
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
								CurrAlloc=RemoveWhiteSpace(CurrAlloc)
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
			if OpDiffNotFound:
				MatchObj=re.match(r'\s*\#OpDiff',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					OpDiff=re.split(',',tmp[1])
					if Init:
						LineNotProcessed=0
						VarCount=0;
						for CurrOpDiff in OpDiff:
							CheckSpace=re.match(r'^\s*$',str(CurrInit))
						        if(CheckSpace):
						       		if debug:
						       			print "\n\t For init parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)						
							else:
								CurrOpDiff=int(RemoveWhiteSpace(CurrOpDiff))#re.sub(r'\s*$','',CurrInit)
								ConfigParams['OpDiff'].append(CurrOpDiff);
								VarCount+=1				
								if debug:
						       			print "\n\t OpDiff for var "+str(CurrDim)+" is "+str(CurrOpDiff)+"\n" 					
						if(VarCount!= ConfigParams['NumVars']):
							print "\n\t The init expression is not specified for each variable. It is specified only for "+str(CurrDim)+ " dimensions while number of dimensions specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit(0)
						else:
							OpDiffNotFound=0	



		if LineNotProcessed:
			if debug:
				print "\n\t Info is not processed in line: "+str(LineCount)+"\n";
		
	
	#Tabs: 1
	AllStridesAvailable=0
	if debug:
		print "\n\t StrideExtracted "+str(StrideExtracted)
	
	for CurrVar in range(len(StrideExtracted)):
		if debug:
			print "\n\t Var: "+str(CurrVar)+" expected stream expression for "+str(ConfigParams['NumStreaminVar'][CurrVar])+" and have extracted "+str(StrideExtracted[CurrVar])	
		if(ConfigParams['NumStreaminVar'][CurrVar] == StrideExtracted[CurrVar] ):
			AllStridesAvailable+=1
		
	if(AllStridesAvailable==ConfigParams['NumVars']):
		StrideForAllVarsNotFound=0
		StrideNotFound=0
	else:
		print "\n\t AllStridesAvailable: "+str(AllStridesAvailable)+" ConfigParams['NumVars'] "+str(ConfigParams['NumVars'])
	#sys.exit()
	if debug:
		print "\n\t RandomAccessNotFound: "+str(RandomAccessNotFound)
	if( (NumVarNotFound==0) and (DimNotFound==0) and (SizeNotFound==0) and (StrideNotFound==0) and (AllocNotFound==0) and (DSNotFound==0) and (InitNotFound==0) and (NumStreamsDimsNotFound==0) and (LoopIterationsNotFound==0) and (RandomAccessNotFound==0) and (OpDiffNotFound==0) ):
		print "\n\t The config file has all the required info: #dims, size and allocation and initialization for all the dimensions! "	
		InitAlloc=[]
		LibAlloc=[]
		ConfigParams['indices']=[]
		tmp='#include<stdio.h>'
		LibAlloc.append(tmp)
		tmp='#include<stdlib.h>'
		LibAlloc.append(tmp)
		tmp='#include <time.h>'
		LibAlloc.append(tmp)
		
#LAURA ADDED
		PinToFunc=[]
		PinToFunc.append('#define __USE_GNU 1')
    		PinToFunc.append('#include <sched.h>')
    		PinToFunc.append('// pins this process to core c')
    		PinToFunc.append('void pinto(int c){')
    		PinToFunc.append('   cpu_set_t cpuset;')
    		PinToFunc.append('   CPU_ZERO(&cpuset);')
    		PinToFunc.append('   CPU_SET(c, &cpuset);')
    		PinToFunc.append(' ')
    		PinToFunc.append('   if(sched_setaffinity(getpid(), sizeof(cpu_set_t), &cpuset) < 0) {')
    		PinToFunc.append('      fprintf(stderr, "Cannot pin process %d to core %d\\n", getpid(), c);')
    		PinToFunc.append('      exit(1);')
    		PinToFunc.append('   }')
    		PinToFunc.append('   if(c==0)')
    		PinToFunc.append('   fprintf(stdout, "Setting affinity to cpu%u for caller task pid %d\\n", c, getpid());')
    		PinToFunc.append('}')
		PinToFunc.append('#include <sys/time.h>')
		PinToFunc.append('double rtclock()')
		PinToFunc.append('{')
    		PinToFunc.append('struct timezone Tzp;')
    		PinToFunc.append('struct timeval Tp;')
    		PinToFunc.append('int stat;')
    		PinToFunc.append('stat = gettimeofday (&Tp, &Tzp);')
    		PinToFunc.append('if (stat != 0) printf("Error return from gettimeofday: %d",stat);')
    		PinToFunc.append('return(Tp.tv_sec + Tp.tv_usec*1.0e-6);')
		PinToFunc.append('}')
#LAURA END ADD
		LibAlloc.append('#include <mpi.h>')

		MainFunc=[]	
		tmp='int main(int argc,char* argv[])'	
		MainFunc.append(tmp)
		MainFunc.append('\n\t{')	
		MPI_Stuff=[]
		MPI_Stuff.append('int rank,MPI_Size;');
		MPI_Stuff.append('MPI_Init(&argc,&argv);');
		MPI_Stuff.append('MPI_Comm_rank( MPI_COMM_WORLD, &rank);');
                MPI_Stuff.append('pinto(rank);');   #LAURA
		MPI_Stuff.append('MPI_Comm_size( MPI_COMM_WORLD, &MPI_Size);');
			
		#tmp='int main()'	
		#InitAlloc.append(tmp)
		#InitAlloc.append('\n\t{')				
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
###

		ConfigParams['GlobalVar']={}
		ConfigParams['GlobalVar']['NumIters']=[]
		ConfigParams['GlobalVar']['NumItersDecl']=[]
		ConfigParams['GlobalVar']['NumItersLastDimVar']=[]
		ConfigParams['GlobalVar']['NumItersLastDimVarDecl']=[]

		for i in range(ConfigParams['NumVars']):
			CurrVarNumLoopVar='NumLoops_Var'+str(i)
			CurrVarNumLoopVarDecl='long int '+str(CurrVarNumLoopVar)+' = '+str(ConfigParams['NumIters'][i])+' ;'
			CurrVarNumLoopLastDimVar='NumLoops_Var'+str(i)+'_LastDim'
			CurrVarNumLoopLastDimVarDecl='long int '+str(CurrVarNumLoopLastDimVar)+' = ( '+str(ConfigParams['NumIters'][i])+' * 10 ) ;'
			#print "\n\t CurrVar: "+str(i)+" CurrVarNumLoopVar: "+str(CurrVarNumLoopVar)+" CurrVarNumLoopVarDecl "+str(CurrVarNumLoopVarDecl)
			ConfigParams['GlobalVar']['NumIters'].append(CurrVarNumLoopVar)
			ConfigParams['GlobalVar']['NumItersDecl'].append(CurrVarNumLoopVarDecl)
			ConfigParams['GlobalVar']['NumItersLastDimVar'].append(CurrVarNumLoopLastDimVar)
			ConfigParams['GlobalVar']['NumItersLastDimVarDecl'].append(CurrVarNumLoopLastDimVarDecl)
			

		ConfigParams['GlobalVar']['Stream']={}	
		ConfigParams['GlobalVar']['Stream']['StrideVarDecl']=[]				
		ConfigParams['GlobalVar']['NumOperandsVar']={}
		ConfigParams['GlobalVar']['NumOperandsVar']['NumOperandsVarDecl']=[]

		for index in range(ConfigParams['NumVars']):
			ConfigParams['GlobalVar']['Stream'][index]=[]
			ConfigParams['GlobalVar']['NumOperandsVar'][index]=[]
			
			if debug:
				print "\n -- NumStreams: "+str(ConfigParams['NumStreaminVar'][index])
			for CurrStream in range(ConfigParams['NumStreaminVar'][index]):
				StrideVar='StrideVar'+str(index)+"_Stream"+str(CurrStream)
				StrideVarDecl='int '+str(StrideVar)+' = '+str(ConfigParams['StrideinStream'][index][CurrStream])+' ;'
				NumOperandsVar='NumOperandsVar'+str(index)+'_Stream'+str(CurrStream)
				NumOperandsVarDecl='int '+str(NumOperandsVar)+' = '+str(ConfigParams['StrideVar'][index][CurrStream]['NumOperands'])+' ; '

				ConfigParams['GlobalVar']['Stream'][index].append(StrideVar)
				ConfigParams['GlobalVar']['Stream']['StrideVarDecl'].append(StrideVarDecl)
				ConfigParams['GlobalVar']['NumOperandsVar'][index].append(NumOperandsVar)
				ConfigParams['GlobalVar']['NumOperandsVar']['NumOperandsVarDecl'].append(NumOperandsVarDecl)

				if debug:
					print "\n\t CurrStream: "+str(CurrStream)+" index "+str(index)+" stride<><> "+str(ConfigParams['StrideinStream'][index][CurrStream])
					print "\t\t Var: "+str(StrideVar)+" StrideVarDecl "+str(StrideVarDecl)

		ConfigParams['GlobalVar']['MaxStream']={}
		for index in range(ConfigParams['NumVars']):
			MaxStride=0
			MaxStrideIdx=-1
			for CurrStream in range(ConfigParams['NumStreaminVar'][index]):
				if( MaxStride < ConfigParams['StrideinStream'][index][CurrStream]):
					if debug:
						print "\n\t CurrStream: "+str(CurrStream)+" index "+str(index)+" existing max stride "+str(MaxStride)+" new max stride "+str(ConfigParams['StrideinStream'][index][CurrStream])
					MaxStride= ConfigParams['StrideinStream'][index][CurrStream] 
					MaxStrideIdx=CurrStream
			ConfigParams['GlobalVar']['MaxStream'][index]=ConfigParams['GlobalVar']['Stream'][index][MaxStrideIdx]


		ConfigParams['GlobalVar']['DimsSize']=[]
		ConfigParams['GlobalVar']['DimsSizeDecl']=[]
		for index in range(ConfigParams['Dims']):
			SizeVar='Size_Dim'+str(index)
			SizeVarDecl='long int '+str(SizeVar)+' = '+str(ConfigParams['size'][index])+' ;'
			if debug:
				print "\n\t Dim: "+str(index)+" Var: "+str(SizeVar)+" declaration "+str(SizeVarDecl)
			ConfigParams['GlobalVar']['DimsSize'].append(SizeVar)
			ConfigParams['GlobalVar']['DimsSizeDecl'].append(SizeVarDecl)
			
		ConfigParams['GlobalVar']['SuccessiveOperandDiff']=[]
		ConfigParams['GlobalVar']['SuccessiveOperandDiffDecl']=[]
		for index in range(ConfigParams['NumVars']):
			OpDiffVar='OpDiffVar'+str(index)
			OpDiffVarDecl='int '+str(OpDiffVar)+' = '+str(ConfigParams['OpDiff'][index])+' ;'
			#if debug:
			print "\n\t Var: "+str(index)+" OpDiffVar "+str(OpDiffVar)+" Decl: "+str(OpDiffVarDecl)
			ConfigParams['GlobalVar']['SuccessiveOperandDiff'].append(OpDiffVar)
			ConfigParams['GlobalVar']['SuccessiveOperandDiffDecl'].append(OpDiffVarDecl)
		
###
		
		ConfigParams['DSforPrintf']=[]			
		for index in range(ConfigParams['NumVars']):
				VarDeclStmt=[]
			
				VarDecl=''
				datatype=''
				if(ConfigParams['datastructure'][index]=='f' or ConfigParams['datastructure'][index]=='float'):
					VarDecl='float' 
					datatype=VarDecl
					ConfigParams['DSforPrintf'].append('f')
					if debug:
						print "\n\t Allocated float to variable "+str(index)
				elif(ConfigParams['datastructure'][index]=='d' or ConfigParams['datastructure'][index]=='double'):
					VarDecl='double' 
					datatype=VarDecl
					ConfigParams['DSforPrintf'].append('lf')
					if debug:
						print "\n\t Allocated double to variable "+str(index)				
				elif(ConfigParams['datastructure'][index]=='i' or ConfigParams['datastructure'][index]=='integer'):
					VarDecl='int' 
					datatype=VarDecl
					ConfigParams['DSforPrintf'].append('d')
					if debug:
						print "\n\t Allocated integer to variable "+str(index)								
				elif(ConfigParams['datastructure'][index]=='l' or ConfigParams['datastructure'][index]=='long'):
					VarDecl='long int' 
					datatype=VarDecl
					ConfigParams['DSforPrintf'].append('ld')
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
						if(ConfigParams['RandomAccess'][index] >0 ):
							FlushVar=' FlushVar'+str(index)+'_Stream'+str(CurrStream)
							
						
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
						if(ConfigParams['RandomAccess'][index] >0 ):
							#FlushVar=
							FlushVarDecl=datatype+prefix+FlushVar+';'
							DynAlloc.append(FlushVarDecl)
							if debug:
								print "\n\t FlushVarDecl: "+str(FlushVarDecl)
							
							if(ConfigParams['Dims']==1):
								#tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['Stream'][index][CurrStream])+' * sizeof('+datatype+suffix+'))'+';'	
								tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'	
								FlushTmp=FlushVar+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'
								DynAlloc.append(tmp)
								DynAlloc.append(FlushTmp)	
							else:
								tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+' * sizeof('+datatype+suffix+'))'+';'
								FlushTmp=FlushVar+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+' * sizeof('+datatype+suffix+'))'+';'
								DynAlloc.append(tmp)
								DynAlloc.append(FlushTmp)
						else:
							if(ConfigParams['Dims']==1):
								#tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['Stream'][index][CurrStream])+' * sizeof('+datatype+suffix+'))'+';'	
								tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'	
							else:
								tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+' * sizeof('+datatype+suffix+'))'+';'

										
							DynAlloc.append(tmp);
						  		
					if debug:
						print "\n\t This is how the first malloc statement look: "+str(tmp)+"\n"
				
					if(ConfigParams['Dims']>1):
						NumForLoops=''
						for i in range(ConfigParams['Dims']-1):
							NumForLoops=i+1
							MallocLHS=''
							for j in range(NumForLoops):
								ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+	str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
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
								if(ConfigParams['RandomAccess'][index] >0 ):
									FlushVar=' FlushVar'+str(index)+'_Stream'+str(CurrStream)								
								if(ConfigParams['RandomAccess'][index]>0):
								
									if(i==(ConfigParams['Dims']-2)): # Since the loop is going from 0 to ConfigParams['Dims']-2
										#MallocEqn=var+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * '+str(ConfigParams['GlobalVar']['Stream'][index][CurrStream])+' * sizeof('+datatype+suffix+'))'+';'
										MallocEqn=var+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * '+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'
										FlushMallocEqn=FlushVar+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * '+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'
									else:
										MallocEqn=var+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * sizeof('+datatype+suffix+'))'+';'		
										FlushMallocEqn=FlushVar+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * sizeof('+datatype+suffix+'))'+';'		
									DynAlloc.append(MallocEqn)
									DynAlloc.append(FlushMallocEqn)
								
								else:
								
									if(i==(ConfigParams['Dims']-2)): # Since the loop is going from 0 to ConfigParams['Dims']-2
										#MallocEqn=var+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * '+str(ConfigParams['GlobalVar']['Stream'][index][CurrStream])+' * sizeof('+datatype+suffix+'))'+';'
										MallocEqn=var+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * '+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'
									else:
										MallocEqn=var+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * sizeof('+datatype+suffix+'))'+';'		
									DynAlloc.append(MallocEqn)
						   		if debug:
									print "\t The malloc equation is: "+str(MallocEqn)+"\n"
							for j in range(NumForLoops):
								DynAlloc.append('}')
					
				else:
					
					VarDecl=''				
					for CurrDim in range(Dims-1):
						VarDecl+='['+str(ConfigParams['GlobalVar']['DimsSize'][CurrDim])+']'					
					for CurrStream in range(ConfigParams['NumStreaminVar'][index]):
						CurrStreamVar=' Var'+str(index)+'_Stream'+str(CurrStream)
						StreamVarDecl=datatype+' '+CurrStreamVar+VarDecl+'['+str(ConfigParams['GlobalVar']['DimsSize'][ConfigParams['Dims']-1])+' * '+str(ConfigParams['StrideinStream'][index][CurrStream])+']'
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
			if index:
				StrideString+='_'
			for CurrStream in range(ConfigParams['NumStreaminVar'][index]):
				if debug:
					print "\n\t -- CurrStream: "+str(CurrStream)+" index "+str(index)+" stride<><> "+str(ConfigParams['StrideinStream'][index][CurrStream])+" StrideString: "+str(StrideString)
				StrideString+=str(ConfigParams['StrideinStream'][index][CurrStream])#+'_'
		
		index=ConfigParams['NumVars']-1
		
		for CurrStream in range(ConfigParams['NumStreaminVar'][index]-1):
			if debug:
				print "\n\t 2. CurrStream: "+str(CurrStream)+" index "+str(index)+" stride<><> "+str(ConfigParams['StrideinStream'][index][CurrStream])+" StrideString: "+str(StrideString)
			StrideString+=str(ConfigParams['StrideinStream'][index][CurrStream])+'_'
		if( (StrideString!='' ) and ( ConfigParams['NumStreaminVar'][index]==1 ) ):
			StrideString+='_'+str(ConfigParams['StrideinStream'][index][(ConfigParams['NumStreaminVar'][index]-1)])
		else:
			StrideString+=str(ConfigParams['StrideinStream'][index][(ConfigParams['NumStreaminVar'][index]-1)])
			
		if debug:
			print "\n\t StrideString: "+str(StrideString)+" ConfigParams['NumStreaminVar'] "+str(ConfigParams['NumStreaminVar'])

		OpStream=''
		for VarIdx,CurrVar in enumerate(ConfigParams['StrideVar']):
			Temp=''
			for Idx,CurrStream in enumerate(ConfigParams['StrideVar'][CurrVar]):
				for OpertnIdx,CurrOperatn in enumerate(ConfigParams['StrideVar'][CurrVar][CurrStream]['ExprnOperations']):
					
					if(CurrOperatn=='+'):
						if OpertnIdx:
							Temp+='p'
						else:
							Temp+='P'
					if(CurrOperatn=='-'):
						if OpertnIdx:
							Temp+='s'
						else:
							Temp+='S'
					if(CurrOperatn=='*'):
						if OpertnIdx:
							Temp+='m'
						else:
							Temp+='M'
					if(CurrOperatn=='/'):
						if OpertnIdx:
							Temp+='d'
						else:
							Temp+='D'
					if(CurrOperatn==''):
						Temp+='0'
					if debug:
						print "\n\t CurrVar: "+str(CurrVar)+" CurrStream "+str(CurrStream)+" CurrOperatn "+str(CurrOperatn)+" Temp "+str(Temp)
				if(len(ConfigParams['StrideVar'][CurrVar][CurrStream]['ExprnOperations'])==0):
					Temp+='0'
					if debug:
						print "\n\t Temp: "+str(Temp)+" (ConfigParams['StrideVar'][CurrVar][CurrStream]['ExprnOperations']): "+str((ConfigParams['StrideVar'][CurrVar][CurrStream]['ExprnOperations']))
			if(VarIdx):
				OpStream+='_'+Temp
			else:
				OpStream+=Temp
		
		if debug:
			print "\n\t OpStream: "+str(OpStream)
		
		alloc_str=''
		for CurrAlloc in ConfigParams['alloc']:
			alloc_str+=str(CurrAlloc)
			
		StreamString=''
		for i in range(ConfigParams['NumVars']-1):
			StreamString+=str(ConfigParams['NumStreaminVar'][i])+'_'
		
		StreamString+=str(ConfigParams['NumStreaminVar'][ConfigParams['NumVars']-1])
		
		IterString='_'
			
		for i in range(ConfigParams['NumVars']-1):
			IterString+=str(ConfigParams['NumIters'][i])+'_'
		IterString+=str(ConfigParams['NumIters'][ConfigParams['NumVars']-1])
		
		DSString=''
		for i in range(ConfigParams['NumVars']):
			DSString+=str(ConfigParams['datastructure'][i])

		RandomAccessString=''
		for i in range(ConfigParams['NumVars']):
				RandomAccessString+=str(ConfigParams['RandomAccess'][i])	
 		if debug:
 			print "\n\t -- DSString: "+str(DSString)+" -- "				
	else:
		print "\n\t The config file has DOES NOT HAVE all the required info: #dims, size and allocation for all the dimensions. If this message is printed, there is a bug in the script, please report. "

		print "\n\t (NumVarNotFound) "+str(NumVarNotFound)+" (DimNotFound) "+str(DimNotFound)+" SizeNotFound: "+str(SizeNotFound)
		print "\n\t StrideNotFound "+str(StrideNotFound)+" AllocNotFound: "+str(AllocNotFound)+" InitNotFound: "+str(InitNotFound)
		print "\n\t NumStreamsDimsNotFound=: "+str(NumStreamsDimsNotFound)+" LoopIterationsNotFound: "+str(LoopIterationsNotFound)
		print "\n\t RandomAccessNotFound: "+str(RandomAccessNotFound)+" OpDiffNotFound: "+str(OpDiffNotFound)
		print "\n\n"
 		sys.exit(0)
	
	SrcFileName='StrideBenchmarks_Iters'+str(IterString)+'_Vars_'+str(ConfigParams['NumVars'])+"_DS_"+str(DSString)+'_Alloc_'+alloc_str+'_Dims_'+str(ConfigParams['Dims'])+'_Size_'+str(SizeString)+'_Random_'+str(RandomAccessString)+'_Streams_'+str(StreamString)+'_Ops_'+str(OpStream)+'_Stride_'+str(StrideString)+'.c'
	WriteFile=open(SrcFileName,'w')			
	InitLoop=[]
	
	WorkigVarsDecl=[]
	WorkingVars={}
	for VarNum in range(ConfigParams['NumVars']):
		if(ConfigParams['RandomAccess'][VarNum]>0):
			TabSpace='\t'
			#for Idx in range(ConfigParams['Dims']):
			#	TabSpace+='\t'
			BoundVar='bound'
			WorkingVars['BoundVar']=BoundVar
			BoundVarDecl=TabSpace+'long int '+BoundVar+' =0; '
			WorkigVarsDecl.append(BoundVarDecl);
			InnerLoopVar='InnerLoopVar'
			WorkingVars['InnerLoopVar']=InnerLoopVar
			InnerLoopVarDecl=TabSpace+'long int '+InnerLoopVar+' =0;'
			WorkigVarsDecl.append(InnerLoopVarDecl)
			TempVar='temp'
			TempVarDecl=TabSpace+'long int '+str(TempVar)+';'
			NumOperandsVar='NumOperands'
			WorkingVars['NumOperandsVar']=NumOperandsVar
			NumOperandsVarDecl=TabSpace+'int '+str(NumOperandsVar)+';'#+'= '+str(ConfigParams['StrideVar'][VarNum][StreamNum]['NumOperands'])+' ;'
			WorkigVarsDecl.append(TempVarDecl);
			WorkigVarsDecl.append(NumOperandsVarDecl)
    			PermuteIndexVar='PermuteIndex'
    			WorkingVars['PermuteIndexVar']=PermuteIndexVar
    			PermuteIndexVarDecl='int PermuteIndex=0 ;'
    			WorkigVarsDecl.append(PermuteIndexVarDecl)			
    			CountVar='CountVar'
    			CountVarDecl='int '+str(CountVar)+' = 0;'
    			WorkingVars['CountVar']=CountVar
    			WorkigVarsDecl.append(CountVarDecl)
			break;
	
	for VarNum in range(ConfigParams['NumVars']):
		ThisVarInit=[]
		for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
			CurrVarName='Var'+str(VarNum)+'_Stream'+str(CurrStream)
			Temp=InitVar(CurrVarName,VarNum,CurrStream,ConfigParams,WorkingVars,debug)	
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
	PermuteGenFuncArray=[]
	
	PermuteGenFuncArray.append('int* RandomPermutationGeneration(int Size)')
	PermuteGenFuncArray.append('{')

	PermuteGenFuncArray.append('	int i=0;')
	PermuteGenFuncArray.append('	int *A,*ToFlag;')
	
	PermuteGenFuncArray.append('	A=malloc(Size*sizeof(int));')
	PermuteGenFuncArray.append('	ToFlag=calloc(Size,sizeof(int));')

	PermuteGenFuncArray.append('	int Count=0;')
	PermuteGenFuncArray.append('	int Node=0;')
	PermuteGenFuncArray.append('	int JumpTo;')

	PermuteGenFuncArray.append('	while(Count< (Size-1))')
	PermuteGenFuncArray.append('	{')
	PermuteGenFuncArray.append('		JumpTo=(int)(rand()%Size);')
	PermuteGenFuncArray.append('		//printf("\\n\t Count: %d Node: %d whose from trying to reach to %d whose toflag is %d ",Count,Node,JumpTo,ToFlag[JumpTo]);')
	PermuteGenFuncArray.append('\n')		
	PermuteGenFuncArray.append('		if( (ToFlag[JumpTo]==0 ) ) //&& ( FromFlag[JumpTo]==0) )')
	PermuteGenFuncArray.append('		{')
	PermuteGenFuncArray.append('			Count++;')
	PermuteGenFuncArray.append('			A[Node]=JumpTo;')
	PermuteGenFuncArray.append('			ToFlag[JumpTo]++;')
	PermuteGenFuncArray.append('			ToFlag[Node]++;')
	PermuteGenFuncArray.append('			//printf("\\n\t Node: %d A[Node]: %d JumpTo: %d ToFlag[Jumpto]: %d ",Node,A[Node],JumpTo,ToFlag[JumpTo]);')
	PermuteGenFuncArray.append('			Node=JumpTo;')
	PermuteGenFuncArray.append('		}')
	PermuteGenFuncArray.append('\n ')		

	PermuteGenFuncArray.append('	}')
	PermuteGenFuncArray.append('	A[Node]=0;')
	PermuteGenFuncArray.append('	int Sum=0;')
	PermuteGenFuncArray.append('	for(i=0;i<Size;i++)')
	PermuteGenFuncArray.append('	{')
	PermuteGenFuncArray.append('		//printf("\\n\t i: %d A[i]: %d ",i,A[i]);')
	PermuteGenFuncArray.append('		Sum+=A[i];')
	PermuteGenFuncArray.append('	}')
	PermuteGenFuncArray.append('	//printf("\\n\t Sum: %d \\n\\n",Sum);')
	PermuteGenFuncArray.append('	free(ToFlag);')
	PermuteGenFuncArray.append('')
	PermuteGenFuncArray.append('return A;')

	PermuteGenFuncArray.append('}')
		
	WriteArray(LibAlloc,WriteFile)	
	WriteArray(ConfigParams['GlobalVar']['NumItersDecl'],WriteFile)
	WriteArray(ConfigParams['GlobalVar']['NumItersLastDimVarDecl'],WriteFile)
	WriteArray(ConfigParams['GlobalVar']['Stream']['StrideVarDecl'],WriteFile)
	WriteArray( ConfigParams['GlobalVar']['NumOperandsVar']['NumOperandsVarDecl'],WriteFile)
	WriteArray(ConfigParams['GlobalVar']['DimsSizeDecl'],WriteFile)
	WriteArray(ConfigParams['GlobalVar']['SuccessiveOperandDiffDecl'],WriteFile)
	WriteArray(PinToFunc,WriteFile)
	WriteArray(PermuteGenFuncArray,WriteFile)	
	
	for VarNum in range(ConfigParams['NumVars']):
		WriteArray(ThisLoop[VarNum],WriteFile)
	
	WriteArray(MainFunc,WriteFile)
	WriteArray(MPI_Stuff,WriteFile)
	WriteArray(InitAlloc,WriteFile)
	WriteArray(DynAlloc,WriteFile)
	WriteFile.write("\n\t long int Sum=0;")
	WriteFile.write("\n\t struct timeval start,end;")
        WriteFile.write("\n\t double etime,stime;")
        WriteFile.write("\n\t double time_buf[MPI_Size];")
	WriteFile.write("\n\t double currtime;")

        WriteFile.write('\n\t gettimeofday(&start,NULL);')
        WriteFile.write('\n\t currtime=(start.tv_sec+start.tv_usec/1000000.0); ')
        WriteFile.write("\n\t srand(currtime); ")


	WriteArray(WorkigVarsDecl,WriteFile)
	for VarNum in range(ConfigParams['NumVars']):
		for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):	
			WriteArray(InitLoop[VarNum][CurrStream],WriteFile)	

 
	WriteArray(Comments,WriteFile)	

	for VarNum in range(ConfigParams['NumVars']):
		prefix='printf(" \\n\\t '
		if(ConfigParams['RandomAccess'][VarNum]>0):
			for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
				FlushVar='FlushVar'+str(VarNum)+'_Stream'+str(CurrStream)
				prefix+=str(FlushVar)+' %d '
				suffix+=','+str(FlushVar)+'[(int) ( rand() % '+str(ConfigParams['size'][ConfigParams['Dims']-1]) +' )]'
	PrintFlushVar=str(prefix)+' \\n " '+str(suffix)+' ); '
	WriteFile.write(PrintFlushVar)
	#print "\n\t "+str(PrintFlushVar)
			#print "\n\t VarNum: "+str(VarNum)
			
	WriteFile.write('\n\t printf("\\n");')
	WriteFile.write('\n\tMPI_Finalize();')
	WriteFile.write("\n\t return 0;")
	WriteFile.write("\n\t}")
	WriteFile.close()		
		
	
		
					



if __name__ == "__main__":
   main(sys.argv[1:])
