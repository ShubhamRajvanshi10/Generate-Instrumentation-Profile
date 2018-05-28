import optparse
import os
import re

def WriteMoveNext(ModuleName,FileObject,Level):
	if (Level == "C"):
		FileObject.write(ModuleName + "|;<.*>d__.*|MoveNext|0|0|" + "\n")
	if (Level == "M"):
		FileObject.write(ModuleName + "|<.*>d__.*|MoveNext|" + "\n")
	return

def Create_DLL_File(SourcePath , DestinationPath):
	DLLFile = open('DLLFiles.bat' , 'w')
	for root, dirs, files in os.walk(SourcePath, topdown=False):
		for name in files:
			withoutExt, Ext = os.path.splitext(name)
			Ext = Ext[1:].lower()
			if name.endswith("dll") | name.endswith("exe"):
				DLLFile.write("copy /Y " + os.path.join(root, name) +  " " +DestinationPath + "\\" + name + "\n")
				
	DLLFile.close()
	cwd=os.getcwd()
	os.system(cwd + "\DLLFiles.bat")
	return


def Create_IL_File(DestinationPath):
	ILFiles = open('KohlsIL.bat' , 'w')
	for root, dirs, files in os.walk(DestinationPath, topdown=False):
		for NameWithDLL in files:
			name, ext = os.path.splitext(NameWithDLL)
			ext = ext[1:].lower()
			if ext in ('dll', 'exe'):
				ILFiles.write("ildasm " + DestinationPath + "\\" + NameWithDLL + " /OUT=" + DestinationPath + "\IL\\" + NameWithDLL + ".il" + "\n")

	ILFiles.close()
	cwd=os.getcwd()
	os.system(cwd + "\KohlsIL.bat")
	return
	

def Create_Ins_file_ClassLevel(DestinationPath):
	print "##########Generating Instrumentation Profile at ClassLevel###########"
	ILPath = DestinationPath + "\IL\\"
	InstrProf = open('InstrProf_ClassLevel.txt', 'w')
	for root, dirs, files in os.walk(DestinationPath, topdown=False):
		for line in files:
			path=root + "\\" + line
			if line.endswith(".il"):
				NameWithOutDLL , Extra=line.split('.il')
				#WriteMoveNext(NameWithOutDLL,InstrProf,"C")
				with open(path, 'r') as ILfile:
					for lineForIL in ILfile:
						rec = lineForIL.strip()
						if "end of class" in rec:
							NoUse, FullClassName = rec.rsplit(" " , 1)
							InstrProf.write(NameWithOutDLL + "|" + FullClassName + "| |0|0\n")	 
	InstrProf.close()
	return

def Create_Ins_file_MethodLevel(DestinationPath):
	print "##########Generating Instrumentation Profile at MethodLevel##########"
	ILPath = DestinationPath + "\IL\\"
	InstrProf = open('InstrProf_MethodLevel.txt', 'w')
	for root, dirs, files in os.walk(ILPath, topdown=False):
		for line in files:
			path=root + "\\" + line
			if line.endswith(".il"):
				NameWithOutDLL , Extra=line.split('.il')
				#WriteMoveNext(NameWithOutDLL,InstrProf,"C")
				with open(path, 'r') as ILfile:
					for lineForIL in reversed(ILfile.readlines()):
						rec = lineForIL.strip()
						if "end of class" in rec:
							firstPart, FullClassName = rec.rsplit(" " , 1)
						if "end of method" in rec:
							FirstPart, MethodName = rec.split("::", 1)
							Nouse, ClassName = FirstPart.rsplit(" ", 1)
							if ClassName in FullClassName:
								if ".ctor" not in MethodName:
									if "<" not in FullClassName:
										 InstrProf.write(NameWithOutDLL + "|" + FullClassName + "|" + MethodName + "|0|0\n")
							
								 
	InstrProf.close()
	return
	
def Create_module_file(DestinationPath):
	print "##########Generating ModuleFile###########"
	SystemModule = ["#System Modules", "mscorlib.dll|", "System.Web.dll|", "System.dll|", "System.Data.dll|", "System.Data.OracleClient.dll|", "System.ServiceModel.Internals.dll|", "System.ServiceModel.Activation.dll|", "System.Web.Http.dll|<.*>d__.*|MoveNext|", "System.Web.Http.WebHost.dll|<.*>d__.*|MoveNext|", " " ,"#APPLICATION Modules"]
	with open('modules.conf', 'w') as MF:
		for line in SystemModule:
			MF.write(line + "\n")
		for root, dirs, files in os.walk(DestinationPath, topdown=False):
			for name in files:
				NameWithoutExt, ext = os.path.splitext(name)
				ext = ext[1:].lower()
				if name.endswith("dll") | name.endswith("exe"):
					WriteMoveNext(name, MF, "M")
					#MF.write(name + "|" + "\n")
	return

def main():
	parser = optparse.OptionParser("Usage %prog" + " -P <Source folder path>" + " -Z <DestinationPath >" + " -C <ClassLevel (Y/N)>" + " -M <MethodLevel (Y/N)>" + " -D <ModuleFile>")
	parser.add_option('-P', dest='SourcePath', type= 'string' , help= 'Specify the full path of source folder')
	parser.add_option('-C', dest='ClassLevel', type= 'string', help= 'Provide Y/N for Class level InstrProfile')
	parser.add_option('-M', dest='MethodLevel', type= 'string', help= 'Provide Y/N for Method level InstrProfile')
	parser.add_option('-D', dest='ModuleFile', type= 'string', help= 'Provide Y/N for Generating Module.conf InstrProfile')
	parser.add_option('-Z', dest='DestinationPath', type= 'string', help= 'Specify the full path of source folder')
	(options, args) = parser.parse_args()
	SourcePath = str(options.SourcePath)
	DestinationPath = str(options.DestinationPath)
	ClassLevel = str(options.ClassLevel)
	MethodLevel = str(options.MethodLevel)
	ModuleFile = str(options.ModuleFile)
	if (SourcePath == None):
		print ("[-] You must specify the path of Sorce Code")
		exit(0)
	if not os.path.exists(SourcePath):
		print "Path is not valid path:= " + SourcePath
	else:
		if not os.path.exists(DestinationPath):
			print " Destination path does not exists :- " + DestinationPath
		else:
			Create_DLL_File(SourcePath, DestinationPath)
			Create_IL_File(DestinationPath)
			if (ClassLevel == "Y") | (ClassLevel == "y") | (ClassLevel == None):
				Create_Ins_file_ClassLevel(DestinationPath)	
			if (MethodLevel == "Y") | (MethodLevel == "y"):
				Create_Ins_file_MethodLevel(DestinationPath)
			if (ModuleFile == "Y") | (ModuleFile == "y"):
				Create_module_file(DestinationPath)
		

main()
