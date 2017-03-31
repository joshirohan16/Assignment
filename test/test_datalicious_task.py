import unittest
import re,json,time
import urlparse,csv,os
from selenium import webdriver

class DataliciousTask(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.PhantomJS()
		print '\n Opening web driver'

	def test_task(self):
		driver = self.driver
		
		#open google.com url
		driver.get('https://www.google.com')
		print '\n -Opened url https://wwww.google.com'
		#assert title of webpage
		self.assertIn("Google",driver.title)
		print '\n -Asserted page title Google'

		#Enter Datalicious in google search text box
		driver.find_element_by_name('q').send_keys('Datalicious')
		print '\n -Set search box textbox with text "Datalicious" '
		#click on search icon
		driver.find_element_by_xpath("//input[@value='Google Search']").click()
		print '\n -Clicked on google search button'
		time.sleep(5)
		self.assertIn("Datalicious - Google Search", driver.title)
		print '\n -Page is on seacrhed results'
		
		#Click on the first link of search
		elements = driver.find_element_by_xpath("//h3/a").click()
		print '\n -Clicked on the first link of search results '
		time.sleep(5) 
		self.assertIn("Smarter Marketing | Datalicious",driver.title)
		print '\n -Asserted page title Smarter Marketing | Datalicious'
		
		#Check for network Http requests
		har_log =driver.get_log("har") 
		time.sleep(4)

		analytics,optima = [],[]
		result_flag = False

		print '\n -Extracting url links'
		#Find all the urls present in har_log
		url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', json.dumps(har_log))
		for my_url in url:
			optima_link = re.search("https://dc.optimahub.com/",my_url) #extract optimahub links
			if optima_link:
				result_flag = True
				optima.append(my_url)
			
			analytics_link = re.search("google-analytics",my_url) #extract google analytics links
			if analytics_link:
				analytics.append(my_url)

		if len(analytics) != 0:
			print '\n -Request to google analytics was made'
		else:
			print '\n -Request to google analytics was not made'
		
		if len(optima) != 0:
			print ' \n -Request to https://dc.optimushub.com was made'
		else:
			print '\n -Request to dc.optimushub.com was not made'



		for url in analytics:
			parsed = urlparse.urlparse(url)
			try:
				dt = urlparse.parse_qs(parsed.query)['dt']
				dl = urlparse.parse_qs(parsed.query)['dl']
				data = [['dt',dt],['dl',dl]]
				print '\n Extracted dt and dl values.'
				print'\n dt value :%s dl value: %s'%(dt,dl)
			except:
				pass

		#Write dt,dl values data to log.csv file
		#Note : dp values was not set but dl was set 
		
		length = len(data[0])
		csv_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','csv','log.csv'))
		
		print '\n -Writing dt and dl values to log.csv file'
		with open(csv_directory, 'wb') as testfile:
		    csv_writer = csv.writer(testfile)
		    for y in range(length):
		        csv_writer.writerow([x[y] for x in data])
	
	def tearDown(self):
		print '\n -Closing webdriver'
		self.driver.quit()

if __name__ == '__main__':
	unittest.main()