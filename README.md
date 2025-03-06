# 📜 KLE Tech eResults CAPTCHA Bypass Exploit

## 🚨 Vulnerability: Persistent CAPTCHA Token Allows Mass Data Scraping

### **Overview**
We discovered a security vulnerability in the [KLE Tech eResults](https://eresults.kletech.ac.in) portal that allows **automated retrieval of student results** without solving multiple CAPTCHAs. The system fails to **generate a new CAPTCHA token** when navigating **back** to the results page, allowing an attacker to reuse the CAPTCHA token for **multiple requests**.  

This **flaw enables mass scraping of student records**, violating privacy policies and exposing sensitive academic data.  

---

## 🎯 **Vulnerability Type**
- **CAPTCHA Replay Attack**
- **Broken Authentication Mechanism**
- **Insecure Direct Object Reference (IDOR)**

---

## 🔍 **How the Exploit Works**
1. **Navigate to the eResults page** and enter a valid **USN** (University Seat Number).  
2. **Solve the CAPTCHA** and submit the request.  
3. **Intercept the request in Burp Suite**, capturing the **POST request** with the solved CAPTCHA.  
4. **Go back in the browser** and try entering a **different USN** → The CAPTCHA does not refresh.  
5. **Replay the intercepted request** with **modified USN values** while keeping the same CAPTCHA token.  
6. The server processes each request **without re-validating the CAPTCHA**, allowing retrieval of **any student's results**.

---

## 🔎 **Burp Suite Request & Response Analysis**

### **🔹 Original Request**
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
