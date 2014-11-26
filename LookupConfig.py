# NOTE: Just a quick look at various parameters that can be configured. NOT a python script! 

        Max={} #; Ensure Max is less than or equal to Min. 
        Min={}
        Max['Vars']=4
        Min['Vars']=4
        Max['Dims']=3
        Min['Dims']=3
        Max['NumStream']=2
        Min['NumStream']=2
        Max['Stride']=3 # ie., 2^4
        Min['Stride']=0 # ie., 2^0=1
        Alloc=[['d','d','d','d']]    
        Init=['index0','index0','index0','index0']
        DS=[['d','d','d','d']]    
        #SpatWindow=[8,16,32];
        LoopIterationBase=10;
        #LoopIterationsExponent=[[1,1.2,1.4],[1,1.5],[1,1.3],[1]];
        LoopIterationsExponent=[[1],[1],[1],[1]];
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

	Max['NumOperands']=[4,2,1,4]
	Min['NumOperands']=[3,1,1,1] #Min: Should be >= 1 
	Operations={}
	Operations['MainOperations']=['+','-','*','/']

	PermutationsFlag={}
	PermutationsFlag['MainOperations']=1 # 0: All operands, in an expression will be same. 1: Permutation of 
	PermutationsFlag['IntraOperations']= 1
	
	Operations['DimLookup']={0:'i',1:'j',2:'k'} # Should have as many dims
	
	# Max/Min['IntraOperandDelta'] = [ (Delta-Per-Dim) * <#Vars>] ; Ensure Max is less than or equal to Min. # Min should be positive when specified and Min and Max cannot be equal to zero, but can play around while chosing the actual indices.
	Max['IntraOperandDelta']=[(+1,+6,1) , ( +3,+3,+4) , ( +3,+3,+4) , ( +3,+3,+4) ]
	Min['IntraOperandDelta']=[ (0,+2,0) , ( +2,+1,+2) , ( +2,+1,+2) , ( +2,+1,+2) ]
	
	Max['Constant']=10
	Min['Constant']=2
	Operations['IntraOperandOperation']=['IntraOperandDelta','Constant']
