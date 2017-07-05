from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from lxml import html
import time, os, csv

#VirusTotal Sample Collector
#Author: Cam Nguyen

KEY_TERMS = "keyword.csv"
SAMPLE_NAMES = "sample_names.csv"
SAMPLE_PATH = r'/home/isec/samples'
SAMPLE_POSITIVES = " positives:50+"
#USERNAME = 'cnguyenUTA'
#PASSWORD = 'W1nter1scom1ng' 
USERNAME = 'jiangmingUTA'
PASSWORD = 'iseclab@uta'

#Parameters 
#terms -> Keywords for searching
#files -> Names of current files
def login(terms, files):
    #Select Driver for the appropiate Browser
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    driver = webdriver.Firefox(profile)
    #Request website
    driver.get("https://www.virustotal.com/intelligence/")

    #checks for the login form
    loginForm = driver.find_element_by_xpath("//form[@id='frm-signin']")

    #checks to see if it is visible
    if loginForm.is_displayed():
      #Finds the username and password fields to put password into
      passEle = driver.find_element_by_id("password")
      userEle = driver.find_element_by_xpath("//form[@id='frm-signin']//input[@id='username']")

      if userEle.is_displayed():
        userEle.clear()
        userEle.send_keys(USERNAME)
      else:
        print "No User"

      if passEle.is_displayed():
        passEle.clear()
        passEle.send_keys(PASSWORD)    
      else:
        print "Failed"

      time.sleep(1)
      driver.find_element_by_id("btn-sign-in").click()

    else:
      print "Not Found"

    time.sleep(2)

    #Searchs files
    search_bar = driver.find_element_by_name("query")
    
    if search_bar.is_displayed():
        search_bar.clear()
        search_bar.send_keys(terms[0] + SAMPLE_POSITIVES)
    else:
        print "Can not search"

    #Clicks the submit
    driver.find_element_by_id("btn-scan-file").click()
    time.sleep(5)
                     
    driver.find_element_by_xpath('//div//a[@id="btn-more-results"]').click()
    
    #creats a list of the sample links from the table
    link = driver.find_elements_by_xpath("//td//a[@class='sample-details']")
   
    previous_link = None
    try:
	    for element in link:
		hash_string = str(element.text)
		element.click()
		print hash_string
         
		#checks if the element was already downloaded
		if(binary_search(hash_string, files)):
		    print "File Exists"
		    time.sleep(1)
	      
		else:
		    print "In Else"
		    if len(hash_string) > 32: 
		        print "not MD5"
		        driver.find_element_by_xpath("//div//a[@class='btn filedownload']").click()
		        time.sleep(2)
		        driver.find_element_by_xpath('//div//a[@class="btn btn-primary"]').click()
		        files.append(element.text)
               
		    else:
		        print "Was MD5"
    except:
        print "No more list elements"
        update_list(files, SAMPLE_NAMES)

    time.sleep(2)
    
    
    #driver.close()

def update_list(files, file_name):
    with open(file_name, 'w+') as f:
        writer = csv.writer(f)
        writer.writerows([files])
 
#Loads csv files into a list
def load_file(file_name):
    with open(file_name) as term_file:
        for term in term_file:
          terms = term.split(',')
    return terms

def print_terms(terms):
    for term in terms:
        print term
    
#Writes all the files in the sample folder in a csv file
def log_all_files():
  files = []
  with open(SAMPLE_NAMES, "w+") as sample_file:
      w= csv.writer(sample_file)      
      for dirname, dirnames, filenames in os.walk(SAMPLE_PATH):
          for filename in filenames:
              w.writerow([filename])
              files.append(filename)
  return files

#Searchs for the sample in the sample set
def binary_search(sample,files):
    files = insertion_sort(files)
    high = len(files) - 1
    low = 0

    while low <= high:
        mid = (low + high) / 2
        if files[mid] < sample:
            low = mid + 1
        elif sample < files[mid]:
            high = mid - 1
        else:
            return mid
    return False

def insertion_sort(files):

    for x in range(1,len(files)):
        currentValue = files[x]
        position = x
        while position > 0 and files[position - 1] > currentValue:
            files[position] = files[position - 1]  
            position = position - 1
        files[position] = currentValue

    return files   

def main():
    term = load_file(KEY_TERMS)
    files = log_all_files()
    files = insertion_sort(files)
    login(term, files)
    
   
if __name__ == "__main__":
  main()
 


