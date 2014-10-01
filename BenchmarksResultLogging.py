
import sys,getopt,subprocess,re,math,commands,time,copy,random

def usage():
	print "\n\t Usage: BenchmarksResultsLogging.py -l/--source file with all the source file that needs to be executed and logged -p <num-of-procs> -c CacheSimulationFlag <0/1> -r ReuseDistance -s SpatialDistanceFlag  -e EnergyMeasureFlag <0/1> -n Number of Counters -a Number of runs for averaging runtime. -p Number of Processors -d \n\t\t -s: spatial distances -v/--vector <Vector-extract-from-PSAPP> -t/--vectorparamstart <vectorparamstart> -u/--numvectorparams <numvectorparams> .\n\t\t -o <Output-file-name> \n "
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
	
def Compile(Input,Options=''):
	CompileCmd='mpicc -g -O2 '+str(Input)+'.c '+str(Options)+' -o '+str(Input)
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
		ExtractFreq=re.match('.*StrideBenchmarks.*\.(.*)\.',CurrFile)
		if(ExtractFreq):
			Freq=int(ExtractFreq.group(1))
			if(not(Freq in AllFreqs)):
				#print "\t Freq: "+str(Freq)	
				AllFreqs[Freq]=[]
				AllFreqs[Freq].append(CurrFile)
			else:
				AllFreqs[Freq].append(CurrFile)
	
	return AllFreqs
	
def ReplaceNumLoops(Input,ReplaceIter):
	ReplaceIter="perl -i -pe 's/NumLoops_Var0\ \=/NumLoops_Var0\ \= "+str(ReplaceIter)+"\;\/\//g' "+str(Input)+'.c'
	print "\t ReplaceIter: "+str(ReplaceIter)
	ReplaceIterOutput=commands.getoutput(ReplaceIter)
	if(ReplaceIterOutput!=''):
		print "\t WARNING: ReplaceIterOutput "+str(ReplaceIterOutput)
		print "\t WARNING is currently handeled as ERROR "
		sys.exit()
	#sys.exit()
	
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
	try:
		opts, args = getopt.getopt(sys.argv[1:],"l:r:s:a:p:c:e:b:d:n:o:h:v:t:u:",["list","reuse","spatial","average","procs","cachesim","energysim","energymeasure=","maxiters=","numcounters","output","help","vector=","vectorparamstart=","numvectorparams="])	
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
			print "\n\t Source file is "+str(SrcFileName)+"\n";
		elif opt in ("-d", "--debug"):
			debug=int(arg)
			print "\n\t Debug option is "+str(debug)+"\n";	
		elif opt in ("-r"):
			reuse=RemoveWhiteSpace(arg)
			print "\n\t Reuse info: "+str(reuse)+"\n"
		elif opt in ("-s"):
			spatial=RemoveWhiteSpace(arg)
			print "\n\t Spatial info: "+str(spatial)+" arg "+str(arg)+"\n"
		elif opt in ("-a"):
			AverageRun=int(RemoveWhiteSpace(arg))
			print "\n\t AverageRun: "+str(AverageRun)+"\n"
		elif opt in ("-c"):
			CacheSimulation=int(RemoveWhiteSpace(arg))
			print "\n\t CacheSimulation: "+str(CacheSimulation)+"\n"
		elif opt in ("-p"):
			NumofProcs=int(RemoveWhiteSpace(arg))
			print "\n\t Number of processors: "+str(NumofProcs)+"\n"
		elif opt in ("-e"):
			EnergySim=int(RemoveWhiteSpace(arg))
			print "\n\t Energy sim option: "+str(EnergySim)+"\n"
		elif opt in ("-n"):
			NumCounters=int(RemoveWhiteSpace(arg))
			print "\n\t Number of counters: "+str(NumCounters)+"\n"
		elif opt in ("-o"):
			OutputFileName=RemoveWhiteSpace(arg)
			print "\n\t Output file name is: "+str(OutputFileName)
		elif opt in ("-v","--vector"):
			VectorExtract=int(RemoveWhiteSpace(arg))
			print "\n\t Vector extract option is: "+str(VectorExtract)
		elif opt in ("-t", "--vectorparamstart"):
			VectorParamStart=int(RemoveWhiteSpace(arg))
			print "\n\t VectorParamStart option is "+str(VectorParamStart)+"\n";	
		elif opt in ("-u", "--numvectorparams"):
			NumVectorParams=int(RemoveWhiteSpace(arg))
			print "\n\t NumVectorParams option is "+str(NumVectorParams)+"\n";	
		elif opt in ("-b", "--energymeasure"):
			EnergyMeasure=int(RemoveWhiteSpace(arg))
			print "\n\t EnergyMeasure option is "+str(EnergyMeasure)+"\n";	
		elif opt in ("-d", "--maxiters"):
			MaxIters=int(RemoveWhiteSpace(arg))
			print "\n\t MaxIters option is "+str(MaxIters)+"\n";				
           	else:
   			usage()

	# If execution has come until this point, the script should have already identified the file with sourcefiles.
	if(SrcFileName==''):
		print "\n\t Nodpa!! "
		usage()
	if( (CacheSimulation==0) and (spatial=='') and (reuse=='')):
		spatial=0 #"16,32"
		reuse=0 #'16'
		print "\n\t INFO: Using default spatial value: "+str(spatial)+" reuse value "+str(16)
	if(AverageRun==0):
		AverageRun=0
		print "\n\t INFO: Using default average run value: "+str(AverageRun)
	if(NumofProcs==''):
		NumofProcs=1
		print "\n\t INFO: Using default number of processors is: "+str(NumofProcs)

	if(NumCounters==''):
		NumCounters=0
		print "\n\t INFO: Using default flag for NumCounter: "+str(NumCounters)
	if(OutputFileName==''):
		OutputFileName='MasterStatsFile.log'
		print "\n\t INFO:  Using default output file name: "+str(OutputFileName)
	if(VectorExtract==''):
		VectorExtract=0
		print "\n\t INFO: Using default Vector extract option: "+str(VectorExtract)
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
			
	SrcFileHandle=open(SrcFileName)
	SrcFile=SrcFileHandle.readlines()
	SrcFileHandle.close()

	NumSourceFiles=len(SrcFile)
	for idx,CurrLine in enumerate(SrcFile):
		Temp=RemoveWhiteSpace(CurrLine)
		if(Temp==''):
			print "\n\t Is this line empty? Temp: "+str(Temp)+" CurrLine "+str(CurrLine)
			SrcFile.pop(idx)
			
	print "\n\t There are "+str(NumSourceFiles)+" source files to be handled. After removing empty lines we have: "+str(len(SrcFile))+" files to work with. "
	NumSourceFiles=len(SrcFile)
	
	CurrSrcFileParams={}
	CurrStatsFileName=''
	CurrStatsFile=''
	#SpatialWindow=[32,128]
	FilesToRename=['.siminst','.dist','.spatial']
	#FilesToExtract=['.dist','.spatial']
	#AverageRun=5
	AverageRuntimeCollection={}
	PowerValueCollection={}
	PredictionVectorParamsCollection={}
	ItersCollection={}
	FileNameCollection=[]

	EnviVars=[]
	if( not (EnergySim==0) ):
		OutputFile='Duh.log'
		for CurrCounter in range(NumCounters):
			CounterEnviVar='HWC'+str(CurrCounter)
			commands.getoutput('echo $'+str(CounterEnviVar)+' > '+str(OutputFile))
			IpFile=open(OutputFile)
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
	InfoExtractionNeeded=( not( (ReuseWindow==0) and (spatial==0) and (CacheSimulation==0) and (EnergySim==0) and (VectorExtract==0) ) )
	JustVectorExtractionNeeded= ( (ReuseWindow==0) and (spatial==0) and (CacheSimulation==0) and (EnergySim==0) )
	print "\n\t SimulationNeeded: "+str(SimulationNeeded)+" InfoExtractionNeeded: "+str(InfoExtractionNeeded)+" JustVectorExtractionNeeded "+str(JustVectorExtractionNeeded)
	
	MasterStatsFile=open(OutputFileName,'w')
	MasterFileNameCollection=[]
	LibPapiPath='/usr/local/lib/libpapi.so'
	
	for idx,CurrSrcFile in enumerate(SrcFile):
		print "\n\t CurrSrcFile: "+str(CurrSrcFile)
		CurrSrcFileParams[idx]={}
		ExtractFileName=re.match('\s*(.*)\.c',CurrSrcFile)
		if ExtractFileName:
			FileName=ExtractFileName.group(1)
			print "\n\t Will run "+str(FileName)+" exe now"
			#CurrSrcFileParams[idx]['FileName']=FileName
			FileNameParts=re.split('_',FileName)
			NumParts=len(FileNameParts)
			CheckParams=re.match('\s*.*\_Iters\_(.*)\_Vars\_(.*)\_DS\_(.*)\_Alloc\_(.*)\_Dims\_(.*)\_Size\_(.*)\_Random\_(.*)\_Streams\_(.*)\_Ops\_(.*)\_Stride\_(.*)',FileName)

			if CheckParams:
				#if debug:
				#print "\n\t Found all of the params! "
				CurrSrcFileParams[idx]['Iters']=CheckParams.group(1)
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
				if(CurrStatsFileName!=TempStatsFileName):
					if(CurrStatsFile):
						CurrStatsFile.write("\n\t Average run times: ") ; 
						CurrStatsFile.write("\n\t\t Exe: \t\t\t\t Average runtime ")
						for CurrFile in FileNameCollection:
							CurrStatsFile.write("\n\t "+str(CurrFile)+"\t\t "+str(AverageRuntimeCollection[CurrFile]))
				                if(not(EnergySim==0)):
				                        CurrStatsFile.write("\n\n\t Energy probes value: ")
							CurrStatsFile.write("\n\t Counters : ")
							for CurrCounter in EnviVars:
								CurrStatsFile.write("\t "+str(CurrCounter))
				                        CurrStatsFile.write("\n\t\t Exe: \t\t\t\t BBID: \t\t Power from each counter ")
							if(EnergyMeasure==1):
				   				#CurrStatsFile.write("\n")
								#print "\n\t CurrFile: "+str(CurrFile)
								for CurrFile in FileNameCollection:
								 #CurrStatsFile.write("\n")
								 if(CurrFile in PowerValueCollection):
									 for CurrBB in (PowerValueCollection[CurrFile]):
										CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB))
										for CurrPower in (PowerValueCollection[CurrFile][CurrBB]):
											CurrStatsFile.write("\t "+str(round(float(CurrPower),4)))
								 else:
									CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB)+"\t error extracting power!!")
							elif(EnergyMeasure==0):
								for CurrFile in FileNameCollection:
									if(CurrFile in PowerValueCollection):
										CurrStatsFile.write("\n\t "+str(CurrFile))
									        for CurrPower in (PowerValueCollection[CurrFile]):
									                 CurrStatsFile.write("\t "+str(round(float(CurrPower),4)))
									else:
										CurrStatsFile.write("\n\t "+str(CurrFile)+"\t  error extracting power!!")
				                if(not(VectorExtract==0)):
				                	CurrStatsFile.write("\n\t\t Exe: \t\t\t\t BBID: \t\t ParamStart: "+str(VectorParamStart)+" Num-params: "+str(NumVectorParams))
				                	for CurrFile in FileNameCollection:
				                		CurrStatsFile.write("\n\t "+str(CurrFile))
				                		if(CurrFile in PredictionVectorParamsCollection):
				                			for CurrParam  in (PredictionVectorParamsCollection[CurrFile]):
				                				CurrStatsFile.write("\t "+str(CurrParam))
				                		else:
				                			print "\n\t Error with extracting param info! "



						CurrStatsFile.write("\n\n")
						CurrStatsFile.close()
					
					CurrStatsFileName=TempStatsFileName
					CurrStatsFile=open(CurrStatsFileName,'w')
					#AverageRuntimeCollection={}
					#PowerValueCollection={}
					FileNameCollection=[]						
					print "\n\t TempStatsFileName: "+str(TempStatsFileName)

				CurrStatsFile.write("\n\t *** Src File Name: "+str(CurrSrcFileParams[idx]['FileName']))
				#CompileSrc='mpicc -g -O3 '+str(FileName)+'.c /usr/lib64/libpapi.so -o '+str(FileName)
				ReplaceNumLoops(FileName,50)
				Compile(FileName,LibPapiPath)
				#sys.exit()
				
				RunOutputFile='RunOutput'+str(FileName)+'.log'
				RuntimeCollection=[]
				AverageRunTime=0.00000000010000001
				for i in range(AverageRun):
					RunCmd='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+' > '+str(RunOutputFile)
					commands.getoutput(RunCmd)
					RunOutput=open(RunOutputFile)
					for CurrLine in RunOutput:
						#print "\n\t CurrLine: "+str(CurrLine)
						CheckTime=re.match('^\s*.*app.*time\:',CurrLine)
						#CheckTime=re.match('\s*Run\-time',CurrLine)
						if CheckTime:
							#print "\n\t CurrLine: "+str(CurrLine)
							CheckRuntime=re.match('\s*.*app.*time\:\s*(\d+)*\.(\d+)*',CurrLine) # 
							#CheckRuntime=re.match('\s*.*Run\-time.*\:\s*(\d+)*\.(\d+)*',CurrLine) 
							if CheckRuntime:
								#CurrStatsFile.write("\n\t CheckRuntime: "+str(CheckRuntime.group(0)))
								Temp=CheckRuntime.group(1)+'.'+CheckRuntime.group(2)
								Temp=float(Temp)
								AverageRunTime+=Temp
								print "\n\t--Runtime--: "+str(Temp)
							else:
								print "\n\t ERROR: Cannot extract runtime! \n" 
								sys.exit()							
						
				if(AverageRun>0):
					AverageRunTime/=AverageRun
				AverageRuntimeCollection[FileName]=AverageRunTime
				FileNameCollection.append(FileName)
				MasterFileNameCollection.append(FileName)
				#sys.exit()
			
				if(InfoExtractionNeeded):	
					
					if(not(VectorExtract==0)):
                        	                CMDPebil='pebil --typ jbb --app '+str(FileName)
                	                        commands.getoutput(CMDPebil)
        	                                CMDJbb='mpirun -np 1 '+' ./'+str(FileName)+'.jbbinst'
	                                        commands.getoutput(CMDJbb)	
						jRunProcess='jRunTool --application '+str(FileName)+' --dataset standard --cpu_count '+str(NumofProcs)+' --processed_dir processed --scratch_dir scratch --raw_pmactrace `pwd` --process > Duh.log '
						print "\n\t -- "+str(jRunProcess)
						commands.getoutput(jRunProcess)
						print "\n\t ??? "
						jRunReport='jRunTool --application '+str(FileName)+' --dataset standard --cpu_count '+str(NumofProcs)+' --processed_dir processed --scratch_dir scratch --raw_pmactrace `pwd` --sysid 111 --functions default --loops default --report blockvector > Duh1.log '
						print "\n\t --- "
						commands.getoutput(jRunReport)
						print "\n\t jRunReport: "+str(jRunReport)
	                                        JbbFileName=str(FileName)+'.r00000000.t00000001.jbbinst'
        	                                JbbFileHandle=open(JbbFileName)
        	                                JbbFile=JbbFileHandle.readlines()
        	                                JbbFileHandle.close()
        	                                #BBFileName='BB_'+str(FileName)+'.txt'
        	                                #BBFile=open(BBFileName,'w')
   						BBIdx=1
						FuncIdx=5
						LineNumIdx=4
						DefIduIdx=23
						NumDefIduParams=5 # Idu, Fdu2, Idu2, Fdu2, Mdu2
						BBstoSearch=[]
       		                                for CurrLine in JbbFile:
        	                                        CheckBlk=re.match('\s*LPP',CurrLine)
                	                                if CheckBlk:
                        	                                BreakFields=re.split('\t',CurrLine)
                	                                        #print "\n\t CurrLine: "+str(CurrLine)+' #Fields: '+str(len(BreakFields))
                                	                        #CheckFuncVar=re.match('\s*FuncVar.*',BreakFields[6])
                                        	                CheckFuncVar=re.match('50',BreakFields[3])
                                                	        if CheckFuncVar:
                                                	                print "\n\t BBID: "+str(BreakFields[BBIdx])+" Function: "+str(BreakFields[FuncIdx])+" LineNm: "+str(BreakFields[LineNumIdx])                                        
                                                	                BBstoSearch.append(BreakFields[BBIdx])	
                                                	                #BBFile.write('\n\t '+str(BreakFields[BBIdx]))
						for CurrBB in BBstoSearch:
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
							
							PredictionVectorParamsCollection[FileName]=Temp
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
	
				        if( not (EnergySim==0)):
				         print "\n\t ------------------------------------------- EnergyMeasure: "+str(EnergyMeasure)				      
					 if(EnergyMeasure==0):

                                       		RunCmd='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+' > '+str(RunOutputFile)
                                       		commands.getoutput(RunCmd)
                                       		RunOutput=open(RunOutputFile)
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
                                       		                        #AverageRunTime+=Temp
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
					  	if(not(VectorExtract==0)):
                        	                 CMDPebil='pebil --typ jbb --app '+str(FileName)
                	                         commands.getoutput(CMDPebil)
        	                                 CMDJbb='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+'.jbbinst'
	                                         commands.getoutput(CMDJbb)	
						jRunProcess='jRunTool --application '+str(FileName)+' --dataset standard --cpu_count '+str(NumofProcs)+' --processed_dir processed --scratch_dir scratch --raw_pmactrace `pwd` --process > Duh.log '
						print "\n\t -- "+str(jRunProcess)
						commands.getoutput(jRunProcess)
						jRunReport='jRunTool --application '+str(FileName)+' --dataset standard --cpu_count '+str(NumofProcs)+' --processed_dir processed --scratch_dir scratch --raw_pmactrace `pwd` --report loopview > Duh1.log '
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
						sortBBs='python SortBBs.py -i processed/'+str(LoopViewStr)+' -o '+str(SortedBBsList)+' >Duh2.log'
						print "\n\t Cmd for SortBBs "+str(sortBBs)
						commands.getoutput(sortBBs)
						InsertEnergyProbes=' pebil --tool LoopIntercept --inp '+str(SortedBBsList)+' --app '+str(FileName)+' --lnc libpapi.so,libpapiinst.so '
						print "\n\t CMD InsertEnergyProbes: "+str(InsertEnergyProbes)
						commands.getoutput(InsertEnergyProbes)
						ObtainPowerValues='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+'.lpiinst > Duh3.log '
						commands.getoutput(ObtainPowerValues)
						
						EnergyStatsFileName=str(FileName)+'.meta_0.lpiinst'
						IpFile=open(EnergyStatsFileName)
						EnergyStatsFile=IpFile.readlines()
						IpFile.close()	
						
						BBIDFound=0
						BBIDline=-1
						RelevantThreadStatsFromBBLine=2
						BBID=-1
						for LineNum,CurrStats in enumerate(EnergyStatsFile):
						        #print "\n\t CurrStats: "+str(CurrStats)	
							CurrLineBreakdown=RemoveWhiteSpace(CurrStats).split('\t')
							LenCurrLineBreakdown=len(CurrLineBreakdown)
							if( (LenCurrLineBreakdown==1) and (CurrLineBreakdown[0]!='') ):
								CheckThread=re.match('\s*Thread\:.*',CurrLineBreakdown[0])
								if not CheckThread:
									BBIDFound=1
									BBIDLine=LineNum
									BBID=RemoveWhiteSpace(CurrLineBreakdown[0])			
									#print "\n\t BBID found!!! "
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
												Temp.append(RemoveWhiteSpace(CurrCounterReading))
										if(not ( FileName in PowerValueCollection)):
											PowerValueCollection[FileName]={}
										PowerValueCollection[FileName][BBID]=Temp	
								BBIDFound=0
								BBIDLine=-1
						if(CacheSimulation==0):
							DirName='Dir'+str(FileName)
							commands.getoutput('mkdir '+str(DirName))
							CMDMvFiles=' mv *'+str(FileName)+'.* '+str(DirName)	
							commands.getoutput(CMDMvFiles)
							CMDMvFiles=' mv *'+str(FileName)+' '+str(DirName)
							commands.getoutput(CMDMvFiles)
							CMDCpLoopVectors=' cp loopVectors.rALL  '+str(DirName);commands.getoutput(CMDCpLoopVectors)
					 elif(EnergyMeasure==2):	

						print "\t Streams: "+str(CurrSrcFileParams[idx]['Stream'])+" NumOperands "+str(CurrSrcFileParams[idx]['Ops'])
						NumOperands=((len(CurrSrcFileParams[idx]['Ops'])/int(CurrSrcFileParams[idx]['Stream']))+1)
						print "\n\t NumOperands: "+str(NumOperands)
						Iters=int( MaxIters/(NumOperands*int(CurrSrcFileParams[idx]['Stream'])*0.5))
						print "\t MaxIters: "+str(MaxIters)+" Iters: "+str(Iters)
						ReplaceNumLoops(FileName,10)#ReplaceNumLoops(FileName,Iters)
						ItersCollection[FileName]=Iters
						print "\n\t **************************** WARNING: ReplaceNumLoops has a dummy iteration count!!!! ********************************* "
						Compile(FileName,LibPapiPath)
						RunOutput=commands.getoutput('./'+str(FileName))
						print "\t RunOutput: "+str(RunOutput)
						
						#TempCmd='run_one_case.sh '+str(FileName)+' 2600000 '
						#TakeIt=commands.getoutput(TempCmd)
						#print "\n\t TakeIt: "+str(TakeIt)						
						AllFreqs={}
						FilePattern='app.out.'+str(FileName)+'*'
						LsOutput=commands.getoutput('ls '+str(FilePattern))
						if(LsOutput==''):
							print "\t ERROR: Unable to obtain file of the form "+str(FilePattern)
							sys.exit()
						
						AllFreqs=ExtractFilesAndFreqs(LsOutput)
						for CurrFreq in AllFreqs:
							print "\t LsFreq: "+str(CurrFreq)

						WattsFilePattern='raw_watts.'+str(FileName)+'*'
						WattsLsOutput=commands.getoutput('ls '+str(WattsFilePattern))
						WattsFreq=ExtractFilesAndFreqs(WattsLsOutput)
						for CurrFreq in WattsFreq:
							print "\t WattsFreq: "+str(CurrFreq)
						for CurrFreq in WattsFreq:
							WattsNotYetFound=True
							for CurrFile in WattsFreq[CurrFreq]:
								IpFile=open(CurrFile)
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
									AvgPower=float(TotalPowerSamples/len(CurrFileContents))
									print "\t File: "+str(CurrFile)+" Power: "+str(AvgPower)
									if(not(FileName in PowerValueCollection)):
										PowerValueCollection[FileName]={}
									PowerValueCollection[FileName][CurrFreq]=AvgPower
									WattsNotYetFound=False
									break
							if(WattsNotYetFound):
								print "\t ERROR: Not able to extract watts for frequency "+str(CurrFreq)
								PowerValueCollection[FileName][CurrFreq]="\t power measure not found!!! "
								#sys.exit()
						
						RaplWattsFilePattern='raw_rapl.'+str(FileName)+'*'
						RaplWattsLsOutput=commands.getoutput('ls '+str(RaplWattsFilePattern))
						RaplWattsFreq=ExtractFilesAndFreqs(RaplWattsLsOutput)
						
						PowerParams={}
						
						PowerParams['FreqParam0']=3;PowerParams['TotalPowerParam0']=4;PowerParams['IAPowerParam0']=7;PowerParams['GTPowerParam0']=10;PowerParams['DRAMPowerParam0']=13 #0-indexed
						PowerParams['FreqParam1']=16;PowerParams['TotalPowerParam1']=17;PowerParams['IAPowerParam1']=20;PowerParams['GTPowerParam1']=23;PowerParams['DRAMPowerParam1']=26 #0-indexed
						
						NumPowerParams=30
						for CurrFreq in RaplWattsFreq:
							print "\t RaplFreq: "+str(CurrFreq)
							RaplWattsNotYetFound=True
 							for CurrFile in RaplWattsFreq[CurrFreq]:
								IpFile=open(CurrFile)
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
										for CurrParam in PowerParams:
											ValueForParam=BreakdownParams[(PowerParams[CurrParam])]
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
										for CurrParam in PowerParams:
											SumOfPowerValues[CurrParam]/=NumSamples
											StrAvgPower+='\t'+str(SumOfPowerValues[CurrParam])
										print "\t File: "+str(CurrFile)+" Power: "+str(StrAvgPower)
										if(not(FileName in PowerValueCollection)):
											PowerValueCollection[FileName]={}
										PowerValueCollection[FileName][CurrFreq]=SumOfPowerValues
										RaplWattsNotYetFound=False
											
									else:
										print "WARNING: Rapl File "+str(CurrFile)+" has zero samples!! "
										
									break
							if(RaplWattsNotYetFound):
								print "\t ERROR: Not able to extract RaplWatts for frequency "+str(CurrFreq)
								PowerValueCollection[FileName][CurrFreq]="\t power measure not found!!! "
								#sys.exit()
								
									
						sys.exit()

					if(SimulationNeeded):
######
						if( (EnergySim==0) and (EnergyMeasure==1) ):
							
		                                       CMDPebil='pebil --typ jbb --app '+str(FileName)
                                		       commands.getoutput(CMDPebil)
                		                       CMDJbb='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+'.jbbinst'
		                                       commands.getoutput(CMDJbb)

	                                        JbbFileName=str(FileName)+'.r00000000.t00000001.jbbinst'
        	                                JbbFileHandle=open(JbbFileName)
        	                                JbbFile=JbbFileHandle.readlines()
        	                                JbbFileHandle.close()
        	                                BBFileName='BB_'+str(FileName)+'.txt'
        	                                BBFile=open(BBFileName,'w')
   						BBIDx=2
						FuncIdx=6
						LinUmIdx=5 
       		                                for CurrLine in JbbFile:
        	                                        CheckBlk=re.match('\s*LPP',CurrLine)
                	                                if CheckBlk:
                        	                                BreakFields=re.split('\t',CurrLine)
                	                                        #print "\n\t CurrLine: "+str(CurrLine)+' #Fields: '+str(len(BreakFields))
                                	                        #CheckFuncVar=re.match('\s*FuncVar.*',BreakFields[6])
                                        	                CheckFuncVar=re.match('.*\.c\:198',BreakFields[5])
                                                	        if CheckFuncVar:
                                                	                print "\n\t BBID: "+str(BreakFields[BBIdx])+" Function: "+str(BreakFields[FuncIdx])+" LineNm: "+str(BreakFields[LineNumIdx])                                        
                                                	                BBFile.write('\n\t '+str(BreakFields[BBIdx]))

                                     	  	BBFile.write("\n\n")
                                     	  	BBFile.close()
#####
						CMDPebilSim='pebil --typ sim --inp '+str(BBFileName)+' --app '+str(FileName)
						print "\n\t CMDPebilSim: "+str(CMDPebilSim) 
						commands.getoutput(CMDPebilSim)
						SimInstFile=str(FileName)+'.siminst'
						DirName='Dir'+str(FileName)
						CMDMkdir='mkdir '+str(DirName)
						commands.getoutput(CMDMkdir)
				
				#CurrStatsFile.write("\n\t AverageRunTime: "+str(AverageRunTime))
						FilesToExtract=[]
						if(ReuseWindow!=0):
							FilesToExtract.append('.dist')
						if(spatial!=''):
							if(spatial!=0):
								FilesToExtract.append('.spatial')
	
						for CurrSW in SpatialWindow:
						
							SimRunScript=open('SimRun.sh','w')
							print "\n\t CurrSW: "+str(CurrSW)
							SimRunScript.write('\n\t export METASIM_SAMPLE_ON=1 ')
							SimRunScript.write('\n\t export METASIM_SAMPLE_OFF=0 ')			
							MetasimReuseWindow='export METASIM_REUSE_WINDOW='+str(ReuseWindow)
							SimRunScript.write("\n\t "+str(MetasimReuseWindow))
							SimRunScript.write('\n\t export METASIM_SPATIAL_WINDOW='+str(CurrSW))
							MetasSimCacheSim='export METASIM_CACHE_SIMULATION='+str(CacheSimulation)
							SimRunScript.write('\n\t '+str(MetasSimCacheSim))			
							SimRunScript.write('\n\t export METASIM_ADDRESS_RANGE=1 ')	
							SimRunScript.write('\n\t ls '+str(FileName)+'*'+' > SimInstOutput.log')
							SimRunScript.write('\n\t ./'+str(SimInstFile))	
							SimRunScript.write('\n\n')							
							SimRunScript.close()
							commands.getoutput('sh SimRun.sh > SimInstOutput.log ')
					
							CurrStatsFile.write("\n\t Spatial Window: "+str(CurrSW)+"\n")
							for CurrExt in FilesToExtract:
								CurrExtFile=FileName+'.r00000000.t00000001'+str(CurrExt)
								DistFileHandle=open(CurrExtFile)
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
								commands.getoutput(MVCommand)
					
						CMDMvFiles=' mv *'+str(FileName)+' '+str(DirName)
						commands.getoutput(CMDMvFiles)
						CMDMvFiles=' mv *'+str(FileName)+'.* '+str(DirName)
						commands.getoutput(CMDMvFiles)
						CMDCpLoopVectors=' cp loopVectors.rALL  '+str(DirName);commands.getoutput(CMDCpLoopVectors)
							
				
	if(CurrStatsFile):
		CurrStatsFile.write("\n\t Average run times: ")
		CurrStatsFile.write("\n\t\t Exe: \t\t\t\t Average runtime ")
		for CurrFile in FileNameCollection:
			CurrStatsFile.write("\n\t "+str(CurrFile)+"\t\t "+str(AverageRuntimeCollection[CurrFile]))
		CurrStatsFile.write("\n\n")

                if(not(EnergySim==0)):
	                CurrStatsFile.write("\n\t Energy probes value: ")                   
			CurrStatsFile.write("\n\t Counters : ")
                        for CurrCounter in EnviVars:
                     		CurrStatsFile.write("\t "+str(CurrCounter))
                        CurrStatsFile.write("\n\t\t Exe: \t\t\t\t BBID: \t\t Power from each counter ")
                        
                        if(EnergyMeasure==1):
   				#CurrStatsFile.write("\n")
				#print "\n\t CurrFile: "+str(CurrFile)
				for CurrFile in FileNameCollection:
				 #CurrStatsFile.write("\n")
				 if(CurrFile in PowerValueCollection):
					 for CurrBB in (PowerValueCollection[CurrFile]):
        			        	CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB))
     	        	                	for CurrPower in (PowerValueCollection[CurrFile][CurrBB]):
							CurrStatsFile.write("\t "+str(round(float(CurrPower),4)))
				 else:
					 CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB)+"\t error extracting power!!")

			elif(EnergyMeasure==0):
				
				for CurrFile in FileNameCollection:
					if(CurrFile in PowerValueCollection):
						CurrStatsFile.write("\n\t "+str(CurrFile))
                                        	for CurrPower in (PowerValueCollection[CurrFile]):
                                                	 CurrStatsFile.write("\t "+str(round(float(CurrPower),4)))
					else:
						CurrStatsFile.write("\n\t "+str(CurrFile)+"\t error extracting power!!")
                if(not(VectorExtract==0)):
                	CurrStatsFile.write("\n\t\t Exe: \t\t\t\t BBID: \t\t ParamStart: "+str(VectorParamStart)+" Num-params: "+str(NumVectorParams))
                	for CurrFile in MasterFileNameCollection:
                		CurrStatsFile.write("\n\t "+str(CurrFile))
                		if(CurrFile in PredictionVectorParamsCollection):
                			for CurrParam  in (PredictionVectorParamsCollection[CurrFile]):
                				CurrStatsFile.write("\t "+str(CurrParam))
                		else:
                			print "\n\t Error with extracting param info! "
						

			CurrStatsFile.write("\n\n\n")
		CurrStatsFile.close()#"""

		MasterStatsFile.write("\n\t Average run times: ") ; 
		MasterStatsFile.write("\n\t\t Exe: \t\t\t\t Average runtime ")
		for CurrFile in MasterFileNameCollection:
			MasterStatsFile.write("\n\t "+str(CurrFile)+"\t\t "+str(AverageRuntimeCollection[CurrFile]))

                if(not(EnergySim==0)):
                         MasterStatsFile.write("\n\n\t Energy probes value: ")
                         MasterStatsFile.write("\n\t Counters : ")
                         for CurrCounter in EnviVars:
                                  MasterStatsFile.write("\t "+str(CurrCounter))
                         MasterStatsFile.write("\n\t\t Exe: \t\t\t\t BBID: \t\t Power from each counter ")
                         if(EnergyMeasure==1):
                                 #print "\n\t CurrFile: "+str(CurrFile)
                                 for CurrFile in MasterFileNameCollection:
					if(CurrFile in PowerValueCollection):		
                                	   for CurrBB in (PowerValueCollection[CurrFile]):
                                        	 MasterStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB))
	                                         for CurrPower in (PowerValueCollection[CurrFile][CurrBB]):
        	                                         MasterStatsFile.write("\t "+str(round(float(CurrPower),4)))
					else:
						MasterStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB)+"\t error extracting power!!")
                         elif(EnergyMeasure==0):
                                 for CurrFile in MasterFileNameCollection:
					if(CurrFile in PowerValueCollection):
	                                         MasterStatsFile.write("\n\t "+str(CurrFile))
        	                                 for CurrPower in (PowerValueCollection[CurrFile]):
                	                                  MasterStatsFile.write("\t "+str(round(float(CurrPower),4)))	
					else:	
						 MasterStatsFile.write("\n\t "+str(CurrFile)+"\t  error extracting power!!")
                if(not(VectorExtract==0)):
                	MasterStatsFile.write("\n\t\t Exe: \t\t\t\t BBID: \t\t ParamStart: "+str(VectorParamStart)+" Num-params: "+str(NumVectorParams))
                	for CurrFile in MasterFileNameCollection:
                		MasterStatsFile.write("\n\t "+str(CurrFile))
                		if(CurrFile in PredictionVectorParamsCollection):
                			for CurrParam  in (PredictionVectorParamsCollection[CurrFile]):
                				MasterStatsFile.write("\t "+str(CurrParam))
                		else:
                			print "\n\t Error with extracting param info! "

						
  
                MasterStatsFile.write("\n\n")
		MasterStatsFile.close()


	RemoveWorkingFiles='rm -f RunOutput.log SimRun.sh *Instr* Duh*.log'
	commands.getoutput(RemoveWorkingFiles)

if __name__ == "__main__":
   main(sys.argv[1:])

