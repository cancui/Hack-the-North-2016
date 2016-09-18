import os
import json
from os.path import join, dirname
from dotenv import load_dotenv

from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage
from watson_developer_cloud import NaturalLanguageClassifierV1 as NaturalLanguageClassifier

from recorder import Recorder

import pyaudio
import wave
import subprocess




class Word_manager(object):
	def __init__(self):
		self.synonym_groups = []
		self.keywords = ["cough", "headache"]

	def word_info(self, word):
		api_key = os.environ.get("WORDS_KEY")
		command = "curl --get --include 'https://wordsapiv1.p.mashape.com/words/" + word + "' -H 'X-Mashape-Key: " + api_key + "' -H 'Accept: application/json'"
		process = subprocess.Popen([command], shell = True, stdout=subprocess.PIPE)
		process_output = process.communicate()[0]
		
		returned_json = json.loads("{" + ((process_output.split("\n{"))[1]))
		print returned_json
		to_return = {}
		if 'results' in returned_json:
			if 'typeOf' in returned_json:
				to_return['type'] = returned_json['results'][0]["typeOf"]
			if 'derivation' in returned_json:
				to_return['derived_from'] = returned_json['results'][0]["derivation"][0]
			if 'synonyms' in returned_json:
				to_return['synonyms'] = returned_json['results'][0]["synonyms"]
		#to_return = {'type' : returned_json['results'][0]["typeOf"], 'derived_from' : returned_json['results'][0]["derivation"][0], 'synonyms' : returned_json['results'][0]["synonyms"]}
		print to_return

	def process_string(self, original_string):
		to_return = []

		first_processed = []
		
		for word in original_string.split():
			if len(word) < 3:
				continue
			elif word[-1] == "!" or word[-1] == "." or word[-1] == "," or word[-1] == "?":
				word = word[:-1]
			elif word[0] == "!" or word[0] == "." or word[0] == "," or word[0] == "?":
				word = word[1:]

			info = self.word_info(word)

			#all the stuff typeOf of symtoms can evaluate as
			if word in self.keywords or ( 'type' in info and ("symptom" in info['type'] or "ache" in info['type'] or "injury" in info['type'] or "disease" in info['type'])):
				first_processed.append(word)
				for item in info['synonyms']:
					first_processed.append(item)
		
		for word in first_processed:
			if word not in to_return:
				to_return.append(word)
		
		return to_return
		#
		
		#replace words with their derivatives


		#if word's type is 'symptom, add all synonyms to original string'


		#check for presence of self.keywords, add to to_return
		#for word in original_string:
		#	if word in self.keywords and word not in to_return:
		#		to_return.append(word)

	#curl --get --include 'https://wordsapiv1.p.mashape.com/words/bump/also' -H 'X-Mashape-Key: WgKtqH033PmshpStvNCFnC7STm0up1g9xv5jsniVszHkDunw1c' -H 'Accept: application/json'






def record_audio(file_name):
	#This block records audio into a .wav file
	recorder = Recorder(str(file_name))
	print("Please say something nice into the microphone\n")
	recorder.record_to_file()

def speech2text(file_name):
	returned_json = ""
	username = os.environ.get("BLUEMIX_USERNAME_S2T")
	password = os.environ.get("BLUEMIX_PASSWORD_S2T")
	speech_to_text = SpeechToText(username=username, password=password)
    #print join(dirname(__file__), path_to_audio_file)
	with open((str(file_name)), 'rb') as audio_file: #with open("/home/can/workspace/speech-sentiment-python/speech.wav", 'rb') as audio_file: 
		returned_json = speech_to_text.recognize(audio_file, content_type='audio/wav')
	#extracts the actual transcript
	transcript_text = returned_json['results'][0]['alternatives'][0]['transcript']	#(((returned_json.split("u'transcript': u'"))[0]).split("'}],"))[0]
	return transcript_text

def text2speech(text_to_say):
	#length_of_text = len(text_to_say.split())
	#print length_of_text

	username = os.environ.get("BLUEMIX_USERNAME_T2S")
	password = os.environ.get("BLUEMIX_PASSWORD_T2S")

	part1 = 'curl -X POST -u ' + username + ':' + password + ' '
	part2 = '--header "Content-Type: application/json" --header "Accept: audio/wav" '
	part3 = '--data "{\\\"text\\\":\\\"' + text_to_say + '\\\"}" '
	part4 = '--output returned_speech.wav "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"'

	bash_command = part1 + part2 + part3 + part4

	#execute command in Bash, requesting a .wav speech file by giving a text file to the text to speech API
	#subprocess.call([bash_command], shell=True)
	process = subprocess.Popen([bash_command], shell = True, stdout=subprocess.PIPE)
	output = process.communicate()[0]

	#define stream chunk   
	chunk = 1024  

	#open a wav format music  
	f = wave.open("returned_speech.wav","rb")  
	
	#instantiate PyAudio  
	p = pyaudio.PyAudio()  
	#open stream  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)  
	#read data  
	data = f.readframes(chunk)  

	#paly stream  
	while data != '':  
	    stream.write(data)  
	    data = f.readframes(chunk)  

	#stop stream  
	stream.stop_stream()  
	stream.close()  

	#close PyAudio  
	p.terminate()  

#Gets entities, key words, concepts
def analyze_user_input(text_to_analyze):
    alchemy_api_key = os.environ.get("ALCHEMY_API_KEY")
    alchemy_language = AlchemyLanguage(api_key=alchemy_api_key)
    sentiment_analysis = alchemy_language.sentiment(text=text_to_analyze)
    print "Sentiment: "
    if sentiment_analysis['docSentiment']['type'] == 'neutral':
        print 'netural', 0
    print sentiment_analysis['docSentiment']['type'], sentiment_analysis['docSentiment']['score']
    print ""

    print "Entities: "
    entity_analysis = alchemy_language.entities(text=text_to_analyze)
    for item in entity_analysis['entities']:
    	print item['text'], item['relevance']
    print ""

    print "Keywords: "
    keyword_analysis = alchemy_language.keywords(text=text_to_analyze)
    for item in keyword_analysis['keywords']:
    	print item['text'], item['relevance']
    print ""

    print "Concepts:"
    concept_analysis = alchemy_language.concepts(text=text_to_analyze)
    for item in concept_analysis['concepts']:
    	print item['text'], item['relevance']
    print ""

def get_injury_classification():
	username = os.environ.get("BLUEMIX_USERNAME_NLC")
	password = os.environ.get("BLUEMIX_PASSWORD_NLC")
	natural_language_classifier = NaturalLanguageClassifier(username=username, password=password)

	print natural_language_classifier.list()

def main():

	transcript1 = "My son is coughing uncontrollably. He's wheezing and can't speak. I'm very distressed. I'm not sure if he's chocking or suffocating."
	transcript1a = "I am coughing uncontrollably. I'm wheezing and can't speak. I'm very distressed. I'm not sure if I'm chocking or suffocating."
	transcript2 = "In 2009, Elliot Turner launched AlchemyAPI to process the written word, with all of its quirks and nuances, and got immediate traction. That first month, the company's eponymous language-analysis API processed 500,000 transactions. Today it's processing three billion transactions a month, or about 1,200 a second. That's a growth rate of 6,000 times over three years, touts Turner. Context is super-important, he adds. 'I'm dying' is a lot different than 'I'm dying to buy the new iPhone.' As we move into new markets, we're going to be making some new hires,\" Turner says. \"We knocked down some walls and added 2,000 square feet to our office.  We're providing the ability to translate human language in the form of web pages and documents into actionable data, Turner says. Clients include Walmart, PR Newswire and numerous publishers and advertising networks. This allows a news organization to detect what a person likes to read about, says Turner of publishers and advertisers."
	transcript3 = "I have very bad chest pain. I have shortness of breath. Pain is radiating to my left arm. Please send help."
	#text2speech("Welcome to X please tell me about the situation")
	#This block records audio into a .wav file
	#record_audio("speech.wav")

	#This block called Watson Speech to Text API to convert a .wav into text
	#returned_text = speech2text("speech.wav")

	#text2speech(returned_text)

	#text2speech("one one one two two two three three three four four four end")

	'''
	print "TEST1: "
	analyze_user_input("Hello, how are you my dear friend?")
	print ""

	print "Transcript 1 (targeting asthma attack): "
	analyze_user_input(transcript1)
	print ""

	print "Transcript 1a (targeting asthma attack in first person): "
	analyze_user_input(transcript1a)
	print ""

	print "Transcript 2 (online demo): "
	analyze_user_input(transcript2)
	print ""

	print "Transcript 3 (heart attack): "
	analyze_user_input(transcript3)
	print ""
	'''

	wm = Word_manager()
	wm.word_info("coughing")
	#get_injury_classification()

	print ""

	print wm.process_string(transcript1)

	#text2speech("Welcome to X please tell me about the situation")
	
	#record input
	#analyze input to make sure all key info is given
	#if not all info given,	ask for missing info

	#merge all the transcripts together, classify



	print "End of main()"


#Makes file executable via command line
if __name__ == '__main__':
	dotenv_path = join(dirname(__file__), '.env')
	load_dotenv(dotenv_path)

	main()
