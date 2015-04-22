#! /usr/bin/python

#Prev-Src: brahma:/home/amoghavs/Projects/PowerModeling/PoCModeling/CheckScript_Kernels_Run2.5/BenchmarksResultLogging.py
import sys,getopt,subprocess,re,math,commands,time,copy,random
from operator import itemgetter, attrgetter

def usage():
	print "\n\t Usage: BenchmarksResultsLogging.py -l/--source file with all the source file that needs to be executed and logged -p <num-of-procs> -c CacheSimulationFlag <0/1> -r ReuseDistance -s SpatialDistanceFlag  -e EnergyMeasureFlag <0/1> -n Number of Counters -a Number of runs for averaging runtime. -p Number of Processors -d \n\t\t -s: spatial distances -v/--vector <Vector-extract-from-PSAPP> -t/--vectorparamstart <vectorparamstart> -u/--numvectorparams <numvectorparams> .\n\t\t -o <Output-file-name> \n "
	sys.exit()

def fopen(FileName,options=''):
	if(options==''):
		try:
			FileHandle=open(FileName)
			return FileHandle
		except IOError:
		 	print 'cannot open', FileName
			return 'IOERROR'
	else:
		try:
			FileHandle=open(FileName,options)
			return FileHandle
		except IOError:
			print 'cannot open', FileName
			return 'IOERROR'

	
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
	
def Compile(Input,Options=''):
	CompileCmd='mpicc -g '+str(Input)+'.c '+str(Options)+' -o '+str(Input)
	print "\t CompileCmd: "+str(CompileCmd)
	CompileOutput=commands.getoutput(CompileCmd)
	if(CompileOutput!=''):
		print "\n\t ERROR: CompileOutput --"+str(CompileOutput)
		sys.exit()
		
def ExtractFilesAndFreqs(LsOutput):
	AllFreqs={}
	StringSoFar=''
	Files=[]
	#print "\t LsOutput: "+str(LsOutput)
	for CurrChar in LsOutput:
		if(CurrChar=='\n'):
			#print "\t StringSoFar: "+str(StringSoFar)
			Files.append(RemoveWhiteSpace(StringSoFar))
			StringSoFar=''
		else:
			StringSoFar+=str(CurrChar)
	Files.append(StringSoFar)

	for CurrFile in Files:
		Breakdown=re.split('\.',CurrFile)
		Freq=Breakdown[len(Breakdown)-2]
		print "\t Freq: {0:s} All: {1:s}".format(Freq,str(Breakdown))
		#sys.exit()
		#ExtractFreq=re.match('.*StrideBenchmarks.*\.(.*)\.',CurrFile)
		#if(ExtractFreq):
		#Freq=int(ExtractFreq.group(1))
		if(not(Freq in AllFreqs)):
			#print "\t Freq: "+str(Freq)	
			AllFreqs[Freq]=[]
			AllFreqs[Freq].append(CurrFile)
		else:
			AllFreqs[Freq].append(CurrFile)
	
	return AllFreqs
	
def SortBBs(SrcFileName,OutputFileName,PercentThreshold):
 InFile=fopen(SrcFileName)
 if(InFile!='IOERROR'):
	BBFile=InFile.readlines()
	InFile.close()
	
	print "\n\t Num of lines: "+str(len(BBFile))
	BBIdx=0
	PercentIdx=1
	CollectTopLoopInfo=[]
	Meh=0
	for LineNum,ExtractLine in enumerate(BBFile):
		#print "\n\t CurrLine: "+str(CurrLine)
		CurrLine=ExtractLine
		CurrLine=RemoveWhiteSpace(ExtractLine)
		TopLoopCheck=ExtractLine.split('\t')
		Fields=CurrLine.split('\t')
		if(len(Fields)<5): # This used to be >5 in labyrinth
			Meh+=1
			#print "\n\t --LineNum: "+str(LineNum)+" #Fields "+str(len(Fields))+" #TopLoopCheck "+str(len(TopLoopCheck))
			#print "\n\t CurrLine: "+str(CurrLine)
		else:
			#print " #Fields "+str(len(Fields))+" #TopLoopCheck "+str(len(TopLoopCheck))+"\t LineNum "+str(LineNum) 
			#print "\t CurrLine: "+str(CurrLine)
			if(len(TopLoopCheck)==9): # This used to be 6 in labyrinth's version.
				#print " #Fields "+str(len(Fields))+" #TopLoopCheck "+str(len(TopLoopCheck))
				#print "\t Fields: "+str(Fields)
				TmpBB=Fields[BBIdx].split(':')
				BB=''
				Percent=RemoveWhiteSpace(Fields[PercentIdx])
				if(len(TmpBB)==2):
					BB=TmpBB[1]
				print "\n\t Percent: "+str(float(Percent))
				CollectTopLoopInfo.append( (BB,float(Percent)) )

	CollectTopLoopInfo=sorted(CollectTopLoopInfo, key=itemgetter(PercentIdx),reverse=True)
	#for Idx,CurrBBTuple in enumerate(CollectTopLoopInfo):	
	#	print "\n\t BB: "+str(CurrBBTuple[BBIdx])+" Percent: "+str(CurrBBTuple[PercentIdx])

	OutputFile=fopen(OutputFileName,'w')
	SortedBBsCollection=[]
	for Idx,CurrBBTuple in enumerate(CollectTopLoopInfo):
		if(CurrBBTuple[PercentIdx] > PercentThreshold):
			OutputFile.write(str(CurrBBTuple[BBIdx])+"\n")
			print("\n\t "+str(CurrBBTuple[PercentIdx]))
			SortedBBsCollection.append(CurrBBTuple[BBIdx])

	return SortedBBsCollection
 else:
	Meh=[]
	return Meh	

def ReplaceNumLoops(Input,ReplaceIter):
	ReplaceIter="perl -i -pe 's/NumLoops_Var0\ \=/NumLoops_Var0\ \= "+str(ReplaceIter)+"\;\/\//g' "+str(Input)+'.c'
	print "\t ReplaceIter: "+str(ReplaceIter)
	ReplaceIterOutput=commands.getoutput(ReplaceIter)
	if(ReplaceIterOutput!=''):
		print "\t WARNING: ReplaceIterOutput "+str(ReplaceIterOutput)
		print "\t WARNING is currently handeled as ERROR "
		sys.exit()

def ObtainTopLoops(FileName,NumofProcs,PercentThreshold=1.0):
	CMDPebil='pebil --typ jbb --app '+str(FileName)
        commands.getoutput(CMDPebil)
	CMDJbb='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+'.jbbinst'
	print "\t JbbOutput: "+str(commands.getoutput(CMDJbb))

	jRunProcess='jRunTool --application '+str(FileName)+' --dataset standard --cpu_count '+str(NumofProcs)+' --processed_dir processed --scratch_dir scratch --raw_pmactrace `pwd` --process > Duh.log '
	print "\n\t -- "+str(jRunProcess)
	commands.getoutput(jRunProcess)
	jRunReport='jRunTool --application '+str(FileName)+' --dataset standard --cpu_count '+str(NumofProcs)+' --processed_dir processed --scratch_dir scratch --raw_pmactrace `pwd` --report loopview > Duh1.log '
	print "\n\t -- "+str(jRunReport)
	commands.getoutput(jRunReport)
	LoopViewStr=str(NumofProcs)
	LoopViewStrNotReady=1
	while LoopViewStrNotReady:
		StrLen=len(LoopViewStr)
		#print "\n\t Str-len: "+str(StrLen)
		if(StrLen<4):
			LoopViewStr='0'+str(LoopViewStr)
		elif(StrLen==4):
			LoopViewStrNotReady=0
		else:
			print "ERROR: Some logical must have happened! "
			sys.exit()
	LoopViewStr=str(FileName)+'_standard_'+str(LoopViewStr)+'.LoopView'
	SortedBBsList='BBsSorted_'+str(FileName)+'.log'
	SortedBBsCollection=SortBBs('processed/'+str(LoopViewStr),SortedBBsList,PercentThreshold)
	jRunReport='jRunTool --application '+str(FileName)+' --dataset standard --cpu_count '+str(NumofProcs)+' --processed_dir processed --scratch_dir scratch --raw_pmactrace `pwd` --sysid 130 --functions default --loops default --report blockvector  > Duh2.log '
	print "\t jRunReport: "+str(jRunReport)
	commands.getoutput(jRunReport)
	return (SortedBBsCollection,SortedBBsList)	
	
def WriteStats(CurrStatsFile,FileNameCollection,EnviVars,AverageRuntimeCollection,PowerValueCollection,RaplPowerValueCollection,
	       PredictionVectorParamsCollection,ItersCollection,EnergySim,EnergyMeasure,VectorExtract,PowerParams,PowerParamsInOrder,
	       VectorParamStart,NumVectorParams,AverageCalc,CounterResultsCollection,PapiCacheSim,
	       AverageRuntimeNontolerantProcsCollection,AverageRuntimeNontolerantIterCollection):
	if(CurrStatsFile):
		CurrStatsFile.write("\n\t Average run times: ") ; 
		if(AverageCalc==0):
			CurrStatsFile.write("\n\t\t Exe: \t\t\t\t Average runtime \t ProcToleranceFlag \t IterToleranceFlag ")
			for CurrFile in FileNameCollection:
				if(CurrFile in AverageRuntimeCollection):
					CurrStatsFile.write("\n\t "+str(CurrFile)+"\t\t "+str(AverageRuntimeCollection[CurrFile])+"\t "+str(AverageRuntimeNontolerantProcsCollection[CurrFile])+"\t "+str(AverageRuntimeNontolerantIterCollection[CurrFile]))
		else:
			CurrStatsFile.write("\n\t\t Exe: \t\t\t\t Freq\t\t Iters\t\t  Average runtime  \t ProcToleranceFlag \t IterToleranceFlag ")
			for CurrFile in FileNameCollection:
				if((CurrFile in AverageRuntimeCollection) and (CurrFile in ItersCollection) ):
					for CurrFreq in (AverageRuntimeCollection[CurrFile]):
						CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrFreq)+"\t "+str(ItersCollection[CurrFile])+"\t "+str(AverageRuntimeCollection[CurrFile][CurrFreq])+"\t "+str(AverageRuntimeNontolerantProcsCollection[CurrFile])+"\t "+str(AverageRuntimeNontolerantIterCollection[CurrFile]) )
		if(PapiCacheSim>0):
			CurrStatsFile.write("\n\t PapiCacheSim result: ");
			CurrStatsFile.write("\n\t\t Exe: \t\t\t\t Average values of counters ")
			for CurrFile in FileNameCollection:
				if(CurrFile in CounterResultsCollection):
					CurrStatsFile.write("\n\t "+str(CurrFile))
					for CurrCounterAverageVal in CounterResultsCollection[CurrFile]:
						CurrStatsFile.write("\t"+str(CurrCounterAverageVal))
		if(not(EnergySim==0)):
			CurrStatsFile.write("\n\n\t Energy probes value: ")
			CurrStatsFile.write("\n\t Counters : ")
			for CurrCounter in EnviVars:
				CurrStatsFile.write("\t "+str(CurrCounter))
			if(EnergyMeasure==0):	
				CurrStatsFile.write("\n\t\t Exe: \t\t\t\t Power from each counter ")			   				
				for CurrFile in FileNameCollection:
					if(CurrFile in PowerValueCollection):
						CurrStatsFile.write("\n\t "+str(CurrFile))
					        for CurrPower in (PowerValueCollection[CurrFile]):
					                 CurrStatsFile.write("\t "+str(round(float(CurrPower),4)))
					else:
						CurrStatsFile.write("\n\t "+str(CurrFile)+"\t  error extracting power!!")
			elif(EnergyMeasure==1):
				CurrStatsFile.write("\n\t\t Exe: \t\t\t\t BBID: \t\t Power from each counter ")
				for CurrFile in FileNameCollection:
				 #CurrStatsFile.write("\n")
				 if(CurrFile in PowerValueCollection):
					 for CurrBB in (PowerValueCollection[CurrFile]):
						CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB))
						for CurrPower in (PowerValueCollection[CurrFile][CurrBB]):
							CurrStatsFile.write("\t "+str(round(float(CurrPower),4)))
				 else:
					CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB)+"\t error extracting power!!")			
			elif(EnergyMeasure==2):
				
				CurrStatsFile.write("\n\t\t Exe: \t\t\t\t Freq \t\t Iters \t\t Power from each counter ")	
				for CurrFile in FileNameCollection:
				 if(CurrFile in PowerValueCollection):
				 	for CurrFreq in (PowerValueCollection[CurrFile]):
				 		if( ( CurrFreq in PowerValueCollection[CurrFile] ) and (CurrFile in ItersCollection) ):
					 		CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrFreq)+"\t "+str(ItersCollection[CurrFile])+"\t "+str(PowerValueCollection[CurrFile][CurrFreq]))
						else:
							CurrStatsFile.write("\n\t "+str(CurrFile)+" error with power measurements!!")
				PowerParamsStr=''
				for CurrParam in PowerParamsInOrder:
					PowerParamsStr+='\t'+str(CurrParam)
				CurrStatsFile.write("\n\n\n\t\t Exe: \t\t\t\t Freq \t\t Iters \t\t "+str(PowerParamsStr))	
				for CurrFile in FileNameCollection:
				 if(CurrFile in RaplPowerValueCollection):
				 	for CurrFreq in (RaplPowerValueCollection[CurrFile]):
				 		if( (CurrFreq in RaplPowerValueCollection[CurrFile]) and (CurrFile in ItersCollection) ):
					 		CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrFreq)+"\t "+str(ItersCollection[CurrFile])+"\t "+str(RaplPowerValueCollection[CurrFile][CurrFreq]))				
						else:
							 CurrStatsFile.write("\n\t "+str(CurrFile)+" error with RAPL power measurements!!")
										
		if(not(VectorExtract==0)):
			CurrStatsFile.write("\n\n\n\t\t Exe: \t\t\t\t BBID: \t\t ParamStart: "+str(VectorParamStart)+" Num-params: "+str(NumVectorParams))
			for CurrFile in FileNameCollection:
				#CurrStatsFile.write("\n\t "+str(CurrFile))
				if(CurrFile in PredictionVectorParamsCollection):
					for CurrBBData  in (PredictionVectorParamsCollection[CurrFile]):
						CurrStatsFile.write("\n\t "+str(CurrFile))
						for CurrParam in CurrBBData:
							CurrStatsFile.write("\t "+str(CurrParam))
				else:
					print "\n\t Error with extracting param info! "
		#CurrStatsFile.write("\n\n")
		#CurrStatsFile.close()
	
def EmailMsg(EmailID,Msg,Subject='Update!!'):
 for CurrEmailID in EmailID:
	EmailCmd=' echo \" '+str(Msg)+' " | mail -s \" '+str(Subject)+' \" '+str(CurrEmailID)
	EmailOutput=commands.getoutput(EmailCmd)
	print "\t Cmd: "+str(EmailCmd)
	print "\t Output: "+str(EmailOutput)


def ExtractRuntime(RunOutputFileList,NumProcs,FileName,AverageRuntimeNontolerantProcsCollection,AverageRuntimeNontolerantIterCollection):
	ItersTime=[]
	AverageRuntimeNontolerantProcsCollection[FileName]=0
	for IterIdx,CurrRunOutputFile in enumerate(RunOutputFileList):
		RunOutput=fopen(CurrRunOutputFile)
		print "\t IterIdx: "+str(IterIdx)+" CurrRunOutputFile "+str(CurrRunOutputFile)+" len(RunOutputFileList): "+str(len(RunOutputFileList))
		IterRuntime=[]
		if(RunOutput!='IOERROR'):	
			for CurrLine in RunOutput:
		        #print "\n\t CurrLine: "+str(CurrLine)
				CheckTime=re.match('^\s*.*time.*',CurrLine)
				#print "\t TopCurrLine: {0:s} ".format(CurrLine)
				#CheckTime=re.match('\s*Run\-time',CurrLine)
				if CheckTime:
					#print "\n\t CurrLine: "+str(CurrLine)
					#CheckRuntime=re.match('\s*.*app.*time\:\s*(\d+)*\.(\d+)*',CurrLine) # 
					CheckRuntime=re.match('\s*.*time(.*)',CurrLine)
					#CheckRuntime=re.match('\s*.*Run\-time.*\:\s*(\d+)*\.(\d+)*',CurrLine) 
					#IterRuntime=[]
					FoundAppTime=False
					print "\t ------***CurrLine: {0:s} ".format(CurrLine)
					if CheckRuntime:
						FoundAppTime=True
					else:
						print "\t INFO: IterIdx: "+str(IterIdx)+" cannot find runtime!! "
						RunOutput.close()
						break
					if CheckRuntime:
						#BreakdownTimeForProcs=re.split('\ \ ',CheckRuntime.group(1))
						BreakdownTimeForProcs=re.split(':',CurrLine)
						print "\t CurrLine: "+str(CurrLine)+"\t Breakdown "+str(BreakdownTimeForProcs)
						if(len(BreakdownTimeForProcs)>(NumProcs)):
							print "\t BreakdownTimeForProcs: "+str(BreakdownTimeForProcs)
							for CurrChunk in (BreakdownTimeForProcs):
								ExtractTime=re.match('\s*(\d+)*\.(\d+)*',CurrChunk)
								if (ExtractTime):
									Temp=str(ExtractTime.group(1))+'.'+str(ExtractTime.group(2))
									#print "\t Runtime-- "+str(Temp)
									IterRuntime.append(float(Temp))
						else:
							print "\t ERROR: len(BreakdownTimeForProcs): "+str(len(BreakdownTimeForProcs))+" where as NumProcs is "+str(NumProcs)
							sys.exit()
		                	        print "\n\t--Runtime--: "+str(IterRuntime[0])
						RunOutput.close()
						break
			TExceededTolerance=0
			CumulTime=0.0
			for CurrProcTime in IterRuntime:
			        CumulTime+=CurrProcTime
			        for InnerLoopCurrProcTime in IterRuntime:
			                Temp=abs(CurrProcTime-InnerLoopCurrProcTime)/(InnerLoopCurrProcTime)
			                if(Temp>0.05):
			                        TExceededTolerance+=1
			AvgTime=0     
			ExceededTolerance=0
			CumulTime=0.00000000010
			for Idx,CurrProcTime in enumerate(IterRuntime): 
			        CumulTime+=(CurrProcTime)
			        AvgTime=CumulTime/(Idx+1)
			        if(AvgTime>0):
			                Temp=abs(CurrProcTime-AvgTime)/AvgTime
			        else:
			                print "\t ERROR: Iter: "+str(i)+" Proc "+str(Idx)+" CurrProcTime "+str(CurrProcTime)+" CumulTime "+str(CumulTime)+" AvgTime "+str(AvgTime)+" AvgTime is zero! "
			                sys.exit()
	     
			        if(Temp>0.05):
			                ExceededTolerance+=1
			                print "\t Tolerance "+str(Temp)+" Proc "+str(Idx)+" Avg "+str(AvgTime)+" CurrProcTime "+str(CurrProcTime)
			if((ExceededTolerance>0) ):
			        AverageRuntimeNontolerantProcsCollection[FileName]+=ExceededTolerance
	     
			CumulTime/=NumProcs
			if(len(IterRuntime)>0):
				CumulTime/=len(IterRuntime)
			else:
				CumulTime=0.00000000010
			ItersTime.append(CumulTime)
			print "\t Iter: "+str(IterIdx)+" ProcExceededTolerance "+str(ExceededTolerance)+" TExceededTolerance "+str(TExceededTolerance)
   		else:
			print "\t IOError, omitting "+str(CurrRunOutputFile)+" from consideration "
	
	CumulTime=0
	ExceededTolerance=0
	AvgTime=0.00000000010
	for Idx,CurrIterTime in enumerate(ItersTime):
		CumulTime+=CurrIterTime
		AvgTime=CumulTime/(Idx+1)
		Temp=abs(CurrIterTime-AvgTime)/AvgTime
		if(Temp>0.05):
			ExceededTolerance+=1
		print "\t Iter: "+str(Idx)+" ExceededTolerance "+str(ExceededTolerance)
	AverageRuntimeNontolerantIterCollection[FileName]=ExceededTolerance
	return AvgTime
	
def main(argv):
	SrcFileName=''
	spatial=''
	reuse=''
	AverageRun=0
	CacheSimulation=0
	NumofProcs=''
	EnergySim=''
	NumCounters=''
	OutputFileName=''
	VectorExtract=''
	VectorParamStart=''
	NumVectorParams=''	
	EnergyMeasure=''
	MaxIters=''
	PapiCacheSim=''
	AverageCalc=''
	try:
		opts, args = getopt.getopt(sys.argv[1:],"l:r:s:a:p:c:e:b:d:n:o:h:v:t:u:x:y:",["list","reuse","spatial","average","procs","cachesim","energysim=","energymeasure=","maxiters=","numcounters","output","help","vector=","vectorparamstart=","numvectorparams=","papicachesim=","averagecalc="])	
	except getopt.GetoptError:
		#print str(err) # will print something like "option -a not recognized"
		usage()
	for opt, arg in opts:
		print "\n\t Opt: "+str(opt)+" argument "+str(arg)	
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-l", "--list"):
			SrcFileName=arg
			print "\t Source file is "+str(SrcFileName)+"\n";
		elif opt in ("-d", "--debug"):
			debug=int(arg)
			print "\t Debug option is "+str(debug)+"\n";	
		elif opt in ("-r"):
			reuse=RemoveWhiteSpace(arg)
			print "\t Reuse info: "+str(reuse)+"\n"
		elif opt in ("-s"):
			spatial=RemoveWhiteSpace(arg)
			print "\t Spatial info: "+str(spatial)+" arg "+str(arg)+"\n"
		elif opt in ("-a"):
			AverageRun=int(RemoveWhiteSpace(arg))
			print "\t AverageRun: "+str(AverageRun)+"\n"
		elif opt in ("-c"):
			CacheSimulation=int(RemoveWhiteSpace(arg))
			print "\t CacheSimulation: "+str(CacheSimulation)+"\n"
		elif opt in ("-p"):
			NumofProcs=int(RemoveWhiteSpace(arg))
			print "\t Number of processors: "+str(NumofProcs)+"\n"
		elif opt in ("-e","--energysim"):
			EnergySim=int(RemoveWhiteSpace(arg))
			print "\t Energy sim option: "+str(EnergySim)+"\n"
		elif opt in ("-n"):
			NumCounters=int(RemoveWhiteSpace(arg))
			print "\t Number of counters: "+str(NumCounters)+"\n"
		elif opt in ("-o"):
			OutputFileName=RemoveWhiteSpace(arg)
			print "\t Output file name is: "+str(OutputFileName)
		elif opt in ("-v","--vector"):
			VectorExtract=int(RemoveWhiteSpace(arg))
			print "\t Vector extract option is: "+str(VectorExtract)
		elif opt in ("-t", "--vectorparamstart"):
			VectorParamStart=int(RemoveWhiteSpace(arg))
			print "\t VectorParamStart option is "+str(VectorParamStart)+"\n";	
		elif opt in ("-u", "--numvectorparams"):
			NumVectorParams=int(RemoveWhiteSpace(arg))
			print "\t NumVectorParams option is "+str(NumVectorParams)+"\n";	
		elif opt in ("-b", "--energymeasure"):
			EnergyMeasure=int(RemoveWhiteSpace(arg))
			print "\t EnergyMeasure option is "+str(EnergyMeasure)+"\n";	
		elif opt in ("-d", "--maxiters"):
			MaxIters=int(RemoveWhiteSpace(arg))
			print "\t MaxIters option is "+str(MaxIters)+"\n";				
		elif opt in ("-x","--papicachesim"):
			PapiCacheSim=int(RemoveWhiteSpace(arg))
			print "\t PapiCacheSim option is "+str(PapiCacheSim)+"\n"
		elif opt in ("-y","--averagecalc"):
			AverageCalc=int(RemoveWhiteSpace(arg))
			print "\t AverageCalc option is "+str(AverageCalc)+"\n"
           	else:
   			usage()

	# If execution has come until this point, the script should have already identified the file with sourcefiles.
	if(SrcFileName==''):
		usage()
	if( (CacheSimulation==0) and (spatial=='') and (reuse=='')):
		spatial=0 #"16,32"
		reuse=0 #'16'
		print "\t INFO: Using default spatial value: "+str(spatial)+" reuse value "+str(16)
	if(AverageRun==0):
		AverageRun=0
		print "\t INFO: Using default average run value: "+str(AverageRun)
	else:
		if(AverageCalc==''):
			print "\t ERROR: AverageCalc is not set while average run is not zero! "
			sys.exit()
	if(NumofProcs==''):
		NumofProcs=1
		print "\t INFO: Using default number of processors is: "+str(NumofProcs)
	elif(NumofProcs<1):
		print "\t ERROR: NumofProcs is "+str(NumofProcs)+" which is less than 1 "
		sys.exit()
	if(NumCounters==''):
		NumCounters=0
		print "\t INFO: Using default flag for NumCounter: "+str(NumCounters)
	if(OutputFileName==''):
		OutputFileName='MasterStatsFile.log'
		print "\t INFO:  Using default output file name: "+str(OutputFileName)
	if(VectorExtract==''):
		VectorExtract=0
		print "\t INFO: Using default Vector extract option: "+str(VectorExtract)
	else:
		if( (VectorParamStart=='') or (NumVectorParams=='') ):
			VectorParamStart=23
			NumVectorParams=5
			print "\n\t INFO: Either or both of NumVectorParams or VectorParamsStart are not defined. Using default params-- VectorParamStart: "+str(VectorParamStart)+" NumVectorParams: "+str(NumVectorParams)
	#EnergyMeasure=0;print "\n\t INFO: By default not using EnergyMeasure method for energy calculation "
	SpatialWindow=[]
	if((spatial!='') and (spatial!=0) ):
		ThisSet=re.split(',',spatial)
		for CurrSW in ThisSet:
			SpatialWindow.append(CurrSW)
	else:
		SpatialWindow.append(0)

        ReuseWindow=0
	if(reuse!=''):
		print "\n\t Reuse window:"+str(reuse)+"--"
		ReuseWindow=int(reuse)
	#else:
	#	print "\n\t Reuse window:"+str(reuse)+"--"
	#	ReuseWindow=int(reuse)		
	if(EnergySim==''):
		EnergySim=0
		print "\n\t Using default EnergySim value: "+str(EnergySim)
	if(EnergyMeasure==''):
		if(EnergySim!=0):
			print "\n\t ERROR: EnergySim is needed but energy measure option is not set! "
			sys.exit()
		else:
			EnergyMeasure=3

	if(PapiCacheSim==''):			
		PapiCacheSim=-1
		print "\t INFO: Using default PapiCacheSim value: "+str(PapiCacheSim)
	else:
		if(AverageRun<2):
			print "\t ERROR: PapiCacheSim needs average run to be greater than 2" 
			sys.exit()
	SrcFileHandle=fopen(SrcFileName)
	ScFile=''
	if(SrcFileHandle!='IOERROR'):
		SrcFile=SrcFileHandle.readlines()
		SrcFileHandle.close()
	else:
		print "\t ERROR: Cannot find file "+str(SrcFileHandle)
		sys.exit()

	NumSourceFiles=len(SrcFile)
	for idx,CurrLine in enumerate(SrcFile):
		Temp=RemoveWhiteSpace(CurrLine)
		if(Temp==''):
			print "\n\t Is this line empty? Temp: "+str(Temp)+" CurrLine "+str(CurrLine)
			SrcFile.pop(idx)
			
	print "\n\t There are "+str(NumSourceFiles)+" source files to be handled. After removing empty lines we have: "+str(len(SrcFile))+" files to work with. "
	NumSourceFiles=len(SrcFile)
	
						
	PowerParams={}
	# These Params are for labyrinth
	#PowerParams['FreqParam0']=3;PowerParams['TotalPowerParam0']=4;PowerParams['IAPowerParam0']=7;PowerParams['GTPowerParam0']=10;PowerParams['DRAMPowerParam0']=13 #0-indexed
	#PowerParams['FreqParam1']=16;PowerParams['TotalPowerParam1']=17;PowerParams['IAPowerParam1']=20;PowerParams['GTPowerParam1']=23;PowerParams['DRAMPowerParam1']=26 #0-indexed
	
	# These params are for brahma
	PowerParams['FreqParam0']=3;PowerParams['TotalPowerParam0']=4;PowerParams['IAPowerParam0']=7;PowerParams['GTPowerParam0']=10;PowerParams['DRAMPowerParam0']=10 #0-indexed

	PowerParams['FreqParam1']=13;PowerParams['TotalPowerParam1']=14;PowerParams['IAPowerParam1']=17;PowerParams['GTPowerParam1']=23;PowerParams['DRAMPowerParam1']=20#0-indexed

	PowerParamsInOrder=[]
	PowerParamsInOrder.append('FreqParam0') 
	PowerParamsInOrder.append('TotalPowerParam0')
	PowerParamsInOrder.append('IAPowerParam0')
	#PowerParamsInOrder.append('GTPowerParam0')
	PowerParamsInOrder.append('DRAMPowerParam0')
	PowerParamsInOrder.append('FreqParam1')
	PowerParamsInOrder.append('TotalPowerParam1')
	PowerParamsInOrder.append('IAPowerParam1')
	#PowerParamsInOrder.append('GTPowerParam1')
	PowerParamsInOrder.append('DRAMPowerParam1')
	
	#for CurrParam in PowerParams:#PowerParamsInOrder.append(CurrParam)
	
	CurrSrcFileParams={}
	CurrStatsFileName=''
	CurrStatsFile=''
	#SpatialWindow=[32,128]
	FilesToRename=['.siminst','.dist','.spatial']
	#FilesToExtract=['.dist','.spatial']
	#AverageRun=5
	#AverageCalc=2
	AverageRuntimeCollection={}
	AverageRuntimeNontolerantProcsCollection={}
	AverageRuntimeNontolerantIterCollection={}
	PowerValueCollection={}
	RaplPowerValueCollection={}
	PredictionVectorParamsCollection={}
	ItersCollection={}
        CounterResultsCollection={}
	FileNameCollection=[]

	EnviVars=[]
	if( not (EnergySim==0) ):
		OutputFile='Duh.log'
		for CurrCounter in range(NumCounters):
			CounterEnviVar='HWC'+str(CurrCounter)
			commands.getoutput('echo $'+str(CounterEnviVar)+' > '+str(OutputFile))
			IpFile=fopen(OutputFile)
			ReadVar=[]
			if(IpFile!='IOERROR'):
				ReadVar=IpFile.readlines()
				IpFile.close()
			if(len(ReadVar)>1):
				print "\n\t Something is fishy out here, cos length of ReadVar's output is more than a line "
				sys.exit()
			else:
				Temp=RemoveWhiteSpace(ReadVar[0])
				print "\n\t Environemnt var: "+str(Temp)
				EnviVars.append(Temp)

	if(MaxIters==''):
		MaxIters=int(200000)
		print "\t INFO: Using default MaxIters option: "+str(MaxIters)
	SimulationNeeded=not( (ReuseWindow==0) and (spatial==0) and (CacheSimulation==0) )
	InfoExtractionNeeded=( not( (ReuseWindow==0) and (spatial==0) and (CacheSimulation==0) and (EnergySim==0) and (VectorExtract==0) and (AverageCalc!=1) ) )
	JustVectorExtractionNeeded= ( (ReuseWindow==0) and (spatial==0) and (CacheSimulation==0) and (EnergySim==0) )
	print "\n\t SimulationNeeded: "+str(SimulationNeeded)+" InfoExtractionNeeded: "+str(InfoExtractionNeeded)+" JustVectorExtractionNeeded "+str(JustVectorExtractionNeeded)
	
	#MasterStatsFile=fopen(OutputFileName,'w')
	MasterFileNameCollection=[]
	#LibPapiPath='/opt/papi/lib/libpapi.so -I /opt/papi/include/ '
	LibPapiPath=' -O2 /usr/local/lib/libpapi.so -I /usr/local/include '
	print "\t WARNING: LibPapiPath is {0:s} ".format(LibPapiPath)
	EmailID=[]
	EmailID.append('avspadiwal@gmail.com')
	for idx,CurrSrcFile in enumerate(SrcFile):
	 print "\n\t CurrSrcFile: "+str(CurrSrcFile)
	 LsCmd='ls '+str(RemoveWhiteSpace(CurrSrcFile)) #BenchmarksResultLogging.py ' #str(CurrSrcFile)
	 TempLsOutput=commands.getoutput(LsCmd)
	 print "\t BeforeLsCheck: "+str(TempLsOutput)
	 LsOutput=RemoveWhiteSpace(TempLsOutput)
	 if(LsOutput==RemoveWhiteSpace(CurrSrcFile)):
		print "\t Yaay found the source file-- "+str(CurrSrcFile)
		print "\t LsOutput: "+str(CurrSrcFile)
		CurrSrcFileParams[idx]={}
		SrcFileProvided=False
		#commands.getoutput('rm -f /mnt/pmfs/* ') # For labyrinth- NVM project.
		ExtractFileName=re.match('\s*(.*)\.c',CurrSrcFile)
		if ExtractFileName:
			SrcFileProvided=True
		else:
			ExtractFileName=True
		if(idx%10==0):
			if(idx>1):
				MasterStatsFile=fopen(OutputFileName,'w')
				WriteStats(MasterStatsFile,MasterFileNameCollection,EnviVars,AverageRuntimeCollection,PowerValueCollection,RaplPowerValueCollection,PredictionVectorParamsCollection,ItersCollection,EnergySim,EnergyMeasure,VectorExtract,PowerParams,PowerParamsInOrder,VectorParamStart,NumVectorParams,AverageCalc,CounterResultsCollection,PapiCacheSim,AverageRuntimeNontolerantProcsCollection,AverageRuntimeNontolerantIterCollection)
				MasterStatsFile.write("\n\n")
				MasterStatsFile.close()
				EmailMsg(EmailID,'Finished running '+str(idx)+' files! ',' Just another update from brahma.sdsc.edu')

		if ExtractFileName:
			if(SrcFileProvided):
				FileName=ExtractFileName.group(1)
			else:
				FileName=RemoveWhiteSpace(CurrSrcFile) 
			print "\n\t Will run "+str(FileName)+" exe now"
			#CurrSrcFileParams[idx]['FileName']=FileName
			FileNameParts=re.split('_',FileName)
			NumParts=len(FileNameParts)
			CheckParams=re.match('\s*.*\_Iters\_(.*)\_Vars\_(.*)\_DS\_(.*)\_Alloc\_(.*)\_Dims\_(.*)\_Size\_(.*)\_Random\_(.*)\_Streams\_(.*)\_Ops\_(.*)\_Stride\_(.*)',FileName)

			if CheckParams:
				#if debug:
				#print "\n\t Found all of the params! "
				CurrSrcFileParams[idx]['Iters']=CheckParams.group(1)
				ItersFileName=int(CheckParams.group(1))
				CurrSrcFileParams[idx]['Vars']=CheckParams.group(2)
				CurrSrcFileParams[idx]['DS']=CheckParams.group(3)
				CurrSrcFileParams[idx]['Alloc']=CheckParams.group(4)
				CurrSrcFileParams[idx]['Dims']=CheckParams.group(5)
				CurrSrcFileParams[idx]['Size']=CheckParams.group(6)
				CurrSrcFileParams[idx]['Random']=CheckParams.group(7)
				CurrSrcFileParams[idx]['Stream']=CheckParams.group(8)
				CurrSrcFileParams[idx]['Ops']=CheckParams.group(9)
				
				OpsLength=( len(CheckParams.group(9))/int(CurrSrcFileParams[idx]['Stream']) )+1;
				CurrSrcFileParams[idx]['OpsLength']=OpsLength
				#print "OpsLength: "+str(OpsLength)+" Stream "+str(CurrSrcFileParams[idx]['Stream'])
				TempStatsFileName='Stats'
				for CurrFeature in CurrSrcFileParams[idx]:
					#print "\n\t Feature: "+str(CurrFeature)+" value: "+str(CurrSrcFileParams[idx][CurrFeature])
					TempStatsFileName+='_'+str(CurrFeature)+'_'+str(CurrSrcFileParams[idx][CurrFeature])
				TempStatsFileName+='.log'
				#print "\n\t TempStatsFileName: "+str(TempStatsFileName)
				CurrSrcFileParams[idx]['FileName']=FileName
				if(SrcFileProvided):
					Compile(FileName,LibPapiPath)

			else:
				if(SrcFileProvided):
					Compile(FileName,LibPapiPath)
				FileNameCollection.append(FileName)
				MasterFileNameCollection.append(FileName)	
			RunOutputFile='RunOutput'+str(FileName)+'.log'
			RuntimeCollection=[]
			AverageRuntime=0.00000000010000001
			if(AverageCalc==0):
				ItersTime=[]
				AverageRuntimeNontolerantProcsCollection[FileName]=0
				RunOutputFileNameCollection=[]
				for i in range(AverageRun):
					RunCmd='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+' > '+str(RunOutputFile)
					print "\t RunCmd: {0:s} ".format(RunCmd)
					commands.getoutput(RunCmd)
					RunOutputFileNameCollection.append(RunOutputFile)
				AvgTime=ExtractRuntime(RunOutputFileNameCollection,NumofProcs,FileName,AverageRuntimeNontolerantProcsCollection,AverageRuntimeNontolerantIterCollection)
				"""	TExceededTolerance=0
					CumulTime=0.0
					for CurrProcTime in IterRuntime:
						CumulTime+=CurrProcTime
						for InnerLoopCurrProcTime in IterRuntime:
							Temp=abs(CurrProcTime-InnerLoopCurrProcTime)/(InnerLoopCurrProcTime)
							if(Temp>0.05):
								TExceededTolerance+=1
					AvgTime=0					
					ExceededTolerance=0
					CumulTime=0.0
					for Idx,CurrProcTime in enumerate(IterRuntime):	
						CumulTime+=(CurrProcTime)
						AvgTime=CumulTime/(Idx+1)
						if(AvgTime>0):
							Temp=abs(CurrProcTime-AvgTime)/AvgTime
						else:
							print "\t ERROR: Iter: "+str(i)+" Proc "+str(Idx)+" CurrProcTime "+str(CurrProcTime)+" CumulTime "+str(CumulTime)+" AvgTime "+str(AvgTime)+" AvgTime is zero! "
							sys.exit()
							
						if(Temp>0.05):
							ExceededTolerance+=1
							print "\t Tolerance "+str(Temp)+" Proc "+str(Idx)+" Avg "+str(AvgTime)+" CurrProcTime "+str(CurrProcTime)
					if((ExceededTolerance>0) ):
						AverageRuntimeNontolerantProcsCollection[FileName]+=ExceededTolerance
												
					CumulTime/=NumofProcs
					ItersTime.append(CumulTime)
					print "\t Iter: "+str(i)+" ProcExceededTolerance "+str(ExceededTolerance)+" TExceededTolerance "+str(TExceededTolerance)
				CumulTime=0
				ExceededTolerance=0
				AvgTime=0
				for Idx,CurrIterTime in enumerate(ItersTime):
					CumulTime+=CurrIterTime
					AvgTime=CumulTime/(Idx+1)
					Temp=abs(CurrIterTime-AvgTime)/AvgTime
					if(Temp>0.05):
						ExceededTolerance+=1
					print "\t Iter: "+str(Idx)+" ExceededTolerance "+str(ExceededTolerance)
				AverageRuntimeNontolerantIterCollection[FileName]=ExceededTolerance"""
				AverageRuntimeCollection[FileName]=AvgTime		
				FileNameCollection.append(FileName)
				MasterFileNameCollection.append(FileName)	
			"""if(PapiCacheSim>0):
				NumCounterSets=2
				CurrCounterValues={}
				for CurrCounterSets in range(NumCounterSets):
					ReplaceSet="perl -i -pe 's/int\*\ Events\=/int\*\ Events\=\ Events"+str(CurrCounterSets)+"\;\/\//g' "+str(FileName)+'.c'	
					CurrCounterValues[CurrCounterSets]={}
					print "\t CMD ReplaceSet: "+str(ReplaceSet)
					commands.getoutput(ReplaceSet)
					Compile(FileName,LibPapiPath)
					for i in range(AverageRun):
						#CurrCounterValues[CurrCounterSets][i]={}
						RunCmd='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+' > '+str(RunOutputFile)
						commands.getoutput(RunCmd)
						RenameOutputFile=' Set'+str(CurrCounterSets)+'_Iter'+str(i)+'_'+str(RunOutputFile)
						RenameOutputFileCmd='mv '+str(RunOutputFile)+' '+str(RenameOutputFile)
						print "\t RenameOutputFileCmd: "+str(RenameOutputFileCmd)
						commands.getoutput(RenameOutputFileCmd)
						GrepCmd='grep After '+str(RenameOutputFile)
						GrepOutput=commands.getoutput(GrepCmd)
						print "\t GrepOutput: "+str(GrepOutput)
						FindCounterVals=re.match('\s*.*\-\-\s*(.*)',GrepOutput)
						if FindCounterVals:
							print "\t Rest of grep "+str(FindCounterVals.group(1))
							BreakdownVals=re.split('\t',FindCounterVals.group(1))
							for CurrCounterVal in BreakdownVals:
								print "\t "+str(CurrCounterVal)
								ExtractVals=re.match('\s*Counter\:(.*)\s*value\:(.*)',CurrCounterVal)
								if ExtractVals:
									CounterNum=int(ExtractVals.group(1))	
									Value=int(ExtractVals.group(2))
									CounterStr='C'+str(CounterNum)
									#print "\t ** CounterNum: "+str(CounterNum)+" value: "+str(Value)
									if(not(CounterStr in CurrCounterValues[CurrCounterSets])):
										CurrCounterValues[CurrCounterSets][CounterStr]=[]									
									CurrCounterValues[CurrCounterSets][CounterStr].append(Value) 
					
				CurrInputCounterValues=[]
				IdxPos=0
				for CurrCounterSets in CurrCounterValues:
					for CounterStr in CurrCounterValues[CurrCounterSets]:
						CurrInputCounterValues.append(0)
					for CounterStr in CurrCounterValues[CurrCounterSets]:
						IterVals=''
						CumulSum=0
						CurrCounterValues[CurrCounterSets][CounterStr]=sorted(CurrCounterValues[CurrCounterSets][CounterStr])
							
						for Idx in range(1,AverageRun-1): #CurrCounterValues[CurrCounterSets][CounterStr]:
							CurrIterVal=CurrCounterValues[CurrCounterSets][CounterStr][Idx]
							IterVals+=str(CurrIterVal)+' ' 
							CumulSum+=CurrIterVal
						AverageVal=CumulSum/(AverageRun-2)	
						print "\t Counter: "+str(CounterStr)+" IterVals "+str(IterVals)+' AverageVal: '+str(AverageVal)
						FindCounterNum=re.match('\s*C(.*)',CounterStr)
						if(FindCounterNum):
							ActualCounterVal=int(FindCounterNum.group(1))
							CurrInputCounterValues[IdxPos+ActualCounterVal]=AverageVal
					IdxPos+=len(CurrInputCounterValues)
				for CurrCounterVal in CurrInputCounterValues:
					print "\t "+str(CurrCounterVal)
				CounterResultsCollection[FileName]=CurrInputCounterValues
				DirName=''
				if( not(InfoExtractionNeeded)):
					DirName='Dir'+str(FileName)
					commands.getoutput('mkdir '+str(DirName))
					CMDMvFiles=' mv *'+str(FileName)+'* '+str(DirName)
                                        commands.getoutput(CMDMvFiles)
					print "\t DirName: "+str(DirName) """
			if(InfoExtractionNeeded):
				NumProcsStrExtension=''
				if(NumofProcs<10):
					NumProcsStrExtension='0'+str(NumofProcs)
				elif(NumofProcs<100):
					NumProcsStrExtension=str(NumofProcs)
				else:
					print "\t ERROR: NumOfProcs is not supposed to be handled "
					sys.exit()
				ExtensionJbb='.r00000000.t000000'+str(NumProcsStrExtension)+'.jbbinst'

			
				SortedBBsList=''
				SortedBBsCollection=[]
				if(AverageCalc!=0):
					FileNameCollection.append(FileName)
					MasterFileNameCollection.append(FileName)							
							
					
				if( not (EnergySim==0) or (AverageCalc==1) ):
					print "\n\t ------------------------------------------- EnergyMeasure: "+str(EnergyMeasure)				      
				if(EnergyMeasure==0):

					RunCmd='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+' > '+str(RunOutputFile)
					commands.getoutput(RunCmd)
					RunOutput=fopen(RunOutputFile)
					if(RunOutput=='IOERROR'):
						print "\t ERROR: Cannot open file "+Str(RunOutputFile)
						RunOutput=[]
					for CurrLine in RunOutput:
					        #print "\n\t CurrLine: "+str(CurrLine)
					        CheckCounters=re.match('^\s*Hardware\s*counters\s*\:',CurrLine)
					        if CheckCounters:
					                #print "\n\t CurrLine: "+str(CurrLine)
					                CheckCounters=re.match('\s*Hardware\s*counters\s*:(.*)',CurrLine) # 
						if CheckCounters:
							#CurrStatsFile.write("\n\t CheckRuntime: "+str(CheckRuntime.group(0)))
							SplitPowerValues=re.split('\t',CheckCounters.group(1)) #+'.'+CheckCounters.group(2)
							if(len(SplitPowerValues)!=NumofProcs):
								Temp=[]
							for CurrPowerValues in SplitPowerValues:
								if(IsNumber(CurrPowerValues)):
									Temp.append(CurrPowerValues)	
									#if verbose:
									print "\t "+str(CurrPowerValues)
								PowerValueCollection[FileName]=Temp
					                        #Temp=float(Temp)
					                        #AverageRuntime+=Temp
					                        #print "\n\t--Runtime: "+str(Temp)+"~~"+str(CheckCounters.group(0))
						else:
							print "\n\t ERROR: Cannot extract runtime! \n" 
							sys.exit()    
					
					if(CacheSimulation==0):
					         DirName='Dir'+str(FileName)
					         commands.getoutput('mkdir '+str(DirName))
					         CMDMvFiles=' mv *'+str(FileName)+'.* '+str(DirName)
					         commands.getoutput(CMDMvFiles)
					         CMDMvFiles=' mv *'+str(FileName)+' '+str(DirName)
					         commands.getoutput(CMDMvFiles)
					         CMDCpLoopVectors=' cp loopVectors.rALL  '+str(DirName);commands.getoutput(CMDCpLoopVectors)
 
				elif(EnergyMeasure==1):
					(SortedBBsCollection,SortedBBsList)=ObtainTopLoops(FileName,NumofProcs)
					InsertEnergyProbes=' pebil --tool LoopIntercept --inp '+str(SortedBBsList)+' --app '+str(FileName)+' --lnc libpapi.so,libpapiinst.so '
					print "\n\t CMD InsertEnergyProbes: "+str(InsertEnergyProbes)
					commands.getoutput(InsertEnergyProbes)
					LpInstFileName='LpInst.sh'
					LpInstFile=open(LpInstFileName,'w')
					#LpInstFile.write('\n\t export HWC0=PAPI_TOT_INS')
					if(PapiCacheSim==0):
						LpInstFile.write('\n\t export HWC0=PAPI_SR_INS')	
						LpInstFile.write('\n\t export HWC1=PAPI_LD_INS')
						LpInstFile.write('\n\t export HWC2=PAPI_L1_DCM')
					elif(PapiCacheSim==1):
							LpInstFile.write('\n\t export HWC0=PAPI_L2_DCM')
							LpInstFile.write('\n\t export HWC1=PAPI_L3_TCA')
							LpInstFile.write('\n\t export HWC2=PAPI_L3_TCM')
					else:
							LpInstFile.write('\n\t export HWC0=PAPI_TOT_INS')	

						LpInstFile.write('\nmpirun -np '+str(NumofProcs)+' ./'+str(FileName)+'.lpiinst > Duh3.log ')
						LpInstFile.close()
					for i in range(AverageRun):
						 print "\t Iter: "+str(i)+" cmd: sh "+str(LpInstFileName)
						 commands.getoutput('sh '+str(LpInstFileName))
						 print "\t Duh3.log: "+str(commands.getoutput('cat Duh3.log'))
						 LsFileName='LsFile.log'
						 LsCmd='ls '+str(FileName)+'.meta_*.lpiinst > LsFile.log'
						 print "\t LsCmd: "+str(LsCmd)
						 commands.getoutput(LsCmd)
						 IpFile=open(LsFileName) #='LsFile.log'
						 LsFiles=IpFile.readlines()
						 IpFile.close()
						 for FileIdx,TempCurrFile in enumerate(LsFiles): 
							CurrFile=RemoveWhiteSpace(TempCurrFile)
							RenameCurrFile='Iter'+str(i)+'_'+str(CurrFile)
							EnergyStatsFileName=(CurrFile) #str(FileName)+'.meta_0.lpiinst'
							CpMetaFileCMD='cp '+str(CurrFile)+' '+str(RenameCurrFile)
							commands.getoutput(CpMetaFileCMD)
							print "\t Opening file "+str(EnergyStatsFileName)
							IpFile=open(EnergyStatsFileName)
							EnergyStatsFile=IpFile.readlines()
							IpFile.close()	
						
							BBIDFound=0
							BBIDline=-1
							RelevantThreadStatsFromBBLine=2
							BBID=-1
							for LineNum,CurrStats in enumerate(EnergyStatsFile):
								print "\n\t CurrStats: "+str(CurrStats)	
								CurrLineBreakdown=RemoveWhiteSpace(CurrStats).split('\t')
								LenCurrLineBreakdown=len(CurrLineBreakdown)
								if( (LenCurrLineBreakdown==1) and (CurrLineBreakdown[0]!='') ):
									CheckThread=re.match('\s*Thread\:.*',CurrLineBreakdown[0])
								if not CheckThread:
									BBIDFound=1
									BBIDLine=LineNum
									BBID=RemoveWhiteSpace(CurrLineBreakdown[0])			
									print "\n\t BBID found!!! "+str(BBID)
									
								#print "\t LenCurrLineBreakdown: "+str(LenCurrLineBreakdown)+" NumCounters "+str(NumCounters)+" CurrLineBreakdown "+str(CurrLineBreakdown)
								if(LenCurrLineBreakdown==(NumCounters+1)):
									if ( BBIDFound  and ( LineNum ==(BBIDLine+RelevantThreadStatsFromBBLine)  ) ):
										#print "\n\t BBID: "+str(BBID)+" LineNum: "+str(LineNum)+" BBIDLineNum: "+str(BBIDLine)
										#print "\n\t LineNum: "+str(LineNum)+" len(CurrLineBreakdown) "+str(len(CurrLineBreakdown))+" CurrLineBreakdown: "+str(CurrLineBreakdown)
										CheckThread=re.match('\s*Thread\:.*',CurrLineBreakdown[0])
										if CheckThread:
											Temp=[]
											for Idx,CurrCounterReading in enumerate(CurrLineBreakdown):
												if(Idx):
													#print "\n\t Counter num: "+str(Idx)+" value: "+str(CurrCounterReading)
													Temp.append(float(RemoveWhiteSpace(CurrCounterReading)))
											if(not ( FileName in PowerValueCollection)):
												PowerValueCollection[FileName]={}
											if(not (BBID in PowerValueCollection[FileName])):
												Temp1=[ 0 for i in range(NumCounters)]
												PowerValueCollection[FileName][BBID]=Temp1
												if(FileIdx>1):
													print "\t ERROR: New BBID found in a different file: "+str(FileIdx)
											for CounterIdx in range(NumCounters):
												print "\t Counter: "+str(CounterIdx)+" Before: "+str(PowerValueCollection[FileName][BBID][CounterIdx])+" adding "+str(Temp[CounterIdx])
												PowerValueCollection[FileName][BBID][CounterIdx]+=Temp[CounterIdx]	
									BBIDFound=0
									BBIDLine=-1
					if(FileName in PowerValueCollection):
						for CurrBB in (PowerValueCollection[FileName]):
							for CounterIdx in range(NumCounters):
								Before=PowerValueCollection[FileName][CurrBB][CounterIdx]
								PowerValueCollection[FileName][CurrBB][CounterIdx]/=(NumofProcs*AverageRun)
								print "\t CurrBB: "+str(CurrBB)+"\t Counter-idx: "+str(CounterIdx)+"\t Counter-value: "+str(PowerValueCollection[FileName][CurrBB])+"\t Before: "+str(Before)
					if(CacheSimulation==0):
						DirName='Dir'+str(FileName)
						commands.getoutput('mkdir '+str(DirName))
						CMDMvFiles=' mv *'+str(FileName)+'.* '+str(DirName)	
						commands.getoutput(CMDMvFiles)
						CMDMvFiles=' mv *'+str(FileName)+' '+str(DirName)
						commands.getoutput(CMDMvFiles)
						CMDCpLoopVectors=' cp loopVectors.rALL  '+str(DirName);commands.getoutput(CMDCpLoopVectors)

				elif((EnergyMeasure==2) or (AverageCalc==1)):	

					#print "\t Streams: "+str(CurrSrcFileParams[idx]['Stream'])+" NumOperands "+str(CurrSrcFileParams[idx]['Ops'])
					#NumOperands=((len(CurrSrcFileParams[idx]['Ops'])/int(CurrSrcFileParams[idx]['Stream']))+1)
					#print "\n\t NumOperands: "+str(NumOperands)
					#Iters=int( MaxIters/(NumOperands*int(CurrSrcFileParams[idx]['Stream'])*0.5))
					#print "\t MaxIters: "+str(MaxIters)+" Iters: "+str(Iters)
					#ReplaceNumLoops(FileName,Iters)
					ItersCollection[FileName]=10 #Iters
					#Compile(FileName,LibPapiPath)
					#print "\n\t **************************** WARNING: ReplaceNumLoops has a dummy iteration count!!!! ********************************* "llFreqs[CurrFreq])
					#RunOutput=commands.getoutput('./'+str(FileName))
					#print "\t RunOutput: "+str(RunOutput)
							
					if(EnergyMeasure==2):
						CallScriptCmd='run_one_case.sh '+str(FileName)+' 2900000 '
					else:
						CallScriptCmd='only_run.sh '+str(FileName)+' 2900000 '
					print "\n\t CallScriptCmd: "+str(CallScriptCmd)+"\t which run_one_case.sh "+str(commands.getoutput('which run_one_case.sh'))
					TakeIt=commands.getoutput(CallScriptCmd)
					print "\n\t TakeIt: "+str(TakeIt)						
					AllFreqs={}
					FilePattern='app.out.'+str(FileName)+'*'
					LsOutput=commands.getoutput('ls '+str(FilePattern))
					if(LsOutput==''):
						print "\t ERROR: Unable to obtain file of the form "+str(FilePattern)
						sys.exit()
					print "\t LsOutput-- "+str(LsOutput)
					AllFreqs=ExtractFilesAndFreqs(LsOutput)
					for CurrFreq in AllFreqs:
						print "\t LsFreq: "+str(CurrFreq)
					if(AverageCalc==1):
						AverageRuntimeCollection[FileName]={}
						for CurrFreq in AllFreqs:
							AvgRuntime=0.0
							NumFiles=len(AllFreqs[CurrFreq])
							AvgRuntime=ExtractRuntime((AllFreqs[CurrFreq]),16,FileName,AverageRuntimeNontolerantProcsCollection,AverageRuntimeNontolerantIterCollection)
							print "\t Freq- "+str(CurrFreq)+" AvgRuntime "+str(AvgRuntime)
							AverageRuntimeCollection[FileName][CurrFreq]=AvgRuntime

					WattsFilePattern='raw_watts.'+str(FileName)+'*'
					WattsLsOutput=commands.getoutput('ls '+str(WattsFilePattern))
					WattsFreq=ExtractFilesAndFreqs(WattsLsOutput)
					for CurrFreq in WattsFreq:
						print "\t WattsFreq: "+str(CurrFreq)
					for CurrFreq in WattsFreq:
						WattsNotYetFound=True
						for CurrFile in WattsFreq[CurrFreq]:
						 IpFile=fopen(CurrFile)
						 if(IpFile!='IOERROR'):
							CurrFileContents=IpFile.readlines()
							IpFile.close()
							#print "\t File: "+str(CurrFile)+" #lines "+str(len(CurrFileContents))
							AllFloats=True
							TotalPowerSamples=0.0
							for TempCurrLine in CurrFileContents:
								CurrLine=RemoveWhiteSpace(TempCurrLine)
								#print "\t CurrLine: "+str(CurrLine)
								if(not(float(CurrLine))):
									AllFloats=False
									print "\t Not a float :-o "+str(CurrLine)
									break
								else:
									TotalPowerSamples+=float(CurrLine)
							if(AllFloats):
							 NumSamples=len(CurrFileContents)
							 if(NumSamples>0):
								AvgPower=float(TotalPowerSamples/NumSamples)
								print "\t File: "+str(CurrFile)+" Power: "+str(AvgPower)
								if(not(FileName in PowerValueCollection)):
									PowerValueCollection[FileName]={}
								PowerValueCollection[FileName][CurrFreq]=AvgPower
								WattsNotYetFound=False
								break
						if(WattsNotYetFound):
							print "\t ERROR/WARNING: Not able to extract watts for frequency "+str(CurrFreq)
							if(not(FileName in PowerValueCollection)):
								PowerValueCollection[FileName]={}
							PowerValueCollection[FileName][CurrFreq]="\t power measure not found!!! "
							#sys.exit()
						

					RaplWattsFilePattern='raw_rapl.'+str(FileName)+'*'
					RaplWattsLsOutput=commands.getoutput('ls '+str(RaplWattsFilePattern))
					RaplWattsFreq=ExtractFilesAndFreqs(RaplWattsLsOutput)
					
					NumPowerParams=24
					for CurrFreq in RaplWattsFreq:
						print "\t RaplFreq: "+str(CurrFreq)
						RaplWattsNotYetFound=True
						for CurrFile in RaplWattsFreq[CurrFreq]:
							IpFile=fopen(CurrFile)
							if(IpFile!='IOERROR'):
								CurrFileContents=IpFile.readlines()
								IpFile.close()
								print "\t File: "+str(CurrFile)+" #lines "+str(len(CurrFileContents))
								ProperFormat=True
								AllNums=True
								SumOfPowerValues={}
								for CurrParam in PowerParams:
									SumOfPowerValues[CurrParam]=0.0
							
								for idx,TempCurrLine in enumerate(CurrFileContents):
									if(idx):
										CurrLine=RemoveWhiteSpace(TempCurrLine)
										#print "\t CurrLine: "+str(CurrLine)
										BreakdownParams=re.split(',',CurrLine)
										#if(not(float(CurrLine))):
										if(len(BreakdownParams)!=NumPowerParams):
											ProperFormat=False
											print "\t Not the right proper format --len "+str(len(BreakdownParams))+" LastTerm "+str(BreakdownParams[(len(BreakdownParams)-1)])+'--'#+str(CurrLine)+""
										else:
											for CurrParam in PowerParamsInOrder:
												ValueForParam=BreakdownParams[(PowerParams[CurrParam])]
												#print "\t Idx: "+str(CurrParam)+" Value: "+str(ValueForParam)
												if(IsNumber(ValueForParam)):
													SumOfPowerValues[CurrParam]+=float(ValueForParam)
												else:
													AllNums=False
													print "\t Not a float :-o "+str(CurrLine)
													break		
								if(AllNums and ProperFormat):
									#AvgPower=float(TotalPowerSamples/len(CurrFileContents))
									NumSamples=len(CurrFileContents)-1
									if(NumSamples>0):
										StrAvgPower=''
										for CurrParam in PowerParamsInOrder:
											SumOfPowerValues[CurrParam]/=NumSamples
											StrAvgPower+='\t'+str(round(SumOfPowerValues[CurrParam],5))
										#print "\t PowerParam-- "+str(CurrParam)+'  Value '+str(SumOfPowerValues[CurrParam])
										print "\t File: "+str(CurrFile)+" Power: "+str(StrAvgPower)
										if(not(FileName in RaplPowerValueCollection)):
											RaplPowerValueCollection[FileName]={}
										RaplPowerValueCollection[FileName][CurrFreq]=StrAvgPower #SumOfPowerValues
										RaplWattsNotYetFound=False
										
									else:
										print "WARNING: Rapl File "+str(CurrFile)+" has zero samples!! "
									
									break
						if(RaplWattsNotYetFound):
							print "\t ERROR: Not able to extract RaplWatts for frequency "+str(CurrFreq)
							if(not(FileName in RaplPowerValueCollection)):
								RaplPowerValueCollection[FileName]={}
							RaplPowerValueCollection[FileName][CurrFreq]="\t power measure not found!!! "
							#sys.exit()

						if(CacheSimulation==0):
							DirName='Dir'+str(FileName)
							commands.getoutput('mkdir '+str(DirName))
							CMDMvFiles=' mv *'+str(FileName)+'.* '+str(DirName)    
							commands.getoutput(CMDMvFiles)
							CMDMvFiles=' mv *'+str(FileName)+' '+str(DirName)
							commands.getoutput(CMDMvFiles)
							CMDCpLoopVectors=' cp loopVectors.rALL  '+str(DirName);commands.getoutput(CMDCpLoopVectors)

				if(SimulationNeeded):
					if(SortedBBsList==''):
						(SortedBBsCollection,SortedBBsList)=ObtainTopLoops(FileName,NumofProcs)
					CMDPebilSim='pebil --typ sim --inp '+str(SortedBBsList)+' --app '+str(FileName)
					print "\n\t CMDPebilSim: "+str(CMDPebilSim) 
					commands.getoutput(CMDPebilSim)
					SimInstFile=str(FileName)+'.siminst'
					DirName='Dir'+str(FileName)
					CMDMkdir='mkdir '+str(DirName)
					commands.getoutput(CMDMkdir)
					FilesToExtract=[]
					if(ReuseWindow!=0):
						FilesToExtract.append('.dist')
					if(spatial!=''):
						#if(spatial!=0):
						if((len(SpatialWindow)==1) and (SpatialWindow[0]==0)):
							FilesToExtract.append('.spatial')
					for CurrSW in SpatialWindow:
					
						SimRunScript=fopen('SimRun.sh','w')
						print "\n\t CurrSW: "+str(CurrSW)
						SimRunScript.write('\n\t export METASIM_SAMPLE_ON=1 ')
						SimRunScript.write('\n\t export METASIM_SAMPLE_OFF=0 ')			
						MetasimReuseWindow='export METASIM_REUSE_WINDOW='+str(ReuseWindow)
						SimRunScript.write("\n\t "+str(MetasimReuseWindow))
						SimRunScript.write('\n\t export METASIM_SPATIAL_WINDOW='+str(CurrSW))
						MetasSimCacheSim='export METASIM_CACHE_SIMULATION='+str(CacheSimulation)
						SimRunScript.write('\n\t '+str(MetasSimCacheSim))			
						SimRunScript.write('\n\t export METASIM_ADDRESS_RANGE=0 ')	
						SimRunScript.write('\n\t export METASIM_SAMPLE_MAX=10000000')
						SimRunScript.write('\n\t ls '+str(FileName)+'*'+' > SimInstOutput.log')
						SimRunScript.write('\n\t mpirun -np '+str(NumofProcs)+' ./'+str(SimInstFile))	
						SimRunScript.write('\n\n')							
						SimRunScript.close()
						commands.getoutput('sh SimRun.sh > SimInstOutput.log ')					
						"""if(CurrStatsFile!=''):
							CurrStatsFile.write("\n\t Spatial Window: "+str(CurrSW)+"\n")
						for CurrExt in FilesToExtract:
							CurrExtFile=FileName+'.r00000000.t00000001'+str(CurrExt)
							DistFileHandle=fopen(CurrExtFile)
							DistFile=DistFileHandle.readlines()			
							BinsNotFound=1
							KeepCopying=1
							CurrStatsFile.write("\n\t Extension: "+str(CurrExt)+"\n")
							#print("\n\t Extension: "+str(CurrExt)+"\n")
							for CurrLine in DistFile:
								if BinsNotFound:
									CheckBins=re.match('\s*Bin\s*Count',CurrLine)
									if CheckBins:
										BinsNotFound=0
								else:
									CheckTotal=re.match('\s*Total\s*Count\:',CurrLine)
									if not(CheckTotal):
										if KeepCopying:
											CurrStatsFile.write("\t "+str(CurrLine))
									else:
										KeepCopying=0
											
						FilePrefix='SW_'+str(CurrSW)+'_'
						#commands.getoutput(
						for CurrExtension in FilesToRename:
							CurrName=FileName+'.r00000000.t00000001'+str(CurrExtension)
							MVCommand='mv '+str(CurrName)+' '+str(FilePrefix)+str(CurrName)
						#print "\n\t MVCommand: "+str(MVCommand)
							commands.getoutput(MVCommand) """

				if(not(VectorExtract==0)):
					if(SortedBBsList==''):
						(SortedBBsCollection,SortedBBsList)=ObtainTopLoops(FileName,NumofProcs)		
					else:
						jRunProcess='jRunTool --application '+str(FileName)+' --dataset standard --cpu_count '+str(NumofProcs)+' --processed_dir processed --scratch_dir scratch --raw_pmactrace `pwd` --process > Duh.log '
						print "\t VecExtract: jRunProcess "+str(jRunProcess)
						commands.getoutput(jRunProcess)
						jRunReport='jRunTool --application '+str(FileName)+' --dataset standard --cpu_count '+str(NumofProcs)+' --processed_dir processed --scratch_dir scratch --raw_pmactrace `pwd` --sysid 130 --functions default --loops default --report blockvector  > Duh2.log '
						print "\t VecExtract: jRunReport "+str(jRunReport)
						commands.getoutput(jRunReport)
						print "\t Did I need to obtain top-loops??"
					print "\t len(SortedBBsCollection) "+str(len(SortedBBsCollection))
					AllBBsStats=[]
					for CurrBB in SortedBBsCollection:
						print "\t Now searching: "+str(CurrBB)
						GrepCmd='grep '+str(CurrBB)+' loopVectors.rALL'	
						GrepOutput=commands.getoutput(GrepCmd)
						BreakGrepOutput=re.split('\t',GrepOutput)
						print "\t GrepOutput: "+str(GrepOutput)
						print"\t len(Breakdown): "+str(len(BreakGrepOutput))
						Temp=[]
						for Idx in range(VectorParamStart,VectorParamStart+NumVectorParams):
							print "\t Idx: "+str(Idx)+" Param: "+str(BreakGrepOutput[Idx])
							Temp.append(BreakGrepOutput[Idx])
						AllBBsStats.append(Temp)
					PredictionVectorParamsCollection[FileName]=AllBBsStats
						#+' 24,idu: '+str(BreakGrepOutput[26])	
					#sys.exit()	
					if(JustVectorExtractionNeeded):
						DirName='Dir'+str(FileName)
						commands.getoutput('mkdir '+str(DirName))
						CMDMvFiles=' mv *'+str(FileName)+'.* '+str(DirName)
						commands.getoutput(CMDMvFiles)
						CMDMvFiles=' mv *'+str(FileName)+' '+str(DirName)
						commands.getoutput(CMDMvFiles)	
						CMDCpLoopVectors=' cp loopVectors.rALL  '+str(DirName);commands.getoutput(CMDCpLoopVectors)					
								
				DirName='Dir'+str(FileName)
				CMDMkdir='mkdir '+str(DirName)
				commands.getoutput(DirName)
				CMDMvFiles=' mv *'+str(FileName)+'* '+str(DirName)
				commands.getoutput(CMDMvFiles)
				print "\t CMDMvFiles: "+str(CMDMvFiles)
				CMDMvFiles=' mv *'+str(FileName)+'.* '+str(DirName)
				commands.getoutput(CMDMvFiles)
				CMDCpLoopVectors=' cp loopVectors.rALL  '+str(DirName);commands.getoutput(CMDCpLoopVectors)
							
	 else:
		print "\t Could not find the SrcFile: "+str(CurrSrcFile)
		print "\t LsOutput: "+str(LsOutput)
	#if(CurrStatsFile):
	#	WriteStats(CurrStatsFile,FileNameCollection,EnviVars,AverageRuntimeCollection,PowerValueCollection,RaplPowerValueCollection,PredictionVectorParamsCollection,ItersCollection,EnergySim,EnergyMeasure,VectorExtract,PowerParams,PowerParamsInOrder,VectorParamStart,NumVectorParams,AverageCalc,CounterResultsCollection,PapiCacheSim,AverageRuntimeNontolerantProcsCollection,AverageRuntimeNontolerantIterCollection)
	#	CurrStatsFile.write("\n\n\n")
	#	CurrStatsFile.close()#"""
	MasterStatsFile=fopen(OutputFileName,'w')	
	WriteStats(MasterStatsFile,MasterFileNameCollection,EnviVars,AverageRuntimeCollection,PowerValueCollection,RaplPowerValueCollection,PredictionVectorParamsCollection,ItersCollection,EnergySim,EnergyMeasure,VectorExtract,PowerParams,PowerParamsInOrder,VectorParamStart,NumVectorParams,AverageCalc,CounterResultsCollection,PapiCacheSim,AverageRuntimeNontolerantProcsCollection,AverageRuntimeNontolerantIterCollection)
	MasterStatsFile.write("\n\n")
	MasterStatsFile.close()


	RemoveWorkingFiles='rm -f RunOutput.log SimRun.sh *Instr* Duh*.log'
	commands.getoutput(RemoveWorkingFiles)

if __name__ == "__main__":
   main(sys.argv[1:])
   EmailID=['avspadiwal@gmail.com']	
   #EmailMsg(EmailID,' Yaay done with running all the files',' End of run update!! ')

