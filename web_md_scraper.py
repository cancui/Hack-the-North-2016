from bs4 import BeautifulSoup
import requests
import urllib2
import urllib
from pprint import pprint
#create a beautiful soup object to extract the URL information
#apply beautiful soup functions on URL

def get_wat_in()
	watson_input = "heart" #get value from watson
	return watson_input

def get_symptoms(outer_id, inner_id):
	url_outid = outer_id.replace(" ", "-") 
	url_inid = inner_id.replace(" ", "-")

	#specify the URL for the first category of possible injuries
	url = "http://www.sja.org.uk/sja/first-aid-advice/" + url_outid + "/" + url_inid ".aspx"
	content = urllib2.urlopen(urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()
	#parse html and store in 'BeautifulSoup' format
	soup = BeautifulSoup(content, "html.parser")
	symptoms = soup.ol.findAll('li') #change to findAll(ol)?

	symps = []
	for item in symptoms:
		symps.append(item.renderContents())
		print item.renderContents()

	symps2 = []
	for item in symps:
		temp1 = item.replace("\n", " ")
		temp2 = temp1.replace("\r", "")
		temp3 = temp2.replace("\xe2\x80\x93", "")
		symps2.append(temp3[3:]) #cuts off the numbers 

# for each item take each word and insert into a list
	symps_words = []
	for string in symps2:
		for item in string:
			symps_words.append(item)

	#str(symptoms)
	print symps_words

	return symps_words

def get_stoke_symp():

def get_choking_symp():

def get_bleeding_symp():

def get_spinal_symp():

def get_diabetic_symp():

def initializeCPR():


def main():

	watson_input = get_wat_in()

	h_symp1 = []
	h_symp2 = []
	h_symp3 = []
	h_symp4 = []
	b_symp1 = []
	b_symp2 = []
	b_symp3 =[]
	hd_symp1 = []
	hd_symp2 = []
	bd_symp1 = []
	bd_symp2 = []
	bm_symp1 = []
	bm_symp2 = []
	bm_symp3 = []
	hc_symp1 = []
	hc_symp2 = []
	hc_symp3 = []
	hc_symp4 = []
	hc_symp5 = []
	cur_symp = []

	#return symptoms for comparison
	if watson_input is "heart":
		h_symp1 = get_symptoms(watson_input, "angina attack")
		h_symp2 = get_symptoms(watson_input, "cardiac arrest")
		h_symp3 = get_symptoms(watson_input, "heart attack")
		h_symp4 = get_symptoms(watson_input, "shock")
		cur_symp = h_symp1 + h_symp2 + h_symp3 + h_symp4
	elif watson_input is "breathing":
		b_symp1 = get_symptoms(watson_input, "asthma attack") #may have an error
		b_symp2 = get_choking_symp() #need special case for choking adults
		b_symp3 = get_symptoms(watson_input, "hyperventilation")
		cur_symp = b_symp1 + b_symp2 + b_symp3
	elif watson_input is "head":
		hd_symp1 = get_symptoms(watson_input, "eye injuries")
		hd_symp2 = get_symptoms(watson_input, "head injuries")
		cur_symp = hd_symp1 + hd_symp2
	elif watson_input is "bleeding":
		bd_symp1 = get_symptoms(watson_input, "shock")
		bd_symp2 = get_bleeding_symp() #special case
		cur_symp = bd_symp1 + bd_symp2
	elif watson_input is "bones and muscles":
		bm_symp1 = get_symptoms(watson_input, "broken bones and fractures")
		bm_symp2 = get_symptoms(watson_input, "dislocated joints")
		bm_symp3 = get_spinal_symp() #second special case
		cur_symp = bm_symp1 + bm_symp2 + bm_symp3
	elif watson_input is "hot and cold conditions":
		hc_symp1 = get_symptoms(watson_input, "burns and scalds")
		hc_symp2 = get_symptoms(watson_input, "frostbite")
		hc_symp3 = get_symptoms(watson_input, "heat exhaustion")
		hc_symp4 = get_symptoms(watson_input, "heatstroke")
		hc_symp5 = get_symptoms(watson_input, "hypothermia")
		cur_symp = hc_symp1 + hc_symp2 + hc_symp3 + hc_symp4 + hc_symp5
	elif watson_input is "poisoning":
		p_symp1 = get_symptoms(watson_input, "alcohol posioning")
		cur_symp = p_symp1
	elif watson_input is "illnesses and conditions":
		ic_symp1 = get_symptoms(watson_input, "asthma attack")
		ic_symp2 = get_symptoms(watson_input, "allergic reactions")
		ic_symp3 = get_stoke_symp()
		ic_symp4 = get_symptoms(watson_input, "shock")
		ic_symp5 = get_symptoms(watson_input, "seizures fits in adults")
		ic_symp1 = get_diabetic_symp()
		cur_symp = ic_symp1 + ic_symp2 + ic_symp3 + ic_symp4 + ic_symp5
	elif watson_input is "loss of responsiveness":
		#might be sleeping or having a heart beat 
		initializeCPR() #could just ask questions
		return #when main is no longer the function identifier

	
	#req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	#query the website and return the html to the variable 'content'
	req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	content = urllib2.urlopen(req).read()
	#parse html and store in 'BeautifulSoup' format
	#soup = BeautifulSoup(content, "html.parser")
	#look at nested structure of html page
	#print soup.encode("utf-8")
	#print soup.prettify()
	
	#html tags are defined with the <a> tag
	#retrieve_links = soup.find_all("a")
	#print links using "href" attriute
	#for link in retrieve_links:
	#	print link.get("href").encode("utf-8") 



	#compare watsons keywords and entities plus our keywords (that we got from the website), compare user input against our keywords and the key, and synonyms
	#calculate the score or probability, indicator of probability, hard code
	# if something returns true, increases the probability that it is one of those injuries, match -> increment the score, pick that injury and provide treatment
	#go into the large category and record symptoms, one function to return symptoms in list

	#retrieve_links2 = soup.find_all("a")
	#pprint(soup2)
	

	#div = soup2.find("div", "col-sm-12")

	#pprint(div)
	#pprint(soup2.get_text())

	#letters = soup2.find_all("div", class_="col-sm-12")

	#pprint(soup2.ol)

	#print [e.text for e in symptoms]


if __name__ == '__main__':
	main()


