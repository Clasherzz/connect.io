# routes.py
from flask import Flask, request, jsonify
from functions import create_table, get_people_info, get_job_usefulness, sget_people_info, sget_job_usefulness, get_goods_info, get_goods_usefulness

app = Flask(__name__)

@app.route('/add_service', methods=['POST'])
def add_service():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    phone_no = data.get('phone_no')
    address = data.get('address')
    email_address = data.get('email_address')
    job = data.get('job')
    description = data.get('description')
    salary = data.get('salary')
    add_links = data.get('add_links')

    if not (name and age and gender and phone_no and address and email_address and job and description and salary and add_links):
        return jsonify({'error': 'Incomplete data'}), 400

    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute('''INSERT INTO services (name, age, gender, phone_no, address, email_address, job, description, salary, add_links) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (name, age, gender, phone_no, address, email_address, job, description, salary, add_links))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Service added successfully'}), 201

@app.route('/add_goods', methods=['POST'])
def add_goods():
    data = request.json
    name = data.get('name')
    volume = data.get('volume')
    quality = data.get('quality')
    certification = data.get('certification')
    pdt_desc = data.get('pdt_desc')
    pdt_price = data.get('pdt_price')
    owner_name = data.get('owner_name')
    owner_phone = data.get('owner_phone')
    owner_email = data.get('owner_email')

    if not (name and volume and quality and certification and pdt_desc and pdt_price and owner_name and owner_phone and owner_email):
        return jsonify({'error': 'Incomplete data'}), 400

    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute('''INSERT INTO goods (name, volume, quality, certification, pdt_desc, pdt_price, owner_name, owner_phone, owner_email) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (name, volume, quality, certification, pdt_desc, pdt_price, owner_name, owner_phone, owner_email))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Goods added successfully'}), 201

@app.route('/analyze_jobs', methods=['POST'])
def analyze_jobs():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt not provided'}), 400

    useful_jobs = get_job_usefulness(prompt)
    if not useful_jobs:
        return jsonify({'message': 'No useful jobs found for the given prompt'}), 200

    people_info = []
    for job in useful_jobs:
        job_info = get_people_info(job)
        people_info.extend(job_info)

    return jsonify({'people_info': people_info}), 200

@app.route('/sanalyze_jobs', methods=['POST'])
def sanalyze_jobs():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt not provided'}), 400

    useful_jobs = sget_job_usefulness(prompt)
    if not useful_jobs:
        return jsonify({'message': 'No useful jobs found for the given prompt'}), 200

    people_info = []
    for job in useful_jobs:
        job_info = sget_people_info(job)
        people_info.extend(job_info)

    return jsonify({'people_info': people_info}), 200

@app.route('/analyze_goods', methods=['POST'])
def analyze_goods():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt not provided'}), 400

    useful_goods = get_goods_usefulness(prompt)
    if not useful_goods:
        return jsonify({'message': 'No useful goods found for the given prompt'}), 200

    goods_infos = []
    for goods_name in useful_goods:
        goods_info = get_goods_info(goods_name)
        goods_infos.extend(goods_info)

    return jsonify({'goods_info': goods_infos}), 200

@app.route('/execute_command', methods=['POST'])
def execute_command():
    command1 = request.form.get('command')
    command = 'streamlit run streamlit1.py'
    if command:
        import subprocess
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode(), 200
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output.decode()}", 400
    else:
        return "No command provided", 400


