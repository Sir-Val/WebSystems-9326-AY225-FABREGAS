#!/usr/bin/env python3
"""
Web Scraper for Student Data
Extracts student ID, name, course, and year from an HTML grade sheet
and saves the data to a CSV file.
"""

from bs4 import BeautifulSoup
import csv
import re


def scrape_student_data(html_file_path, output_csv_path):
    """
    Scrape student data from HTML file and save to CSV.
    
    Args:
        html_file_path (str): Path to the HTML file
        output_csv_path (str): Path where CSV file will be saved
    """
    # Read the HTML file with proper encoding (windows-1252 instead of utf-8)
    try:
        with open(html_file_path, 'r', encoding='windows-1252') as file:
            html_content = file.read()
    except UnicodeDecodeError:
        # If windows-1252 fails, try latin-1 as fallback
        with open(html_file_path, 'r', encoding='latin-1') as file:
            html_content = file.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all student rows (they have class="nav" and id starting with "msg")
    student_rows = soup.find_all('tr', class_='nav', id=re.compile(r'^msg\d+$'))
    
    # List to store student data
    students = []
    
    # Extract data from each row
    for row in student_rows:
        try:
            # Find all td elements in the row
            cells = row.find_all('td')
            
            # Extract student ID (2nd cell, within font tag)
            student_id_cell = cells[1].find('font')
            student_id = student_id_cell.text.strip() if student_id_cell else ''
            
            # Extract student name (3rd cell, within font tag)
            student_name_cell = cells[2].find('font')
            student_name = student_name_cell.text.strip() if student_name_cell else ''
            
            # Extract course (4th cell, within font tag)
            course_cell = cells[3].find('font')
            course = course_cell.text.strip() if course_cell else ''
            
            # Extract year (5th cell, within font tag)
            year_cell = cells[4].find('font')
            year = year_cell.text.strip() if year_cell else ''
            
            # Add to students list if we have at least student ID
            if student_id:
                students.append({
                    'Student ID': student_id,
                    'Student Name': student_name,
                    'Course': course,
                    'Year': year
                })
        
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
    
    # Write to CSV file
    if students:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Student ID', 'Student Name', 'Course', 'Year']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write student data
            for student in students:
                writer.writerow(student)
        
        print(f"Successfully scraped {len(students)} students")
        print(f"Data saved to: {output_csv_path}")
        
        # Display first few records as preview
        print("\nPreview of extracted data:")
        print("-" * 80)
        for i, student in enumerate(students[:5], 1):
            print(f"{i}. {student['Student ID']} | {student['Student Name']} | {student['Course']} | Year {student['Year']}")
        if len(students) > 5:
            print(f"... and {len(students) - 5} more students")
    else:
        print("No student data found in the HTML file")


if __name__ == "__main__":
    # Input and output file paths - UPDATE THESE PATHS TO MATCH YOUR FILE LOCATIONS
    input_html = "faculty_acad_contentFrame.html"  # Change this to your HTML file path
    output_csv = "students_data.csv"  # Change this to your desired output path
    
    # Run the scraper
    print(f"Reading HTML file: {input_html}")
    print(f"Output CSV file: {output_csv}")
    print("-" * 80)
    
    scrape_student_data(input_html, output_csv)