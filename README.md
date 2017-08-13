Scraper to get property information from AirBnB and save the results in a CSV file.

Dependencies:
  1. BeautifulSoup
  2. Selenium
  3. PhantomJS
  
This scraper makes us of Selenium and PhantomJS to create a browser object to run the javascript code. If requests, or urllib library is used, only the initial snapshot of the html source is returned. Hence, hidden items are not shown. Using the browser object enable javascript to be run.

Running the script:
```
python -m scraper --links-file /localtion/of/links/file
```
Hence:
```
python -m scraper --links-file airbnb_links.txt
```  
The results are saved in a csv file named results_time.csv.



 
