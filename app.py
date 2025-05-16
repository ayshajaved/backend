#Backend Code for SOlar Chatbot
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

class GeminiBot:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        genai.configure(api_key=api_key)
        
        # Updated configuration for Gemini 1.5 Flash
        self.generation_config = {
            "temperature": 1.1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config
        )
        
        # Initialize chat session with history
        self.chat_session = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": ["What services do you offer?"],
                },
                {
                    "role": "model",
                    "parts": [
                        """Assalam o Alaikum! As Solaiel, I offer three key services:

1. **Solaiel Chatbot:** I provide expert guidance on solar solutions.

2. **AI Solar Planning:** Our advanced service helps design your perfect solar system:
   - Input your roof size
   - Add your devices and usage patterns
   - Get detailed system specifications
   - Receive cost estimates and ROI analysis
   Visit our Solar Planner section to get started!

3. **Find Local Installers:** We connect you with verified solar professionals in your area.

How can I assist you today?"""
                    ],
                }
            ]
        )

    def get_gemini_response(self, user_input):
        try:
            # Check for solar planning related keywords
            planning_keywords = ["plan", "design", "system", "house", "home", "calculate"]
            installer_keywords = ["installer", "install", "professional", "engineer", "find", "near"]
            
            if any(keyword in user_input.lower() for keyword in planning_keywords):
                planning_response = """I'll help you with our AI Solar Planning service! Here's how it works:

1. Visit our Solar Planner section
2. Input your:
   - Roof size (in square feet)
   - List of electrical devices
   - Daily usage patterns

Our AI will then:
- Design an optimal solar system for your needs
- Calculate required components
- Provide detailed cost analysis in PKR
- Show expected ROI and savings

Would you like to try our AI Solar Planner now? Explore our service"""
                return planning_response

            # Check for installer related keywords
            elif any(keyword in user_input.lower() for keyword in installer_keywords):
                installer_response = """I'll help you find certified solar installers in your area! Here's how our Find Installers service works:

1. Visit our Find Installers section
2. Simply input your:
   - Location (city/area in Pakistan)
   - Project details (optional)

Our system will then:
- Show you verified installers near you
- Display their ratings and reviews
- Provide their expertise and experience
- Show their previous installations
- Help you get installation quotes

Would you like to find installers in your area now? Explore our service"""
                return installer_response

            # Regular chat response
            response = self.chat_session.send_message(user_input)
            return response.text

        except Exception as e:
            return f"Error: {str(e)}"

# Initialize GeminiBot
bot = GeminiBot()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        response = bot.get_gemini_response(user_message)
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)