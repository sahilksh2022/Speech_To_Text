Prerequisites
Before running the script, ensure you have the following:
•	Python installed on your system (version 3.6 or higher).
•	Azure Cognitive Services subscription key and endpoint. You can obtain these from the Azure portal.
•	Install the Azure Cognitive Services Speech SDK using pip:
                     pip install azure-cognitiveservices-speech 


Usage
1.	Run the script by executing the following command:
                                            python audio.py
  	
3.	Fill in the required fields in the GUI:
•	API Key: Your Azure Cognitive Services subscription key.
•	Region: The region associated with your Azure Cognitive Services resource.
•	Input File Path: Path to the audio file you want to transcribe.
•	Output File Path: Path where you want to save the transcribed text.
•	Language: The language spoken in the audio file (e.g., "en-US" for English, "hi-IN" for Hindi).
5.	Click the Start Recognition button to initiate the transcription process.
6.	Once the transcription is complete, the status will be displayed in the GUI.
7.	If successful, the transcribed text will be saved to the specified output file path.

