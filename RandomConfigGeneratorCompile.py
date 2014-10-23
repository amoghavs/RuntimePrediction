
import sys,subprocess,re,math,commands,time,copy,random

### WORKING ASSUMPTIONS:
# NumVars is constant

### ShortComing/Future-work: 
# 1. stream, stride is not permutable; Hence similar stream and stride is used for all variable. 
	# Current working solution: Split the "stride/stream" space amongst variable, instead of making each possible combination. 
	# Might work for now, but for generalizing the tool, will need this flexibility. Might not take too long to incorporate this!
	# Even the intraoperanddelta generated is common across all streams.
# 2. <>

def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output

def RemoveBraces(Input):
	temp=re.sub('^\s*\(*','',Input)
	Output=re.sub('\)*\s*$','',temp)
	#print "\n\t RemoveBraces--Input: "+str(Input)+" tmp: "+str(temp)+" Output "+str(Output)
	return Output
	

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
		print "\t Min['NumOperands'][CurrVar]: "+str(Min['NumOperands'][CurrVar])+"\t Max['NumOperands'][CurrVar] "+str(Max['NumOperands'][CurrVar])
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
	#OpComboKeys=[(0,'c'),(1,'d'),(2,'s')]
	OpComboKeys=Operations['OpComboKeys']
	NumOperandsSet.append(Temp)
	NeedToRepeat=0
	for CurrVar in range(0,NumVars):
		TempNumOperandsSet=[]
		for CurrSet in NumOperandsSet:
			for CurrNumOperand in RequiredNumOperandsRange[CurrVar]:
				Temp=copy.deepcopy(CurrSet)
				Temp.append(CurrNumOperand)
				TempNumOperandsSet.append(Temp)
				print "\n\t Temp: "+str(Temp)			
		NumOperandsSet=copy.deepcopy(TempNumOperandsSet)

	#OperandsCombo={}
	OpComboSet={}
	for CurrNumOperandSet in NumOperandsSet:
		for CurrNumOperand in CurrNumOperandSet: 
			print "\n\t CurrNumOperands: "+str(CurrNumOperand)
			NumOpComboMin=0
			NumOpComboMax=0
	  		for Idx,CurrOpCombo in (OpComboKeys):
	  			NumOpComboMin+=Min['OperandsCombo'][Idx][1]
	  			NumOpComboMax+=Max['OperandsCombo'][Idx][1]
			  	#print "\t Min: "+str(Min['OperandsCombo'][Idx])+" Max: "+str(Max['OperandsCombo'][Idx])	
			print "\t NumOpComboMin: "+str(NumOpComboMin)
			if(NumOpComboMin<=CurrNumOperand):
				print "\n\t NumOpComboMin: "+str(NumOpComboMin)+"  NumOpComboMax: "+str(NumOpComboMax)+" NumOperands: "+str(CurrNumOperand)
				CurrOpComboSet=[[]]
				TempSet=[]
				for Idx,CurrOpCombo in (OpComboKeys):
					TempSet=[]
					#TempSet=copy.deepcopy(CurrOpComboSet)
					#print "\t Key :"+str(CurrOpCombo)+" Idx "+str(Idx)+" CurrOpComboSet "+str(CurrOpComboSet)
					#print "\t Min['OperandsCombo'][Idx][1] : "+str(Min['OperandsCombo'][Idx][1])+" Max['OperandsCombo'][Idx][1]+1) "+str(Max['OperandsCombo'][Idx][1]+1)
					for CurrSet in CurrOpComboSet:
						for CurrNumOpCombo in range(Min['OperandsCombo'][Idx][1],Max['OperandsCombo'][Idx][1]+1):
							Temp=copy.deepcopy(CurrSet)
							Temp.append(CurrNumOpCombo)
							TempSet.append(Temp)
							print "\n\t CurrNumOpCombo: "+str(CurrNumOpCombo)+" TempSet: "+str(Temp)
					CurrOpComboSet=copy.deepcopy(TempSet)
					
				print "\n\t Before--Len(OperandsSet): "+str(len(CurrOpComboSet))
				PopIdx=[]		
				for OpComboSetIdx,CurrSet in enumerate(CurrOpComboSet):
					#print "\t CurrSet "+str(CurrSet)
					TotalNumOperands=0
					for Idx,CurrKey in (OpComboKeys):
						TotalNumOperands+=CurrSet[Idx]
					if(TotalNumOperands!=CurrNumOperand):
						#print "\t  CurrOpComboSet: "+str(CurrSet)+" CurrNumOperand: "+str(CurrNumOperand)+" TotalNumOperands: "+str(TotalNumOperands)+" OpComboSetIdx "+str(OpComboSetIdx)
						PopIdx.append(OpComboSetIdx)

				#print "\n\t Before pop! ";				for CurrSet in CurrOpComboSet: ;					print "\t CurrOpComboSet: "+str(CurrSet)
					
				PopIdx.sort(reverse=True)
				for LoopIdx in (PopIdx):
					print "\t LoopIdx: "+str(LoopIdx)
					
				for LoopIdx,CurrIdx in enumerate(PopIdx):
					if(len(CurrOpComboSet)>CurrIdx):
						CurrOpComboSet.pop(CurrIdx)
						
				print "\t After--Len(OperandsSet): "+str(len(CurrOpComboSet))
				for CurrSet in CurrOpComboSet:
					print "\t CurrOpComboSet: "+str(CurrSet)
				
				OpComboSet[CurrNumOperand]=(CurrOpComboSet)
			else:
				print "\n\t ERROR: Minimum number of operands combination is "+str(NumOpComboMin)+" more than that of number of operands "+str(CurrNumOperand)
		
	ExpectedNumOperandsinSet=1
	for i in range(NumVars):
		ExpectedNumOperandsinSet*=len(RequiredNumOperandsRange[i])
		print "\n\t ExpectedNumOperandsinSet: "+str(ExpectedNumOperandsinSet)+" len(RequiredNumOperandsRange[CurrVar]): "+str(len(RequiredNumOperandsRange[i]))
		
	print "\n\t len(NumOperandsSet): "+str(len(NumOperandsSet))+" ExpectedNumOperandsinSet: "+str(ExpectedNumOperandsinSet)		

	StreamConfig['NumOperandsSet']=NumOperandsSet
	StreamConfig['OperandsCombo']=OpComboSet

	MainOperationsSet={}
	StreamConfig['OpComboSet']={}
	if(Operations['PermutationsFlag']['MainOperations']):
		print "\n\t Will start permutating now for the sake of MainOperations "
		for CurrKey in Operations['Range']:
			CurrNumOperationsSet=[]
			Temp=[]
			CurrNumOperationsSet.append(Temp)
			TempCurrNumOperationsSet=[]
			for CurrNumOperations in range(1,MaxNumOperands):
			 for CurrOperationsSet in CurrNumOperationsSet:
 				for CurrOperations in Operations['Range'][CurrKey]: #'MainOperations']:
					Temp=[]
					Temp=copy.deepcopy(CurrOperationsSet)
					Temp.append(CurrOperations)
					TempCurrNumOperationsSet.append(Temp)
					#print "\n\t Temp: "+str(Temp)+" len(TempCurrNumOperationsSet): "+str(len(TempCurrNumOperationsSet))

			 CurrNumOperationsSet=copy.deepcopy(TempCurrNumOperationsSet)
			 TempCurrNumOperationsSet=[]
			 MainOperationsSet[CurrNumOperations]= CurrNumOperationsSet # CAUTION/WARNING: Assuming that the CurrNumOperations!=0 will access this dictionary, since that is an illegal case.
			 #print "\n\t CurrNumOperations: "+str(CurrNumOperations)+" len(CurrNumOperationsSet): "+str(len(CurrNumOperationsSet))
			StreamConfig['OpComboSet'][CurrKey]=MainOperationsSet
	else:
		print "\n\t Will NOT start permutating for the sake of MainOperations "	
		for CurrKey in Operations['Range']:
			StreamConfig['OpComboSet'][CurrKey]=Operations['Range'][CurrKey]		
		#MainOperationsSet['Default']=(Operations) #['MainOperations'])

	StreamConfig['MainOperationsSet']=MainOperationsSet

	StreamConfig['IntraOperandDelta']={}
	StreamConfig['IntraOperandDelta']['Max']=Max['IntraOperandDelta']
	StreamConfig['IntraOperandDelta']['Min']=Min['IntraOperandDelta']
		
	#StreamConfig['CurrNumDims']=Max['Dims'] 
	#print "\n\t StreamConfig['CurrNumDims']: "+str(StreamConfig['CurrNumDims'])+" is set to be Max['Dims'] "	
	print "\n "
	return	StreamConfig	

	
def PermuteforStrideConfig(StreamConfig,NumVars,Operations,OperandsCombo):

	StrideConfigPrep={}
	OpComboKeys=Operations['OpComboKeys']
	
	for CurrNumOperands in (StreamConfig['NumOperandsSet']):
		#print "\n\t AAHA CurrNumOperands: "+str(CurrNumOperands)+" len(StreamConfig['OperandsCombo'][CurrNumOperands]): "+str(len(StreamConfig['OperandsCombo'][CurrNumOperands]))
		CurrNumOperandsString=''
		for i in (CurrNumOperands):
			CurrNumOperandsString+=str(i)
		#print "\n\t CurrNumOperands: "+str(CurrNumOperands)+" string: "+str(CurrNumOperandsString)	
		StrideConfigPrep[CurrNumOperandsString]={}
		for CurrVar in range(NumVars):
			#+" Should use the key for MainOperationSet: "+str(CurrNumOperands[CurrVar]-1)
			StrideConfigPrep[CurrNumOperandsString][CurrVar]={}
			StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo']=[]
			StrideConfigPrep[CurrNumOperandsString][CurrVar]['OperandsCombo']=[]
			#print "\t --[CurrNumOperands[CurrVar] "+str(CurrNumOperands[CurrVar])
			print "\n\t AAHA CurrNumOperands: "+str(CurrNumOperands)+" len(StreamConfig['OperandsCombo'][CurrNumOperands]): "+str(len(StreamConfig['OperandsCombo'][CurrNumOperands[CurrVar]]))
			if(StreamConfig['OperandsCombo'][CurrNumOperands[CurrVar]]>1):
				MasterOperandsCombo=[]
				MasterOperationsCombo=[]
				for CurrSet in (StreamConfig['OperandsCombo'][CurrNumOperands[CurrVar]]):
					print "\n\t CurrSet: "+str(CurrSet)
					
					OpComboInit=0
					CurrOperandsCombo=''
					OperandsComboSet=[CurrOperandsCombo]
					TempOperandsComboSet=[]
					
					for CurrKey in OperandsCombo:
						print "\n\t CurrKey: "+str(CurrKey)
						
					for KeyIdx,CurrKey in OpComboKeys:
						TempOperandsComboSet=[]
						#print "\n\t OperandsCombo['DS'][CurrKey]: "+str(OperandsCombo['DS'][CurrKey])
						#print "\t CurrSet[KeyIdx] "+str(CurrSet[KeyIdx])+" len(OperandsComboSet): "+str(len(OperandsComboSet))
						for CurrOperandCombo in OperandsComboSet: #OperandsCombo['DS'][CurrKey]:
							if(CurrSet[KeyIdx]>0):
								if(Operations['PermutationsFlag']['OperandsComboDS'][CurrKey]=='l' ):
									for CurrDS in OperandsCombo['DS'][CurrKey]:
										TempCurrOperandCombo=CurrOperandCombo
										for i in range(CurrSet[KeyIdx]):
											if(TempCurrOperandCombo!=''):
												TempCurrOperandCombo+=','
											TempCurrOperandCombo+='('+str(CurrKey)+','+str(CurrDS)+')'
										TempOperandsComboSet.append(TempCurrOperandCombo)
								elif(Operations['PermutationsFlag']['OperandsComboDS'][CurrKey]=='r' ):
									LenNumDS=len(OperandsCombo['DS'][CurrKey])
									TempCurrOperandCombo=CurrOperandCombo
									for i in range(CurrSet[KeyIdx]):
										if(TempCurrOperandCombo!=''):
											TempCurrOperandCombo+=','									
										CurrDS=OperandsCombo['DS'][CurrKey][random.randrange(LenNumDS)]
										TempCurrOperandCombo+='('+str(CurrKey)+','+str(CurrDS)+')'
									TempOperandsComboSet.append(TempCurrOperandCombo)
												
								OperandsComboSet=copy.deepcopy(TempOperandsComboSet)
						
								#OperandsCombo+='('+str(CurrKey)+',d)'
					print "\n\t Operand combos: "			
					for Idx,CurrOperandCombo in enumerate(OperandsComboSet[:]):
						OperandsComboSet[Idx]='('+str(OperandsComboSet[Idx])+')'
						print "\t "+str(OperandsComboSet[Idx])
					
					StrideConfigPrep[CurrNumOperandsString][CurrVar]['OperandsCombo']=(OperandsComboSet)
					OperationsCombo=[]			
					for KeyIdx,CurrKey in OpComboKeys:
						#print "\n\t 1. Key: "+str(CurrKey)+" NumOperands "+str(CurrSet[KeyIdx])
						if(CurrSet[KeyIdx]>0):		
							if(OpComboInit==0):
								#for ComboIdx,CurrCombo in enumerate(StreamConfig['OpComboSet'][CurrKey][CurrSet[KeyIdx]]):
								OpCombo='('
								OperationsCombo.append(OpCombo)
								OpComboInit=1
							else:
								continue
							
					TempOperationsCombo=[]
					TotalNumOperands=0
					if(Operations['PermutationsFlag']['MainOperations']):
						for KeyIdx,CurrKey in OpComboKeys:
							TempOperationsCombo=[]
							#print "\n\t CurrKey: "+str(CurrKey)+" KeyIdx: "+str(KeyIdx)+" len(OperationsCombo) "+str(len(OperationsCombo))+" TotalNumOperands: "+str(TotalNumOperands)
							for CurrCombo in OperationsCombo:
								print "\t Len(OperationsCombo): "+str(len(OperationsCombo))
								TotalNumOperands+=CurrSet[KeyIdx]
								if(CurrSet[KeyIdx]>0):
									if(CurrSet[KeyIdx]==1):
										CurrOperationsSet=(Operations['Range'][CurrKey])
									else:
										if(KeyIdx=='s'):
											CurrOperationsSet=(StreamConfig['OpComboSet'][CurrKey][CurrSet[KeyIdx]-1])
										else:
											CurrOperationsSet=(StreamConfig['OpComboSet'][CurrKey][CurrSet[KeyIdx]])
									if(TotalNumOperands>1):
										for CurrKeyCombo in CurrOperationsSet:
											for OperationIdx,CurrOperation in enumerate(CurrKeyCombo):
												TempCurrCombo=CurrCombo
												if(TempCurrCombo!='('):
													TempCurrCombo+=','
												TempCurrCombo+=CurrOperation
											TempOperationsCombo.append(TempCurrCombo)
										OperationsCombo=copy.deepcopy(TempOperationsCombo)

						
						for Idx,CurrCombo in enumerate(OperationsCombo[:]):
							OperationsCombo[Idx]+=')'
						for CurrCombo in OperationsCombo:
							MasterOperationsCombo.append(CurrCombo)
						print "\n\t There yo go number of combinations: "+str(len(OperationsCombo))+" len(MasterOpsCombo): "+str(len(MasterOperationsCombo))+" MasterOperationsCombo[0] "+str(MasterOperationsCombo[0])
					else:
						OpCombo='('
						for KeyIdx,CurrKey in OpComboKeys:
							NumOperations=len(Operations['Range'][CurrKey])
							#print "\t NumOperations: "+str(NumOperations)+" CurrSet[KeyIdx]: "+str(CurrSet[KeyIdx])+" OpCombo "+str(OpCombo)+" CurrKey "+str(CurrKey)
							if(CurrKey=='s'):
								for i in range(CurrSet[KeyIdx]-1):
									TempOperation=Operations['Range'][CurrKey][random.randrange(NumOperations)]
									if(OpCombo!='('):
										OpCombo+=','
									OpCombo+=TempOperation
							
							else:
								for i in range(CurrSet[KeyIdx]):
									TempOperation=Operations['Range'][CurrKey][random.randrange(NumOperations)]
									if(OpCombo!='('):
										OpCombo+=','
									OpCombo+=TempOperation
						if(OpCombo=='('):
							OpCombo=''
						else:
							OpCombo+=')'
						print "\n\t OpCombo: "+str(OpCombo)
						
						MasterOperationsCombo.append(OpCombo)
				StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo']=(MasterOperationsCombo)	
										
			else:
				#print "\n\t CurrNumOperands[CurrVar] "+str(CurrNumOperands[CurrVar])+" does not need any operation"
				print "\n\t BooYeah! "
				StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo'].append('')
				print "\n\t BooYeah!! StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo'] "+str(StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo'])
					
	return StrideConfigPrep
	
########		
def main():

        Max={} #; Ensure Max is less than or equal to Min. 
        Min={}
        Max['Vars']=4
        Min['Vars']=4
        Max['Dims']=1
        Min['Dims']=1
        Max['NumStream']=1
        Min['NumStream']=1
        Max['Stride']=0 # ie., 2^4
        Min['Stride']=0 # ie., 2^0=1
        Alloc=[['d','d','d','d']]    
        Init=['index0','index0','index0','index0']
        DS=[['l','l','l','l']]#,'d','d','d']]    
        StrideScaling=[1,1,1,1]# 0 0 0 
	RandomAccess=[[1,1,1,1]] # 1,1,1]]
	PAPIInst=[0,0,0,0]
        LoopIterationBase=1;
        #LoopIterationsExponent=[[1,1.2,1.4],[1,1.5],[1,1.3],[1]];
        LoopIterationsExponent=[[1],[1],[1],[1]] # ,[1],[1],[1]];
	#LoopIterationsExponent=[[2.5]]# ,[1],[1],[1]];
	DifferentOperandsFlag=[0,0,0,0]#1,0,0 0: All "different" operand are same, 1: All "different" operand are different
	IndirectionFlag=[0,0,0,0]#1,0,1 : 1: Indirection, 0: No-indirection.

 	NumVars=(Max['Vars']-Min['Vars']+1)
 	if(Max['Vars']==Min['Vars']):	
 		NumVars=(Min['Vars'])
 	NumVarsLessOne=NumVars-1
 	
 	NumDims=(Max['Dims']-Min['Dims']+1)
 	if(Max['Dims']==Min['Dims']):
 		NumDims=Min['Dims']
 	NumDimsLessOne=NumDims-1
 	
 	print "\n\t WARNING: NumVars is assumed to be equal, you have been warned!! "

	# Max['NumOperands'] array has maximum number of operands for each variable ; Ensure Max is less than or equal to Min. 
   
	Min['MbyteSize']=10
	Max['MbyteSize']=11
        MbyteSize=13 # 2^28=256M = 2^20[1M] * 2^8 [256] ; # Int= 256M * 4B = 1GB. # Double= 256M * 8B= 2GB 
        MaxSize=2**MbyteSize
        HigherDimSizeIndex=8
        Dim0Size=2**(MbyteSize-HigherDimSizeIndex)
        HigherDimSize= MaxSize/ Dim0Size
        NumSizeIter=6
        SuccessiveOperandDiff=[8,8,8,8] #ie., Op1[i]+Op1[i+SuccessiveOperandDiff*1]+Op1[i+SuccessiveOperandDiff*2]+..+Op1[i+SuccessiveOperandDiff*n]
	Max['NumOperands']=[3] #,2,1,4]
	Min['NumOperands']=[1] #,1,1,1] #Min: Should be >= 1 

	Operations={}
	Operations['MainOperations']=['|'] #,'+','-','*','/']

	Operations['Range']={}
	Operations['Range']['c']=['|']#'+','-','*','/']	
	Operations['Range']['s']=['|']#'+','-','*','/']	
	Operations['Range']['d']=['|']#'+','-','*','/']	
	OpComboKeys=[(0,'c'),(1,'d'),(2,'s')]
	Operations['OpComboKeys']=OpComboKeys

	PermutationsFlag={}
	PermutationsFlag['MainOperations']=0 # 0: All operands, in an expression will be same. 1: Permutation of 
	
	Min['OperandsCombo']=[('c',0),('d',0),('s',1)]
	Max['OperandsCombo']=[('c',0),('d',0),('s',1)]
	
	OperandsCombo={} 
	OperandsCombo['DS']={}

	OperandsCombo['DS']['c']=['d','f']
	OperandsCombo['DS']['d']=['d','f']
	OperandsCombo['DS']['s']=[]
	
	for CurrDSSet in DS:
		for CurrDS in CurrDSSet:
			OperandsCombo['DS']['s'].append(CurrDS)
				
	PermutationsFlag={}
	PermutationsFlag['MainOperations']=0 # 0: All operands, in an expression will be same. 1: Permutation of 
	PermutationsFlag['OperandsComboDS']={}
	PermutationsFlag['OperandsComboDS']['c']= 'r' # r: Random, l: linear-combination(i.e, all of them one at a time)
	PermutationsFlag['OperandsComboDS']['d']= 'l'
	PermutationsFlag['OperandsComboDS']['s']= 'l'
	
	Operations['DimLookup']={0:'i',1:'j',2:'k'} # Should have as many dims
	
	# Max/Min['IntraOperandDelta'] = [ (Delta-Per-Dim) * <#Vars>] ; Ensure Max is less than or equal to Min. # Min should be positive when specified and Min and Max cannot be equal to zero, but can play around while chosing the actual indices.
	Max['IntraOperandDelta']=[(+1,+1,1),(+1,+1,1),(+1,+1,1),(+1,+1,1)]#, ( +3,+3,+4) , ( +3,+3,+4) , ( +3,+3,+4) ]
	Min['IntraOperandDelta']=[(0,0,0),(0,0,0),(0,0,0),(0,0,0) ] #, ( +2,+1,+2) , ( +2,+1,+2) , ( +2,+1,+2) ]
	
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
	
 	for CurrIterIdx in range(NumSizeIter):
 	 CurrIter=2**CurrIterIdx
 	 print "\n\t CurrIter: "+str(CurrIter)
	 for CurrMbyteSize in range(Min['MbyteSize'],Max['MbyteSize']):	
		MbyteSize=CurrMbyteSize#+1
		MaxSize=2**(MbyteSize)
		HigherDimSizeIndex=8
		Dim0Size=2**(MbyteSize-HigherDimSizeIndex)
		HigherDimSize= MaxSize/ Dim0Size	
		print "\n\t CurrIter: "+str(CurrIter)+" MbyteSize: "+str(MbyteSize)+" MaxSize: "+str(MaxSize)
		
		Min['NumOperands']=[]
		Max['NumOperands']=[]
		Temp=[]
		for CurrVar in range(NumVars):
			Temp.append(CurrIter)
		Min['NumOperands']=Temp
		Max['NumOperands']=Temp
			
		print "\t Min['NumOperands']: "+str(Min['NumOperands'])+"\t Max['NumOperands']: "+str(Max['NumOperands'])
		Min['OperandsCombo']=[('c',0),('d',0)]
		Max['OperandsCombo']=[('c',0),('d',0)]
		Min['OperandsCombo'].append(('s',CurrIter))
		Max['OperandsCombo'].append(('s',CurrIter))
		
		for CurrRandomAccess in RandomAccess:
			for Idx,CurrVar in enumerate(CurrRandomAccess):
				if(CurrVar):
					SimpleMinTuple=()
					SimpleMaxTuple=()
					SimpleMinTuple+=(0,)
					SimpleMaxTuple+=((CurrIter+1),)
					for i in range(NumDims-1):
						SimpleMinTuple+=(0,)
						SimpleMaxTuple+=(1,)
						print "\n\t SimpleMinTuple: "+str(SimpleMinTuple)+" SimpleMaxTuple: "+str(SimpleMaxTuple)
					print "\n\t SimpleMinTuple: "+str(SimpleMinTuple)+" SimpleMaxTuple: "+str(SimpleMaxTuple)
					Max['IntraOperandDelta'][Idx]=SimpleMaxTuple
					Min['IntraOperandDelta'][Idx]=SimpleMinTuple
					#sys.exit()
			
	 
		  	StreamConfig=PerStreamConfig(Max,Min,Operations)
		  	StrideConfigPrep=PermuteforStrideConfig(StreamConfig,NumVars,Operations,OperandsCombo)
	  	
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
		 		
		 		SuccessiveOperandsDiffString=''
		 		for i,CurrOpDiff in enumerate(SuccessiveOperandDiff):
		 			if(i):
		 				SuccessiveOperandsDiffString+=','+str(CurrOpDiff)
		 			else:
		 				SuccessiveOperandsDiffString+=str(CurrOpDiff)
		 				
				StideScalingString=''
				StrideScalingName=''
				for i,CurrStrideScaling in enumerate(StrideScaling):
					if(i):
						StrideScalingString+=','+str(CurrStrideScaling)
					else:
						StrideScalingString=str(CurrStrideScaling)
					StrideScalingName+=str(CurrStrideScaling) 		

				PAPIInstString=''
				PAPIInstName=''
				for i,CurrPAPIInstFlag in enumerate(PAPIInst):
					if(i):
						PAPIInstString+=','+str(CurrPAPIInstFlag)
					else:
						PAPIInstString=str(CurrPAPIInstFlag)
					PAPIInstName=str(CurrPAPIInstFlag)

				DifferentOperandsFlagString=''
				for i,CurrDifferentOperandsFlag	in enumerate(DifferentOperandsFlag):
					if(i):
						DifferentOperandsFlagString+=','+str(CurrDifferentOperandsFlag)
					else:
						DifferentOperandsFlagString=str(CurrDifferentOperandsFlag)
					#DifferentOperandsFlagName

				IndirectionFlagString=''
				for i,CurrIndirectionFlag	in enumerate(IndirectionFlag):
					if(i):
						IndirectionFlagString+=','+str(CurrIndirectionFlag)
					else:
						IndirectionFlagString=str(CurrIndirectionFlag)
		
		 		
		 		#MasterSWStats.write("\n\n\t ################################ \n\n");
		 		for NumDims in range(Min['Dims'],Max['Dims']+1):
		 			StreamConfig['CurrNumDims']=NumDims
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

						CurrString=''
						PrefixString=''
						StreamCollection=['']
				
						for CurrLength in range(1,NumStreams+1):
							print "\n\t CurrLength: "+str(CurrLength)
							TempStreamCollection=[]
					
							for CurrStreamCombi in StreamCollection:
								print "\n\t CurrStreamCombi: "+str(CurrStreamCombi)
								BreakCurrStreamCombi=re.split(',',str(CurrStreamCombi))
								print "\t BreakCurrStreamCombi: "+str(BreakCurrStreamCombi)
								if(CurrLength>1):
									if( (len(BreakCurrStreamCombi)==(CurrLength-1)) ):# and (len(BreakCurrStreamCombi)>1)):
										MinString=int(RemoveWhiteSpace(BreakCurrStreamCombi[len(BreakCurrStreamCombi)-1]))
										MinStringIdx=int(math.log(float(MinString),2))
										#print "\n\t MinString: "+str(MinString)+" MinStringIdx "+str(MinStringIdx)
										#for CurrStride in range(Min['Stride'],Max['Stride']+1):
										for CurrStride in range(MinStringIdx,Max['Stride']+1):
											ActualStride=(2**CurrStride) 
											NewStreamCombi=str(CurrStreamCombi)+','+str(ActualStride)
											TempStreamCollection.append(NewStreamCombi)
											#print "\n\t ActualStride: "+str(ActualStride)+"\t Newcombi: "+str(NewStreamCombi)
									else:
										print "\n\t len(BreakCurrStreamCombi): "+str(len(BreakCurrStreamCombi))+" BreakCurrStreamCombi "+str(BreakCurrStreamCombi)+" CurrLength: "+str(CurrLength)
										
								else:
												
									for CurrStride in range(Min['Stride'],Max['Stride']+1):
										ActualStride=(2**CurrStride) 
										TempStreamCollection.append(ActualStride)
										print "\n\t ActualStride: "+str(ActualStride)
						
					
							StreamCollection=[]
							print "\t TempStreamCollection: "+str(TempStreamCollection)
							StreamCollection=copy.deepcopy(TempStreamCollection)
						StrideSet=StreamCollection
						NumStreamString='#StreamDims '+str(NumStreams) # CAUTION: Should change this when NumVars > 1
						StrideString=''
						StrideName=''
						print "\n\t This is the length of StrideSet: "+str(len(StrideSet))
						#sys.exit()
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
					
							ExtractStrideforStream=re.split(',',str(CurrStrideSet))
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
										for CurrOperandCombo in (StrideConfigPrep[CurrNumOperandsString][CurrVar]['OperandsCombo']):
											print "\t CurrOperandCombo: "+str(CurrOperandCombo)
											BreakdownCurrOperandCombo=re.split('\),',CurrOperandCombo)
											for Idx,CurrBreakdown in enumerate(BreakdownCurrOperandCombo):
												BreakdownCurrOperandCombo[Idx]=RemoveBraces(CurrBreakdown)
												#print "\t CurrBreakdown: "+str(CurrBreakdown)+" BreakdownCurrOperandCombo[Idx] "+str(BreakdownCurrOperandCombo										
											for OpComboIdx,CurrCombo in enumerate(StrideConfigPrep[CurrNumOperandsString][CurrVar]['OpCombo']):
												CurrOpCombo=str(CurrOperandCombo)+';'+str(CurrCombo)+'; ('
												for Idx in range((CurrNumOperands[CurrVar])):
													if(Idx):
														CurrOpCombo+=','
													#print "\t CurrOperand: "+str(BreakdownCurrOperandCombo[Idx])
													if(BreakdownCurrOperandCombo[Idx][0]!='c'):
														PickIdx=random.randrange(StreamConfig['CurrNumDims'])
														PickDelta=random.randrange(StreamConfig['IntraOperandDelta']['Min'][CurrVar][PickIdx],StreamConfig['IntraOperandDelta']['Max'][CurrVar][PickIdx])
														if(0): #random.randrange(2)==0):
															OperandIdx=str(Operations['DimLookup'][PickIdx])+'-'+str(PickDelta)
														else:
															OperandIdx=str(Operations['DimLookup'][PickIdx])+'+'+str(PickDelta)	
														CurrOpCombo+=str(OperandIdx)
													else:
														Const=-0.0010
														if(BreakdownCurrOperandCombo[Idx][2]!=i):
															Const=random.uniform(Min['Constant'],Max['Constant'])
															Const=round(Const,4)
														else:
															Const=random.randrange(Min['Constant'],Max['Constant'])
														CurrOpCombo+='='+str(Const)
														#print "\n\t CurrOpCombo: "+str(CurrOpCombo)
														#sys.exit()

												"""CurrOpCombo=str(CurrCombo)+'; ('
												for Idx in range((CurrNumOperands[CurrVar])):
													if(Idx):
														CurrOpCombo+=','
												
													if(CurrRandomAccess[CurrVar]):
														PickIdx=0
														PickDelta=(Idx*SuccessiveOperandDiff[CurrVar])
														OperandIdx=str(Operations['DimLookup'][PickIdx])+'+'+str(PickDelta)
													else:
														PickIdx=random.randrange(StreamConfig['CurrNumDims'])
														PickDelta=random.randrange(StreamConfig['IntraOperandDelta']['Min'][CurrVar][PickIdx],StreamConfig['IntraOperandDelta']['Max'][CurrVar][PickIdx])
														if(random.randrange(2)==0):
															OperandIdx=str(Operations['DimLookup'][PickIdx])+'-'+str(PickDelta)
														else:
															OperandIdx=str(Operations['DimLookup'][PickIdx])+'+'+str(PickDelta)	
													CurrOpCombo+=str(OperandIdx)"""

													#print "\n\t CurrRandomAccess[CurrVar]: "+str(CurrRandomAccess[CurrVar])+" PickIdx "+str(PickIdx)+" PickDelta "+str(PickDelta)
												CurrOpCombo+=')'
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
											print "\t AllocString: "+str(AllocString)	
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
												f.write("\n#OpDiff "+str(SuccessiveOperandsDiffString))
												f.write("\n#datastructure "+str(DSString))
												f.write("\n#stridescaling "+str(StrideScalingString) )	
												f.write("\n#papiinst "+str(PAPIInstString) )
												f.write("\n#DifferentOperand "+str(DifferentOperandsFlagString))
												f.write("\n#Indirection "+str(IndirectionFlagString))
											
							
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
												sys.exit()


if __name__=="__main__":
	main() #sys.argv[1:])
	
