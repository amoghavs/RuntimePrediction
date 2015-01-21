#! /usr/bin/python
import sys,subprocess,re,math,commands,time,copy,random

### WORKING ASSUMPTIONS:
# NumVars is constant

### ShortComing/Future-work: 
# 1. stream, stride is not permutable; Hence similar stream and stride is used for all variable. 
	# Current working solution: Split the "stride/stream" space amongst variable, instead of making each possible combination. 
	# Might work for now, but for generalizing the tool, will need this flexibility. Might not take too long to incorporate this!
	# Even the intraoperanddelta generated is common across all streams.
# 2. <>

# 09/08/2014:  
# 1. Extension of multiple variables in one "stream" is done assuming script is used with var=1

def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output
	
def RemoveBraces(Input):
	temp=re.sub('^\s*\(*','',Input)
	Output=re.sub('\)*\s*$','',temp)
	#print "\n\t RemoveBraces--Input: "+str(Input)+" tmp: "+str(temp)+" Output "+str(Output)
	return Output
	
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
			
			if(NumOpComboMin<=CurrNumOperand):
				print "\n\t NumOpComboMin: "+str(NumOpComboMin)+"  NumOpComboMax: "+str(NumOpComboMax)+" NumOperands: "+str(CurrNumOperand)
				CurrOpComboSet=[[]]
				TempSet=[]
				for Idx,CurrOpCombo in (OpComboKeys):
					TempSet=[]
					#TempSet=copy.deepcopy(CurrOpComboSet)
					for CurrSet in CurrOpComboSet:
						for CurrNumOpCombo in range(Min['OperandsCombo'][Idx][1],Max['OperandsCombo'][Idx][1]+1):
							Temp=copy.deepcopy(CurrSet)
							Temp.append(CurrNumOpCombo)
							TempSet.append(Temp)
							#print "\n\t CurrNumOpCombo: "+str(CurrNumOpCombo)+" TempSet: "+str(Temp)
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
						print "\n\t OperandsCombo['DS'][CurrKey]: "+str(OperandsCombo['DS'][CurrKey])
						print "\t CurrSet[KeyIdx] "+str(CurrSet[KeyIdx])+" len(OperandsComboSet): "+str(len(OperandsComboSet))
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
						print "\n\t 1. Key: "+str(CurrKey)+" NumOperands "+str(CurrSet[KeyIdx])
								
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
	Max['Vars']=1
	Min['Vars']=1
	Max['Dims']=1
	Min['Dims']=1
	Max['NumStream']=1
	Min['NumStream']=1
	Max['Stride']=3 # ie., 2^4
	Min['Stride']=0 # ie., 2^0=1
	Alloc=[['d']] #,'d','d','d']]    
	Init=['index0+4']#,'index0','index0','index0']
	DS=[['i']]#,'d','d','d']]    
	StrideScaling=[1]# 0 0 0 
	RandomAccess=[[0]] # 1,1,1]]
	PAPIInst=[0] # 0,1,0
	#SpatWindow=[8,16,32];
	LoopIterationBase=100;
	#LoopIterationsExponent=[[1,1.2,1.4],[1,1.5],[1,1.3],[1]];
	LoopIterationsExponent=[[1]]# ,[1],[1],[1]];
	DifferentOperandsFlag=[0]#1,0,0 0: All "different" operand are same, 1: All "different" operand are different
	IndirectionFlag=[0]#1,0,1 : 1: Indirection, 0: No-indirection.

 	NumVars=(Max['Vars']-Min['Vars']+1)
 	if(Max['Vars']==Min['Vars']):	
 		NumVars=(Min['Vars'])
 	NumVarsLessOne=NumVars-1
 	print "\n\t WARNING: NumVars is assumed to be equal, you have been warned!! "

	# Max['NumOperands'] array has maximum number of operands for each variable ; Ensure Max is less than or equal to Min. 
   
	MbyteSize=25 # 2^28=256M = 2^20[1M] * 2^8 [256] ; # Int= 256M * 4B = 1GB. # Double= 256M * 8B= 2GB 
	MaxSize=2**MbyteSize
	HigherDimSizeIndex=8
	Dim0Size=2**(MbyteSize-HigherDimSizeIndex)
	HigherDimSize= MaxSize/ Dim0Size

	Min['Size']=22
	Max['Size']=23
	
	SuccessiveOperandDiff=[8] #ie., Op1[i]+Op1[i+SuccessiveOperandDiff*1]+Op1[i+SuccessiveOperandDiff*2]+..+Op1[i+SuccessiveOperandDiff*n]
	Max['NumOperands']=[3] #,2,1,4]
	Min['NumOperands']=[1] #,1,1,1] #Min: Should be >= 1 

	OpComboKeys=[(0,'c'),(1,'d'),(2,'s')]
	
	#OpComboKeys=['c','d','s'] #  'c': constant, 's': same, 'd': different	
	
	Min['OperandsCombo']=[('c',1),('s',1),('d',0)]
	Min['OperandsCombo']=[('c',1),('s',1),('d',1)]
	
	SameDSTuple=()

	OperandsCombo={} 
	OperandsCombo['DS']={}

	OperandsCombo['DS']['c']=['d']#,'f']
	OperandsCombo['DS']['d']=['d']#,'f']
	OperandsCombo['DS']['s']=[]
	
	for CurrDSSet in DS:
		for CurrDS in CurrDSSet:
			OperandsCombo['DS']['s'].append(CurrDS)
			

	Min['NumOperandsIdx']=1
	Max['NumOperandsIdx']=4

	Operations={}
	#Operations['MainOperations']=['+','-','*','/']
	Operations['Range']={}
	Operations['Range']['c']=['+']#,'-','*','/']	
	Operations['Range']['s']=['+','*','/']	
	Operations['Range']['d']=['+','*','/']	
	
	Operations['OpComboKeys']=OpComboKeys
	
	PermutationsFlag={}
	PermutationsFlag['MainOperations']=0 # 0: All operands, in an expression will be same. 1: Permutation of 
	PermutationsFlag['OperandsComboDS']={}
	PermutationsFlag['OperandsComboDS']['c']= 'r' # r: Random, l: linear-combination(i.e, all of them one at a time)
	PermutationsFlag['OperandsComboDS']['d']= 'l'
	PermutationsFlag['OperandsComboDS']['s']= 'l'
	
	Operations['DimLookup']={0:'i',1:'j',2:'k'} # Should have as many dims
	
	# Max/Min['IntraOperandDelta'] = [ (Delta-Per-Dim) * <#Vars>] ; Ensure Max is less than or equal to Min. # Min should be positive when specified and Min and Max cannot be equal to zero, but can play around while chosing the actual indices.
	Max['IntraOperandDelta']=[(+9,+9,9)]#, ( +3,+3,+4) , ( +3,+3,+4) , ( +3,+3,+4) ]
	Min['IntraOperandDelta']=[(1,+1,1) ] #, ( +2,+1,+2) , ( +2,+1,+2) , ( +2,+1,+2) ]
	
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

  	#StreamConfig=PerStreamConfig(Max,Min,Operations)
  	#StrideConfigPrep=PermuteforStrideConfig(StreamConfig,NumVars,Operations)
  	
  	InitExpression=''
  	for i,CurrVarInit in enumerate(Init):
  		if(i):
  			InitExpression+=','+str(CurrVarInit)
  		else:
  			InitExpression+=str(CurrVarInit)
	SuperSourceFile=open('SuperSourceFiles.log','w')	
   	for CurrSetIterations in OutputSet:	
	 for CurrNumOperandsIdx in range(Min['NumOperandsIdx'],Max['NumOperandsIdx']):
	  Min['NumOperands']=[]
	  Max['NumOperands']=[]
	  Min['NumOperands'].append((2**CurrNumOperandsIdx))
	  Max['NumOperands'].append((2**CurrNumOperandsIdx))
	  print "\n\t --NumOperands: Idx"+str(CurrNumOperandsIdx)+" Value "+str(2**CurrNumOperandsIdx)
	  
	  Min['OperandsCombo']=[('c',1),('s',1),('d',0)]
	  Min['OperandsCombo']=[('c',1),('s',1),('d',1)]
	
	  Min['OperandsCombo']=[]
	  Max['OperandsCombo']=[]	  
	  CurrNumOperands=Min['NumOperands'][0]
	  NumOperandsAllocated=0

	  Num={};Size={}
	  Min['StreamsInHierarchy']=Min['NumStream']
	  Max['StreamsInHierarchy']=Max['NumStream']
	  Num['StreamsInHierarchy']={}
	  Size['StreamsInHierarchy']={}
	  Num['StreamsInHierarchy'][1]=[1,0,0,0,0] # (RequestedLevel,L1,L2,L3,Mem)
	  Num['StreamsInHierarchy'][2]=[1,1,0,0,0] # (RequestedLevel,L1,L2,L3,Mem)
	  Num['StreamsInHierarchy'][3]=[2,0,1,0,0] # (RequestedLevel,L1,L2,L3,Mem)
	  Num['StreamsInHierarchy'][4]=[2,0,1,1,0]# (RequestedLevel,L1,L2,L3,Mem)
	  Num['StreamsInHierarchy'][5]=[2,0,2,1,0]
	  
	  Min['GlobalNestedLoops']=1
	  Max['GlobalNestedLoops']=2
	  
	  StreamwiseNestedLoopDistribution={}
	  StreamwiseNestedLoopDistribution[1]=[[1],[],[],[],[]] # [Choice-of-nested-loop-for-(RequestedLevel,L1,L2,L3,Mem)] # eg: For a given size [1,2,0,1] ==> 1 stream in NestedLoop-0(NL-0), 2 streams in NL-1, 0 streams in NL-2, 1 stream in NL-3.
	  StreamwiseNestedLoopDistribution[2]=[[1],[0,1],[],[],[]]
	  StreamwiseNestedLoopDistribution[3]=[[1,1],[],[1],[],[]]
	  StreamwiseNestedLoopDistribution[4]=[[1,1],[],[1],[0,1],[]]	
	  StreamwiseNestedLoopDistribution[5]=[[1,1],[],[1,1],[0,1],[]]
	  
	  if( (Min['GlobalNestedLoops']<1) and (Max['GlobalNestedLoops']<1) ):
	  	print "\t ERROR: Min['NestedLoop'] "+str(Min['GlobalNestedLoop'])+" is less than one! "
	  	sys.exit()
	  
	  for CurrNumStreams in range(Min['StreamsInHierarchy'],Max['StreamsInHierarchy']+1):
	  	if(not(CurrNumStreams in Num['StreamsInHierarchy'])):
	  		print "\t ERROR: Num['StreamsInHierarchy'] not presented for "+str(CurrNumStreams)+" number of streams!! "
	  		sys.exit()
	  PerStreamNestedLoopConfig={}
	  for CurrNumStreams in range(Min['StreamsInHierarchy'],Max['StreamsInHierarchy']+1):
	  	PerStreamNestedLoopConfig[CurrNumStreams]=[]
	  	for CurrNestedLoopNum in range(Min['GlobalNestedLoops'],Max['GlobalNestedLoops']+1):
		  	Tmp=[]
		  	for CurrMemLevel in range(len(Num['StreamsInHierarchy'][CurrNumStreams])):
	  			Tmp.append(0)
	  		PerStreamNestedLoopConfig[CurrNumStreams].append(Tmp)
	  		
		if(CurrNumStreams in StreamwiseNestedLoopDistribution):
			for MemLevelofStreamwiseNestedLoopDistribution,CurrMemLevelLoopDistribution in  enumerate(StreamwiseNestedLoopDistribution[CurrNumStreams]):
		  		if( (len(CurrMemLevelLoopDistribution)<=Max['GlobalNestedLoops'] ) and (len(CurrMemLevelLoopDistribution) >= 0 ) ) :
		  			NumStreamsRequested=0
		  			for NestedLoopNum,CurrMemLevelReqStreams in enumerate(CurrMemLevelLoopDistribution):
		  				PerStreamNestedLoopConfig[CurrNumStreams][NestedLoopNum][MemLevelofStreamwiseNestedLoopDistribution]+=CurrMemLevelReqStreams
		  				NumStreamsRequested+=CurrMemLevelReqStreams
		  				print "\t CurrNumStreams: "+str(CurrNumStreams)+"\t NestedLoopNum "+str(NestedLoopNum)+"\t MemLevelofStreamwiseNestedLoopDistribution "+str(MemLevelofStreamwiseNestedLoopDistribution)+"\t NumStreamsReq: "+str(CurrMemLevelReqStreams)
		  			if( not( (NumStreamsRequested==Num['StreamsInHierarchy'][CurrNumStreams][MemLevelofStreamwiseNestedLoopDistribution]) and ( (Num['StreamsInHierarchy'][CurrNumStreams][MemLevelofStreamwiseNestedLoopDistribution] >=0) and (Num['StreamsInHierarchy'][CurrNumStreams][MemLevelofStreamwiseNestedLoopDistribution]<=Max['NumStream']) ) ) ):
			  			print "\t ERROR: CurrNumStreams: "+str(CurrNumStreams)+"\tNumStreamsRequested "+str(NumStreamsRequested)+" but according to specs, it should be "+str(Num['StreamsInHierarchy'][CurrNumStreams][MemLevelofStreamwiseNestedLoopDistribution])
			  			
			  			sys.exit()
		  		else:
		  			print "\t ERROR: len(CurrMemLevelLoopDistribution)): "+str(len(CurrMemLevelLoopDistribution))+" is not legal. "
		  			print "\t Legal range-- Min >=0 , Max: "+str(Max['GlobalNestedLoops'])+" as mentioned in Max['GlobalNestedLoops'] "
		  			sys.exit()
		else:
		  	print "\t ERROR: StreamwiseNestedLoopDistribution is not available for "+str(CurrNumStreams)+" number of streams!! "
		TotalStreamsRequested=0
		for NLNumber,CurrNestedLoopConfig in enumerate(PerStreamNestedLoopConfig[CurrNumStreams]):
			for CurrMemLevelInNestedLoop in CurrNestedLoopConfig:
				TotalStreamsRequested+=CurrMemLevelInNestedLoop
		if(TotalStreamsRequested!=CurrNumStreams):
			print "\t ERROR: After calculating total num-streams at different memory levels across nested loops, the total requested is: "+str(TotalStreamsRequested)+" where as CurrNumStreams is "+str(CurrNumStreams)
			print "\t Please check the specifications of NestedLoop "
			sys.exit()
				
		for NLNumber,CurrNestedLoopConfig in enumerate(PerStreamNestedLoopConfig[CurrNumStreams]):
			print "\t $$$$#### CurrNumStreams: "+str(CurrNumStreams)+"\t NestedLoop number: "+str(NLNumber)+"\t "+str(CurrNestedLoopConfig)+"\t TotalStreamsRequested: "+str(TotalStreamsRequested)	  	
			
	  for OpComboIdx,CurrOpCombo in OpComboKeys:
	  	
	  	if(CurrNumOperands > 2):
	  		if(CurrOpCombo=='c'):
	  			NumConstantOperands=1
	  			TempTuple=('c',NumConstantOperands)
	  			TempTuple1=('c',NumConstantOperands)
	  			NumOperandsAllocated+=NumConstantOperands
	  			print "\n\t 11. NumOperands: "+str(CurrNumOperands)+" NumOperandsAllocated "+str(NumOperandsAllocated)	  
	  		elif(CurrOpCombo=='s'):
	  			NumSameOperands=(CurrNumOperands-NumOperandsAllocated)/2
	  			TempTuple=('s',NumSameOperands)
	  			TempTuple1=('s',(CurrNumOperands-NumOperandsAllocated))
				NumOperandsAllocated+=NumSameOperands
				print "\n\t 12. NumOperands: "+str(CurrNumOperands)+" NumOperandsAllocated "+str(NumOperandsAllocated)	  
	  		elif(CurrOpCombo=='d'):
	  			NumDiffOperands=(CurrNumOperands-NumOperandsAllocated)/3
	  			TempTuple=('d',NumDiffOperands)
	  			TempTuple1=('d',NumDiffOperands+1)
				NumOperandsAllocated+=NumDiffOperands
				print "\n\t 13. NumOperands: "+str(CurrNumOperands)+" NumOperandsAllocated "+str(NumOperandsAllocated)+" NumDiffOperands "+str(NumDiffOperands)	  
				
	  		Min['OperandsCombo'].append(TempTuple)
	  		Max['OperandsCombo'].append(TempTuple1)  	
	  	elif(CurrNumOperands==2):
	  		if(CurrOpCombo=='c'):
	  			NumConstantOperands=0
	  			TempTuple=('c',NumConstantOperands)
	  			TempTuple1=('c',NumConstantOperands)
	  			NumOperandsAllocated+=NumConstantOperands
	  		elif(CurrOpCombo=='s'):
	  			NumSameOperands=(CurrNumOperands/2)#-NumOperandsAllocated)/2
	  			TempTuple=('s',NumSameOperands)
	  			TempTuple1=('s',NumSameOperands)
				NumOperandsAllocated+=NumSameOperands
	  		elif(CurrOpCombo=='d'):
	  			NumDiffOperands=CurrNumOperands/2 #(NumOperands-NumOperandsAllocated)/2
	  			TempTuple=('d',NumDiffOperands)
	  			TempTuple1=('d',NumDiffOperands)
				NumOperandsAllocated+=NumDiffOperands
				
	  		Min['OperandsCombo'].append(TempTuple)
	  		Max['OperandsCombo'].append(TempTuple1)
	  		
	  	elif(CurrNumOperands==1):
	  		if(CurrOpCombo=='c'):
	  			NumConstantOperands=0
	  			TempTuple=('c',NumConstantOperands)
	  			TempTuple1=('c',NumConstantOperands)
	  			NumOperandsAllocated+=NumConstantOperands
	  		elif(CurrOpCombo=='s'):
	  			NumSameOperands=(CurrNumOperands)#-NumOperandsAllocated)/2
	  			TempTuple=('s',NumSameOperands)
	  			TempTuple1=('s',NumSameOperands)
				NumOperandsAllocated+=NumSameOperands
	  		elif(CurrOpCombo=='d'):
	  			NumDiffOperands=0 #(NumOperands-NumOperandsAllocated)/2
	  			TempTuple=('d',NumDiffOperands)
	  			TempTuple1=('d',NumDiffOperands)
				NumOperandsAllocated+=NumDiffOperands
				
	  		Min['OperandsCombo'].append(TempTuple)
	  		Max['OperandsCombo'].append(TempTuple1)
	  		
	  	
	  #for OpComboIdx,CurrOpCombo in enumerate(OpComboKeys):
	  #		print "\n\t Min: "+str(Min['OperandsCombo'][OpComboIdx])+" Max: "+str(Max['OperandsCombo'][OpComboIdx])		
	  	  
	  for CurrMbyteSize in range(Min['Size'],Max['Size']):
		print "\n\t CurrMbyteSize: "+str(CurrMbyteSize)
		MaxSize=2**CurrMbyteSize
		HigherDimSizeIndex=8
		Dim0Size=2**(CurrMbyteSize-HigherDimSizeIndex)
		HigherDimSize= MaxSize/ Dim0Size

		StreamConfig=PerStreamConfig(Max,Min,Operations)
		for CurrKey in OperandsCombo['DS']:
			print "\n\t CurrKey: "+str(CurrKey)
			for CurrDS in (OperandsCombo['DS'][CurrKey]):
				print "\t "+str(CurrDS)
		
		StrideConfigPrep=PermuteforStrideConfig(StreamConfig,NumVars,Operations,OperandsCombo)

   		print "\n\t CurrMbyteSize: "+str(CurrMbyteSize)+" Dim0Size "+str(Dim0Size)+" HigherDimSize "+str(HigherDimSize)
	   	IterationsString=''
	   	IterationsName=''
	   	for i,CurrVarIterations in enumerate(CurrSetIterations):
	   		if(i):
	   			IterationsString+=','+str(CurrVarIterations)
	   			IterationsName+='_'+str(CurrVarIterations)
	   		else:
	   			IterationsString+=str(CurrVarIterations)
	   			IterationsName+=str(CurrVarIterations)
 		
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
			for NumStreams in range(Min['NumStream'],Max['NumStream']+1):	
				LogNumStreams=int(math.ceil(math.log(NumStreams,2)))

				LocalMbyteSize=CurrMbyteSize-LogNumStreams
		                MaxSize=2**LocalMbyteSize

                		HigherDimSizeIndex=8
		                Dim0Size=2**(LocalMbyteSize-HigherDimSizeIndex)
		                HigherDimSize= MaxSize/ Dim0Size
		
				print "\n\t LogNumStreams: "+str(LogNumStreams)+" LocalMbyteSize "+str(LocalMbyteSize)+" CurrMbyteSize "+str(CurrMbyteSize)+" MaxSize "+str(MaxSize)
				Size['StreamsInHierarchy'][NumStreams]=[ Idx*0 for Idx in range(len(Num['StreamsInHierarchy'][NumStreams])) ] 
				for Idx in range(len(Num['StreamsInHierarchy'][NumStreams])):
					if(Idx==0):
						if(NumDims==1):
							Size['StreamsInHierarchy'][NumStreams][Idx]=MaxSize-1
						else:
							Size['StreamsInHierarchy'][NumStreams][Idx]=Dim0Size-1
					elif(Idx==1):
						Size['StreamsInHierarchy'][NumStreams][Idx]=2047
					elif(Idx==2):
						Size['StreamsInHierarchy'][NumStreams][Idx]=16383
					elif(Idx==3):
						Size['StreamsInHierarchy'][NumStreams][Idx]=65535
					elif(Idx==4):
						Size['StreamsInHierarchy'][NumStreams][Idx]=2097151
					
				IterationsString=''
                 		IterationsName=''
				LogNumStreams=0
 		                for i,CurrVarIterations in enumerate(CurrSetIterations):
 					CurrVarIterations*=(2**LogNumStreams)
 	                        	if(i):
         			        	IterationsString+=','+str(CurrVarIterations)
 	                                	IterationsName+='_'+str(CurrVarIterations)
         	                	else:
                 	                	IterationsString+=str(CurrVarIterations)
 	                	                IterationsName+=str(CurrVarIterations)
        			        print "\n\t CurrSetIterations: "+str(CurrSetIterations)+" IterationsString: "+str(IterationsString)
				
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
				
				StreamCollection=['']
				
				for CurrLength in range(1,NumStreams+1):
					print "\n\t CurrLength: "+str(CurrLength)
					TempStreamCollection=[]
					
					for CurrStreamCombi in StreamCollection:
						#print "\n\t CurrStreamCombi: "+str(CurrStreamCombi)
						BreakCurrStreamCombi=re.split(',',str(CurrStreamCombi))
						if(CurrLength>1):
							if(len(BreakCurrStreamCombi)==(CurrLength-1)):
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
					StreamCollection=copy.deepcopy(TempStreamCollection)
				StrideSet=StreamCollection
				print "\n\t This is the length of StrideSet: "+str(len(StrideSet))
				
				#for CurrStrideCombi in StrideSet:
				#	print "\t "+str(CurrStrideCombi)
		
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
				print "\n\t CurrNumOperands "+str(CurrNumOperandsIdx)
			        ActualCurrNumOperands=2**CurrNumOperandsIdx 	
				SourceFilesLogName='SourceFiles_Iters_'+str(IterationsName)+'_DS_'+str(DS[0][0])+'_Dims_'+str(NumDims)+'_Size_'+str(SizeName)+'_Stream_'+str(StreamName)+'_NumOperands_'+str(ActualCurrNumOperands)+'_StrideScaling_'+str(StrideScalingString)+'_PAPIInst_'+str(PAPIInstName)+'.log'
				print "\n\t SourceFilesLogName: "+str(SourceFilesLogName)
				
				SourceFilesLog=open(SourceFilesLogName,'w')
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
								
						#print "\n\t DCurrStrideString: "+str(CurrStrideString)
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
											#print "\t CurrBreakdown: "+str(CurrBreakdown)+" BreakdownCurrOperandCombo[Idx] "+str(BreakdownCurrOperandCombo[Idx])+" CurrNumOperands[CurrVar]: "+str(CurrNumOperands[CurrVar])+" "
										#sys.exit()
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
											CurrOpCombo+=')'
											#print "\n\t CurrCombo: "+str(CurrCombo)+" CurrOpCombo "+str(CurrOpCombo)
											OpComboSet.append(CurrOpCombo)
											#if(OpComboIdx>1):
											#	sys.exit()
## $$$$$$$$$$$$$$$$$							
	
									StrideOperationsPrefix=[]
									OverflowString=[]
									for NLNumber,CurrNestedLoopConfig in enumerate(PerStreamNestedLoopConfig[NumStreams]):
										for CurrMemLevel,Idx in enumerate(CurrNestedLoopConfig):
											if(Idx>0):
												TempOverflowString=str(NLNumber)+';'+str(Size['StreamsInHierarchy'][NumStreams][CurrMemLevel])
												print "\t NLNumber "+str(NLNumber)+"\t MemLevel: "+str(CurrMemLevel)+"\t OverflowTemplate: "+str(TempOverflowString)
												OverflowString.append(TempOverflowString)
								 	for CurrStreamIdx,CurrStreamConfig in enumerate(OverflowString):
										print "\t Idx: "+str(CurrStreamIdx)+" CurrStreamConfig "+str(CurrStreamConfig)			
									for CurrNumStream in range(NumStreams):
										Temp='#strideoperations_var'+str(CurrVar)+'_'+str(CurrNumStream)
										Temp+=' <'+str(ExtractStrideforStream[CurrNumStream])+';'+str(CurrNumOperands[CurrVar])+';'+str(OverflowString[CurrNumStream])
										StrideOperationsPrefix.append(Temp)
										print "\t OverflowString[CurrNumStream] "+str(OverflowString[CurrNumStream])+"\t NumStreams "+str(NumStreams)
											#print "\n\t -- StrideOperationsPrefix: "+str(Temp)+' CurrNumStream: '+str(CurrNumStream)

									for CurrOpCombo in OpComboSet:
										Temp=[]
									#print "\n\t CurrOpCombo: "+str(CurrOpCombo)#+' AccumCount: '+str(AccumCount)
										for CurrNumStream in range(NumStreams):	
											Temp1=str(StrideOperationsPrefix[CurrNumStream])+' ; '+str(CurrOpCombo)+'>'
											Temp.append(Temp1)
										StreamConfigCollection[CurrStrideString][CurrNumOperandsString][CurrVar].append(Temp)	
										#print "\n\t -- StrideOperationsPrefix: "+str(StrideOperationsPrefix)+' CurrNumStream: '+str(CurrNumStream)"""
								
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
						#print "\n\t AccumulationCount: "+str(AccumulationCount)+' * (NumOperands) '+str(len(StreamConfigCollection[CurrStrideString]))+' * '+str(len(CurrStrideStringSet))
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
										f.write("\n#OpDiff "+str(SuccessiveOperandsDiffString))
										f.write("\n#datastructure "+str(DSString))
										f.write("\n#stridescaling "+str(StrideScalingString) )	
										f.write("\n#papiinst "+str(PAPIInstString) )
										f.write("\n#DifferentOperand "+str(DifferentOperandsFlagString))
										f.write("\n#Indirection "+str(IndirectionFlagString))

										for CurrCombi in CurrCombiAccumulation:
											#print "\n\t CurrCombi: "+str(CurrCombi)
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
												CMDCompileFile='mpicc -g -O3 '+str(SRCFileName)+' /usr/local/lib/libpapi.so -o '+str(FileName.group(1))
												print "\n\t CMDCompileFile: "+str(CMDCompileFile)
												commands.getoutput(CMDCompileFile)
												SourceFilesLog.write("\n\t "+str(SRCFileName))
												SuperSourceFile.write("\n\t "+str(SRCFileName))		
										#sys.exit()		
				#sys.exit()
				SourceFilesLog.write("\n\n")
				SourceFilesLog.close() #"""
									
						#sys.exit()
						



if __name__=="__main__":
	main() #sys.argv[1:])
	
