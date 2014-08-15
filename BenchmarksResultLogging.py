
import sys,getopt,subprocess,re,math,commands,time,copy,random

def usage():
	print "\n\t Usage: BenchmarksResultsLogging.py -l/--source file with all the source file that needs to be executed and logged -p <num-of-procs> -c CacheSimulationFlag <0/1> -r ReuseDistance -s SpatialDistanceFlag  -e EnergyMeasureFlag <0/1> -n Number of Counters -a Number of runs for averaging runtime. -p Number of Processors -d \n\t\t -s: .\n\t\t -d: Debug option, 1 for printing debug messages and 0 to forego printing debug statements. \n "
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

def main(argv):
	SrcFileName=''
	debug=0
	spatial=''
	reuse=''
	AverageRun=0
	CacheSimulation=0
	NumofProcs=''
	EnergySim=''
	NumCounters=''
	try:
	   opts, args = getopt.getopt(sys.argv[1:],"l:d:r:s:a:p:c:e:n:h:v",["list","deubg","reuse","spatial","average","procs","cachesim","energysim","numcounters","help","verbose"])
	except getopt.GetoptError:
		#print str(err) # will print something like "option -a not recognized"
	   usage()
	   sys.exit(2)
	verbose=False   
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
           else:
   		usage()

	# If execution has come until this point, the script should have already identified the config file.
	if(SrcFileName==''):
		usage()
	if( (CacheSimulation==0) and (spatial=='') and (reuse=='')):
		spatial="16,32"
		reuse='16'
		print "\n\t INFO: Using default spatial value: "+str(spatial)+" reuse value "+str(16)
	if(AverageRun==0):
		AverageRun=5
		print "\n\t INFO: Using default average run value: "+str(AverageRun)
	if(NumofProcs==''):
		NumofProcs=1
		print "\n\t INFO: Using default number of processors is: "+str(NumofProcs)

	if(NumCounters==''):
		NumCounters=0
		print "\n\t INFO: Using default flag for NumCounter: "+str(NumCounters)

	SpatialWindow=[]
	if(spatial!=''):
		ThisSet=re.split(',',spatial)
		for CurrSW in ThisSet:
			SpatialWindow.append(CurrSW)
	else:
		SpatialWindow.append(0)

        ReuseWindow=0
	if(reuse!=''):
		print "\n\t Reuse window:"+str(reuse)+"--"
		ReuseWindow=int(reuse)
	if(EnergySim==''):
		EnergySim=0
		print "\n\t Using default EnergySim value: "+str(EnergySim)
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

				TempStatsFileName='Stats'
				for CurrFeature in CurrSrcFileParams[idx]:
					#print "\n\t Feature: "+str(CurrFeature)+" value: "+str(CurrSrcFileParams[idx][CurrFeature])
					TempStatsFileName+='_'+str(CurrFeature)+'_'+str(CurrSrcFileParams[idx][CurrFeature])
				TempStatsFileName+='.log'
				#print "\n\t TempStatsFileName: "+str(TempStatsFileName)
				CurrSrcFileParams[idx]['FileName']=FileName
				if(CurrStatsFileName!=TempStatsFileName):
					if(CurrStatsFile):
						CurrStatsFile.write("\n\t Average run times: ")
						CurrStatsFile.write("\n\t\t Exe: \t\t\t\t Average runtime ")
						for CurrFile in FileNameCollection:
							CurrStatsFile.write("\n\t "+str(CurrFile)+"\t\t "+str(AverageRuntimeCollection[CurrFile]))
				                if(not(EnergySim==0)):
				                        CurrStatsFile.write("\n\n\t Energy probes value: ")
							CurrStatsFile.write("\n\t Counters : ")
							for CurrCounter in EnviVars:
								CurrStatsFile.write("\t "+str(CurrCounter))
				                        CurrStatsFile.write("\n\t\t Exe: \t\t\t\t BBID: \t\t Power from each counter ")
				                        for CurrFile in FileNameCollection:
                                				CurrStatsFile.write("\n")
				                        	for CurrBB in (EnergyValueCollection[CurrFile]):
                                					CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB))
			                                        	for CurrCounter in (EnergyValueCollection[CurrFile][CurrBB]):
										TmpPower=float(CurrCounter)/AverageRuntimeCollection[CurrFile]
                        			                        	CurrStatsFile.write("\t "+str(round(float(TmpPower),4)))


						CurrStatsFile.write("\n\n")
						CurrStatsFile.close()
					AverageRuntimeCollection={}
					FileNameCollection=[]
					CurrStatsFileName=TempStatsFileName
					CurrStatsFile=open(CurrStatsFileName,'w')
					AverageRuntimeCollection={}
					EnergyValueCollection={}
					FileNameCollection=[]						
					print "\n\t TempStatsFileName: "+str(TempStatsFileName)

				CurrStatsFile.write("\n\t *** Src File Name: "+str(CurrSrcFileParams[idx]['FileName']))

				RunOutputFile='RunOutput.log'
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
								#print "\n\t Runtime: "+str(Temp)
							else:
								print "\n\t ERROR: Cannot extract runtime! \n" 
								sys.exit()							
						
				AverageRunTime/=AverageRun
				AverageRuntimeCollection[FileName]=AverageRunTime
				FileNameCollection.append(FileName)
				#sys.exit()
			
				if( not( (ReuseWindow==0) and (spatial=='0') and (CacheSimulation==0) and (EnergySim==0)) ):	
					CMDPebil='pebil --typ jbb --app '+str(FileName)
					commands.getoutput(CMDPebil)
					CMDJbb='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+'.jbbinst'
					commands.getoutput(CMDJbb)
				        if( not (EnergySim==0)):	
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
						ObtainEnergyValues='mpirun -np '+str(NumofProcs)+' ./'+str(FileName)+'.lpiinst > Duh3.log '
						commands.getoutput(ObtainEnergyValues)
						
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
										if(not ( FileName in EnergyValueCollection)):
											EnergyValueCollection[FileName]={}
										EnergyValueCollection[FileName][BBID]=Temp	
								BBIDFound=0
								BBIDLine=-1
						if(CacheSimulation==0):
							DirName='Dir'+str(FileName)
							commands.getoutput('mkdir '+str(DirName))
							CMDMvFiles=' mv *'+str(FileName)+'.* '+str(DirName)	
							commands.getoutput(CMDMvFiles)
							CMDMvFiles=' mv *'+str(FileName)+' '+str(DirName)
							commands.getoutput(CMDMvFiles)
						
				        if( not (CacheSimulation==0) ):

######
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
							if(spatial!='0'):
								FilesToExtract.append('.spatial')
	
						for CurrSW in SpatialWindow:
						
							SimRunScript=open('SimRun.sh','w')
							print "\n\t CurrSW: "+str(CurrSW)
							SimRunScript.write('\n\t export METASIM_SAMPLE_ON=1 ')
							SimRunScript.write('\n\t export METASIM_SAMPLE_OFF=0 ')			
							MetasimReuseWindow='export METASIM_REUSE_WINDOW='+str(ReuseWindow)
							SimRunScript.write("\n\t "+str(MetasimReuseWindow))
							SimRunScript.write('\n\t export METASIM_SPATIAL_WINDOW='+str(CurrSW))
							SimRunScript.write('\n\t export METASIM_CACHE_SIMULATION=1 ')			
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
                        for CurrFile in FileNameCollection:
				CurrStatsFile.write("\n")
				#print "\n\t CurrFile: "+str(CurrFile)
				for CurrBB in (EnergyValueCollection[CurrFile]):
        		        	CurrStatsFile.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB))
     	                        	for CurrCounter in (EnergyValueCollection[CurrFile][CurrBB]):
						if AverageRuntimeCollection[CurrFile]:
							TmpPower=(float(CurrCounter)/AverageRuntimeCollection[CurrFile])
						else:
							CurrStatsFile.write("\t energy: ")							
                	                	#CurrStatsFile.write("\t ("+str(CurrCounter)+","+str(TmpPower)+")")
						CurrStatsFile.write("\t "+str(round(float(TmpPower),4)))

			CurrStatsFile.write("\n\n\n")
		CurrStatsFile.close()

	RemoveWorkingFiles='rm -f RunOutput.log SimRun.sh *Inst* Duh*.log'
	commands.getoutput(RemoveWorkingFiles)

if __name__ == "__main__":
   main(sys.argv[1:])

