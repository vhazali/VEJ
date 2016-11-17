# VEJ
Very Easy Job — A program to simplify the process of taint analysis using FlowDroid for android apps

### Dependencies to be installed in environment
1. [Java 8 Runtime Environment](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html)
2. [Python 3](https://www.python.org/download/releases/3.0/#download)

### Usage
1. Place the apk file(s) into the "apk" folder
2. Run the run.py (Windows) or run-mac.py (Mac) for taint analysis
3. Result, if any, will be placed in "sootOutput" folder

### To generate source sink list for a new android platform automatically
1. Create a new directory under android-platforms with the appropriate name
 1. You must use the android-\<api-number\> syntax to ensure that VEJ can find your android-platform
2. Place android.jar into the new directory
 1. Ensure that it is a fully-implemented Android JAR file and not one that ships with Google's Android SDK
 2. Platform JAR files that ships with Google's Android SDK contains method stubs and are not suitable for SuSi
 3. Fully-implemented Android JAR files can be extracted from an emulator or a real phone
3. Run the susi.sh to generate the new source sink lists
 1. For now we only support automation with a bash shell script
 2. Windows users may try running it with a bash shell or performing the steps manually
 
### To generate source sink list for a new android platform manually (Windows)
1. Create a new directory under android-platforms with the appropriate name
 1. You must use the android-\<api-number\> syntax to ensure that VEJ can find your android-platform
2. Place android.jar into the new directory
 1. Ensure that it is a fully-implemented Android JAR file and not one that ships with Google's Android SDK
 2. Platform JAR files that ships with Google's Android SDK contains method stubs and are not suitable for SuSi
 3. Fully-implemented Android JAR files can be extracted from an emulator or a real phone.
3. Then, open up cmd and go to the folder containing SuSi
4. The command to run SuSi manually is `java -Xmx4g -cp susi\weka.jar;flowdroid\soot-trunk.jar;flowdroid\soot-infoflow.jar;flowdroid\soot-infoflow-android.jar;susi\susi.jar de.ecspride.sourcesinkfinder.SourceSinkFinder <filepath> permissionMethodWithLabel.pscout out.pscout`
5. Upon completion, SuSi will produce multiple files. What we'll need is the `out_CatSources.pscout` and `out_CatSinks.pscout` files
6. Move the two files into the directory that you have created earlier in step 1