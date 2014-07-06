
import sys,getopt,subprocess,re,math,commands,time,copy,random

def usage():
	print "\n\t Usage: BenchmarksResultsLogging.py -s/--source -d \n\t\t -s: file with all the source file that needs to be executed and logged.\n\t\t -d: Debug option, 1 for printing debug messages and 0 to forego printing debug statements. \n "
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
	try:
	   opts, args = getopt.getopt(sys.argv[1:],"l:d:r:s:a:h:v",["list","deubg","reuse","spatial","average","help","verbose"])
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
           else:
   		usage()

	# If execution has come until this point, the script should have already identified the config file.
	if(SrcFileName==''):
		usage()
	if( (spatial=='') and (reuse=='')):
		spatial="16,32"
		reuse='16'
		print "\n\t Using default spatial value: "+str(spatial)+" reuse value "+str(16)
	if(AverageRun==0):
		AverageRun=5
		print "\n\t Using default average run value: "+str(AverageRun)

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
	
	for idx,CurrSrcFile in enumerate(SrcFile):
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

				TempStatsFileName='Stats'
				for CurrFeature in CurrSrcFileParams[idx]:
					#print "\n\t Feature: "+str(CurrFeature)+" value: "+str(CurrSrcFileParams[idx][CurrFeature])
					TempStatsFileName+='_'+str(CurrFeature)+'_'+str(CurrSrcFileParams[idx][CurrFeature])
				TempStatsFileName+='.log'
				print "\n\t TempStatsFileName: "+str(TempStatsFileName)
				CurrSrcFileParams[idx]['FileName']=FileName
				if(CurrStatsFileName!=TempStatsFileName):
					if(CurrStatsFile):
						CurrStatsFile.write("\n\t Average run times: ")
						CurrStatfFile.write("\n\t\t Exe: \t\t\t\t Average runtime ")
						for CurrFile in AverageRuntimeCollection:
							CurrStatsFile.write("\n\t "+str(CurrFile)+"\t\t "+str(verageRuntimeCollection[CurrFile]))
						CurrStatsFile.write("\n\n")
						CurrStatsFile.close()
					else:
						CurrStatsFileName=TempStatsFileName
						CurrStatsFile=open(CurrStatsFileName,'w')
						print "\n\t Yaay!! "			

				CurrStatsFile.write("\n\t *** Src File Name: "+str(CurrSrcFileParams[idx]['FileName']))

				RunOutputFile='RunOutput.log'
				RuntimeCollection=[]
				AverageRunTime=0.0
				for i in range(AverageRun):
					RunCmd='./'+str(FileName)+' > '+str(RunOutputFile)
					commands.getoutput(RunCmd)
					RunOutput=open(RunOutputFile)
					for CurrLine in RunOutput:
						#print "\n\t CurrLine: "+str(CurrLine)
						#CheckTime=re.match('^\s*app.*time\:',CurrLine)
						CheckTime=re.match('\s*Run\-time.*\:',CurrLine)
						if CheckTime:
							CheckRuntime=re.match('\s*Run\-time.*\:\s*(\d+)*\.(\d+)*',CurrLine) # 
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
				#sys.exit()
			
				if( not( (ReuseWindow==0) and (spatial=='0')) ):	
					CMDPebil='pebil --typ jbb --app '+str(FileName)
					commands.getoutput(CMDPebil)
					CMDJbb='./'+str(FileName)+'.jbbinst'
					commands.getoutput(CMDJbb)
					JbbFileName=str(FileName)+'.r00000000.t00000001.jbbinst'
					JbbFileHandle=open(JbbFileName)
					JbbFile=JbbFileHandle.readlines()
					JbbFileHandle.close()
					BBFileName='BB_'+str(FileName)+'.txt'
					BBFile=open(BBFileName,'w')
				
					for CurrLine in JbbFile:
						CheckBlk=re.match('\s*BLK',CurrLine)
						if CheckBlk:
							BreakFields=re.split('\t',CurrLine)
							#print "\n\t CurrLine: "+str(CurrLine)+' #Fields: '+str(len(BreakFields))
							CheckFuncVar=re.match('\s*FuncVar.*',BreakFields[6])
							if CheckFuncVar:
								print "\n\t BBID: "+str(BreakFields[2])+" Function: "+str(BreakFields[6])							
								BBFile.write('\n\t '+str(BreakFields[2]))

					BBFile.write("\n\n")
					BBFile.close()
				
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
					
					CMDMvFiles=' mv *'+str(FileName)+'* '+str(DirName)
					commands.getoutput(CMDMvFiles)
							
				
	if(CurrStatsFile):
		CurrStatsFile.write("\n\t Average run times: ")
		CurrStatsFile.write("\n\t\t Exe: \t\t\t\t Average runtime ")
		for CurrFile in AverageRuntimeCollection:
			CurrStatsFile.write("\n\t "+str(CurrFile)+"\t\t "+str(AverageRuntimeCollection[CurrFile]))
		CurrStatsFile.write("\n\n")
		CurrStatsFile.close()
	RemoveWorkingFiles='rm -f RunOutput.log SimRun.sh *Inst* '
	commands.getoutput(RemoveWorkingFiles)

if __name__ == "__main__":
   main(sys.argv[1:])

