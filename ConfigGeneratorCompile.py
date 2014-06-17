
import sys,subprocess,re,math,commands,time,copy,random

### WORKING ASSUMPTIONS:
# NumVars is constant

### ShortComing/Future-work: 
# 1. stream, stride is not permutable; Hence similar stream and stride is used for all variable. 
	# Current working solution: Split the "stride/stream" space amongst variable, instead of making each possible combination. 
	# Might work for now, but for generalizing the tool, will need this flexibility. Might not take too long to incorporate this!
# 2. <>

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
		return 

 	CurrPrefixPos=0
  	StartStream+=1 
	while(CurrPrefixPos!=(NumStrides-2)):
		if(CurrPrefix==''):	
			CurrString=CurrPrefix+str((2**CurrPrefixPos))	
		else:
			CurrString=CurrPrefix+','+str((2**CurrPrefixPos))
		#print "\n\t -- CurrPrefixPos: "+str(CurrPrefixPos)+' CurrStream: '+str(CurrStream)+" CurrString: "+str(CurrString)+" CurrPrefix: "+str(CurrPrefix)		
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
	NumIntraOperandsRange={}
	MaxIntraNumOperands=0
	for CurrVar in range(NumVars):
		NumIntraOperandsRange[CurrVar]={}
		#print "\n\t CurrVar: "+str(CurrVar)
		for CurrOperand in range(Operations['NumIntraOperandsNeeded'][CurrVar]):
			MinVal=Min['NumIntraOperands'][CurrVar][CurrOperand]
			MaxVal=Max['NumIntraOperands'][CurrVar][CurrOperand]
			Temp=[]
			if(MaxVal > MaxIntraNumOperands):
				MaxIntraNumOperands=MaxVal
			for CurrVal in range(MinVal,MaxVal+1):
				Temp.append(CurrVal)
				print "\n\t CurrVal: "+str(CurrVal)+" Temp: "+str(Temp)
			NumIntraOperandsRange[CurrVar][CurrOperand]=Temp
			print "\n\t CurrVar: "+str(CurrVar)+" CurrOperand "+str(CurrOperand)+" len(NumIntraOperandsRange[CurrVar][CurrOperand]): "+str(len(NumIntraOperandsRange[CurrVar][CurrOperand]))
			print "\n\t NumIntraOperandsRange[CurrVar][CurrOperand]): "+str(NumIntraOperandsRange[CurrVar][CurrOperand])
	#sys.exit()	
	StreamConfig['NumIntraOperandsRange']=NumIntraOperandsRange

	IntraOperationsSet={}
	if(Operations['PermutationsFlag']['IntraOperations']):
		print "\n\t Will start permutating now for the sake of MainOperations "
		CurrIntraNumOperationsSet=[]
		Temp=[]
		CurrIntraNumOperationsSet.append(Temp)
		TempCurrIntraNumOperationsSet=[]
		
		for CurrNumOperations in range(1,MaxIntraNumOperands): # CAUTION: Where 
			for CurrIntraOperationsSet in CurrIntraNumOperationsSet:
				for CurrIntraOperations in Operations['IntraOperations']:
					Temp=[]
					Temp=copy.deepcopy(CurrIntraOperationsSet)
					Temp.append(CurrIntraOperations)
					TempCurrIntraNumOperationsSet.append(Temp)
					#print "\n\t Temp: "+str(Temp)+" len(TempCurrNumOperationsSet): "+str(len(TempCurrIntraNumOperationsSet))

			CurrIntraNumOperationsSet=copy.deepcopy(TempCurrIntraNumOperationsSet)
			TempCurrIntraNumOperationsSet=[]
			IntraOperationsSet[CurrNumOperations]= CurrIntraNumOperationsSet # CAUTION/WARNING: Assuming that the CurrNumOperations!=0 will access this dictionary, since that is an illegal case.
			print "\n\t CurrNumOperations: "+str(CurrNumOperations)+" len(CurrNumOperationsSet): "+str(len(CurrIntraNumOperationsSet))
		print "\n\t MaxIntraNumOperands: "+str(MaxIntraNumOperands)
	else:
		print "\n\t Will NOT start permutating for the sake of MainOperations "			
		IntraOperationsSet['Default']=(Operations['MainOperations'])

	StreamConfig['IntraOperationsSet']=IntraOperationsSet
	
	ConstantsSet=[]
	for i in range(Min['Constant'],Max['Constant']+1):	# WARNING: This feature is mostly foolish! 
		ConstantsSet.append(i)
		#print "\n\t Constant: "+str(i)
	StreamConfig['ConstantsSet']=ConstantsSet

	StreamConfig['IntraOperandDelta']={}
	StreamConfig['IntraOperandDelta']['Max']=Max['IntraOperandDelta']
	StreamConfig['IntraOperandDelta']['Min']=Min['IntraOperandDelta']
		
	StreamConfig['CurrNumDims']=Max['Dims'] 
	print "\n\t StreamConfig['CurrNumDims']: "+str(StreamConfig['CurrNumDims'])+" is set to be Max['Dims'] "	
	print "\n\n "
	return	StreamConfig	
	
def PermuteforStrideConfig(StreamConfig,NumVars,Operations):

	StrideConfigPrep={}
	for CurrNumOperands in (StreamConfig['NumOperandsSet']):
		CurrNumOperandsString=''
		for i in (CurrNumOperands):
			CurrNumOperandsString+=str(i)
		print "\n\t CurrNumOperands: "+str(CurrNumOperands)+" string: "+str(CurrNumOperandsString)	
		StrideConfigPrep[CurrNumOperandsString]={}
		for CurrVar in range(NumVars):
			#+" Should use the key for MainOperationSet: "+str(CurrNumOperands[CurrVar]-1)
			StrideConfigPrep[CurrNumOperandsString][CurrVar]={}
			StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo']=[]
			if(CurrNumOperands[CurrVar]>1):
				MainOpsKey=CurrNumOperands[CurrVar]-1
				#print "\n\t CurrNumOperands[CurrVar] "+str(CurrNumOperands[CurrVar])+" can permutate over a set of operations: "+str(len(StreamConfig['MainOperationsSet'][MainOpsKey]))
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
				StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo'].append(0)
			
			for CurrOperand in range(Operations['NumIntraOperandsNeeded'][CurrVar]):
				#print "\n\t CurrVar: "+str(CurrVar)+" CurrOperand "+str(CurrOperand)+" Operations['NumIntraOperandsNeeded'][CurrVar][CurrOperand]) "+str(StreamConfig['NumIntraOperandsRange'][CurrVar][CurrOperand])
				StrideConfigPrep[CurrNumOperandsString][CurrVar][CurrOperand]={}
				for CurrIntraOperands in StreamConfig['NumIntraOperandsRange'][CurrVar][CurrOperand]:
					StrideConfigPrep[CurrNumOperandsString][CurrVar][CurrOperand][CurrIntraOperands]={}
					StrideConfigPrep[CurrNumOperandsString][CurrVar][CurrOperand][CurrIntraOperands]['OpCombo']=[]
					if(CurrIntraOperands>1):
						IntraOpsKey=CurrIntraOperands-1
						#print "\n\t\t CurrIntraOperands: "+str(CurrIntraOperands)+" will permute over a set of operations: "+str(len(StreamConfig['IntraOperationsSet'][IntraOpsKey]))+" LastSet: "+str(StreamConfig['IntraOperationsSet'][IntraOpsKey][(len(StreamConfig['IntraOperationsSet'][IntraOpsKey])-1)])
						for CurrIntraOperationsSet in (StreamConfig['IntraOperationsSet'][IntraOpsKey]):
							OpCombo='('+str(CurrIntraOperands)+':'
							for Idx,CurrIntraOperation in enumerate(CurrIntraOperationsSet):
								if Idx:
									OpCombo+=','+str(CurrIntraOperation)
								else:
									OpCombo+=str(CurrIntraOperation)
							OpCombo+=':'
							#print "\n\t OpCombo: "+str(OpCombo)
							StrideConfigPrep[CurrNumOperandsString][CurrVar][CurrOperand][CurrIntraOperands]['OpCombo'].append(OpCombo)
					else:
						OpCombo='('+str(CurrIntraOperands)+':'
						StrideConfigPrep[CurrNumOperandsString][CurrVar][CurrOperand][CurrIntraOperands]['OpCombo'].append(OpCombo)
						#print "\n\t OpCombo: "+str(OpCombo)#"""
		
	return StrideConfigPrep

def PrepareStreamConfig(StreamConfigPreparation,CurrVar,CurrNumOperands,PrefixStream,StrideConfigPrep,StreamConfig,NumVars,Operations):

	print "\n\t CurrVar: "+str(CurrVar)+" CurrNumOperands: "+str(CurrNumOperands)+" -- \n"
	#sys.exit()
	#for CurrNumOperands in (StreamConfig['NumOperandsSet']):
	CurrNumOperandsString=''
	for i in (CurrNumOperands):
		CurrNumOperandsString+=str(i)
	print "\n\t CurrNumOperands: "+str(CurrNumOperands)+" string: "+str(CurrNumOperandsString)	
	
	#for CurrVar in range(NumVars):
		#+" Should use the key for MainOperationSet: "+str(CurrNumOperands[CurrVar]-1)
	StreamConfigPreparation[CurrNumOperandsString]={}
	StreamConfigPreparation[CurrNumOperandsString][CurrVar]={}
	print "\n\t CurrNumOperands[CurrVar] "+str(CurrNumOperands[CurrVar])
	for CurrCombo in (StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo']):
		CurrStream=PrefixStream
		CurrStream+=','+str(CurrCombo)
		print "\n\t CurrCombo: "+str(CurrCombo)+' CurrStream: '+str(CurrStream)+' PrefixStream: '+str(PrefixStream)
		
		for CurrOperand in range(Operations['NumIntraOperandsNeeded'][CurrVar]):
			#print "\n\t CurrVar: "+str(CurrVar)+" CurrOperand "+str(CurrOperand)+" Operations['NumIntraOperandsNeeded'][CurrVar][CurrOperand]) "+str(StreamConfig['NumIntraOperandsRange'][CurrVar][CurrOperand])
			print "\n\t CurrVar: "+str(CurrVar)+" CurrOperandCheckOut: "+str(CurrOperand)+" StreamConfig['NumIntraOperandsRange'][CurrVar][CurrOperand] "+str(StreamConfig['NumIntraOperandsRange'][CurrVar][CurrOperand])+" --Duh-- "+str(Operations['NumIntraOperandsNeeded'][CurrVar])
			#StreamSoFar=CurrStream
			StreamConfigPreparation[CurrNumOperandsString][CurrVar][CurrOperand]={}
			for CurrIntraOperands in StreamConfig['NumIntraOperandsRange'][CurrVar][CurrOperand]:
				print "\n\t --CurrIntraOperands-- : "+str(CurrIntraOperands)
				StreamConfigPreparation[CurrNumOperandsString][CurrVar][CurrOperand][CurrIntraOperands]=[]
				for CurrOpCombo in (StrideConfigPrep[CurrNumOperandsString][CurrVar][CurrOperand][CurrIntraOperands]['OpCombo']):
					for Idx in range(CurrIntraOperands):
						if(Idx):
							CurrOpCombo+=','
							#print"\n\t Idx: "+str(Idx)+" CurrOpCombo: "+str(CurrOpCombo)
							
						PickDelta=random.randrange(StreamConfig['CurrNumDims'])
						Duh=int(StreamConfig['IntraOperandDelta']['Max'][CurrVar][PickDelta])
						PickIdx=random.randrange(StreamConfig['IntraOperandDelta']['Min'][CurrVar][PickDelta],StreamConfig['IntraOperandDelta']['Max'][CurrVar][PickDelta])
						if(random.randrange(2)==0):
							PickIdx=str(Operations['DimLookup'][PickDelta])+'-'+str(PickIdx)
						else:
							PickIdx=str(Operations['DimLookup'][PickDelta])+'+'+str(PickIdx)
						CurrOpCombo+=str(PickIdx)
						
					CurrOpCombo+=')'
					StreamConfigPreparation[CurrNumOperandsString][CurrVar][CurrOperand][CurrIntraOperands].append(CurrOpCombo)
					#StreamSoFar+=','+str(CurrOpCombo)
					#print "\n\t CurrOpCombo: "+str(CurrOpCombo)#+' StramConfigPrep... '+str(Stream)
			for CurrIntraOperands in StreamConfig['NumIntraOperandsRange'][CurrVar][CurrOperand]:
				print "\n\t CurrIntraOperands: "+str(CurrIntraOperands)
				for CurrIntraOperandCombo in (StreamConfigPreparation[CurrNumOperandsString][CurrVar][CurrOperand][CurrIntraOperands]):
					print "\n\t CurrIntraOperandCombo: "+str(CurrIntraOperandCombo)
			
			print "\n\t NumIntraOperands: "+str(StreamConfig['NumIntraOperandsRange'][CurrVar][CurrOperand])+" Operations['NumIntraOperandsNeeded'][CurrVar]: "+str(Operations['NumIntraOperandsNeeded'][CurrVar])
	
	#" ""
	print "\n\t Boo-Yeah!! "
	#sys.exit()
	return StreamConfigPreparation

	
########		
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
	Max['NumOperands']=[3,2,1,4]
	Min['NumOperands']=[2,1,1,1] #Min: Should be >= 1 
	Operations={}
	Operations['MainOperations']=['+','-','*','/']

	PermutationsFlag={}
	PermutationsFlag['MainOperations']=1 # 0: All operands, in an expression will be same. 1: Permutation of 
	PermutationsFlag['IntraOperations']= 1
	
	Operations['NumIntraOperandsNeeded']=[]
	for CurrVar in range(NumVars):
		CurrNumIntraOperandsNeeded=(Max['NumOperands'][CurrVar]-Min['NumOperands'][CurrVar]+1)
		Operations['NumIntraOperandsNeeded'].append(CurrNumIntraOperandsNeeded)
		
		
	# Max/Min['NumIntraOperands']= [ [<Variable-Num-Operands(Max-Min)>] * <#Vars> ] ; Ensure Max is less than or equal to Min. 
	Max['NumIntraOperands']=[[3,1],[1,3],[1],[1,2,2,4]]
	Min['NumIntraOperands']=[[2,1],[1,2],[1],[1,1,1,1]] #Min: Should be >= 1 
	Operations['IntraOperations']=['+','-','*','/']
	Operations['DimLookup']={0:'i',1:'j',2:'k'} # Should have as many dims
	
	# Max/Min['IntraOperandDelta'] = [ (Delta-Per-Dim) * <#Vars>] ; Ensure Max is less than or equal to Min. # Min should be positive when specified and Min and Max cannot be equal to zero, but can play around while chosing the actual indices.
	Max['IntraOperandDelta']=[(+1,+6,1) , ( +3,+3,+4) , ( +3,+3,+4) , ( +3,+3,+4) ]
	Min['IntraOperandDelta']=[ (0,+2,0) , ( +2,+1,+2) , ( +2,+1,+2) , ( +2,+1,+2) ]
	
	Max['Constant']=10
	Min['Constant']=2
	Operations['IntraOperandOperation']=['IntraOperandDelta','Constant']
 	#Operations['Operand']	
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

  	StreamConfig=PerStreamConfig(Max,Min,Operations)
  	StrideConfigPrep=PermuteforStrideConfig(StreamConfig,NumVars,Operations)
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
				StrideSet=[]
				RecursiveStrideGen(CurrStream,NumStreams,StartStream,NumStrides,CurrString,CurrPrefix,CurrPrefixPos,StrideSet)
		
				NumStreamString='#StreamDims '+str(NumStreams) # CAUTION: Should change this when NumVars > 1
				StrideString=''
				StrideName=''
				print "\n\t This is the length of StrideSet: "+str(len(StrideSet))
				
				# StreamConfig['NumOperandsSet'] 
				# StreamConfig['MainOperationsSet']
				# StreamConfig['NumIntraOperandsRange']
				# StreamConfig['IntraOperationsSet']
				# StreamConfig['ConstantsSet']
				
				StreamConfigPreparation={}
				for CurrStrideSet in StrideSet:
					
					ExtractStrideforStream=re.split(',',CurrStrideSet)
					if ExtractStrideforStream:
						CurrStrideString=''
						for idx,CurrStride in enumerate(ExtractStrideforStream):
							if(idx):
								CurrStrideString+='_'+str(CurrStride)
							else:
								CurrStrideString+=(CurrStride)
							print "\n\t CurrStride: "+str(CurrStride)
						StreamConfigPreparation[CurrStrideString]={}
					else:
						print "\n\t ERROR: Some error with extracting stride for the stream. "
					for CurrNumOperands in (StreamConfig['NumOperandsSet']):
						print "\n\t CurrNumOperands: "+str(CurrNumOperands) 
						#for CurrKey in (StreamConfig['MainOperationsSet']):
						#	print "\n\t CurrKey: "+str(CurrKey)+" len(StreamConfig['MainOperationsSet'][CurrKey]): "+str(len(StreamConfig['MainOperationsSet'][CurrKey]))
						for CurrVar in range(NumVars):
								if(len(ExtractStrideforStream)==NumStreams):
									for CurrNumStream in range(NumStreams):
										StrideOperationsPrefix='#strideoperations_var'+str(CurrVar)+'_'+str(CurrNumStream)
										StrideOperationsPrefix+=' <'+str(ExtractStrideforStream[CurrNumStream])+','+str(CurrNumOperands[CurrVar])
										print "\n\t -- StrideOperationsPrefix: "+str(StrideOperationsPrefix) 
										PrepareStreamConfig(StreamConfigPreparation[CurrStrideString],CurrVar,CurrNumOperands,StrideOperationsPrefix,StrideConfigPrep,StreamConfig,NumVars,Operations)
								
								else:
									print "\n\t ERROR: NumStreams "+str(NumStreams)+" is not equal to len(ExtractStrideforStream): "+str(len(ExtractStrideforStream))
									sys.exit()
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
	
