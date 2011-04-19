@echo off
ECHO ----------------------------------------
echo Creating Confluence Build Folder
rmdir /S /Q skin.Big-cirrus.Extended
md skin.Big-cirrus.Extended
md skin.Big-cirrus.Extended\media

Echo .svn>exclude.txt
Echo Thumbs.db>>exclude.txt
Echo Desktop.ini>>exclude.txt
Echo dsstdfx.bin>>exclude.txt
Echo Build>>exclude.txt
Echo media>>exclude.txt
Echo exclude.txt>>exclude.txt

ECHO ----------------------------------------
ECHO Creating XBT File...
START /B /WAIT TexturePacker -input ..\skin.Big-cirrus.Extended\media -output .\skin.Big-cirrus.Extended\media\Textures.xbt

ECHO ----------------------------------------
ECHO XBT Texture Files Created...
ECHO Building Skin Directory...
c:\windows\system32\xcopy.exe "..\skin.Big-cirrus.Extended" "skin.Big-cirrus.Extended" /E /Q /I /Y /EXCLUDE:exclude.txt

del exclude.txt
ECHO Skin Created...
