from googlesearch import search  # Updated library for web search
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector
import csv
import re

# Configure MySQL connection
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2006",
            port=3307,
            database="scrapper"
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

# Global URL storage
urls = []

# Function to search organization URLs using Google Search
def search_organizations():
    query = org_entry.get().strip()
    if not query:
        messagebox.showwarning("Input Error", "Please enter an organization name.")
        return

    try:
        with open("web_urls.txt", "a") as file:
            for url in search(query, num_results=10):
                if url not in urls:
                    file.write(url + '\n')
                    urls.append(url)
        messagebox.showinfo("Success", f"URLs for '{query}' saved to 'web_urls.txt'.")
    except Exception as e:
        print(f"Error during search: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to scrape data from URLs
def scrape_urls():
    if not urls:
        messagebox.showwarning("No URLs", "Please search for URLs before scraping.")
        return

    try:
        # Configure Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=chrome_options)

        db = connect_to_db()
        if not db:
            return
        cursor = db.cursor()

        # Ask user to select an existing CSV file or create a new one
        csv_file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

        if not csv_file_path:
            messagebox.showwarning("File Save Cancelled", "Please select a location to save the file.")
            return

        data_extracted = []
        file_exists = False

        # Check if the file exists
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
                file_exists = True
        except FileNotFoundError:
            file_exists = False

        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write header only if the file is new
            if not file_exists:
                csv_writer.writerow(["Search Term", "Website", "Email", "Phone"])

            for url in urls:
                try:
                    print(f"Scraping {url}...")
                    driver.get(url)
                    html = driver.page_source

                    # Extract emails
                    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)

                    # Extract phone numbers
                    phones = re.findall(r"\b\d{10}\b|\b(?:\+91[-\s]?)?[6-9]\d{9}\b", html)

                    # Save extracted data
                    for email in emails:
                        phone = phones[0] if phones else None  # Take the first phone if available
                        entry = (org_entry.get(), url, email, phone)

                        if entry not in data_extracted:
                            data_extracted.append(entry)
                            csv_writer.writerow(entry)
                            cursor.execute(
                                "INSERT INTO contact (searchs, website, email, phone) VALUES (%s, %s, %s, %s)",
                                entry
                            )

                except Exception as scrape_error:
                    print(f"Error scraping {url}: {scrape_error}")

        db.commit()
        cursor.close()
        db.close()
        driver.quit()

        if data_extracted:
            result_box.delete("1.0", tk.END)
            for entry in data_extracted:
                result_box.insert(tk.END, f"Search Term: {entry[0]}, Website: {entry[1]}, Email: {entry[2]}, Phone: {entry[3]}\n")
            messagebox.showinfo("Scraping Complete", f"Data extracted successfully and saved to:\n{csv_file_path}")
        else:
            messagebox.showinfo("No Data", "No data found on the provided URLs.")

    except Exception as e:
        print(f"Scraping error: {e}")
        messagebox.showerror("Error", f"An error occurred during scraping: {e}")

# GUI Setup
root = tk.Tk()
root.title("Web Scraping Tool")
root.geometry("800x700")
root.configure(bg="#ffffff")

# Styles
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), background="#f1f1f1", foreground="#333333")
style.configure("TButton", font=("Helvetica", 12), background="#4CAF50", foreground="white", borderwidth=2, width=20)
style.configure("TEntry", font=("Helvetica", 12), padding=5)

# Header
header_frame = tk.Frame(root, bg="#4CAF50", pady=20)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Web Scraping Tool", font=("Helvetica", 22, "bold"), bg="#4CAF50", fg="white")
header_label.pack()

# Input frame
input_frame = tk.Frame(root, bg="#f1f1f1", pady=30)
input_frame.pack()

org_label = ttk.Label(input_frame, text="Enter Organization Name:")
org_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
org_entry = ttk.Entry(input_frame, width=40)
org_entry.grid(row=0, column=1, padx=10, pady=10)

search_button = tk.Button(root, text="Search and Save URLs", command=search_organizations)
search_button.pack(pady=10)

scrape_button = tk.Button(root, text="Scrape URLs", command=scrape_urls)
scrape_button.pack(pady=10)

# Result frame
result_frame = tk.Frame(root, bg="#f1f1f1", pady=20)
result_frame.pack()

result_label = ttk.Label(result_frame, text="Extracted Data:")
result_label.pack(anchor="w", padx=10)
result_box = tk.Text(result_frame, height=15, width=120, font=("Helvetica", 10), wrap=tk.WORD)
result_box.pack(padx=10, pady=10)

# Footer
footer_frame = tk.Frame(root, bg="#4CAF50", pady=20)
footer_frame.pack(fill="x", side="bottom")
footer_label = tk.Label(footer_frame, text="Developed by Abhishek Khursange", font=("Helvetica", 10), bg="#4CAF50", fg="white")
footer_label.pack()

root.mainloop()