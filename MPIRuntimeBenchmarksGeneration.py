 #!/usr/bin/python

#### Pending items:
# * To allocate stride*limit number of elements. -  Done
# * To write allocated elements into a file. - Done
#

import sys, getopt,re,math


def usage():
	print "\n\t Usage: StrideBenchmarks.py -c/--config -d \n\t\t -c: file with all the configuration.\n\t\t -d: Debug option, 1 for printing debug messages and 0 to forego printing debug statements. \n "
	sys.exit()

def ObtainDS(CurrDS):
	datatype=''
	CurrDS=RemoveWhiteSpace(CurrDS)
	if(CurrDS=='i'):
		datatype='int'
	elif(CurrDS=='f'):
		datatype='float'
	elif(CurrDS=='d'):
		datatype='double'
	elif(CurrDS=='l'):
		datatype='long int'
	else:
		print "\n\t ERROR: Supported datatype is int/float/double/long int, but requested datatype is: "+str(CurrDS)
		sys.exit()
	return datatype


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

def IsInt(s):
# Credits: StackExchange: DanielGoldberg: http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
	try:
		float(s)
		try:
			int(s)
			return True
		except ValueError:
			return False
	except ValueError:
		return False

def RemoveBraces(Input):
	temp=re.sub('^\s*\(*','',Input)
	Output=re.sub('\)*\s*$','',temp)
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

      	j=NumForLoops-1
 	ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'	
 
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


def InitVar(CurrVarName,VarNum,StreamNum,ConfigParams,WorkingVars,debug,Indirection=0):

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
	    	BoundVar=WorkingVars['BoundVar'] #'bound'     		#BoundVarDecl=TabSpace+'long int '+BoundVar+' =0; '     		#ThisLoop.append(BoundVarDecl);
    		InnerLoopVar=WorkingVars['InnerLoopVar']
    		#InnerLoopVarDecl=TabSpace+'long int '+InnerLoopVar+' =0;' 
    		#ThisLoop.append(InnerLoopVarDecl)    		#TempVar='temp'   		#TempVarDecl=TabSpace+'long int '+str(TempVar)+';'       		#ThisLoop.append(TempVarDecl);
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
    		PermuteSizeCalc=TabSpace+str(PermuteSizeVar)+' = (int) ( ( '+str(ConfigParams['GlobalVar']['DimsSize'][LastDim])+' * '+str(ConfigParams['GlobalVar']['Stream'][VarNum][StreamNum])+' ) / ( '+str(ConfigParams['GlobalVar']['NumOperandsVar'][VarNum][StreamNum])+' * '+str(ConfigParams['GlobalVar']['SuccessiveOperandDiff'][VarNum])+') );'
	    	ThisLoop.append(PermuteSizeCalc)
    		CallPermuteFunc=TabSpace+str(PermuteArrayVar)+' = RandomPermutationGeneration( '+str(PermuteSizeVar)+' );'
    		ThisLoop.append(CallPermuteFunc)
	    	FlushForLoop.append(CallPermuteFunc)
    		PermuteIndexVar='PermuteIndex'
    		PermuteIndexVarInit=' PermuteIndex=0 ;'
    		CountVar=WorkingVars['CountVar']
    		TempCountVar=WorkingVars['TempCountVar']
    		ThisLoop.append(PermuteIndexVarInit)		
	LHSindices=''
	if(ConfigParams['RandomAccess'][VarNum] >0):
		for j in range(NumForLoops):
			TabSpace='\t'
			for k in range(j):
				TabSpace+='\t'
			ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
			ThisLoop.append(TabSpace+ThisForLoop)
			ThisLoop.append(TabSpace+'{')
			LHSindices+='['+str(ConfigParams['indices'][j])+']'	
		Eqn="\t\t"+TabSpace+str(CurrVarName)+LHSindices+' = 0; '
		ThisLoop.append(Eqn)
	        for k in range(NumForLoops):
        	        TabSpace='' #\t' 
                	for l in range(NumForLoops-k):
                        	TabSpace+="\t"
                	ThisLoop.append(TabSpace+'}')

			
	LHSindices=''
    	for j in range(NumForLoops):
		TabSpace='\t'
		for k in range(j):
			TabSpace+='\t'
    		DontSkip=1
    		if(j==NumForLoops-1):
	    		if(ConfigParams['RandomAccess'][VarNum]>0):
    				LoopStmt=[]
				LoopStmt.append(TabSpace+'for('+str(ConfigParams['indices'][j])+'=0 , '+str(PermuteIndexVar)+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+= ( '+str(ConfigParams['GlobalVar']['SuccessiveOperandDiff'][VarNum])+' * '+str(ConfigParams['GlobalVar']['NumOperandsVar'][VarNum][StreamNum])+') , '+str(PermuteIndexVar)+'+=1) ')
				LoopStmt.append(TabSpace+'{')
				LoopStmt.append(TabSpace+'\t '+str(BoundVar)+'= '+str(ConfigParams['indices'][j])+' + '+str(ConfigParams['GlobalVar']['SuccessiveOperandDiff'][VarNum])+' ;')
 				for CurrLine in LoopStmt:
					ThisLoop.append(CurrLine)
					FlushForLoop.append(CurrLine)
				
				DontSkip=0
			else:
				#ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' * '+str(ConfigParams['GlobalVar']['MaxStream'][VarNum])+' ; '+str(ConfigParams['indices'][j])+'+=1 )'
				if(ConfigParams['StrideScaling'][VarNum]):
					ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1 )'					
				else:
					ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+ str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' * '+str(ConfigParams['GlobalVar']['Stream'][VarNum][StreamNum])+' ; '+str(ConfigParams['indices'][j])+'+=1 )'					
			
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
			#LHSindices+='['+str(InnerLoopVar)+']'
			LHSindices+='['+str(ConfigParams['indices'][j])+']'

    	TabSpace=''
    	for k in range(NumForLoops):
		TabSpace+='\t'
		
    	if(ConfigParams['RandomAccess'][VarNum]):
	    	#eqn="\t\t"+TabSpace+str(CurrVarName)+LHSindices+' = '+str(TempVar)+';' #+str(ConfigParams['init'][VarNum])+';'
	    	#eqn="\t\t"+TabSpace+str(CurrVarName)+LHSindices+' = '+PermuteArrayVar+'['+str(PermuteIndexVar)+']'+';'
	    	eqn="\t\t"+TabSpace+str(CurrVarName)+LHSindices+' = '+PermuteArrayVar+'['+str(PermuteIndexVar)+'] * ( '+str(ConfigParams['GlobalVar']['NumOperandsVar'][VarNum][StreamNum])+' * '+str(ConfigParams['GlobalVar']['SuccessiveOperandDiff'][VarNum])+');'
	    	FlushEqn="\t\t"+TabSpace+str(FlushVarName)+LHSindices+' = '+PermuteArrayVar+'['+str(PermuteIndexVar)+']'+';'
	    	FlushForLoop.append(FlushEqn)
    	else:
    		if(Indirection==1):
    			eqn="\t"+TabSpace+str(CurrVarName)+LHSindices+' = ( rand() % '+str(ConfigParams['size'][(ConfigParams['Dims']-1)])+' );'
    		else:
    			eqn="\t"+TabSpace+str(CurrVarName)+LHSindices+' = '+str(ConfigParams['init'][VarNum])+';'
    	
    	
	ThisLoop.append(eqn)
	#print "\n So, the equation should be: "+str(eqn)+" is it ?? "+str(ThisLoop[len(ThisLoop)-1])	
    	for k in range(NumForLoops):
    		TabSpace='' #\t'
    		for l in range(NumForLoops-k):
    			TabSpace+="\t"
	    	ThisLoop.append(TabSpace+'}')
	    	if(ConfigParams['RandomAccess'][VarNum]>0):
	    		FlushForLoop.append(TabSpace+'}')
	
	if(ConfigParams['FlushVarDeclared'][VarNum]==0):
		for CurrLine in FlushForLoop:
			#print "\n\t FlushForLoop: "+str(CurrLine)
			ThisLoop.append(CurrLine)
		 	#for CurrLine in ThisLoop: 
		 	#	print "\t CurrLine: "+str(CurrLine)
		 	ConfigParams['FlushVarDeclared'][VarNum]=1
	return ThisLoop

def StridedLoopInFunction(Stride,StrideDim,A,VarNum,ConfigParams,debug):
    if( (StrideDim > ConfigParams['Dims']) or (StrideDim < 0) ):
      print "\n\t ERROR: For variaable "+str(A)+" a loop with stride access: "+str(StrideDim)+" has been requested, which is illegal!"
      sys.exit(0)

    if debug:	
	    print "\n\t In StrideLoop: Variable: "+str(A)+" dimension: "+str(StrideDim)+" and requested stride is "+str(Stride)
	    

    VarFuncDeclString=''
    VarDeclString=''
    
    if(ConfigParams['Indirection'][VarNum]==0):
	for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
		StreamVarFound=0
		DiffVarFound=0
		for CurrOperand in range(ConfigParams['StrideVar'][VarNum][CurrStream]['NumOperands']):
			if debug:
				print "\n\t VarNum: "+str(VarNum)+" CurrStream "+str(CurrStream)+" CurrOperand "+str(CurrOperand)    
				print "\n\t ConfigParams['StrideVar'][VarNum][CurrStream]['OperandsInfo'][CurrOperand][0]: "+str(ConfigParams['StrideVar'][VarNum][CurrStream]['OperandsInfo'][CurrOperand][0])				
			if( (ConfigParams['StrideVar'][VarNum][CurrStream]['OperandsInfo'][CurrOperand][0]=='s') and (StreamVarFound==0) ):
				VarFuncDeclString+=ConfigParams['VarDecl'][VarNum][CurrStream][CurrOperand]+','
				VarDeclString+=ConfigParams['VarOperands'][VarNum][CurrStream][CurrOperand]+',' 
				StreamVarFound=1
			elif(ConfigParams['StrideVar'][VarNum][CurrStream]['OperandsInfo'][CurrOperand][0]=='d'):
				if(ConfigParams['DifferentOperand'][VarNum]>0):
					VarFuncDeclString+=ConfigParams['VarDecl'][VarNum][CurrStream][CurrOperand]+','
					VarDeclString+=ConfigParams['VarOperands'][VarNum][CurrStream][CurrOperand]+',' 
				elif(DiffVarFound==0):
					VarFuncDeclString+=ConfigParams['VarDecl'][VarNum][CurrStream][CurrOperand]+','
					VarDeclString+=ConfigParams['VarOperands'][VarNum][CurrStream][CurrOperand]+',' 
					DiffVarFound=1
    else:
		for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
			CurrOperand=0
			VarFuncDeclString+=ConfigParams['VarDecl'][VarNum][CurrStream][CurrOperand][0]+','
			VarDeclString+=ConfigParams['VarOperands'][VarNum][CurrStream][CurrOperand]+','
			VarFuncDeclString+=ConfigParams['VarDecl'][VarNum][CurrStream][CurrOperand][1]+','
			VarDeclString+=ConfigParams['IndirOperands'][VarNum][CurrStream]['b']+','
			VarFuncDeclString+=ConfigParams['VarDecl'][VarNum][CurrStream][CurrOperand][2]+','
			VarDeclString+=ConfigParams['IndirOperands'][VarNum][CurrStream]['c']+','
 
    if(ConfigParams['PapiInst'][VarNum]):
    	VarFuncDeclString+=' int* '+str(ConfigParams['PapiEventsArray'])+' , long long int* '+str( ConfigParams['PAPIValueVars'][VarNum])+','
    	VarDeclString+=str(ConfigParams['PapiEventsArray'])+' , '+ConfigParams['PAPIValueVars'][VarNum]+' , '
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
    ThisLoop.append('   int ii; ')
    if(ConfigParams['PapiInst'][VarNum]):
	ThisLoop.append(' char ConcatCounters[800]; ')	
	ThisLoop.append(' strcpy(ConcatCounters,"Hardware counters: "); ');
	ThisLoop.append('for(ii=0; ii< '+str(ConfigParams['NumPAPIHardwareCounters'])+'; ii++)')
	ThisLoop.append('{')
	ThisLoop.append('\t double tmp= ('+str(ConfigParams['PAPIValueVars'][VarNum])+'[ii]'+')/(1.0e9)/(time_buf[0]); char tmpStr[25]; ')
	#ThisLoop.append('printf("\\t %s %lf ",counters[ii],tmp);')
	ThisLoop.append('sprintf(tmpStr,"\\t %.6lf ",tmp);')
	ThisLoop.append('strcat(ConcatCounters,tmpStr) ;')
	ThisLoop.append('}')
	ThisLoop.append('sleep(2);')
	ThisLoop.append(' printf("\\n\t %s ",ConcatCounters);')
	ThisLoop.append('printf("\\n ");')
         	
    ThisLoop.append(' printf("app '+str(FuncNamePrint)+' "); ');
    ThisLoop.append('   for(ii=0; ii<MPI_Size; ii++) ')
    #AVS
    ThisLoop.append(' printf (" %f ",time_buf[ii]); ')
    #ThisLoop.append('      printf("\t time: %f\\n\t Starttime: %lf\\n\t Endtime: %lf  ", time_buf[ii],stime,etime); ')
    ThisLoop.append('      printf("\\n"); ')
    ThisLoop.append('} ')
#LAURA END ADD
    #LAURA ThisLoop.append('printf("\\n\\t Run-time for function- '+str(FuncName)+': %lf from rank: %d",currtime,rank);')
    #LAURA PrintResult='printf("\\n\\t Sum: %ld ",Sum);'
    #LAURA ThisLoop.append(PrintResult)
    PopCode+=14  #LAURA was PopCode+=8
    if(ConfigParams['PapiInst'][VarNum]):
	PopCode+=11
    
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

    LHSIndicesPerStream={}
    for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
                LHSIndicesPerStream[CurrStream]=[]

    for CurrDim in range(NumDims):
        if (CurrDim!=StrideDim):
                for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
                        LHSIndicesPerStream[CurrStream].append(ConfigParams['indices'][CurrDim])
			if debug:
				print "\n\t CurrStream: "+str(CurrStream)+" LHSIndicesPerStream[CurrStream]: "+str( LHSIndicesPerStream[CurrStream])
	else:
		 for i in range(ConfigParams['NumStreaminVar'][VarNum]):
    			if(ConfigParams['StrideinStream'][VarNum][i]==ConfigParams['maxstride'][VarNum]):
                        	LHSIndicesPerStream[i].append(ConfigParams['indices'][StrideDim])
                        else:
                        	index=str('StreamIndex'+str(i))
                       		LHSIndicesPerStream[i].append(index)				
			if debug:
				print "\n\t i: "+str(i)+" LHSIndicesPerStream[CurrStream]: "+str( LHSIndicesPerStream[i])	

    PermuteSizeVarforStream={}    		
    for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):	
	    #eqn="\t"+TabSpace+str(A)+LHSindices+' = '+'Sum'+' + '+str(A)+RHSindices+';'
	    LHSindices=''
	    RHSindices=''
	    indices=''
 
 	    LastDim=ConfigParams['Dims']-1
 	    PermuteSizeVar='PermuteSizeVar'+str(VarNum)+'_'+str(CurrStream)	    
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
	    	#print "\n\t --*-- CurrOperandIdx "+str(CurrOperandIdx)+" CurrOperandExprn "+str(CurrOperandExprn)
	    	if debug:
	    		print "\n\t CurrOperand: "+str(CurrOperandExprn)  	
## ***********
	    	if(CurrOperandExprn[0]=='='):
	    		#if debug:
	    		#RHSExprn='Const_Var'+str(VarNum)+'_Stream'+str(CurrStream)
	    		RHSExprn=ConfigParams['VarOperands'][VarNum][CurrStream][CurrOperandIdx]
	    		ExtractNumber=re.match('\s*\=(.*)',CurrOperandExprn)
	    		if debug:
	    			print "\n\t CurrOperandExprn: "+str(CurrOperandExprn)
	    		if ExtractNumber:
	    			#print "\n\t Datatype: "+str(ConfigParams['StrideVar'][VarNum][CurrStream]['OperandsInfo'][CurrOperandIdx][1])
	    			datatype=ConfigParams['StrideVar'][VarNum][CurrStream]['OperandsInfo'][CurrOperandIdx][1]
	    			DeclareVar=str(datatype)+' '+str(RHSExprn)+str(CurrOperandExprn)+';'
	    			"""NumberCheck=re.match('\s*(\d+)*\.(\d+)*',ExtractNumber.group(1))
	    			if NumberCheck:
	    				DeclareVar='double '+str(RHSExprn)+str(CurrOperandExprn)+';'
	    			else:
	    				IntCheck=re.match('\s*(\d+)*',ExtractNumber.group(1))
	    				if IntCheck:
	    					#DeclareVar='long int '+str(RHSExprn)+str(CurrOperandExprn)+';'
	    					DeclareVar=str(ConfigParams['datatype'])+' '+str(RHSExprn)+str(CurrOperandExprn)+';'
	    				else:
	    					print "\n\t ERROR: Const-var does not have number! Use debug to locate the error! \n"
	    					sys.exit()"""
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
		    					AppendIndexChange='+ ( '+str(ConfigParams['GlobalVar']['SuccessiveOperandDiff'][VarNum])+' * '+str(CurrOperandIdx)+')'
		    					#AppendIndexChange='+ ( '+str(PermuteSizeVarforStream[CurrStream])+' * '+str(CurrOperandIdx)+')'
		    					IndexChangeParameterized=ConfigParams['OpDiff'][VarNum] * CurrOperandIdx
		    					if( IndexChangeParameterized == IndexChangeBreakdown['Delta'] ):
			    					if debug:
										print "\n\t Yaay Parameterized delta "+str(IndexChangeParameterized)+" is equal to specified delta: "+str(IndexChangeBreakdown['Delta'])
			    					#sys.exit()
		    					else:
		    						print "\n\t WARNING: Parameterized delta "+str(IndexChangeParameterized)+" is not equal to specified delta: "+str(IndexChangeBreakdown['Delta'])
		    						if debug:
		    							print "\n\t VarNum: "+str(VarNum)+" CurrOperandIdx "+str(CurrOperandIdx)
		    						
		    				if debug:
		    					print "\n\t -- Sign: "+str(IndexChangeBreakdown['Sign'])+" Delta "+str(IndexChangeBreakdown['Delta'])
		    			else:
		    				print "\n\t ERROR: Unable to decode index change. Likely that the index change term was not of the form \"+-number\". Use debug to locate the source of error" 
		    				sys.exit()

    					OperandIndices=''
    					OperandIndicesExceptStrideDim=''
    					if( (ConfigParams['RandomAccess'][VarNum]>0) ):
		    				for i in range(NumDims-1):
			    				if(i==StreamDim):
			    					#PushIndexChange=str(ConfigParams['indices'][i])+str(AppendIndexChange)	
								PushIndexChange=str(LHSIndicesPerStream[CurrStream][i])+str(AppendIndexChange)
			    					OperandIndices+='['+str(PushIndexChange)+']'
			    					
			    				else:
			    					#OperandIndices+='['+str(ConfigParams['indices'][i])+']'
								OperandIndices+='['+str(LHSIndicesPerStream[CurrStream][i])+']'
								OperandIndicesExceptStrideDim=OperandIndices
			    			if(StreamDim==(NumDims-1)):
			    				PushIndexChange=str(RandomAccessVarPerStream[CurrStream])+str(AppendIndexChange)
			    				OperandIndices+='['+str(PushIndexChange)+']'
			    				
			    			else:
			    				PushIndexChange=str(RandomAccessVarPerStream[CurrStream])
							OperandIndices+='['+str(PushIndexChange)+']'
							OperandIndicesExceptStrideDim=OperandIndices
							
	    				else:
		    				for i in range(NumDims):
			    				if(i==StreamDim):
			    					#PushIndexChange=str(ConfigParams['indices'][i])+str(AppendIndexChange)	
								PushIndexChange=str(LHSIndicesPerStream[CurrStream][i])+str(AppendIndexChange)
			    					OperandIndices+='['+str(PushIndexChange)+']'
			    						
			    				else:
			    					#OperandIndices+='['+str(ConfigParams['indices'][i])+']'
								OperandIndices+='['+str(LHSIndicesPerStream[CurrStream][i])+']'
								OperandIndicesExceptStrideDim=OperandIndices
	    				#ThusOperand=str(StreamVar)+str(OperandIndices)
	    				if(ConfigParams['Indirection'][VarNum]==0):
	    					ThusOperand=str(ConfigParams['VarOperands'][VarNum][CurrStream][CurrOperandIdx])+str(OperandIndices)
	    				else:
	    					ThusOperand=str(ConfigParams['IndirOperands'][VarNum][CurrStream]['b'])+str(OperandIndicesExceptStrideDim)+'['+str(ConfigParams['IndirOperands'][VarNum][CurrStream]['c'])+str(OperandIndices)+']'
	    					#print "\n\t ThusOperand: "+str(ThusOperand)
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

    IdxForBound='IdxForBound'
    IdxForBoundDecl='long int '+str(IdxForBound)+'=0;'
    if(ConfigParams['StrideScaling'][VarNum]):
	ShouldDeclareVars.append(IdxForBoundDecl)

    LHSIndicesPerStream={}
    for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
		LHSIndicesPerStream[CurrStream]=[]

    NestedLoop={}
    NestedLoop['Incr']={}
    NestedLoop['Init']={}
    MaxNumNestedLoops=-1
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
		#MaxNumNestedLoops=-1
		for StreamNum in (ConfigParams['StrideVar'][VarNum]):
			CurrNestedLoopNum=ConfigParams['StrideVar'][VarNum][StreamNum]['NestedLoop']
			if(MaxNumNestedLoops<CurrNestedLoopNum):
				MaxNumNestedLoops=CurrNestedLoopNum
			#print "\t VarNum: "+str(VarNum)+" StreamNum: "+str(StreamNum)+" CurrNestedLoopNum: "+str(CurrNestedLoopNum)+" MaxNumNestedLoops: "+str(MaxNumNestedLoops)
		#sys.exit()
			
		for i in range(ConfigParams['NumStreaminVar'][VarNum]):
			CurrAccumVar=str('Accum')+str(i)
			AccumVar.append(CurrAccumVar)
		 	CurrAccumVarDecl+='long int '+str(CurrAccumVar)+'='+str(i+1)+';'
		 	StreamNestedLoopNum=ConfigParams['StrideVar'][VarNum][i]['NestedLoop']
			if(LargestIndexNotFound and (ConfigParams['StrideinStream'][VarNum][i]==ConfigParams['maxstride'][VarNum]) ):
				LargestIndexNotFound=0

				if(ConfigParams['RandomAccess'][VarNum]>0):
				#bounds= '(' + str(ConfigParams['GlobalVar']['DimsSize'][StrideDim])+' - ('  + str(ConfigParams['GlobalVar']['Stream'][VarNum][i])+' + '+str(FinalStreamIndexChange[StrideDim]['Final'])+') )'  
					if( (FinalStreamIndexChange[StrideDim]['Final']) != ( ( ConfigParams['StrideVar'][VarNum][i]['NumOperands'] -1) * ( ConfigParams['OpDiff'][VarNum] ) ) ):
						print "\n\t WARNING: FinalStreamIndexChange[StrideDim]['Final'] "+str(FinalStreamIndexChange[StrideDim]['Final'])+" is not equal to ( ConfigParams['StrideVar'][VarNum][i]['NumOperands'] * ( ConfigParams['OpDiff'][VarNum]-1 ) "+str(ConfigParams['StrideVar'][VarNum][i]['NumOperands'])+' * '+str( ConfigParams['OpDiff'][VarNum]-1)+" --"
					#if(ConfigParams['StrideScaling'][VarNum]):
					#	bounds= '( ' + str(ConfigParams['GlobalVar']['DimsSize'][StrideDim])+' - ( '+str(ConfigParams['GlobalVar']['NumOperandsVar'][VarNum][i] )+' * '+str(ConfigParams['GlobalVar']['SuccessiveOperandDiff'][VarNum])+') )'
					#else:
					bounds= '( ( ' + str(ConfigParams['GlobalVar']['DimsSize'][StrideDim])+' * '+str(ConfigParams['GlobalVar']['NumItersLastDimVar'][VarNum])+' ) '+' - ( '+str(ConfigParams['GlobalVar']['NumOperandsVar'][VarNum][i] )+' * '+str(ConfigParams['GlobalVar']['SuccessiveOperandDiff'][VarNum])+') )' 		
					BoundForDim.append(str(bounds))

				else:
					if(ConfigParams['StrideScaling'][VarNum]):
						bounds= '( ' + str(ConfigParams['GlobalVar']['DimsSize'][StrideDim])+' - ('  + str(ConfigParams['GlobalVar']['Stream'][VarNum][i])+' + '+str(FinalStreamIndexChange[StrideDim]['Final'])+') )'
					else:
						bounds= '((' + str(ConfigParams['GlobalVar']['DimsSize'][StrideDim])+' * '+str(ConfigParams['StrideinStream'][VarNum][i] )+' )- ('  + str(ConfigParams['GlobalVar']['Stream'][VarNum][i])+' + '+str(FinalStreamIndexChange[StrideDim]['Final'])+') )'  	
					BoundForDim.append(str(bounds))#BoundForDim.insert(0,str(bounds))
				#if( (ConfigParams['StrideScaling'][VarNum] ) and (ConfigParams['StrideinStream'][VarNum][i] > 1) ):	
				CurrIndexIncr=str(ConfigParams['indices'][StrideDim])+'+= '+str(ConfigParams['GlobalVar']['Stream'][VarNum][i])+' , '+str(str(ConfigParams['indices'][StrideDim]))+' &= '+str(ConfigParams['GlobalVar']['LastDimOverflowVar'][VarNum][i])
				#else:
				#	CurrIndexIncr=str(ConfigParams['indices'][StrideDim])+'+= '+str(ConfigParams['GlobalVar']['Stream'][VarNum][i])
				#IndexIncr=str(CurrIndexIncr)+','+str(IndexIncr)    	
				IndexIncr=str(CurrIndexIncr)+str(IndexIncr)    
				
				if(not StreamNestedLoopNum in NestedLoop['Incr']):
					NestedLoop['Incr'][StreamNestedLoopNum]=''
					NestedLoop['Init'][StreamNestedLoopNum]=''
					
				#VarIndexIncr[StreamNestedLoopNum]=str(CurrIndexIncr)+str(VarIndexIncr[StreamNestedLoopNum])
				NestedLoop['Incr'][StreamNestedLoopNum]=str(CurrIndexIncr)+str(NestedLoop['Incr'][StreamNestedLoopNum])
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
				#if( (ConfigParams['StrideScaling'][VarNum]) and (ConfigParams['StrideinStream'][VarNum][i] > 1) ):
				CurrIndexIncr=str(index)+'+= '+str(ConfigParams['GlobalVar']['Stream'][VarNum][i])+','+str(index)+' &= '+str(ConfigParams['GlobalVar']['LastDimOverflowVar'][VarNum][i])
				#else:
				#CurrIndexIncr=str(index)+'+= '+str(ConfigParams['GlobalVar']['Stream'][VarNum][i])
				IndexIncr+=','+str(CurrIndexIncr)
				if(not StreamNestedLoopNum in NestedLoop['Incr']):
					NestedLoop['Incr'][StreamNestedLoopNum]=''
					NestedLoop['Init'][StreamNestedLoopNum]=''
					NestedLoop['Incr'][StreamNestedLoopNum]+=str(CurrIndexIncr)
				else:
					NestedLoop['Incr'][StreamNestedLoopNum]+=','+str(CurrIndexIncr)
				NestedLoop['Init'][StreamNestedLoopNum]+=','+str(index)+'='+str(FinalStreamIndexChange[CurrDim]['Init'])
				#VarIndexIncr[StreamNestedLoopNum]+=str(CurrIndexIncr)	
				
				IndexDecl+='long int '+str(index)+'='+str(FinalStreamIndexChange[StrideDim]['Init'])+';'
				IndexInit+=','+str(index)+'='+str(FinalStreamIndexChange[CurrDim]['Init'])
				
				if debug:
					print "\n\t The minnions are here!! Bound: "+str(bounds)+' IndexIncr: '+str(CurrIndexIncr)+" IndexInit "+str(IndexInit)
				StrideIndex.append(str(index))
				LHSIndicesPerStream[i].append(index)
		InitForStrideDim='='+str(FinalStreamIndexChange[StrideDim]['Init'])+str(IndexInit)
		if(ConfigParams['StrideScaling'][VarNum]):
			InitForStrideDim+=','+str(IdxForBound)+'='+str(FinalStreamIndexChange[CurrDim]['Init'])
		for CurrNestedLoop in NestedLoop['Incr']:
			NestedLoop['Init'][CurrNestedLoop]='='+str(FinalStreamIndexChange[StrideDim]['Init'])+str(NestedLoop['Init'][CurrNestedLoop])
			if(ConfigParams['StrideScaling'][VarNum]):
				NestedLoop['Init'][CurrNestedLoop]+=','+str(IdxForBound)+'='+str(FinalStreamIndexChange[CurrDim]['Init'])
			
		InitForDim.append(InitForStrideDim)	    

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
   
    if(ConfigParams['PapiInst'][VarNum]):
	PAPIStartStmt='PAPI_start_counters( '+str(ConfigParams['PapiEventsArray'])+' , '+str(ConfigParams['NumPAPIHardwareCounters'])+' );'	
	ThisLoop.append('\t '+str(PAPIStartStmt))
 
    TabSpace='\t'
    # ConfigParams['GlobalVar']['NumItersDecl']
    ThisForLoop=TabSpace+'for('+str(LoopIter)+'=0; '+str(LoopIter)+' < '+str(ConfigParams['GlobalVar']['NumIters'][VarNum])+' ; '+str(LoopIter)+'+=1)'
    ThisLoop.append(ThisForLoop)
    ThisLoop.append(TabSpace+'{')
    
    NestedLoopCode={}
    for j in range(NumDims):
		if(j==StrideDim): 		    	
		    	for CurrNestedLoopNum in range(MaxNumNestedLoops+1):
				if(ConfigParams['StrideScaling'][VarNum]):
					ThisForLoop='for('+str(ConfigParams['indices'][j])+str(NestedLoop['Init'][CurrNestedLoopNum])+';'+str(IdxForBound)+'<='+str(BoundForDim[j])+';'+str(NestedLoop['Incr'][CurrNestedLoopNum])+','+str(IdxForBound)+'+=1)'
				else:
					ThisForLoop='for('+str(ConfigParams['indices'][j])+str(NestedLoop['Init'][CurrNestedLoopNum])+';'+str(ConfigParams['indices'][j])+'<='+str(BoundForDim[j])+';'+str(NestedLoop['Incr'][CurrNestedLoopNum])+')'
				TabSpace='\t\t'
				for k in range(j):
					TabSpace+='\t'
				ThisForLoop=TabSpace+ThisForLoop
				NestedLoopCode[CurrNestedLoopNum]=[]
				NestedLoopCode[CurrNestedLoopNum].append(ThisForLoop)
				NestedLoopCode[CurrNestedLoopNum].append(TabSpace+'{')
		elif(j!=StrideDim):
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
	StreamVar=ConfigParams['StreamWideOperand'][VarNum][CurrStream] #'Var'+str(VarNum)+'_Stream'+str(CurrStream)
	LHSVariableCurrStream=str(StreamVar)
	if(ConfigParams['RandomAccess'][VarNum]>0):
		LHSVariableCurrStream=(RandomAccessVarPerStream[CurrStream])
	else:
		for CurrDim in range(NumDims):
			LHSVariableCurrStream+='['+str(LHSIndicesPerStream[CurrStream][CurrDim])+']'
			
 	if(ConfigParams['RandomAccess'][VarNum]):	
		#Method3:
		#StreamExprn=LHSVariableCurrStream+' = ( '+ str(LHSVariableCurrStream)+'* ( '+str(ConfigParams['GlobalVar']['NumOperandsVar'][VarNum][CurrStream])+' * '+str(ConfigParams['GlobalVar']['SuccessiveOperandDiff'][VarNum])+') ) ;'
		StreamExprn=''
		StreamExprn+='\n\t '+LHSVariableCurrStream+'= ('+'(int) ('+str(RHSExprnPerStream[CurrStream])+') ) ; '			
	else:
		StreamExprn=LHSVariableCurrStream+'='+'('+str(RHSExprnPerStream[CurrStream])+') ;'
	
	if debug:
		print "\n\t StreamExprn: "+str(StreamExprn)
	NestedLoopNum=ConfigParams['StrideVar'][VarNum][CurrStream]['NestedLoop']
	#if(not(NestedLoopNum in NestedLoopCode)):
	NestedLoopCode[NestedLoopNum].append(StreamExprn)	
	#ThisLoop.append(StreamExprn)

    for CurrNestedLoopNum in range(MaxNumNestedLoops+1):		
    	for CurrLine in (NestedLoopCode[CurrNestedLoopNum]):
    		ThisLoop.append(CurrLine)
	TabSpace='\t\t'
	for k in range(StrideDim):
		TabSpace+='\t'
	ThisLoop.append(TabSpace+'}')
    	
    	
    #for k in range(NumDims+1): # NumDims+1 since we are looping over the loops! 
    for k in range(NumDims):
    	TabSpace='' #\t'
    	for l in range(NumDims-k):
    		TabSpace+="\t"
    	ThisLoop.append(TabSpace+'}')
    
    if(ConfigParams['PapiInst'][VarNum]):
    	StopCountersCall='PAPI_stop_counters( '+str(ConfigParams['PAPIValueVars'][VarNum])+' , '+str(ConfigParams['NumPAPIHardwareCounters'])+' );'
	ThisLoop.append('\t '+str(StopCountersCall))
    		
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
			StreamVar=ConfigParams['StreamWideOperand'][VarNum][CurrStream] #'Var'+str(VarNum)+'_Stream'+str(CurrStream)
			for CurrDim in range(NumDims):
				StreamVar+='[('+str(LHSIndicesPerStream[CurrStream][CurrDim])+'-1)]'
			PrintStmt+=' '+str(StreamVar)+' :%'+str(ConfigParams['DSforPrintf'][VarNum])+' '
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
		File.write("\n\t "+str(Array[i]))
		
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
	ConfigParams['datatype']=[]
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
	ConfigParams['StrideScaling']=[]
	ConfigParams['PapiInst']=[]
	ConfigParams['DifferentOperand']=[]
	ConfigParams['Indirection']=[]
		
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
	StrideScalingNotFound=1
	PAPIInstNotFound=1
	DifferentOperandNotFound=1
	IndirectionNotFound=1
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
								
								NestedLoopIdx=2
								OverflowSizeIdx=3
								OperandsIdx=4
								OperationsIdx=5
								OperandsIndicesIdx=6
								
								ConfigParams['StrideVar'][CurrVar][CurrStream]['NestedLoop']=int(RemoveWhiteSpace(ExprnBreakdown[NestedLoopIdx]))
								ConfigParams['StrideVar'][CurrVar][CurrStream]['OverflowSize']=int(RemoveWhiteSpace(ExprnBreakdown[OverflowSizeIdx]))
								
								ConfigParams['StrideVar'][CurrVar][CurrStream]['OperandsInfo']=[]
								TmpExprnOperands=re.split('\),',ExprnBreakdown[OperandsIdx])
								ExprnOperands=[]
								#print "\t TmpExprnOperands: "+str(TmpExprnOperands)+' ExprnBreakdown[OperandsIdx] '+str(ExprnBreakdown[OperandsIdx])
								for CurrOperand in TmpExprnOperands:
									Tmp=RemoveBraces(CurrOperand)
									Tmp1=re.split(',',Tmp)
									if(len(Tmp1)!=2):
										print "\n\t ERROR: One of the operands mentioned in stream is not in expected format! Expected 2 terms and have got "+str(len(Tmp1))+" terms "
										sys.exit()
									else:
										Tmp2Tuple=()
										for idx,i in enumerate(Tmp1):
											if(idx):
												i=RemoveWhiteSpace(i)
												CheckDSType=re.match('[idlf]',i)
												if CheckDSType:
													if(i=='i'):
														Tmp2Tuple+=('int',)
													elif(i=='d'):
														Tmp2Tuple+=('double',)
													elif(i=='f'):
														Tmp2Tuple+=('float',)
													elif(i=='l'):
														Tmp2Tuple+=('long int',)
												else:
													print "\n\t ERROR: Illegal DStype provided for one of the operands in a stream. Use debug option to find source of the problem! " 
													sys.exit()
											else:
												i=RemoveWhiteSpace(i)
												CheckOperandType=re.match('[csd]',i)
												if CheckOperandType:
													Tmp2Tuple+=(i,)
												else:
													print "\n\t ERROR: Illegal operand-type provided for one of the operands in a stream. Use debug option to find source of the problem! " 
													sys.exit()

														
									ExprnOperands.append(Tmp2Tuple)
									
								ConfigParams['StrideVar'][CurrVar][CurrStream]['OperandsInfo']=ExprnOperands
								for CurrOperand in ConfigParams['StrideVar'][CurrVar][CurrStream]['OperandsInfo']:	
									if debug:
										print"\n\t CurrOperand: "+str(CurrOperand[0])+" "+str(CurrOperand[1])
								#sys.exit()
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
											CheckOperation=re.match('\s*[\+\-\*\/\|]',CurrOperation)
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
								OperandsSet=RemoveBraces(ExprnBreakdown[OperandsIndicesIdx])
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
							#CheckSpace=re.match(r'^\s*$',CurrDS)
							CurrDS=RemoveWhiteSpace(CurrDS)
						        if(CurrDS==''):
						       		if debug:
						       			print "\n\t For datastructure parameter, the input is not in the appropriate format. Please check! \n"
						       		sys.exit(0)						
							else:
								ConfigParams['datastructure'].append(CurrDS);
								datatype=''
								datatype=ObtainDS(CurrDS)
								ConfigParams['datatype'].append(datatype)
								
								CurrDim+=1				
								if debug:
						       			print "\n\t DS for dim "+str(CurrDim)+" is "+str(CurrDS)+"\n" 					
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
							print "\n\t The opdiff expression is not specified for each variable. It is specified only for "+str(VarCount)+ " number of variables while number of dimensions specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit(0)
						else:
							OpDiffNotFound=0	
			if StrideScalingNotFound:
				MatchObj=re.match('\s*\#stridescaling',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					StrideScaling=re.split(',',tmp[1])
					if StrideScaling:
						LineNotProcessed=0
						VarCount=0
						for CurrStrideScaling in StrideScaling:
							tmp=RemoveWhiteSpace(CurrStrideScaling)
							if IsInt(tmp):
								ConfigParams['StrideScaling'].append(int(tmp))
								VarCount+=1
							else:
								print "\n\t ERROR: Stride scaling parameter is provided in following form: "+str(tmp)+" which is illegal! "
								sys.exit()
						if(VarCount!=ConfigParams['NumVars']):
							print "\n\t The stride scaling expression is not specified for each variable. It is specified only for "+str(VarCount)+" number of variables while number of variables specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit()
						else:
							StrideScalingNotFound=0

			if PAPIInstNotFound:
				MatchObj=re.match('\s*\#papiinst',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					PapiInst=re.split(',',tmp[1])
					if PapiInst:
						LineNotProcessed=0
						VarCount=0
						for CurrPapiInstFlag in PapiInst:
							tmp=RemoveWhiteSpace(CurrPapiInstFlag)
							if IsInt(tmp):
								ConfigParams['PapiInst'].append(int(tmp))
								VarCount+=1
							else:
								print "\n\t ERROR: Papi inst parameter is provided in following form: "+str(tmp)+" which is illegal! "
								sys.exit()
						if(VarCount!=ConfigParams['NumVars']):
							print "\n\t The papi inst expression is not specified for each variable. It is specified only for "+str(VarCount)+" number of variables while number of variables specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit()
						else:
							PAPIInstNotFound=0
			if DifferentOperandNotFound:
				MatchObj=re.match('\s*\#DifferentOperand',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					DifferentOperand=re.split(',',tmp[1])
					if DifferentOperand:
						LineNotProcessed=0
						VarCount=0
						for CurrDifferentOperand in DifferentOperand:
							tmp=RemoveWhiteSpace(CurrDifferentOperand)
							if IsInt(tmp):
								ConfigParams['DifferentOperand'].append(int(tmp))
								VarCount+=1
							else:
								print "\n\t ERROR: Papi inst parameter is provided in following form: "+str(tmp)+" which is illegal! "
								sys.exit()
						if(VarCount!=ConfigParams['NumVars']):
							print "\n\t The DifferentOperand expression is not specified for each variable. It is specified only for "+str(VarCount)+" number of variables while number of variables specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit()
						else:
							DifferentOperandNotFound=0
							
			if IndirectionNotFound:
				MatchObj=re.match('\s*\#Indirection',CurrLine)
				if MatchObj:
					tmp=re.split(' ',CurrLine)
					Indirection=re.split(',',tmp[1])
					if Indirection:
						LineNotProcessed=0
						VarCount=0
						for CurrIndirection in Indirection:
							tmp=RemoveWhiteSpace(CurrIndirection)
							if IsInt(tmp):
								ConfigParams['Indirection'].append(int(tmp))
								VarCount+=1
							else:
								print "\n\t ERROR: Papi inst parameter is provided in following form: "+str(tmp)+" which is illegal! "
								sys.exit()
						if(VarCount!=ConfigParams['NumVars']):
							print "\n\t The Indirection expression is not specified for each variable. It is specified only for "+str(VarCount)+" number of variables while number of variables specified is "+str(ConfigParams['NumVars'])+"\n";
							sys.exit()
						else:
							IndirectionNotFound=0
							

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
	

	#ConfigParams['PAPIInstNeeded']=-1
	PAPIInstNeeded=-1
	NumPAPIHardwareCounters=6 # Currently designing it assuming we would use 6 energy related counters "
	ConfigParams['NumPAPIHardwareCounters']='NUM_HWC' 
	HWCountersStmt='#define '+str(ConfigParams['NumPAPIHardwareCounters'])+' '+str(NumPAPIHardwareCounters)
	
	if debug:
		print "\n\t RandomAccessNotFound: "+str(RandomAccessNotFound)
	if( (NumVarNotFound==0) and (DimNotFound==0) and (SizeNotFound==0) and (StrideNotFound==0) and (AllocNotFound==0) and (DSNotFound==0) and (InitNotFound==0) and (NumStreamsDimsNotFound==0) and (LoopIterationsNotFound==0) and (RandomAccessNotFound==0) and (OpDiffNotFound==0) and (StrideScalingNotFound==0) and ( PAPIInstNotFound==0) and (DifferentOperandNotFound==0) and (IndirectionNotFound==0) ):
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
		tmp='#include <string.h>'
		LibAlloc.append(tmp)	
		for VarNum,CurrVarPapiInst in enumerate(ConfigParams['PapiInst']):	
			if (CurrVarPapiInst>0):
				PAPIInstNeeded=1
			if debug:
				print "\n\t Var: "+str(VarNum)+" PAPIInstNeeded "+str(PAPIInstNeeded)+" CurrVarPapiInst: "+str(CurrVarPapiInst)
		
		if(PAPIInstNeeded>0):
			tmp='#include <papi.h> '
			LibAlloc.append(tmp)
			tmp='#define NUM_HWC '+str(NumPAPIHardwareCounters)
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


		ConfigParams['FlushVarDeclared']=[]
		for i in range(ConfigParams['NumVars']):
			ConfigParams['FlushVarDeclared'].append(0)
			
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
			CurrVarNumLoopLastDimVarDecl='long int '+str(CurrVarNumLoopLastDimVar)+' = ( '+str(ConfigParams['NumIters'][i])+' * 100 ) ;'
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
		ConfigParams['GlobalVar']['LastDimOverflowVar']={}
		ConfigParams['GlobalVar']['DimsSizeDecl']=[]
		ConfigParams['GlobalVar']['LastDimOverflowVarDecl']=[]
		
		SizeDataType='long int '
		SizeDataTypeBits=64
		
		for index in range(ConfigParams['Dims']):
			SizeVar='Size_Dim'+str(index)
			SizeVarDecl=str(SizeDataType)+str(SizeVar)+' = '+str(ConfigParams['size'][index])+' ;'
			if debug:
				print "\n\t Dim: "+str(index)+" Var: "+str(SizeVar)+" declaration "+str(SizeVarDecl)
			ConfigParams['GlobalVar']['DimsSize'].append(SizeVar)
			ConfigParams['GlobalVar']['DimsSizeDecl'].append(SizeVarDecl)
		
		LastDimSize=ConfigParams['size'][ConfigParams['Dims']-1]
		NumberofBits=-1
		OverflowDetectValue=-1
		for CurrPos in range(SizeDataTypeBits):
			CheckSize=2**CurrPos
			if(CheckSize==int(LastDimSize)):
				NumberofBits=CurrPos+1
				OverflowDetectValue=CheckSize-1
				break
			elif(CheckSize>int(LastDimSize)):
				break

		if (NumberofBits==-1):
			print "\n\t WARNING: Last dimension size should be power of 2, while it is: "+str(LastDimSize)
			OverflowDetectValue=int(LastDimSize)-1
			#sys.exit()
			
			
		if debug:
			print "\n\t LastDim-size: "+str(LastDimSize)+" NumberofBits "+str(NumberofBits)+" OverflowDetectValue: "+str(OverflowDetectValue)
		
		for CurrVar in range(ConfigParams['NumVars']):
			ConfigParams['GlobalVar']['LastDimOverflowVar'][CurrVar]=[]
			for CurrStreamNum in range(ConfigParams['NumStreaminVar'][CurrVar]):
				OverflowDetectMask='Overflow_Var'+str(CurrVar)+'_Stream'+str(CurrStreamNum)
				#OverflowDetectMaskDecl=str(SizeDataType)+' Overflow_Var'+str(CurrVar)+str(CurrStreamNum)' = '+str(OverflowDetectValue)+' ;'
				OverflowDetectMaskDecl=str(SizeDataType)+' Overflow_Var'+str(CurrVar)+'_Stream'+str(CurrStreamNum)+' = '+str(ConfigParams['StrideVar'][CurrVar][CurrStream]['OverflowSize'])+';'
				if debug:
					print "\n\t Var: "+str(CurrVar)+" overflow declaration: "+str(OverflowDetectMaskDecl)
				ConfigParams['GlobalVar']['LastDimOverflowVar'][CurrVar].append(OverflowDetectMask)
				ConfigParams['GlobalVar']['LastDimOverflowVarDecl'].append(OverflowDetectMaskDecl)
			
		ConfigParams['GlobalVar']['SuccessiveOperandDiff']=[]
		ConfigParams['GlobalVar']['SuccessiveOperandDiffDecl']=[]
		for index in range(ConfigParams['NumVars']):
			OpDiffVar='OpDiffVar'+str(index)
			OpDiffVarDecl='int '+str(OpDiffVar)+' = '+str(ConfigParams['OpDiff'][index])+' ;'
			if debug:
				print "\n\t Var: "+str(index)+" OpDiffVar "+str(OpDiffVar)+" Decl: "+str(OpDiffVarDecl)
			ConfigParams['GlobalVar']['SuccessiveOperandDiff'].append(OpDiffVar)
			ConfigParams['GlobalVar']['SuccessiveOperandDiffDecl'].append(OpDiffVarDecl)
		
###
		
		ConfigParams['DSforPrintf']=[]		
		ConfigParams['VarOperands']={}	
		ConfigParams['StreamWideOperand']={}
		ConfigParams['StreamWideDiffOperand']={}
		ConfigParams['IndirOperands']={}
		ConfigParams['VarDecl']={}
		ConfigParams['VarDeclCollection']=[]
		ConfigParams['InitVar']={}

		for index in range(ConfigParams['NumVars']):
			if( (ConfigParams['Indirection'][index]==1) and (ConfigParams['RandomAccess'][index]==1) ):
				print "\n\t ERROR: Variable "+str(index)+" has conflicting requests, both indirection and random access is requested. "
				sys.exit
			else:	
				if(not(index in ConfigParams['StreamWideOperand'])):
					ConfigParams['StreamWideOperand'][index]={}
				ConfigParams['VarOperands'][index]={}
				ConfigParams['VarDecl'][index]={}
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
					 prefix=''
					 suffix=''
					 for CurrDim in range(ConfigParams['Dims']):
					   prefix+='*'
					 for CurrDim in range(ConfigParams['Dims']-1):
					   suffix+='*'				   
					 if(ConfigParams['RandomAccess'][index] >0 ):
						FlushVar=' FlushVar'+str(index)+'_Stream'+str(CurrStream)
						FlushVarDecl=datatype+prefix+FlushVar+';'
						DynAlloc.append(FlushVarDecl)
						if debug:
							print "\n\t FlushVarDecl: "+str(FlushVarDecl)
						if(ConfigParams['Dims']==1):
							FlushTmp=FlushVar+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'
							DynAlloc.append(FlushTmp)	
						else:
							FlushTmp=FlushVar+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+' * sizeof('+datatype+suffix+'))'+';'
							DynAlloc.append(FlushTmp)

								#if(ConfigParams['Dims']>1):
							NumForLoops=''
							for i in range(ConfigParams['Dims']-1):
								NumForLoops=i+1
								MallocLHS=''
								for j in range(NumForLoops):
									ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
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
								if(i==(ConfigParams['Dims']-2)): # Since the loop is going from 0 to ConfigParams['Dims']-2
									if (ConfigParams['StrideScaling'][index]):
										FlushMallocEqn=FlushVar+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * '+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'
									else:
										FlushMallocEqn=FlushVar+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * '+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'
								else:
									FlushMallocEqn=FlushVar+MallocLHS+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * sizeof('+datatype+suffix+'))'+';'		
								DynAlloc.append(FlushMallocEqn)
								for j in range(NumForLoops):
									DynAlloc.append('}')						
				
					for CurrStream in range(ConfigParams['NumStreaminVar'][index]):
 						SameOperandDeclared=0
 						DifferentOperandDeclared=0
						if( not( CurrStream in (ConfigParams['VarOperands'][index]) ) ):
							ConfigParams['VarOperands'][index][CurrStream]={}
						if debug:
							print "\n\t CurrVar "+str(index)+" Stream: "+str(CurrStream)+" Dim "+str(i)+" #Ops "+str(ConfigParams['StrideVar'][index][CurrStream]['NumOperands'])
 						
						if (not CurrStream in ConfigParams['VarDecl'][index]):
							ConfigParams['VarDecl'][index][CurrStream]={}
						for CurrOperand in range(ConfigParams['StrideVar'][index][CurrStream]['NumOperands']):
							prefix=''
							suffix=''
							for CurrDim in range(ConfigParams['Dims']):
							   prefix+='*'
							for CurrDim in range(ConfigParams['Dims']-1):
							   suffix+='*'		
						
							Declare=0
							if debug:
								print "\n\t CurrOperand: "+str(CurrOperand)+" requested "+str(ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand])
#####						
							if(ConfigParams['Indirection'][index]):
								var='Var'+str(index)+'_Stream'+str(CurrStream)+'_Operand'+str(CurrOperand)	
								ConfigParams['VarOperands'][index][CurrStream][CurrOperand]=var	
								ConfigParams['StreamWideOperand'][index][CurrStream]=var
								if(not(index in ConfigParams['IndirOperands'])): 
									ConfigParams['IndirOperands'][index]={}
								ConfigParams['IndirOperands'][index][CurrStream]={}	
								ConfigParams['IndirOperands'][index][CurrStream]['b']='Var'+str(index)+'_Stream'+str(CurrStream)+'_Operand'+str(CurrOperand)+'B'	
								ConfigParams['IndirOperands'][index][CurrStream]['c']='Var'+str(index)+'_Stream'+str(CurrStream)+'_Operand'+str(CurrOperand)+'C'	
								#Declare=1
								CurrOperand=0
								DeclareVars=[]
								DeclareVars.append((ConfigParams['VarOperands'][index][CurrStream][CurrOperand],datatype))
								DeclareVars.append((ConfigParams['IndirOperands'][index][CurrStream]['b'],ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]))
								DeclareVars.append((ConfigParams['IndirOperands'][index][CurrStream]['c'],'int'))
								
								VarDeclareReproduce=[]
								for DeclareVarIdx,CurrDeclareVar in enumerate(DeclareVars):
									prefix=''
									suffix=''
									for CurrDim in range(ConfigParams['Dims']):
									   prefix+='*'
									for CurrDim in range(ConfigParams['Dims']-1):
									   suffix+='*'		
									#print "\t Idx: "+str(DeclareVarIdx)+" CurrDeclareVar "+str(CurrDeclareVar)
									#ConfigParams['VarOperands'][index][CurrStream][CurrOperand]=var
									Var=CurrDeclareVar[1] #ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]
									VarDeclPrefix=CurrDeclareVar[1]+' '+prefix
									VarDecl=VarDeclPrefix+' '+str(CurrDeclareVar[0])
									VarDeclStmt.append(VarDecl)
									#if(DeclareVarIdx==0):
									VarDecl
									VarDeclareReproduce.append(VarDecl)
									VarDecl+=';'
									if debug:
										print "\n\t Var: "+str(index)+" CurrStream "+str(CurrStream)+" CurrOperand "+str(CurrOperand)
							
										print "\n\t var: "+str(var)+" ConfigParams['VarOperands'][index][CurrStream][CurrOperand]: "+str(ConfigParams['VarOperands'][index][CurrStream][CurrOperand])							

									if debug:
										print "\n\t This is the prefix: "+str(prefix)+" and this is the suffix: "+str(suffix)+" and this'd be the variable declaration: "+str(VarDecl)+ "\n "
									DynAlloc.append(VarDecl)
								
									if(ConfigParams['Dims']==1):
										if (ConfigParams['StrideScaling'][index]):
											tmp=CurrDeclareVar[0]+'= ('+VarDeclPrefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+' * sizeof('+CurrDeclareVar[1]+suffix+'))'+';'
										else:
											tmp=CurrDeclareVar[0]+'= ('+VarDeclPrefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['Stream'][index][CurrStream])+' * sizeof('+CurrDeclareVar[1]+suffix+'))'+';'	
											#tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'	
										DynAlloc.append(tmp);
									else:
										tmp=CurrDeclareVar[0]+'= ('+VarDeclPrefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+' * sizeof('+CurrDeclareVar[1]+suffix+'))'+';'
									
										DynAlloc.append(tmp);
										NumForLoops=''
										for i in range(ConfigParams['Dims']-1):
											NumForLoops=i+1
											MallocLHS=''
											for j in range(NumForLoops):
												ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
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

											if(i==(ConfigParams['Dims']-2)): # Since the loop is going from 0 to ConfigParams['Dims']-2
												if (ConfigParams['StrideScaling'][index]):
													MallocEqn=CurrDeclareVar[0]+MallocLHS+'= ('+Var+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * sizeof('+CurrDeclareVar[1]+suffix+'))'+';'										
												else:
													MallocEqn=CurrDeclareVar[0]+MallocLHS+'= ('+Var+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * '+str(ConfigParams['GlobalVar']['Stream'][index][CurrStream])+' * sizeof('+CurrDeclareVar[1]+suffix+'))'+';'
											else:
												MallocEqn=CurrDeclareVar[0]+MallocLHS+'= ('+Var+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * sizeof('+CurrDeclareVar[1]+suffix+'))'+';'		
										   	if debug:
													print "\t The malloc equation is: "+str(MallocEqn)+"\n"
											DynAlloc.append(MallocEqn)
											for j in range(NumForLoops):
												DynAlloc.append('}')
								ConfigParams['VarDecl'][index][CurrStream][CurrOperand]=VarDeclareReproduce
#####								
							elif(not(ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][0]=='c')):
								if(ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][0]=='d'):
									if(ConfigParams['DifferentOperand'][index]==0):
										if(DifferentOperandDeclared==0):
											var=' Var'+str(index)+'_Stream'+str(CurrStream)+'_Operand'+str(CurrOperand)
											Declare=1
											ConfigParams['StreamWideDiffOperand'][index]=var
											ConfigParams['VarOperands'][index][CurrStream][CurrOperand]=var
											DifferentOperandDeclared=1
										else:
											ConfigParams['VarOperands'][index][CurrStream][CurrOperand]=ConfigParams['StreamWideDiffOperand'][index]
									else:
										var=' Var'+str(index)+'_Stream'+str(CurrStream)+'_Operand'+str(CurrOperand)	
										Declare=1
								elif(ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][0]=='s'):
									if(SameOperandDeclared==0):
										var=' Var'+str(index)+'_Stream'+str(CurrStream)+'_Operand'+str(CurrOperand)
										SameOperandDeclared=1
										ConfigParams['StreamWideOperand'][index][CurrStream]=var
										ConfigParams['VarOperands'][index][CurrStream][CurrOperand]=var
										Declare=1
									else:
										ConfigParams['VarOperands'][index][CurrStream][CurrOperand]=ConfigParams['StreamWideOperand'][index][CurrStream]
								
							else:
								var='ConstVar'+str(index)+'_Stream'+str(CurrStream)+'_Operand'+str(CurrOperand)
								ConfigParams['VarOperands'][index][CurrStream][CurrOperand]=var
							
							if(Declare):
								ConfigParams['VarOperands'][index][CurrStream][CurrOperand]=var
								if(not(index in ConfigParams['InitVar'])):
									ConfigParams['InitVar'][index]=[]
								ConfigParams['InitVar'][index].append(ConfigParams['VarOperands'][index][CurrStream][CurrOperand])
								Var=ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]
								VarDeclPrefix=ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]+' '+prefix
								VarDecl=VarDeclPrefix+' '+str(ConfigParams['VarOperands'][index][CurrStream][CurrOperand])
								VarDeclStmt.append(VarDecl)
								ConfigParams['VarDecl'][index][CurrStream][CurrOperand]=VarDecl
								VarDecl+=';'
								if debug:
									print "\n\t Var: "+str(index)+" CurrStream "+str(CurrStream)+" CurrOperand "+str(CurrOperand)
							
									print "\n\t var: "+str(var)+" ConfigParams['VarOperands'][index][CurrStream][CurrOperand]: "+str(ConfigParams['VarOperands'][index][CurrStream][CurrOperand])							

								if debug:
									print "\n\t This is the prefix: "+str(prefix)+" and this is the suffix: "+str(suffix)+" and this'd be the variable declaration: "+str(VarDecl)+ "\n "
								DynAlloc.append(VarDecl)
								
								if(ConfigParams['Dims']==1):
									if (ConfigParams['StrideScaling'][index]):
										tmp=ConfigParams['VarOperands'][index][CurrStream][CurrOperand]+'= ('+VarDeclPrefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+' * sizeof('+ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]+suffix+'))'+';'
									else:
										tmp=ConfigParams['VarOperands'][index][CurrStream][CurrOperand]+'= ('+VarDeclPrefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['Stream'][index][CurrStream])+' * sizeof('+ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]+suffix+'))'+';'	
										#tmp=var+'= ('+datatype+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+'*'+str(ConfigParams['GlobalVar']['MaxStream'][index])+' * sizeof('+datatype+suffix+'))'+';'	
									DynAlloc.append(tmp);
								else:
									tmp=ConfigParams['VarOperands'][index][CurrStream][CurrOperand]+'= ('+VarDeclPrefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][0]+' * sizeof('+ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]+suffix+'))'+';'
									
									DynAlloc.append(tmp);
									NumForLoops=''
									for i in range(ConfigParams['Dims']-1):
										NumForLoops=i+1
										MallocLHS=''
										for j in range(NumForLoops):
											ThisForLoop='for('+str(ConfigParams['indices'][j])+'=0 ; '+str(ConfigParams['indices'][j])+' < '+str(ConfigParams['GlobalVar']['DimsSize'][j])+' ; '+str(ConfigParams['indices'][j])+'+=1)'
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

										if(i==(ConfigParams['Dims']-2)): # Since the loop is going from 0 to ConfigParams['Dims']-2
											if (ConfigParams['StrideScaling'][index]):
												MallocEqn=ConfigParams['VarOperands'][index][CurrStream][CurrOperand]+MallocLHS+'= ('+Var+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * sizeof('+ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]+suffix+'))'+';'										
											else:
												MallocEqn=ConfigParams['VarOperands'][index][CurrStream][CurrOperand]+MallocLHS+'= ('+Var+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * '+str(ConfigParams['GlobalVar']['Stream'][index][CurrStream])+' * sizeof('+ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]+suffix+'))'+';'
										else:
											MallocEqn=ConfigParams['VarOperands'][index][CurrStream][CurrOperand]+MallocLHS+'= ('+Var+prefix+')'+' malloc('+ConfigParams['GlobalVar']['DimsSize'][i+1]+' * sizeof('+ConfigParams['StrideVar'][index][CurrStream]['OperandsInfo'][CurrOperand][1]+suffix+'))'+';'		
									   	if debug:
												print "\t The malloc equation is: "+str(MallocEqn)+"\n"
										DynAlloc.append(MallocEqn)
										for j in range(NumForLoops):
											DynAlloc.append('}')
										DynAlloc.append('\n')
					
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
				ConfigParams['VarDeclCollection'].append(VarDeclStmt)
	
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
					if(CurrOperatn=='|'):
						if OpertnIdx:
							Temp+='o'
						else:
							Temp+='O'
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
		print "\n\t RandomAccessNotFound: "+str(RandomAccessNotFound)+" OpDiffNotFound: "+str(OpDiffNotFound)+" StrideScalingNotFound: "+str(StrideScalingNotFound)
		print "\n\t PAPIInstNotFound: "+str(PAPIInstNotFound)+" DifferentOperandNotFound: "+str(DifferentOperandNotFound)+" IndirectionNotFound "+str(IndirectionNotFound)
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
			TempCountVar='TempCountVar'
			TempCountVarDecl='int '+str(TempCountVar)+' =0;'
			WorkingVars['TempCountVar']=TempCountVar
			WorkigVarsDecl.append(TempCountVarDecl)
			break;
	
	for VarNum in range(ConfigParams['NumVars']):
		ThisVarInit=[]
		for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
			#print "\t --$$%%--------%%$$ CurrStream: "+str(CurrStream)+" ConfigParams['StreamWideOperand'][VarNum][CurrStream] "+str(ConfigParams['StreamWideOperand'][VarNum][CurrStream])
			CurrVarName=ConfigParams['StreamWideOperand'][VarNum][CurrStream] #'Var'+str(VarNum)+'_Stream'+str(CurrStream)
			if(ConfigParams['Indirection'][VarNum]==0):
				ThisStreamInit=[]
				#for CurrVarName in (ConfigParams['InitVar'][VarNum]):
				Temp=InitVar(CurrVarName,VarNum,CurrStream,ConfigParams,WorkingVars,debug)	
				ThisStreamInit.append(Temp)
				ThisVarInit.append(ThisStreamInit)
			else:
				ThisStreamInit=[]
				Temp=InitVar(CurrVarName,VarNum,CurrStream,ConfigParams,WorkingVars,debug)	
				ThisStreamInit.append(Temp)
				CurrVarName=ConfigParams['IndirOperands'][VarNum][CurrStream]['b']
				
				Temp=InitVar(CurrVarName,VarNum,CurrStream,ConfigParams,WorkingVars,debug)	
				ThisStreamInit.append(Temp)
				CurrVarName=ConfigParams['IndirOperands'][VarNum][CurrStream]['c']
				
				Temp=InitVar(CurrVarName,VarNum,CurrStream,ConfigParams,WorkingVars,debug,1)
				ThisStreamInit.append(Temp)
				ThisVarInit.append(ThisStreamInit)
			#print "\n\t len(ThisVarInit) "+str(len(ThisVarInit))
		InitLoop.append(ThisVarInit)

	ConfigParams['PapiEventsArray']=''
	if(PAPIInstNeeded>0):
		PAPIInitCode=[]
		PAPICounters=[]
		ConfigParams['PAPIValueVars']=[]
		PAPICounters.append('"rapl:::PACKAGE_ENERGY:PACKAGE0"')
		PAPICounters.append('"rapl:::PACKAGE_ENERGY:PACKAGE1"')
		PAPICounters.append('"rapl:::DRAM_ENERGY:PACKAGE0"')
		PAPICounters.append('"rapl:::DRAM_ENERGY:PACKAGE1"')
		PAPICounters.append('"rapl:::PP0_ENERGY:PACKAGE0"')
		PAPICounters.append('"rapl:::PP0_ENERGY:PACKAGE1"')
	
	
		CountersArray='char counters[][PAPI_MAX_STR_LEN]= {'
		for count,CurrCounter in enumerate(PAPICounters):
			if(count):
				CountersArray+=','+str(CurrCounter)
			else:
				CountersArray+=str(CurrCounter)
		CountersArray+=' };'
		if debug:
			print "\n\t CountersArray: "+str(CountersArray)
		ConfigParams['PapiEventsArray']='events'
		PAPIInitCode.append(CountersArray)
		PAPIInitCode.append('int '+str(ConfigParams['PapiEventsArray'])+'[NUM_HWC];')
		PAPIInitCode.append('PAPI_library_init(PAPI_VER_CURRENT);')
		PAPIInitCode.append('for(index0=0;index0<NUM_HWC;index0++)')
		PAPIInitCode.append('{'   )
		PAPIInitCode.append('       PAPI_event_name_to_code(counters[index0],&(events[index0]));')
		#PAPIInitCode.append('       printf("\\n\\t index0: %d Counter: %s Code: %d ",index0,counters[index0],events[index0]);')
		PAPIInitCode.append('} '  )

		for CurrVar in range(ConfigParams['NumVars']):
			PAPIValueVars='ValuesVar'+str(CurrVar)
			MemAllocStmt='long long int* '+str(PAPIValueVars)+' = (long long int*)calloc(NUM_HWC,sizeof(long long int));'
			PAPIInitCode.append(MemAllocStmt)
			ConfigParams['PAPIValueVars'].append(PAPIValueVars)

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
 	 
	#{"rapl:::PACKAGE_ENERGY:PACKAGE0","rapl:::PACKAGE_ENERGY:PACKAGE1","rapl:::DRAM_ENERGY:PACKAGE0","rapl:::DRAM_ENERGY:PACKAGE1","rapl:::PP0_ENERGY:PACKAGE0","ra    pl:::PP0_ENERGY:PACKAGE1"}')

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
	PermuteGenFuncArray.append('		if( (ToFlag[JumpTo]==0 ) ) //&& ( FromFlag[JumpTo]==0) )')
	PermuteGenFuncArray.append('		{')
	PermuteGenFuncArray.append('			Count++;')
	PermuteGenFuncArray.append('			A[Node]=JumpTo;')
	PermuteGenFuncArray.append('			ToFlag[JumpTo]++;')
	PermuteGenFuncArray.append('			ToFlag[Node]++;')
	PermuteGenFuncArray.append('			//printf("\\n\t Node: %d A[Node]: %d JumpTo: %d ToFlag[Jumpto]: %d ",Node,A[Node],JumpTo,ToFlag[JumpTo]);')
	PermuteGenFuncArray.append('			Node=JumpTo;')
	PermuteGenFuncArray.append('		}')
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
	WriteArray(ConfigParams['GlobalVar']['LastDimOverflowVarDecl'],WriteFile)
	WriteArray(PinToFunc,WriteFile)
	RandomAccessCheck=0
	for CurrVarRandomAccess in ConfigParams['RandomAccess']:
		RandomAccessCheck+=CurrVarRandomAccess
		#print "\t RandomAccessCheck: "+str(CurrVarRandomAccess)+" CurrVarRandomAccess "+str(CurrVarRandomAccess)
	#print "\t RandomAccessCheck: "+str(RandomAccessCheck)	
	if(RandomAccessCheck>0):
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
	if(PAPIInstNeeded>0):
		WriteArray(PAPIInitCode,WriteFile)
	for VarNum in range(ConfigParams['NumVars']):
		for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
			for CurrArray in (InitLoop[VarNum][CurrStream]):
				WriteArray(CurrArray,WriteFile)
			"""if(ConfigParams['Indirection'][VarNum]==0):	
				WriteArray(InitLoop[VarNum][CurrStream],WriteFile)	
			else:
				WriteArray(InitLoop[VarNum][CurrStream][0],WriteFile)
				WriteArray(InitLoop[VarNum][CurrStream][1],WriteFile)	
				WriteArray(InitLoop[VarNum][CurrStream][2],WriteFile)	"""

 
	WriteArray(Comments,WriteFile)	
	suffix=''
	prefix=''
	for VarNum in range(ConfigParams['NumVars']):
		prefix='printf(" \\n\\t '
		if(ConfigParams['RandomAccess'][VarNum]>0):
			for CurrStream in range(ConfigParams['NumStreaminVar'][VarNum]):
				FlushVar='FlushVar'+str(VarNum)+'_Stream'+str(CurrStream)
				prefix+=str(FlushVar)+' %'+str(ConfigParams['DSforPrintf'][VarNum])
				suffix+=','+str(FlushVar)
				for CurrDim in range(ConfigParams['Dims']-1):
					suffix+='[0]'
				suffix+='[(int) ( rand() % '+str(ConfigParams['GlobalVar']['DimsSize'][ConfigParams['Dims']-1])+' )]'
				if debug:
					print "\n\t Prefix: "+str(prefix)
					print "\n\t Suffix: "+str(suffix)
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
