Title: Ball Following Using Backpropagation
Author: Mislav Mandarić

Each folder is consisted of six Python scripts, two C programs (source and application) 
and three text files needed for execution of the application.

Python scripts:
	MMMemory.py - proxy class for the NaoQi API. It encapsulates NaoQi ALProxy "ALMemory".
	MMMotion.py - proxy class for the NaoQi API. It encapsulates NaoQi ALProxy "ALMotion".
	MMVision.py - proxy class for the NaoQi API. It encapsulates NaoQi ALProxy "ALVideoDevice".
	coding.py - module that has methods used in coding and decoding input and output 
				data. Methods for coding/decoding are used from other modules.
	collecting.py - module that is used for collecting data for training neural network. 
					It saves data in two text files (images.txt and joints.txt)
					Usage: collecting.py [IP] [PORT]
	running.py - module that is used for running the application. It creates text file 
				 image.txt where data for picture values is saved.
				 Usage: collecting.py [IP] [PORT]

C programs:
	NNTrain.exe - application for training neural network. It reads images.txt and joints.txt 
				  files and saves weights of the neural network in weights.txt text file.
				  Usage: NNTrain.exe
	NNRun.exe - application for running neural network and getting joint values. It uses 
				image.txt file for getting image data as inputs and weights.txt file for getting 
				values of weights of neural network. Returns joint values through standard output.

Global usage:
1. collecting.py is used for collecting data of input and desired output values of neural network. 
Images are stored in images.txt file and joints in joints.txt.
2. NNTrain.exe is used for training neural network. It will use images.txt and joints.txt and 
save wights values in weights.txt.
3. running.py is used for running the application. It saves image data in image.txt and calls 
NNRun.exe which runs neural network and returns joint values to running.py script via stdout.

NOTE: if file doesn't have usage description then it shouldn't be used on its own!
