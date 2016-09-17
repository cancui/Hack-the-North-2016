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


from pprint import pprint

class Word_manager(object):
	def __init__(self):
		self.synonym_groups = [["unresponsive", "unconscious", "fainted"],["cough", "coughing"],["breath", "breathing"],["cold", "freezing"],["nausea", "nauseous"],["bleeding", "blood"],["spine","back"],["muscle", "muscles"],["bone", "bones"],["ache, headache"],["hurt", "pain", "painful", "crying"]]
		self.keywords = ["cough","wheezing","chocking", "suffocating", "rasping", "croaky", "anxious", "unresponsive", "chest", "pain", "shortness", "breath", "asthma", "cold", "hot", "burn", "skin", "blister", "seizure", "dehydrated", "hives", "shock", "can't", "face", "sharp", "object", "allergic", "numb", "nausea", "nauseous", "loss", "memory", "confused", "face", "head", "ache", "pupil", "conditions", "freezing", "weather", "outdoors", "shivering", "bleeding", "blood", "muscle", "muscles", "bones", "broken", "spine", "headache"]

	'''
	def word_info(self, word):
		api_key = os.environ.get("WORDS_KEY")
		command = "curl --get --include 'https://wordsapiv1.p.mashape.com/words/" + word + "' -H 'X-Mashape-Key: " + api_key + "' -H 'Accept: application/json'"
		process = subprocess.Popen([command], shell = True, stdout=subprocess.PIPE)
		process_output = process.communicate()[0]
		process.wait()
		if len(process_output.split("\n{")) < 2:
			return []
		returned_json = json.loads("{" + ((process_output.split("\n{"))[1]))
		returned_json_string = str("{" + ((process_output.split("\n{"))[1]))
		print returned_json
		to_return = {}
		if 'results' in returned_json:
			if u'typeOf' in returned_json_string:
				to_return['type'] = returned_json['results'][0][u"typeOf"]
			else:
				print "No typeof"
			if 'derivation' in returned_json_string:
				to_return['derived_from'] = returned_json['results'][0]["derivation"][0]
			else:
				print "No derivation"
			if 'synonyms' in returned_json_string:
				to_return['synonyms'] = returned_json['results'][0]["synonyms"]
			else:
				print "No synon"
		else:
			print "NOT MATCHED RESULTS"
		#to_return = {'type' : returned_json['results'][0]["typeOf"], 'derived_from' : returned_json['results'][0]["derivation"][0], 'synonyms' : returned_json['results'][0]["synonyms"]}
		return to_return

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
			if not info:
				continue
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
	'''
	def process_string(self, original_string):
		original_string = original_string.split(" ")
		to_return = []

		for word in original_string:
			if word[-1] == "." or word[-1] == ",":
				word = word[:-1]
			print word
			for wordlist in self.synonym_groups:
				if word in wordlist and word not in to_return:
					for item in wordlist:
						to_return.append(item)
			if word in self.keywords and word not in to_return:
				to_return.append(word)

		print to_return
		return to_return


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

    to_return = {}
    '''
    print "Sentiment: "
    if sentiment_analysis['docSentiment']['type'] == 'neutral':
        print 'netural', 0
    print sentiment_analysis['docSentiment']['type'], sentiment_analysis['docSentiment']['score']
    print ""
	'''
    to_return['sentiment'] = (sentiment_analysis['docSentiment']['type'], sentiment_analysis['docSentiment']['score'])

    to_return['entities'] = []
    print "Entities: "
    entity_analysis = alchemy_language.entities(text=text_to_analyze)
    for item in entity_analysis['entities']:
    	to_return['entities'].append((item['text'], item['relevance']))
    
    to_return['keywords'] = []
    print "Keywords: "
    keyword_analysis = alchemy_language.keywords(text=text_to_analyze)
    for item in keyword_analysis['keywords']:
    	to_return['keywords'].append((item['text'], item['relevance']))

    to_return['concepts'] = []
    print "Concepts:"
    concept_analysis = alchemy_language.concepts(text=text_to_analyze)
    for item in concept_analysis['concepts']:
    	to_return['concepts'].append((item['text'], item['relevance']))

    return to_return

def relative_similarity(wordlist1, wordlist2):
	similarity = 0
	for word in wordlist1:
		if word in wordlist2:
			similarity += 1

	return 1.0 * similarity / (0.5 * len(wordlist1) + len(wordlist2))

def get_injury_classification():
	username = os.environ.get("BLUEMIX_USERNAME_NLC")
	password = os.environ.get("BLUEMIX_PASSWORD_NLC")
	natural_language_classifier = NaturalLanguageClassifier(username=username, password=password)

	print natural_language_classifier.list()

def train_injury_classification(csv_file_location):
	username = os.environ.get("BLUEMIX_USERNAME_NLC")
	password = os.environ.get("BLUEMIX_PASSWORD_NLC")
	natural_language_classifier = NaturalLanguageClassifier(username=username, password=password)

	csvfile = open(csv_file_location)
	final_string = csvfile.readlines()
	#pprint(final_string)

	print natural_language_classifier.create(csv_file_location)

def main():

	transcript1 = "My son is coughing uncontrollably. Hes wheezing and can't speak. Im very distressed. Im not sure if hes chocking or suffocating."
	transcript1b = "burn skin coughing my boy swag wheezing super hot swag swag unconscious. Very hot and unconcious"
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




	#text2speech("Welcome to X please tell me about the situation")
	#This block records audio into a .wav file
	#record_audio("speech.wav")

	#This block called Watson Speech to Text API to convert a .wav into text
	#returned_text = speech2text("speech.wav")
	
	extracted_keywords = analyze_user_input(transcript1b)
	extracted_keywords = wm.process_string(extracted_keywords)

	wm = Word_manager()
	processed_string = wm.process_string(transcript1b)

	#text2speech("Welcome to X please tell me about the situation")
	
	#record input
	#analyze input to make sure all key info is given
	#if not all info given,	ask for missing info

	#merge all the transcripts together, classify
	



	#get_injury_classification()
	#train_injury_classification("/home/can/workspace/hack-the-north-2016/injury_training_data.csv")
	#train_injury_classification("/home/can/workspace/hack-the-north-2016/injury_training_data.csv")


	print "End of main()"


#Makes file executable via command line
if __name__ == '__main__':
	dotenv_path = join(dirname(__file__), '.env')
	load_dotenv(dotenv_path)

	main()

'''
help my friend just ate a peanut and he is allergic. it looks like an anaphylactic reaction. he can't breathe. his face is swelling,illnesses and conditions
this kid can barely breathe. her throat and tongue are swelling. she's anxious and wheezing. help i think she's going into shock,illnesses and conditions
my boyfriend has asthma and he can barely breathe. he forgot to take his medication. he won't stop wheezing. he is starting to turn blue,illnesses and conditions
help this person is having a seizure. they're flailing and arching their back and having convulsions. they might bite their tongue,illnesses and conditions
i think my friend is having a seizure. they're jerking around everywhere and are not responding. they lost bladder control,illnesses and conditions
help i think my mom had a stroke. she can only smile on one side of her face and can only lift one arm,illnesses and conditions
this person is struggling to speak and can only raise one arm. they are only smiling on one side,illnesses and conditions
i think my dad is having an allergic reaction. he can hardly breathe and i think he is going into shock,illnesses and conditions
i think my wife had a stroke. i can barely understand her and she only only move one side of her body,illnesses and conditions
my husband can't breathe. his throat is swelling and his skin is breaking out in hives and becoming blotchy,illnesses and conditions
eyes hurt and pain. eyelash stuck in eye,head
hit in the face. eye got hit. head hurts from sharp object,head
scalp hair head wound. is dissy and nautious from playing sports,head
friend confused and doesn't remember. loss of memory. hit in head and memory lost,head
dissy and confused. nausious and nausea exercising,head
confused and unresponsive. lost consciousness from dissy,head
her nose bleed and loss of blood from head. confused and loss of memory,head
unequal pupil size on eyes and hurts not respond to shake,head
head hurts blow to head football soccer rugby,head
friend has red skin and blisters. burned on stove. skin peeling and burnt,hot and cold conditions
her skin is hurting and peeling. yellow and fire at camp. they have blisters and hot,hot and cold conditions
was outside cold hurts. skin is numb and cold. person has hard and stiff skin black,hot and cold conditions
change in skin color on his face. thumbs hot and painful. outside winter ice snow,hot and cold conditions
she is hot cold outside winter skiing hurts skin on ice black numb,hot and cold conditions
tired and exhausted outside in heat hot headache. woman outside hot and cold,hot and cold conditions
dizzy and hot. he is confused and feeling sick and nausea tired exhausted,hot and cold conditions
shallow breathing headache hot warm humid outside playing sports and getting exercise. he is exhausted,hot and cold conditions
body temperature very high and confused. she is unresponsive and has flushed dry skin. outside hot weather,hot and cold conditions
he is camping sleeping outside cold and shivering. pale and confused,hot and cold conditions
man has slow breathing and is very tired. he says he is cold and confused. weak pulse shivering and cold,hot and cold conditions
oh my god help my friend is just lying there. there is so much blood. help he's in so much pain,bleeding
my mother fell and now she's bleeding. there is blood everywhere,bleeding
help sam just fell and now he's losing so much blood. i don't know how long he will last he's bleeding so much,bleeding
my friend just cut herself on a knife and now she's really bleeding. there is blood everywhere. i don't know what to do,bleeding
help my mom just fell onto a knife and she's losing so much blood. i think she's going into shock,bleeding
my father hurt himself and now he's bleeding everywhere. he's so pale and cold. and his pulse is so slow,bleeding
help my brother hurt himself and has lost so much blood he fainted. there is blood everywhere and his breathing is so shallow,bleeding
i'm hurt and the bleeding is so extensive i can barely think i'm so confused. i'm so cold and there is blood everywhere,bleeding
help help my boyfriend is bleeding god there is blood everywhere. he looks so pale and he looks so tired. i'm scared he will go into shock,bleeding
my friend was stabbed and her bleeding is severe. she looks so pale and faint. she's so cold and oh my god there is blood everywhere,bleeding
help my mother fell and i think she broke her leg. she's in so much pain. i can see the bone sticking out and there is so much swelling,bones and muscles
my boyfriend tripped and now he can't move his arm. i think it's broken. he has such a difficulty moving it,bones and muscles
my friend tripped and i think she broke something. her ankle looks twisted. it's sticking out at an odd angle. and there is this horrible sound,bones and muscles
it looks like this person was hit by something. they can barely move and their limbs appear twisted and broken,bones and muscles
this person was hurt. i think they dislocated their shoulder. they are in agony and they can barely move their arm,bones and muscles
it looks like someone has dislocated their knee. they can't walk and their leg is just hanging there,bones and muscles
someone fell and hurt their neck and back. im scared they've broken their spine. they can't feel anything below their hips,bones and muscles
this kid hurt himself and is having breathing difficulties. he dosen't have much feeling in his legs and his back and neck are in pain,bones and muscles
my brother slipped and landed on his back. i think he broke something. his neck is in pain and he can barely breathe,bones and muscles
they slipped and landed on their back. they may have injured their spine. they're back is in so much pain,bones and muscles
'''