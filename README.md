# Generate-Instrumentation-Profile
Through this Script we can Generate instrumentation profile for ClassLevel and MethodLevel

Dependencies
-------------
1:Machine should be Windows Machine
2:Python version 2.7 should be installed (Not Python 3.x)
3:ILDASM utility should be present in machine (ildasm path is installed:= C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.6.2 Tools\x64)

Syntax
-----------
python GenerateInsProf.py -P <path> -Z <Destination Folder path> -C <y/n> -M <y/n> -D <y/n>
 
   -P :- Provide the path for source code(DLLs) on which you want to operate this script
   -Z :- Provide the path for Destination Folder in which DLL files will be copied
   -C :- Provide "Y/y" to generate Instrumentation file for Class Level otherwise provide "N/n"
   -M :- Provide "Y/y" to generate Instrumentation file for Method Level otherwise profile "N/n"
   -D :- Provide "Y/y" to generate module.conf file otherwise provide "N/n"
 

Note:- All the file will get generated at same path from which you are running the script.
            There Should be a "IL" Folder in Destination Folder, in this folder our .il File gets copied.

 
eg:- python GenerateInsProf.py -P C:\Users\compass-409\Desktop\KohlsApps -Z F:\DLLFilesForDotNET -C y -M y -D y
   
     This will generate the Instrumentation file for both class level and method level , and will generate module.conf
    
eg:- python GenerateInsProf.py -P C:\Users\compass-409\Desktop\KohlsApps -Z F:\DLLFilesForDotNET -C n -M y -D y
 
     This will generate the Instrumentation file for method level , and will generate module.conf
