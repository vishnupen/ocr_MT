from flask import Flask, jsonify, request
import os
from concurrent.futures import ThreadPoolExecutor
from run_ocr import ocr_function

app = Flask(__name__)

def perform_ocr_task(doc_path):
    result = ocr_function(doc_path)
    return result

@app.route('/perform_ocr', methods=['POST'])
def perform_ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join(os.getcwd(), 'uploaded_file.pdf')  # Save the file temporarily
        file.save(file_path)

        # num_threads = request.form.get('num_threads', default=4, type=int)

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(perform_ocr_task, file_path)
            result = future.result()

        os.remove(file_path)  # Remove the temporary file

        return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
