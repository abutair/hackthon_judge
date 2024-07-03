from flask import Flask, request, jsonify
#from flask_cors import CORS
from ai import judge_idea
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/judge', methods=['POST'])
def judge():
    data = request.get_json()
    idea = data.get('idea')
    if not idea:
        return jsonify({'error': 'No idea provided'}), 400

    try:
        result = judge_idea(idea)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload_schedule', methods=['POST'])
def upload_schedule():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
        try:
            if file.filename.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)
            
            # Convert DataFrame to JSON
            schedule_json = df.to_json(orient='records')
            return jsonify({'schedule': schedule_json})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Allowed file types are .xlsx, .csv'}), 400

if __name__ == '__main__':
    app.run(debug=True)
