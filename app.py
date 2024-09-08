from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import io
import base64

app = Flask(__name__)

genai.configure(api_key='AIzaSyBEA78n_neLXQAeqd8Pdmuce7NOU2s7ARg')
model = genai.GenerativeModel('gemini-1.5-flash')

# Predefined prompt
PREDEFINED_PROMPT = """Analyze the uploaded screenshot(s) of the application. Based on the visible features and functionalities, generate a detailed set of test cases. Each test case should thoroughly examine a specific feature or functionality shown in the image(s).
For each identified feature, provide a test case with the following information:

Feature Name: Name of the feature being tested
Description: A brief description of what this test case is about
Preconditions: List of conditions that need to be set up or ensured before testing
Steps: Clear, step-by-step instructions on how to perform the test
Expected Result: What should happen if the feature works correctly

Important guidelines:

Analyze all visible elements, buttons, input fields, and apparent functionalities in the screenshot(s).
Create multiple test cases if a feature has various aspects or scenarios to test.
Ensure the steps are detailed and sequential, covering all necessary actions to test the feature thoroughly.
The expected result should clearly state what the tester should observe if the feature is working as intended.
If multiple screenshots are provided, consider how features might interact across different screens or states of the application.

Format your response as a numbered list of test cases, with each test case clearly separated and containing all the required information (Feature Name, Description, Preconditions, Steps, and Expected Result)."""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_prompt = request.form['prompt']
    image_data = request.form['image']
    
    # Combine predefined prompt with user input
    full_prompt = f"{PREDEFINED_PROMPT}{user_prompt}"
    
    # Convert base64 image to PIL Image
    image_data = base64.b64decode(image_data.split(',')[1])
    img = Image.open(io.BytesIO(image_data))
    
    # Generate content
    response = model.generate_content([full_prompt, img])
    response_text = response.text
    
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
