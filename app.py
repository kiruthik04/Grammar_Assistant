from flask import Flask, render_template, request, jsonify
import language_tool_python  # Library to check grammar

app = Flask(__name__)

# Initialize the language tool (using English grammar checker here)
tool = language_tool_python.LanguageTool('en-US')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_grammar():
    user_text = request.form['text']
    
    if not user_text:
        return jsonify({'error': 'Please provide some text to check.'})
    
    # Check the grammar using LanguageTool
    matches = tool.check(user_text)
    corrected_text = language_tool_python.utils.correct(user_text, matches)
    
    # Collect suggestions (errors in the text)
    suggestions = []
    for match in matches:
        suggestions.append(f"Error: {match.message} at position {match.offset}-{match.offset + match.errorLength}")
    
    return jsonify({
        'corrected_text': corrected_text,
        'suggestions': suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)
