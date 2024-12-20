# Web-Scrapping-Project
Contact Miner: Extract, Save, and Manage Web Data

The Contact Miner project is a comprehensive web scraping tool designed to automate the process of extracting, saving, and managing organizational contact information from websites. Built with Python, the tool integrates seamlessly with MySQL databases using the mysql-connector library for data storage and utilizes HeidiSQL as the preferred database management interface. Additionally, scraped data is stored locally in CSV files, ensuring flexible and accessible record-keeping.

The tool leverages the Google Search API for sourcing organization URLs, which are then stored and processed. Selenium WebDriver is employed for scraping, utilizing Chrome in headless mode for efficiency. Extracted data includes emails and phone numbers, parsed using regular expressions from HTML page sources. The MySQL database schema is set up to store the search term, URL, email, and phone number in a structured format.

A user-friendly graphical interface is created using Tkinter, allowing users to input organization names, perform searches, and initiate scraping operations. The tool features real-time status updates, result display within the GUI, and CSV file export functionality. Styling elements ensure a clean and intuitive user experience.

This project highlights robust integration between data scraping, structured storage, and user interactivity, offering a complete solution for managing contact data.
