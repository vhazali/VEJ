#!/bin/bash
set -o errexit
# check for correct invocation
if [ $# -ne 1 ]
  then
    echo "Usage: ./runSuSi.sh <path to new android jar>"
    exit 1
fi

# get filename and output directory
androidJarFile="$1"
outputDirectory=$(dirname $androidJarFile)

echo "Running SuSi on " $androidJarFile

java -Xmx4g -cp susi/weka.jar:flowdroid/soot-trunk.jar:flowdroid/soot-infoflow.jar:flowdroid/soot-infoflow-android.jar:susi/susi.jar de.ecspride.sourcesinkfinder.SourceSinkFinder $androidJarFile susi/permissionMethodWithLabel.pscout susi/out.pscout

# move output to correct folder for flowdroid
cp susi/out_CatSources.pscout $outputDirectory/out_CatSources.pscout
cp susi/out_CatSinks.pscout $outputDirectory/out_CatSinks.pscout

echo "SuSi successfully generated sources and sinks list. Stored in " $outputDirectory

# Cleaning susi folder
rm susi/out*
# Removing arff files used by susi
rm *.arff