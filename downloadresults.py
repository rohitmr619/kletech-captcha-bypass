import requests
import webbrowser

# Base URL for the eResults portal
base_url = "https://eresults.kletech.ac.in/index.php"
captcha_url = f"{base_url}?showCaptcha=True&instanceNo=0"

# Start a session to maintain cookies and avoid CAPTCHA refresh
session = requests.Session()

# Initialize session to keep CAPTCHA valid across multiple requests
print("Starting session...")
session.get(base_url)

# Fetch and display CAPTCHA in the browser
print("Retrieving CAPTCHA...")
captcha_response = session.get(captcha_url)

if captcha_response.status_code == 200:
    captcha_path = "captcha.jpg"
    with open(captcha_path, "wb") as file:
        file.write(captcha_response.content)

    print(f"CAPTCHA saved as {captcha_path}. Opening in browser...")
    webbrowser.open(captcha_path)
else:
    print("Failed to retrieve CAPTCHA.")
    exit()

# Prompt user to enter the CAPTCHA manually
captcha_value = input("Enter CAPTCHA value: ").strip()

# Ask for the starting USN to allow resuming downloads
start_usn = int(input("Enter starting USN (e.g., 192 to resume): ").strip())

# Store session cookies to ensure CAPTCHA stays valid
cookies = session.cookies.get_dict()

# Headers copied from Burp Suite for authenticity
headers = {
    "Origin": "https://eresults.kletech.ac.in",
    "Referer": "https://eresults.kletech.ac.in/index.php",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
}

# Loop through the USN range and fetch results
for i in range(start_usn, 301):
    usn = f"01fe22bcs{i:03d}"  # Format USN as per the expected pattern
    data = {
        "usn": usn,
        "osolCatchaTxt": captcha_value,  # Using the same CAPTCHA for all requests
        "osolCatchaTxtInst": "0",
    }

    print(f"Fetching results for {usn}...")

    # Send the request with stored cookies to maintain the session
    response = session.post(
        f"{base_url}?option=com_examresult&task=getResult",
        headers=headers,
        data=data,
        cookies=cookies,
    )

    # Check if CAPTCHA validation failed
    if "You have entered the wrong CAPTCHA sequence" in response.text:
        print("\nCAPTCHA validation failed. Please restart and enter the correct CAPTCHA.\n")
        break

    # Save the response as an HTML file for later processing
    filename = f"{usn}.html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.text)

    print(f"Saved: {filename}")

print("Process completed. All responses saved.")

