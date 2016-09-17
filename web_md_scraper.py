from bs4 import BeautifulSoup
import requests
import urllib2
import urllib
#create a beautiful soup object to extract the URL information
#apply beautiful soup functions on URL

def main():
	mystring = str(raw_input("Please enter your symptoms, seperated by commas: "))
	symptom_list = mystring.split(", ") #returns a list
	temp_string = "http://www.webmd.com/search/search_results/default.aspx?query="
	x = "%20"
	symptom_string = ""

	for index in range(len(symptom_list)):
		if index < (len(symptom_list) - 1):
			symptom_string = symptom_string + str(symptom_list[index]) + x
		else:
			symptom_string = symptom_string + str(symptom_list[index])

	#specify the URL
	print symptom_string
	url = temp_string + symptom_string
	print url
	req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	#query the website and return the html to the variable 'content'
	content = urllib2.urlopen(req).read()
	#parse html and store in 'BeautifulSoup' format
	soup = BeautifulSoup(content, "html.parser")
	#look at nested structure of html page
	#print soup.prettify()

	letters = soup.find_all("li")
	print type(letters)
	letters[0]

	#html tags are defined with the <a> tag
	retrieve_links = soup.find_all("a")
	#print links using "href" attriute
	for link in retrieve_links:
		print link.get("href") 


if __name__ == '__main__':

	main()

