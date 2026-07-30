import os
import json
from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Resolve absolute paths for Vercel execution environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, '../templates'))

app = Flask(__name__, template_folder=TEMPLATE_DIR)

MODEL_NAME = "llama-3.3-70b-versatile"

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your local .env or production environment settings.")
    return Groq(api_key=api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/audit', methods=['POST'])
def audit_incident():
    try:
        data = request.get_json() or {}
        employment_status = data.get('employment_status', 'Full-time Corporate')
        narrative = data.get('narrative', '')
        
        if not narrative.strip():
            return jsonify({"error": "Narrative payload cannot be empty."}), 400
            
        client = get_groq_client()
        system_prompt = (
            "You are a rigorous employment law expert and strategic advisor. "
            "Analyze the worker's scenario based on their employment status. Identify exact potential regulatory violations "
            "and compute case severity metrics. You must return your analysis strictly in valid JSON format. "
            "Do not include markdown wrappers (e.g. ```json). Match this schema perfectly:\n"
            "{\n"
            "  \"violations\": [{\"title\": \"Violation Category Name\", \"explanation\": \"Precise analysis under labor law\"}],\n"
            "  \"severity\": \"Low\" | \"Medium\" | \"High\" | \"Critical\",\n"
            "  \"urgency_reason\": \"Why this severity status was assigned\",\n"
            "  \"statutory_deadlines\": \"Clear warnings concerning filing windows (e.g., EEOC 180/300-day thresholds)\"\n"
            "}"
        )
        user_content = f"Employment Class: {employment_status}\nUser Narrative: {narrative}"
        
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            model=MODEL_NAME,
            response_format={"type": "json_object"}
        )
        return jsonify(json.loads(completion.choices[0].message.content))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/escalate', methods=['POST'])
def design_escalation():
    try:
        data = request.get_json() or {}
        target_pathway = data.get('target_pathway', 'Internal Corporate HR')
        available_docs = data.get('available_docs', [])
        narrative = data.get('narrative', '')
        
        if not narrative.strip():
            return jsonify({"error": "Narrative payload must be present to map document pathways."}), 400
            
        client = get_groq_client()
        system_prompt = (
            "You are an executive legal communications strategist. Build a highly structured, emotionally objective, "
            "fact-focused grievance document tailored to the specified escalation endpoint. Also analyze missing documents. "
            "Return your final response strictly as raw JSON text matching this schema layout:\n"
            "{\n"
            "  \"grievance_draft\": \"Complete formal letter draft incorporating placeholders like [Your Name] and [Date]\",\n"
            "  \"evidence_gap_analysis\": [\"Prioritized list item identifying missing records or elements needed to solidify the argument\"]\n"
            "}"
        )
        user_content = (
            f"Escalation Channel Target: {target_pathway}\n"
            f"Documents Already Secured: {', '.join(available_docs) if available_docs else 'None'}\n"
            f"Incident Framework: {narrative}"
        )
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            model=MODEL_NAME,
            response_format={"type": "json_object"}
        )
        return jsonify(json.loads(completion.choices[0].message.content))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/deobfuscate', methods=['POST'])
def deobfuscate_policy():
    try:
        data = request.get_json() or {}
        policy_text = data.get('policy_text', '')
        
        if not policy_text.strip():
            return jsonify({"error": "Policy raw text space cannot be empty."}), 400
            
        client = get_groq_client()
        system_prompt = (
            "You are a contract compliance auditor. Translate convoluted employment terms or policy text into simple, "
            "straightforward English, explicitly highlighting hidden vulnerabilities or trick liabilities. "
            "Return the content in JSON syntax following this schema structure:\n"
            "{\n"
            "  \"plain_translation\": \"Clear layperson explanation of the statement's true meaning\",\n"
            "  \"hidden_loops_or_risks\": [\"Specific legal catch, loop, or risk item uncovered within the terms\"]\n"
            "}"
        )
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Policy segment to clean:\n{policy_text}"}
            ],
            model=MODEL_NAME,
            response_format={"type": "json_object"}
        )
        return jsonify(json.loads(completion.choices[0].message.content))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/timeline', methods=['POST'])
def generate_timeline():
    try:
        data = request.get_json() or {}
        narrative = data.get('narrative', '')
        
        if not narrative.strip():
            return jsonify({"error": "Narrative base text cannot be empty."}), 400
            
        client = get_groq_client()
        system_prompt = (
            "You are a legal cases evidence organizer. Transform messy, fragmented descriptions into an orderly chronological timeline. "
            "Format the output strictly as valid JSON parsing this schema:\n"
            "{\n"
            "  \"timeline\": [\n"
            "    {\n"
            "      \"date\": \"Extracted date or relative timestamp description\",\n"
            "      \"incident\": \"Brief descriptive title of event occurrence\",\n"
            "      \"details\": \"Condensed factual overview of this incident point\"\n"
            "    }\n"
            "  ]\n"
            "}"
        )
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract chronology from: {narrative}"}
            ],
            model=MODEL_NAME,
            response_format={"type": "json_object"}
        )
        return jsonify(json.loads(completion.choices[0].message.content))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    