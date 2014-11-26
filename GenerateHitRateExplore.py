#! /usr/bin/python
import sys,getopt,subprocess,re,math,commands,time,copy,random

def usage():
	print "\t python GenerateHitRateExplore.py -i/--input <Sample-Input-File> -m/--memorylevel <Memory being used>" #-m/--mod <Index-mod> -r/--ratecontrolbegin <RateControlBegin> -q/--ratecontrolend <RateControlEnd> 
	print "\t Accepted inputs for memory level: L1,L2,L3,Mem "
	print "\n"
	sys.exit()
	
def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output

def FileOpen(FileName,options=''):
	if(options==''):
		try:
			FileHandle=open(FileName)
		except IOError:
		 	print 'cannot open', FileName
	else:
		try:
			FileHandle=open(FileName,options)
		except IOError:
			print 'cannot open', FileName
			
	FileContents=FileHandle.readlines()
	FileHandle.close()
	return FileContents		

def main(argv):
	InputFileName=''
	MemoryLevel=''
	try:
		opts, args = getopt.getopt(sys.argv[1:],"i:m:",["input=","memorylevel="])	
	except getopt.GetoptError:
		#print str(err) # will print something like "option -a not recognized"
		usage()
	for opt, arg in opts:
		#print "\n\t Opt: "+str(opt)+" argument "+str(arg)	
		if opt in('-i', "--input"):
			InputFileName=RemoveWhiteSpace(arg)
			print "\t Input file name: "+str(InputFileName)
		elif opt in('-m', "--memorylevel"):
			MemoryLevel=RemoveWhiteSpace(arg)
			print "\t Memory level name: "+str(MemoryLevel)

		else:
			usage()
	if(InputFileName==''):
		usage()
	if(MemoryLevel==''):
		MemoryLevel='L1'
		print "\t INFO: Assuming default memory level: "+str(MemoryLevel)
		
	print "\n"
	LevelIndexMod=10
	Begin={};End={}
	Begin['LevelIndexMod']=10
	End['LevelIndexMod']=10
	Begin['RateControl']=0
	End['RateControl']=9
	#Begin['CacheLevel']=
	#End['CacheLevel']=
	
	SizeIdx=2 # Increment from 'mem-level' in FileName
	DSIdx=4
	OpsIdx=6
	PANIdx=8
	BreakdownParams=re.split('\_',InputFileName)
	ArraySize=''
	DS=''
	Ops=''
	PAN=''
	
	StopIdx=-1
	Prefix=''
	MemLevelParams=''
	for Idx,CurrParam in enumerate(BreakdownParams):
		if(CurrParam==MemoryLevel):
			print "\t Found MemoryLevel in param: "+str(CurrParam)
			print "\t Memory level at index: "+str(Idx)
			ArraySize=int(RemoveWhiteSpace(BreakdownParams[Idx+SizeIdx]))
			DS=RemoveWhiteSpace(BreakdownParams[Idx+DSIdx])
			Ops=RemoveWhiteSpace(BreakdownParams[Idx+OpsIdx])
			PAN=int(RemoveWhiteSpace(BreakdownParams[Idx+PANIdx]))
			print "\t ArraySize: "+str(ArraySize)+" DS "+str(DS)+" Ops "+str(Ops)+" PAN: "+str(PAN) 
			MemLevelParams=str(CurrParam)+'_Size_'+str(ArraySize)+'_DS_'+str(DS)+'_PAN_'
			StopIdx=Idx+PANIdx+1
			break
		else:
			Temp=str(CurrParam)+'_'
			Prefix+=str(Temp)

	Length=len(BreakdownParams)		
	Suffix=''
	for Idx in range(StopIdx,Length-1):	
		CurrParam=BreakdownParams[Idx]		
		Temp=str(CurrParam)+'_'
		Suffix+=str(Temp)
	Suffix+=str(BreakdownParams[Length-1])
	print "\t Prefix: "+str(Prefix)+" Suffix "+str(Suffix)
	
	HitRateControlParam='int\ '+str(MemoryLevel)+'HitRateControl\='
	IterationVarModParam='int\ '+str(MemoryLevel)+'IterationVarMod\='
	for CurrLevelIndexMod in range(Begin['LevelIndexMod'],End['LevelIndexMod']+1):
		for CurrRateControl in range(Begin['RateControl'],End['RateControl']+1):
			CurrPAN=CurrLevelIndexMod*(CurrRateControl+1);
			TempMemLevelParams=str(MemLevelParams)+str(CurrPAN)
			print "\t CurrPAN: "+str(CurrPAN)+" MemLevelParams "+str(TempMemLevelParams)
			NewFileName=str(Prefix)+str(TempMemLevelParams)+'_'+str(Suffix)
			CpCmd='cp '+str(InputFileName)+' '+str(NewFileName)
			print "\t CpCmd: "+str(CpCmd)
		
			commands.getoutput(CpCmd)
		
			ReplaceHitRateControl="perl -i -pe 's/"+str(HitRateControlParam)+"/"+str(HitRateControlParam)+str(CurrRateControl)+"\;\/\//g' "+str(NewFileName)
			commands.getoutput(ReplaceHitRateControl)
			print "\t ReplaceHitRateControl: "+str(ReplaceHitRateControl)
			
			ReplaceIterationVarMod="perl -i -pe 's/"+str(IterationVarModParam)+"/"+str(IterationVarModParam)+str(CurrLevelIndexMod)+"\;\/\//g' "+str(NewFileName)
			print "\t "+str(commands.getoutput(ReplaceIterationVarMod))
			print "\t ReplaceIterationVarMod: "+str(ReplaceIterationVarMod)

			#sys.exit()
				
		

if __name__=="__main__":
	main(sys.argv[1:])
