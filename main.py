import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai

# Configuration
API_KEY = os.environ.get("GEMINI_API_KEY")
SENDER_EMAIL = os.environ.get("EMAIL")
SENDER_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
YEAR_FOLDER = "2026"

def generate_news():
    client = genai.Client(api_key=API_KEY)
    
    prompt = f"""
    Act as a professional regional news editor for Telangana. Today is {TODAY}.
    Collect and summarize major news in these 10 categories: 
    1. Political, 2. Law & Order, 3. Welfare, 4. Economy/IT, 5. Accidents, 
    6. Culture, 7. Diplomatic, 8. Health/Edu, 9. Infrastructure, 10. Public Opinion.
    
    OUTPUT FORMAT:
    1. A detailed English summary for storage.
    2. A distinct section titled 'TELUGU_SUMMARY' containing the top 10 bulletins 
       formatted in clear Telugu with HTML tags like <h2>, <p>, and <li>.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def save_and_email(content):
    # Create directory if not exists
    os.makedirs(YEAR_FOLDER, exist_ok=True)
    file_path = f"{YEAR_FOLDER}/{TODAY}.txt"
    
    # Save the full response to the text file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    # Extract Telugu HTML part (assuming the model follows the prompt)
    telugu_html = content.split("TELUGU_SUMMARY")[-1].strip()

    # Create HTML Email
    msg = MIMEMultipart()
    msg['Subject'] = f"తెలంగాణ వార్తా వాహిని - {TODAY}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL

    html_body = f"""
    <html>
    <body style="font-family: 'Arial', sans-serif; line-height: 1.6; color: #333;">
        <div style="background-color: #f4f4f4; padding: 20px; border-bottom: 4px solid #007bff;">
            <h1 style="color: #007bff; margin: 0;">తెలంగాణ డైలీ బులెటిన్</h1>
            <p style="font-size: 1.1em; color: #555;">తేదీ: {TODAY}</p>
        </div>
        <div style="padding: 20px;">
            {telugu_html}
        </div>
        <div style="margin-top: 30px; padding: 15px; background: #eee; font-size: 0.8em; text-align: center;">
            <p>TelanganaVarthaVahini Automation System | Gemini AI powered</p>
            <p>© 2026 మీ వార్తా విశ్లేషణ విభాగం</p>
        </div>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html_body, 'html'))

    # Send Email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    full_content = generate_news()
    save_and_email(full_content)
