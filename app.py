from flask import Flask, render_template, request
import google.genai as genai
import os
from dotenv import load_dotenv
load_dotenv()  # 👈 this loads .env into environment


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY environment variable not set!")

client = genai.Client(api_key=API_KEY)

# Home route - inspection form
@app.route("/")
def index():
    return render_template("form.html")

# Process form submission
@app.route("/generate", methods=["POST"])
def generate():
    # Collect form inputs
    site = request.form["site"]
    inspector = request.form["inspector"]
    date = request.form["date"]
    equipment = request.form["equipment"]
    safety = request.form["safety"]
    environment = request.form["environment"]
    notes = request.form["notes"]

    # Combine inputs into structured inspection text
    inspection_text = f"""
    Oil Plant Inspection Report
    Site: {site}
    Inspector: {inspector}
    Date: {date}

    Equipment Condition:
    {equipment}

    Safety Observations:
    {safety}

    Environmental Observations:
    {environment}

    Additional Notes:
    {notes}
    """

    # Ask Gemini Flash to generate a structured professional HTML report
    prompt = f"""
    You are a professional inspection report generator for oil plants.
    Based on the following inspection notes, generate a structured **HTML report** 
    with the following sections:
    
    1. Executive Summary  
    2. Risk Assessment & Prioritization (list hazards with severity ratings and recommended actions)  
    3. Corrective Action Plan (specific tasks, stakeholders, and timeline)  
    
    Ensure it looks like an official report with headings, bullet points, and professional tone.

    Inspection Notes:
    {inspection_text}
    """

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )

    report_html = response.text

    return render_template("report.html", report=report_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
