@echo off
TITLE SuSi

rem Check for correct usage
if ["%~1"]==[""] (
	echo Usage: susi.bat <path to new android jar>
	goto end
)

SET filepath=%~s1

rem Check for correct filepath supplied
if not exist filepath (
	echo file does not exist. Ensure that you have used the correct file path
	goto end
)

SET folderpath=%~dp1

echo Running SuSi on %filepath%

java -Xmx4g -cp susi\weka.jar;flowdroid\soot-trunk.jar;flowdroid\soot-infoflow.jar;flowdroid\soot-infoflow-android.jar;susi\susi.jar de.ecspride.sourcesinkfinder.SourceSinkFinder %filepath% permissionMethodWithLabel.pscout out.pscout

rem Move the categorised sink and source to correct folder
move susi\out_CatSources.pscout %folderpath%\out_CatSources.pscout
move susi\out_CatSinks.pscout %folderpath%\out_CatSinks.pscout

echo SuSi successfully generated sources and sinks list. Stored in %folderpath%

rem Cleanup files created by susi
del susi\out*
del *.arff

:end
PAUSE