
import sys,subprocess,re,math,commands,time,copy,random

### WORKING ASSUMPTIONS:
# NumVars is constant

### ShortComing/Future-work: 
# 1. stream, stride is not permutable; Hence similar stream and stride is used for all variable. 
	# Current working solution: Split the "stride/stream" space amongst variable, instead of making each possible combination. 
	# Might work for now, but for generalizing the tool, will need this flexibility. Might not take too long to incorporate this!
	# Even the intraoperanddelta generated is common across all streams.
# 2. <>

def RecursiveStrideGen(CurrStream,NumStreams,StartStream,NumStrides,CurrString,CurrPrefix,CurrPrefixPos,ResultString):
	#print "\n\t StartStream: "+str(StartStream)+' and NumStrides: '+str(NumStrides)
	if(CurrStream==(NumStreams)):
		#print "\n\t ++ CurrStream: "+str(CurrStream)
		if(CurrString):
			for i in range(StartStream,NumStrides):
				Result=CurrString+','+str((2**i))
				ResultString.append(Result)
				print "\n\t 1. Result: "+Result
		else:
			#print "\n\t ---- StartStream: "+str(StartStream)+"\n"
			for i in range(StartStream,StartStream+NumStrides):
				Result=CurrString+str((2**i))
				ResultString.append(Result)
				#print "\n\t 2. Result: "+Result		
			
		CurrStream-=1
		return 

 	CurrPrefixPos=0
  	StartStream+=1 
	while(CurrPrefixPos!=(NumStrides-2)):
		if(CurrPrefix==''):	
			CurrString=CurrPrefix+str((2**CurrPrefixPos))	
		else:
			CurrString=CurrPrefix+','+str((2**CurrPrefixPos))
		print "\n\t -- CurrPrefixPos: "+str(CurrPrefixPos)+' CurrStream: '+str(CurrStream)+" CurrString: "+str(CurrString)+" CurrPrefix: "+str(CurrPrefix)		
		#print "\n\t $$ CurrStream: "+str(CurrStream)+" CurrPrefixPos: "+str(CurrPrefixPos)
		RecursiveStrideGen(CurrStream+1,NumStreams,StartStream,NumStrides,CurrString,CurrString,CurrPrefixPos,ResultString)
		CurrPrefixPos+=1
 		
	CurrStream-=1
 	return  	
	
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

			
def PerStreamConfig(Max,Min,Operations):
	print "\n\t In PerStreamConfig "
	StreamConfig={}
	
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

	StreamConfig['NumOperandsSet']=NumOperandsSet

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

	StreamConfig['MainOperationsSet']=MainOperationsSet

	StreamConfig['IntraOperandDelta']={}
	StreamConfig['IntraOperandDelta']['Max']=Max['IntraOperandDelta']
	StreamConfig['IntraOperandDelta']['Min']=Min['IntraOperandDelta']
		
	StreamConfig['CurrNumDims']=Max['Dims'] 
	print "\n\t StreamConfig['CurrNumDims']: "+str(StreamConfig['CurrNumDims'])+" is set to be Max['Dims'] "	
	print "\n "
	return	StreamConfig	

	
def PermuteforStrideConfig(StreamConfig,NumVars,Operations):

	StrideConfigPrep={}
	for CurrNumOperands in (StreamConfig['NumOperandsSet']):
		CurrNumOperandsString=''
		for i in (CurrNumOperands):
			CurrNumOperandsString+=str(i)
		#print "\n\t CurrNumOperands: "+str(CurrNumOperands)+" string: "+str(CurrNumOperandsString)	
		StrideConfigPrep[CurrNumOperandsString]={}
		for CurrVar in range(NumVars):
			#+" Should use the key for MainOperationSet: "+str(CurrNumOperands[CurrVar]-1)
			StrideConfigPrep[CurrNumOperandsString][CurrVar]={}
			StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo']=[]
			if(Operations['PermutationsFlag']['MainOperations']):
				if(CurrNumOperands[CurrVar]>1):
					MainOpsKey=CurrNumOperands[CurrVar]-1
					print "\n\t CurrNumOperands[CurrVar] "+str(CurrNumOperands[CurrVar])+" can permutate over a set of operations: "+str((StreamConfig['MainOperationsSet'][MainOpsKey]))
					NumOpsLastIdx=(CurrNumOperands[CurrVar]-1)-1
					for CurrOperationsSet in (StreamConfig['MainOperationsSet'][MainOpsKey]):
						OpCombo='('
						for Idx,CurrOperation in enumerate(CurrOperationsSet):
							OpCombo+=str(CurrOperation)
							if(NumOpsLastIdx>Idx):
								OpCombo+=','
						OpCombo+=')'
						#print "\n\t OpCombo: "+str(OpCombo)+" CurrSet: "+str(CurrOperationsSet)	
						StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo'].append(OpCombo)
				else:
					#print "\n\t CurrNumOperands[CurrVar] "+str(CurrNumOperands[CurrVar])+" does not need any operation"
					StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo'].append('')
			else:
				NumOperations=len(Operations['MainOperations'])
				OpCombo='('
				print "\n\t CurrNumOperands: "+str(CurrNumOperands)
				for i in range(CurrNumOperands[CurrVar]-1):
					Idx=random.randrange(NumOperations)
					CurrOperation=Operations['MainOperations'][Idx]
					if(i):
						OpCombo+=','+str(CurrOperation)
					else:
						OpCombo+=str(CurrOperation)
				if(CurrNumOperands[CurrVar]==1):
					OpCombo=''
				else:
					OpCombo+=')'

				StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo'].append(OpCombo)
					
	return StrideConfigPrep

########		
def main():

        Max={} #; Ensure Max is less than or equal to Min. 
        Min={}
        Max['Vars']=1
        Min['Vars']=1
        Max['Dims']=3
        Min['Dims']=3
        Max['NumStream']=1
        Min['NumStream']=1
        Max['Stride']=3 # ie., 2^4
        Min['Stride']=1 # ie., 2^0=1
        Alloc=[['d']] #,'d','d','d']]    
        Init=['index0+1']#,'index0','index0','index0']
        DS=[['i']]#,'d','d','d']]    
	RandomAccess=[[0]] # 1,1,1]]
        #SpatWindow=[8,16,32];
        LoopIterationBase=10;
        #LoopIterationsExponent=[[1,1.2,1.4],[1,1.5],[1,1.3],[1]];
        LoopIterationsExponent=[[1]]# ,[1],[1],[1]];


 	NumVars=(Max['Vars']-Min['Vars']+1)
 	if(Max['Vars']==Min['Vars']):	
 		NumVars=(Min['Vars'])
 	NumVarsLessOne=NumVars-1
 	print "\n\t WARNING: NumVars is assumed to be equal, you have been warned!! "

	# Max['NumOperands'] array has maximum number of operands for each variable ; Ensure Max is less than or equal to Min. 
   
        MbyteSize=24 # 2^28=256M = 2^20[1M] * 2^8 [256] ; # Int= 256M * 4B = 1GB. # Double= 256M * 8B= 2GB 
        MaxSize=2**MbyteSize
        HigherDimSizeIndex=8
        Dim0Size=2**(MbyteSize-HigherDimSizeIndex)
        HigherDimSize= MaxSize/ Dim0Size
        
	Max['NumOperands']=[3] #,2,1,4]
	Min['NumOperands']=[1] #,1,1,1] #Min: Should be >= 1 

	Operations={}
	Operations['MainOperations']=['+','-','*','/']

	PermutationsFlag={}
	PermutationsFlag['MainOperations']=0 # 0: All operands, in an expression will be same. 1: Permutation of 
	
	Operations['DimLookup']={0:'i',1:'j',2:'k'} # Should have as many dims
	
	# Max/Min['IntraOperandDelta'] = [ (Delta-Per-Dim) * <#Vars>] ; Ensure Max is less than or equal to Min. # Min should be positive when specified and Min and Max cannot be equal to zero, but can play around while chosing the actual indices.
	Max['IntraOperandDelta']=[(+3,+4,2)]#, ( +3,+3,+4) , ( +3,+3,+4) , ( +3,+3,+4) ]
	Min['IntraOperandDelta']=[(0,+1,0) ] #, ( +2,+1,+2) , ( +2,+1,+2) , ( +2,+1,+2) ]
	
	Max['Constant']=10
	Min['Constant']=2
	Operations['IntraOperandOperation']=['IntraOperandDelta','Constant']
 	#Operations['Operand']	
	Operations['PermutationsFlag']=PermutationsFlag 
 
        LoopIterations=[]
        for CurrVar in range(NumVars):
        	Temp=[]
        	for CurrLoopIterExponent in (LoopIterationsExponent[CurrVar]):
        		CurrNumLoops= int( (LoopIterationBase) ** (CurrLoopIterExponent) )
        		Temp.append(CurrNumLoops)
        		#print "\n\t Base: "+str(LoopIterationBase)+" CurrLoopIterExponent: "+str(CurrLoopIterExponent)+" CurrNumLoops: "+str(CurrNumLoops)
 		LoopIterations.append(Temp)
 
  	CurrVar=0
 	Prefix=[]
 	StartIdx=0
 	for i in range(NumVars):
 		Prefix.append(0)
 	OutputSet=IterationsCombination(LoopIterations,NumVars)

  	StreamConfig=PerStreamConfig(Max,Min,Operations)
  	StrideConfigPrep=PermuteforStrideConfig(StreamConfig,NumVars,Operations)
  	
  	InitExpression=''
  	for i,CurrVarInit in enumerate(Init):
  		if(i):
  			InitExpression+=','+str(CurrVarInit)
  		else:
  			InitExpression+=str(CurrVarInit)
	
   	for CurrSetIterations in OutputSet:	
	   	
	   	IterationsString=''
	   	for i,CurrVarIterations in enumerate(CurrSetIterations):
	   		if(i):
	   			IterationsString+=','+str(CurrVarIterations)
	   		else:
	   			IterationsString+=str(CurrVarIterations)
 		
 		print "\n\t CurrSetIterations: "+str(CurrSetIterations)+" IterationsString: "+str(IterationsString)
 		
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
 				CurrStream=1
				NumStrides=((Max['Stride']-Min['Stride'])+1)	
				CurrString=''
				CurrPrefix=''
				CurrPrefixPos=0
				StartStream=0 #Min['Stride'] 
				StrideSet=[]
				RecursiveStrideGen(CurrStream,NumStreams,StartStream,NumStrides,CurrString,CurrPrefix,CurrPrefixPos,StrideSet)
		
				for i in range(NumVars):	
					if(i):
						NumStreamString+=','+str(NumStreams) 
						StreamName+='_'+str(NumStreams)
					else:
						NumStreamString=str(NumStreams)
						StreamName=str(NumStreams)
				StrideString=''
				StrideName=''
				print "\n\t This is the length of StrideSet: "+str(len(StrideSet))

				StreamConfigCollection={}
				CurrStrideStringSet=[]
				
				for CurrStrideSet in StrideSet:
					
					ExtractStrideforStream=re.split(',',CurrStrideSet)
					if ExtractStrideforStream:
						CurrStrideString=''
						CurrStrideCombi=''
						for idx,CurrStride in enumerate(ExtractStrideforStream):
							if(idx):
								CurrStrideString+='_'+str(CurrStride)
								CurrStrideCombi+=','+str(CurrStride)
							else:
								CurrStrideString+=(CurrStride)
								CurrStrideCombi+=str(CurrStride)
								
						print "\n\t DCurrStrideString: "+str(CurrStrideString)
						CurrStrideStringSet.append((CurrStrideString,CurrStrideCombi) )
						StreamConfigCollection[CurrStrideString]={}
					else:
						print "\n\t ERROR: Some error with extracting stride for the stream. "

					for CurrNumOperands in (StreamConfig['NumOperandsSet']):
						
						CurrNumOperandsString=''
						for i in CurrNumOperands:
							CurrNumOperandsString+=str(i)	
						
 						if( not(CurrNumOperandsString in StreamConfigCollection[CurrStrideString]) ):
							StreamConfigCollection[CurrStrideString][CurrNumOperandsString]={}
							
						for CurrVar in range(NumVars):
								
								if(len(ExtractStrideforStream)==NumStreams):
## $$$$$$$$$$$$$$$
									if( not( CurrVar in StreamConfigCollection[CurrStrideString][CurrNumOperandsString] ) ):
										StreamConfigCollection[CurrStrideString][CurrNumOperandsString][CurrVar]=[]
									
									OpComboSet=[]
									for CurrCombo in (StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo']):

										CurrOpCombo=str(CurrCombo)+'; ('
										for Idx in range((CurrNumOperands[CurrVar])):
											if(Idx):
												CurrOpCombo+=','
											PickIdx=random.randrange(StreamConfig['CurrNumDims'])
											PickDelta=random.randrange(StreamConfig['IntraOperandDelta']['Min'][CurrVar][PickIdx],StreamConfig['IntraOperandDelta']['Max'][CurrVar][PickIdx])
											if(random.randrange(2)==0):
												OperandIdx=str(Operations['DimLookup'][PickIdx])+'-'+str(PickDelta)
											else:
												OperandIdx=str(Operations['DimLookup'][PickIdx])+'+'+str(PickDelta)	
											CurrOpCombo+=str(OperandIdx)
										CurrOpCombo+=')'
										#print "\n\t CurrCombo: "+str(CurrCombo)+" CurrOpCombo "+str(CurrOpCombo)
										OpComboSet.append(CurrOpCombo)
## $$$$$$$$$$$$$$$$$							
	
									StrideOperationsPrefix=[]
									for CurrNumStream in range(NumStreams):
										Temp='#strideoperations_var'+str(CurrVar)+'_'+str(CurrNumStream)
										Temp+=' <'+str(ExtractStrideforStream[CurrNumStream])+';'+str(CurrNumOperands[CurrVar])
										StrideOperationsPrefix.append(Temp)
										#print "\n\t -- StrideOperationsPrefix: "+str(Temp)+' CurrNumStream: '+str(CurrNumStream)
									
									#print "\n\t len(OpComboSet): "+str(len(OpComboSet))	
									for CurrOpCombo in OpComboSet:
										Temp=[]
										
										#print "\n\t CurrOpCombo: "+str(CurrOpCombo)+' AccumCount: '+str(AccumCount)
										for CurrNumStream in range(NumStreams):	
											Temp1=str(StrideOperationsPrefix[CurrNumStream])+' ; '+str(CurrOpCombo)+'>'
											Temp.append(Temp1)
										StreamConfigCollection[CurrStrideString][CurrNumOperandsString][CurrVar].append(Temp)	
										#print "\n\t -- StrideOperationsPrefix: "+str(StrideOperationsPrefix)+' CurrNumStream: '+str(CurrNumStream)
								
								else:
									print "\n\t ERROR: NumStreams "+str(NumStreams)+" is not equal to len(ExtractStrideforStream): "+str(len(ExtractStrideforStream))
				
									sys.exit()
				CombinedStreamConfig={}
				for StrideTuple in (CurrStrideStringSet):
					CurrStrideString=StrideTuple[0]
					CurrStrideCombi=StrideTuple[1]
					CombinedStreamConfig[CurrStrideString]={}
					print "\n\t -- 	CurrStrideString: "+str(CurrStrideString)
					for CurrNumOperandsStringKey in (StreamConfigCollection[CurrStrideString]):
						Temp=[]
						CombiAccumulation=[]
						CombiAccumulation.append(Temp)
						AccumulationCount=0;
						for CurrVar in range(NumVars):
							TempCombiAccumulation=[]
							for CurrCombi in (CombiAccumulation):
								#print "\n\t CurrCombi: "+str(CurrCombi)
								for CurrVarCombiSet in (StreamConfigCollection[CurrStrideString][CurrNumOperandsStringKey][CurrVar]):
									Temp=[]
									Temp=copy.deepcopy(CurrCombi)
									AccumulationCount+=1
									for CurrVarCombi in (CurrVarCombiSet):
										Temp.append(CurrVarCombi)
 									TempCombiAccumulation.append(Temp)
								
							CombiAccumulation=copy.deepcopy(TempCombiAccumulation)
						print "\n\t AccumulationCount: "+str(AccumulationCount)+' * (NumOperands) '+str(len(StreamConfigCollection[CurrStrideString]))+' * '+str(len(CurrStrideStringSet))
						

						for CurrCombiAccumulation in (CombiAccumulation):
							
							for CurrAllocSet in Alloc:
								AllocString=''
								for i,CurrAlloc in enumerate(CurrAllocSet):
									if(i):
										AllocString+=','+str(CurrAlloc)
									else:
										AllocString+=str(CurrAlloc)
								DSString=''
								for CurrDSSet in DS:
									for i,CurrDS in enumerate(CurrDSSet):
										if(i):
											DSString+=','+str(CurrDS)
										else:
											DSString+=str(CurrDS)
									RandomAccessString=''
									for CurrVarRandomAccessSet in RandomAccess:
										for i,CurrVarRandomAccess in enumerate(CurrVarRandomAccessSet):
											 	if(i):
											 		RandomAccessString+=','+str(CurrVarRandomAccess)
											 	else:
											 		RandomAccessString+=str(CurrVarRandomAccess)		
										
										ConfigFileName='SampleConfig_Vars'+str(NumVars)+'_Dims'+str(NumDims)+'_Streams_'+str(StreamName)+'.txt'
										print "\n\t ConfigFileName: "+str(ConfigFileName)

										f=open(ConfigFileName,'w')
										f.write("\n#vars "+str(NumVars))
										f.write("\n#dims "+str(NumDims))
										f.write("\n#StreamDims "+str(NumStreamString))
										f.write("\n#RandomAccess "+str(RandomAccessString))
										f.write("\n#loop_iterations "+str(IterationsString))
										#f.write("\n"+str(StrideString))
										f.write("\n#size "+str(SizeString))
										f.write("\n#allocation "+str(AllocString) )
										f.write("\n#init "+str(InitExpression))
										f.write("\n#datastructure "+str(DSString))
								
										for CurrCombi in CurrCombiAccumulation:
											print "\n\t CurrCombi: "+str(CurrCombi)
											f.write("\n"+str(CurrCombi))
									
										f.write("\n\n")
										f.close()
										OutputFileName='Duh.log'
										CMDrunStrideBenchmarks='python MPIRuntimeBenchmarksGeneration.py -c '+str(ConfigFileName)+' > '+str(OutputFileName)
										commands.getoutput(CMDrunStrideBenchmarks)
										print "\n\t CMDrunStrideBenchmarks: "+str(CMDrunStrideBenchmarks)
										OutputFile=open(OutputFileName)
										ReadOutput=OutputFile.readlines()
										OutputFile.close()
										for CurrLine in ReadOutput:
											FileName=re.match('^\s*Source\s*file\s*name\:\s*(.*).c',CurrLine)
											if FileName:
												print "\n\t CurrFile Name is: "+str(FileName.group(1))+'.c'
												SRCFileName=str(FileName.group(1))+'.c'
												CMDCompileFile='mpicc -g -O3 '+str(SRCFileName)+' -o '+str(FileName.group(1))
												print "\n\t CMDCompileFile: "+str(CMDCompileFile)
												commands.getoutput(CMDCompileFile)
						#sys.exit()
						



if __name__=="__main__":
	main() #sys.argv[1:])
	
