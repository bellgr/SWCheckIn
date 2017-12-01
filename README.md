# SWCheckIn
Southwest Check-In Tool

A lightweight Python script that utilizies Selenium to automatically check in to Southwest at exactly the 24 hour mark. The script then will send the confirmation to the specified phone number. If you need multiple check-ins, you can execute the script multiple times at once as needed. Also important, the script will start a browser session exactly 1 minute before check-in and continously attempt check-in until it's successful. 

Example:
python /opt/southwest/southwest.py -l Doe -f John -c JJQWC4 -p 5028759080 -t 'Nov 24 2017 12:40PM'

-l last name
-f first name
-c confirmation number
-p phone number for text of confirmation
-t exact time of flight

Installation:

1. Install Python and Selenium 
2. Get the latest chromedriver or use the one included
