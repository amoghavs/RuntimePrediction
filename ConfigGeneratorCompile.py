
import sys,subprocess,re,math,commands,time,copy
 
def RecursiveStrideGen(CurrStream,NumStreams,StartStream,NumStrides,CurrString,CurrPrefix,CurrPrefixPos,ResultString):
	#print "\n\t StartStream: "+str(StartStream)+' and NumStrides: '+str(NumStrides)
	if(CurrStream==(NumStreams)):
		#print "\n\t ++ CurrStream: "+str(CurrStream)
		if(CurrString):
			for i in range(StartStream,NumStrides):
				Result=CurrString+','+str((2**i))
				ResultString.append(Result)
				#print "\n\t Result: "+Result
		else:
			#print "\n\t ---- \n"
			for i in range(NumStrides):
				Result=CurrString+str((2**i))
				ResultString.append(Result)
				#print "\n\t Result: "+Result		
			
		CurrStream-=1
		return #(CurrStream,CurrPrefixPos)

 	CurrPrefixPos=0
 	#if(StartStream):
 	#	StartStream-=1
 	StartStream+=1 #CurrStream-1	
	while(CurrPrefixPos!=(NumStrides-2)):
		if(CurrPrefix==''):	
			CurrString=CurrPrefix+str((2**CurrPrefixPos))	
		else:
			CurrString=CurrPrefix+','+str((2**CurrPrefixPos))
		#print "\n\t -- CurrPrefixPos: "+str(CurrPrefixPos)+' CurrStream: '+str(CurrStream)+" CurrString: "+str(CurrString)+" CurrPrefix: "+str(CurrPrefix)		
		#print "\n\t $$ CurrStream: "+str(CurrStream)+" CurrPrefixPos: "+str(CurrPrefixPos)
		RecursiveStrideGen(CurrStream+1,NumStreams,StartStream,NumStrides,CurrString,CurrString,CurrPrefixPos,ResultString)
		CurrPrefixPos+=1
		#StartStream+=1
		#print "\n\t %% CurrStream: "+str(CurrStream)+" CurrPrefixPos: "+str(CurrPrefixPos)		
		#return CurrStream
		
	CurrStream-=1
	#print "\n\t ^^ CurrPrefixPos: "+str(CurrPrefixPos)+' CurrStream: '+str(CurrStream)+" CurrString: "+str(CurrString)+" CurrPrefix: "+str(CurrPrefix)	
	return #(CurrStream,CurrPrefixPos)	
	
def IterationsCombination(LoopIterations,NumVars):
	OutputSet=[]
	Temp=[]
	OutputSet.append(Temp)
	TempOutputSet=[]
	print "\n\t NumVars: "+str(NumVars)+" len(LoopIterations): "+str(len(LoopIterations))
	for CurrVar in range(NumVars):
		for CurrLoopIterationsSet in OutputSet:
			for CurrLoopIterationsNum in (LoopIterations[CurrVar]):
				Temp=copy.deepcopy(CurrLoopIterationsSet)
				Temp.append((CurrLoopIterationsNum))
				TempOutputSet.append(Temp)
				#print "\n\t Temp: "+str(Temp)+" CurrLoopIterationsNum "+str(CurrLoopIterationsNum)+" len(TempOutputSet): "+str(len(TempOutputSet))+" "

		OutputSet=copy.deepcopy(TempOutputSet)
		TempOutputSet=[]
		#print "\n\t CurrVar: "+str(CurrVar)+" len(OutputSet): "+str(len(OutputSet))
				
	return OutputSet;		

"""

	# Max['NumOperands'] array has maximum number of operands for each variable ; Ensure Max is less than or equal to Min. 
	Max['NumOperands']=[2,2,1]
	Min['NumOperands']=[1,1,1]
	Operations={}
	Operations['MainOperations']=['+','-','*','/']

	# Max/Min['NumIntraOperands']= [ [<Variable-Num-Operands>] * <#Vars> ] ; Ensure Max is less than or equal to Min. 
	Max['NumIntraOperands']=[[2,1],[1,3],[1]]
	Min['NumIntraOperands']=[[1,1],[1,2],[1]]
	Operations['IntraOperations']=Operations['MainOperations']
	
	# Max/Min['IntraOperandDelta'] = [ (Delta-Per-Dim) * <#Vars>] ; Ensure Max is less than or equal to Min. 
	Max['IntraOperandDelta']=[(+1;-2;0) , ( +2,+3,+4) , (0,0,0) ]
	Min['IntraOperandDelta']=[ (0;-3;0) , ( +2,+3,+4) , (0,0,0) ]
	
	Max['Constant']=10
	Min['Constant']=2
	Operations['IntraOperandOperation']=['IntraOperandDelta','Constant']


"""
			
def PerStreamConfig(ResultString,Max,Min,Operations):
	print "\n\t In PerStreamConfig "
	StreamConfigResults={}
	
	NumOperands=[]
	NumVars=(Max['Vars']-Min['Vars']+1)
	if(Max['Vars']==Min['Vars']):
		NumVars=Max['Vars']
	
 	NumVarsMinusOne=NumVars-1
 	
	RequiredNumOperandsRange=[]
	MaxNumOperands=0
	for CurrVar in range(NumVars):
		Temp=[]
		for CurrVarNumOperands in range(Min['NumOperands'][CurrVar],Max['NumOperands'][CurrVar]+1):
			Temp.append(CurrVarNumOperands)
			if(CurrVarNumOperands > MaxNumOperands):
				print "\n\t MaxNumOperands: "+str(MaxNumOperands)+" CurrVarNumOperands: "+str(CurrVarNumOperands)
				MaxNumOperands= CurrVarNumOperands
		RequiredNumOperandsRange.append(Temp)


	VarsCovered=[]
	NeedToRepeat=0
	for CurrVar in range(NumVars):
		VarsCovered.append(len(RequiredNumOperandsRange[CurrVar]))
		if((len(RequiredNumOperandsRange[CurrVar]))):
			NeedToRepeat+=1

	NumOperandsSet=[]
	Temp=[]
	NumOperandsSet.append(Temp)
	NeedToRepeat=0
	for CurrVar in range(0,NumVars):
		TempNumOperandsSet=[]
		for CurrSet in NumOperandsSet:
			for CurrNumOperand in RequiredNumOperandsRange[CurrVar]:
				Temp=copy.deepcopy(CurrSet)
				Temp.append(CurrNumOperand)
				TempNumOperandsSet.append(Temp)
				#print "\n\t Temp: "+str(Temp)
		NumOperandsSet=copy.deepcopy(TempNumOperandsSet)

	ExpectedNumOperandsinSet=1
	for i in range(NumVars):
		ExpectedNumOperandsinSet*=len(RequiredNumOperandsRange[i])
		print "\n\t ExpectedNumOperandsinSet: "+str(ExpectedNumOperandsinSet)+" len(RequiredNumOperandsRange[CurrVar]): "+str(len(RequiredNumOperandsRange[i]))
		
	print "\n\t len(NumOperandsSet): "+str(len(NumOperandsSet))+" ExpectedNumOperandsinSet: "+str(ExpectedNumOperandsinSet)		
	StreamConfigResults['NumOperandsSet']=NumOperandsSet
	
	MainOperationsSet={}
	if(Operations['PermutationsFlag']['MainOperations']):
		print "\n\t Will start permutating now for the sake of MainOperations "
		CurrNumOperationsSet=[]
		Temp=[]
		CurrNumOperationsSet.append(Temp)
		TempCurrNumOperationsSet=[]
		for CurrNumOperations in range(1,MaxNumOperands):
			for CurrOperationsSet in CurrNumOperationsSet:
				for CurrOperations in Operations['MainOperations']:
					Temp=[]
					Temp=copy.deepcopy(CurrOperationsSet)
					Temp.append(CurrOperations)
					TempCurrNumOperationsSet.append(Temp)
					#print "\n\t Temp: "+str(Temp)+" len(TempCurrNumOperationsSet): "+str(len(TempCurrNumOperationsSet))

			CurrNumOperationsSet=copy.deepcopy(TempCurrNumOperationsSet)
			TempCurrNumOperationsSet=[]
			MainOperationsSet[CurrNumOperations]= CurrNumOperationsSet # CAUTION/WARNING: Assuming that the CurrNumOperations!=0 will access this dictionary, since that is an illegal case.
			print "\n\t CurrNumOperations: "+str(CurrNumOperations)+" len(CurrNumOperationsSet): "+str(len(CurrNumOperationsSet))
			
	else:
		print "\n\t Will NOT start permutating for the sake of MainOperations "			
		MainOperationsSet['Default']=(Operations['MainOperations'])

	#for CurrVar in range(NumVars):
		
		
	print "\n\n "
	return	StreamConfigResults	
	
	
	
def main():

        Max={} #; Ensure Max is less than or equal to Min. 
        Min={}
        Max['Vars']=4
        Min['Vars']=4
        Max['Dims']=3
        Min['Dims']=3
        Max['NumStream']=4
        Min['NumStream']=1
        Max['Stride']=3 # ie., 2^4
        Min['Stride']=0 # ie., 2^0=1
        Alloc=['d']    
        Init='index0'
        DS='d'
        #SpatWindow=[8,16,32];
        LoopIterationBase=10;
        LoopIterationsExponent=[[1,1.2,1.4],[1,1.5],[1,1.3],[1]];
        MbyteSize=20 # 2^28=256M = 2^20[1M] * 2^8 [256] ; # Int= 256M * 4B = 1GB. # Double= 256M * 8B= 2GB 
        MaxSize=2**MbyteSize
        Dim0Size=2**(MbyteSize-8)
        HigherDimSize= MaxSize/ Dim0Size

 	NumVars=(Max['Vars']-Min['Vars']+1)
 	if(Max['Vars']==Min['Vars']):	
 		NumVars=(Min['Vars'])
 	NumVarsLessOne=NumVars-1
 	print "\n\t WARNING: NumVars is assumed to be equal, you have been warned!! "

	# Max['NumOperands'] array has maximum number of operands for each variable ; Ensure Max is less than or equal to Min. 
	Max['NumOperands']=[2,3,2,4]
	Min['NumOperands']=[1,2,1,1] #Min: Should be >= 1 
	Operations={}
	Operations['MainOperations']=['+','-','*','/']

	PermutationsFlag={}
	PermutationsFlag['MainOperations']=1 # 0: All operands, in an expression will be same. 1: Permutation of 
	
	Operations['NumIntraOperandsNeeded']=[]
	for CurrVar in range(NumVars):
		CurrNumIntraOperandsNeeded=(Max['NumOperands'][CurrVar]-Min['NumOperands'][CurrVar]+1)
		Operations['NumIntraOperandsNeeded'].append(CurrNumIntraOperandsNeeded)
		
		
	# Max/Min['NumIntraOperands']= [ [<Variable-Num-Operands(Max-Min)>] * <#Vars> ] ; Ensure Max is less than or equal to Min. 
	Max['NumIntraOperands']=[[2,1],[1,3],[1],[1,2,2,1]]
	Min['NumIntraOperands']=[[1,1],[1,2],[1],[1,1,1,1]] #Min: Should be >= 1 
	Operations['IntraOperations']=Operations['MainOperations']
	
	# Max/Min['IntraOperandDelta'] = [ (Delta-Per-Dim) * <#Vars>] ; Ensure Max is less than or equal to Min. 
	Max['IntraOperandDelta']=[(+1,-2,0) , ( +2,+3,+4) , (0,0,0) , (0,0,0) ]
	Min['IntraOperandDelta']=[ (0,-3,0) , ( +2,+3,+4) , (0,0,0) , (0,0,0) ]
	
	Max['Constant']=10
	Min['Constant']=2
	Operations['IntraOperandOperation']=['IntraOperandDelta','Constant']
	
	Operations['PermutationsFlag']=PermutationsFlag
	
	ScriptUniqueID=''
	if(len(Alloc)==1):
		if( Alloc[0]=='d'):
			ScriptUniqueID='Dynamic'
		elif(Alloc[0]=='s'):
			ScriptUniqueID='Static'
		else:
			print "\n\t Data Alloc is neither dynamic or static \n"
			sys.exit()
		
		if(DS=='i' or DS=='int'):
			ScriptUniqueID='Int_'+ScriptUniqueID
		elif(DS=='f' or DS=='float'):
			ScriptUniqueID='Float_'+ScriptUniqueID		
		elif(DS=='d' or DS=='double'):
			ScriptUniqueID='Double_'+ScriptUniqueID		
	
	else:
		print "\n\t The script is designed only for including name of one allocation type and alloc has "+str(len(Alloc))+" alloc requests. You are doomed!! \n"
		sys.exit()
	
				
	MasterSWStatsPrefix='MasterSWStats_'+ScriptUniqueID+'_Stride'+str(Min['Stride'])+'to'+str(Max['Stride'])
	#MasterSWStatsSuffix='_Size2power'+str(MbyteSize)+'_dim'+str(Min['Dims'])+'to'+str(Max['Dims'])+'_Stride'+str(Min['Stride'])+'to'+str(Max['Stride'])+'_Streams'+str(Min['NumStream'])+'to'+str(Max['NumStream'])+'_Iterations'+str(LoopIterations[0])+'to'+str(LoopIterations[len(LoopIterations)-1])
	#FolderName='SRC_'+ScriptUniqueID+MasterSWStatsSuffix
	#MasterSWStatsFile=MasterSWStatsPrefix+MasterSWStatsSuffix+'.txt'

	
	
        LoopIterations=[]
        for CurrVar in range(NumVars):
        	Temp=[]
        	for CurrLoopIterExponent in (LoopIterationsExponent[CurrVar]):
        		CurrNumLoops= int( (LoopIterationBase) ** (CurrLoopIterExponent) )
        		Temp.append(CurrNumLoops)
        		#print "\n\t Base: "+str(LoopIterationBase)+" CurrLoopIterExponent: "+str(CurrLoopIterExponent)+" CurrNumLoops: "+str(CurrNumLoops)
 		LoopIterations.append(Temp)
 	#sys.exit()
 	#OutputSet=[]
 	CurrVar=0
 	Prefix=[]
 	StartIdx=0
 	for i in range(NumVars):
 		Prefix.append(0)
 	OutputSet=IterationsCombination(LoopIterations,NumVars)

 	#for CurrSetIterations in OutputSet:
 	#	print "\n\t CurrSetIterations: "+str(CurrSetIterations) 

 	#sys.exit()
   	for CurrSetIterations in OutputSet:	
	   	print "\n\t CurrSetIterations: "+str(CurrSetIterations)
 		#MasterSWStats.write("\n\n\t ################################ \n\n");
 		for NumDims in range(Min['Dims'],Max['Dims']+1):
			SizeString=''
			SizeName=''				
			if (NumDims>1):
				ResolveBases=1
				IncrementLastDim=0
				while ResolveBases:
					EachDimBase=( math.log(float(HigherDimSize),2) - IncrementLastDim)/(NumDims-1)
					if(int(EachDimBase)==EachDimBase):
						ResolveBases=0
					else:
						IncrementLastDim+=1					
			
				print "\n\t NumDims: "+str(NumDims)+" Each Dim Base: "+str(EachDimBase)+" IncrementLastDim: "+str(IncrementLastDim)+" CurrSetIterations: "+str(CurrSetIterations)
				EachDimSize=int(2**EachDimBase)
				for i in range(NumDims-2):
					SizeString=str(EachDimSize)+','+str(SizeString)
					SizeName=str(EachDimSize)+'_'+str(SizeName)
				
				SizeString=str(SizeString)+str(int(EachDimSize*(2**IncrementLastDim)))+','+str(Dim0Size)
				SizeName=str(SizeName)+str(int(EachDimSize*(2**IncrementLastDim)))+'_'+str(Dim0Size)
				
			else:
				SizeString=MaxSize
				SizeName=MaxSize
			print "\n\t SizeName: "+str(SizeName)+" SizeString "+str(SizeString)
			

			for NumStreams in range(Min['NumStream'],Max['NumStream']+1):
					#MasterSWStatsFile=MasterSWStatsPrefix+'_Iters'+str(NumLoopIterations)+'_dim'+str(NumDims)+'_Streams'+str(NumStreams)+'.txt'
					#print "\n\t MasterSWStatsFile: "+str(MasterSWStatsFile)+" NumStreams: "+str(NumStreams)
					#MasterSWStats=open(MasterSWStatsFile,'w')
				CurrStream=1
				NumStrides=((Max['Stride']-Min['Stride'])+1)	
				CurrString=''
				CurrPrefix=''
				CurrPrefixPos=0
				StartStream=-1 
				ResultString=[]
				RecursiveStrideGen(CurrStream,NumStreams,StartStream,NumStrides,CurrString,CurrPrefix,CurrPrefixPos,ResultString)
		
				NumStreamString='#StreamDims '+str(NumStreams) # CAUTION: Should change this when NumVars > 1
				StrideString=''
				StrideName=''
				print "\n\t This is the length of ResultString: "+str(len(ResultString))
				StreamConfigResults=PerStreamConfig(ResultString,Max,Min,Operations)
				sys.exit()	
				"""for CurrStreamCombi in ResultString:
					StrideString='#stride0 '+str(CurrStreamCombi)
					Strides=re.split(',',CurrStreamCombi)
					StrideName=''
					MaxStride=0
					if Strides:
						for i in range(len(Strides)-1):
							StrideName+=str(Strides[i])+'_'
							if(MaxStride<int(Strides[i])):
								MaxStride=int(Strides[i]) # CAUTION: Should change this when NumVars > 1
							else:
								print "\n\t We think strides[i]: "+str(Strides[i])+" is lesser than Maxstrides: "+str(MaxStride)
						StrideName+=str(Strides[len(Strides)-1])
						if(MaxStride<int(Strides[len(Strides)-1])):
							MaxStride=int(Strides[len(Strides)-1]) # CAUTION: Should change this when NumVars > 1
						else:
							print"\n\t -- Stride: "+str(Strides[len(Strides)-1])+" MaxStride: "+str(MaxStride)
						
						#StrideName+=str(MaxStride) # CAUTION: Should change this when NumVars > 1
						print "\n\t Stride-Name: "+str(StrideName)+' StrideString '+str(StrideString)+" and Maxstride: "+str(MaxStride)
					else:
						print "\n\t CurrStreamCombi: "+str(StrideName)+" seems to be corrupted, exitting! "
						sys.exit()
						
							
					for CurrAlloc in Alloc:
						UniqueID='Iters'+str(NumLoopIterations)+'_'+str(NumVars)+"vars_"+str(CurrAlloc)+'_'+str(NumDims)+"dims_"+str(SizeName)+'_streams_'+str(NumStreams)+'_stride_'+str(StrideName)
						SRCID='Iters'+str(NumLoopIterations)+'_'+str(NumVars)+"vars_"+str(CurrAlloc)+'_'+str(NumDims)+"dims_"+str(SizeName)+'_streams_'+str(NumStreams)+'_stride_'+str(StrideName)
						Config="Config_"+UniqueID
						ConfigFile=str(Config)+'.txt'

						f=open(ConfigFile,'w')
						f.write("\n#vars "+str(NumVars))
						f.write("\n#dims "+str(NumDims))
						f.write("\n"+str(NumStreamString))
						f.write("\n#loop_iterations "+str(NumLoopIterations))
						f.write("\n"+str(StrideString))
						#f.write("\n#stride "+str(Stride))
						f.write("\n#size "+str(SizeString))
						f.write("\n#allocation "+str(CurrAlloc) )
						f.write("\n#init "+str(Init))
						f.write("\n#datastructure "+str(DS))
						f.close()
					
					#CMDConfigDir='mkdir '+str(Config)
					#commands.getoutput(CMDConfigDir)						
					
					CMDrunStrideBenchmarks='python RuntimeBenchmarksGeneration.py -c '+str(ConfigFile)
					commands.getoutput(CMDrunStrideBenchmarks)
					SRCCode='StrideBenchmarks_'+str(SRCID)+'.c'
					EXE='StrideBenchmarks_'+str(SRCID)
					print "\n\t Config file: "+str(ConfigFile)#+" source: "+str(SRCCode)+" exe "+str(EXE)						
					CMDCompileSRC='gcc -O3 -g '+str(SRCCode)+' -o '+str(EXE)
					#print "\n\t CMDCompile: "+str(CMDCompileSRC)
					commands.getoutput(CMDCompileSRC) """




if __name__=="__main__":
	main() #sys.argv[1:])
	
