import os
from bs4 import BeautifulSoup

# Directory where the HTML files are stored
html_folder = "./"
output_file = "students_cgpa.txt"

# Open the output file in append mode to store results
with open(output_file, "a", encoding="utf-8") as out_file:
    
    # Loop through all USNs from 001 to 300
    for i in range(1, 301):
        filename = f"{html_folder}01fe22bcs{i:03d}.html"
        
        # Skip if the file does not exist
        if not os.path.exists(filename):
            print(f"Skipping {filename} (file not found)")
            continue

        # Read the HTML file and parse it with BeautifulSoup
        with open(filename, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # Extract the student name from the <h3> tag
        name_tag = soup.find("h3")
        student_name = name_tag.text.strip() if name_tag else "Unknown"

        # Extract CGPA from a <p> tag that follows an <h3> with text "CGPA"
        cgpa = "Not Found"
        for h3 in soup.find_all("h3"):
            if h3.text.strip() == "CGPA":
                cgpa_tag = h3.find_next("p")
                if cgpa_tag:
                    cgpa = cgpa_tag.text.strip()
                break

        # Write the extracted details to the output file
        out_file.write(f"{student_name}: {cgpa}\n")
        print(f"Extracted: {student_name} - CGPA: {cgpa}")

print(f"Process complete. Results saved in {output_file}.")

