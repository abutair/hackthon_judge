from flask import Flask, request, jsonify
#from flask_cors import CORS
from ai import judge_idea
import pandas as pd
from io import BytesIO
import zipfile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/judge', methods=['POST'])
def judge():
    data = request.get_json()
    idea = data.get('idea')
   
    if not idea:
        return jsonify({'error': 'No idea provided'}), 400
    
    code = ""
   # Check for additional file uploads in request.files
    if 'code_file' in request.files:
        code_file = request.files['code_file']
        logger.info(f"Received file: {code_file.filename}")
        logger.info(f"File content type: {code_file.content_type}")
        logger.info("loading files ")

        if code_file.filename.endswith('.zip'):
            with zipfile.ZipFile(code_file, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    logger.info(f"Processing file in zip: {file_info.filename}")
                    if file_info.filename.endswith('.py') or file_info.filename.endswith('.txt'):
                        with zip_ref.open(file_info.filename) as file:
                            file_content = file.read().decode('utf-8')
                            logger.info(f"Extracted file content: {file_content}")
                            code += "\n" + file_content
        else:
            code += "\n" + code_file.read().decode('utf-8')
            logger.info(f"Read file content: {code}")
            logger.info('i am here')
    else :
        logger.info('no document attached !')


    logger.info(f"Final combined code: {code}")
    try:
        result = judge_idea(idea, code)
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
