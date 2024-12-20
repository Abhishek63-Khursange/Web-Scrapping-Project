The Contact Miner project is an efficient web scraping tool designed to extract, save, and manage web-based contact data. Built with Python, this application leverages modern libraries and frameworks like tkinter for the GUI, selenium for web scraping, and mysql.connector for database connectivity. It allows users to search organization URLs via Google Search and scrape essential contact details such as emails and phone numbers from the retrieved websites. The application ensures smooth management of data through its integration with MySQL and local CSV files.

Key Features:
Google Search Integration:

Users can input an organization name, and the tool fetches relevant URLs using the googlesearch library.
All the retrieved URLs are stored in a text file (web_urls.txt), ensuring that links are saved separately for later use.
Web Scraping and Data Extraction:

Using Selenium WebDriver with headless Chrome mode, the tool visits each URL, scrapes the webpage's content, and extracts email addresses and phone numbers through regular expressions.
The scraped data is saved in both a MySQL database and a CSV file for offline use.
Database Connectivity:

The project uses MySQL for structured data storage, with tables designed to hold search terms, websites, emails, and phone numbers.
HeidiSQL serves as the database management interface, ensuring seamless interaction between the Python script and the database.
Local File Management:

CSV file support allows users to select or create a file to store the extracted data locally. This ensures data portability and easy access for further analysis.
User-Friendly GUI:

The application is powered by tkinter, providing a clean and interactive graphical interface.
Users can effortlessly input organization names, view search results, and monitor extracted data through a well-organized text box.
Error Handling and Notifications:

Robust error-handling mechanisms inform users of connection issues, invalid inputs, or any failures during the scraping process.
Notifications for successful data operations are displayed through message boxes.
This tool is ideal for users who need to automate the extraction and organization of contact information for market research or outreach purposes. The integration of MySQL and CSV ensures that data can be stored, managed, and shared effectively.

The project code and documentation are available on GitHub for further exploration and contribution. It is a robust solution for simplifying web data extraction and storage, enabling users to gather meaningful insights from the web efficiently.






