# functions.py
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

genai.configure(api_key= os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS services
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 age TEXT,
                 gender TEXT,
                 phone_no TEXT,
                 address TEXT,
                 email_address TEXT,
                 job TEXT,
                 description TEXT,
                 salary TEXT,
                 add_links TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS goods
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 volume TEXT,
                 quality TEXT,
                 certification TEXT,
                 pdt_desc TEXT,
                 pdt_price TEXT,
                 owner_name TEXT,
                 owner_phone TEXT,
                 owner_email TEXT)''')
    conn.commit()
    conn.close()

# Function to fetch people's information based on job title
def get_people_info(job_title):
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute("SELECT * FROM services WHERE job=?", (job_title,))
    rows = c.fetchall()
    conn.close()
    return rows

# Function to fetch distinct job titles
def get_jobs():
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT job FROM services")
    rows = c.fetchall()
    conn.close()
    return rows

# Example function to interact with Gemini API and get job usefulness
def get_job_usefulness(prompt):
    response = model.generate_content('you are being used in a website for filtering services , this is the usecase of user ['+prompt+'] and these are service titles available ['+str(get_jobs())+'] show output of the names of services suitable. The output should be in the same format string seperated by commas')
    return response.text.split(', ')

# Specialization related functions
def sget_people_info(job_desc):
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute("SELECT * FROM services WHERE description=?", (job_desc,))
    rows = c.fetchall()
    conn.close()
    return rows

def sget_jobs():
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute("SELECT description FROM services")
    rows = c.fetchall()
    conn.close()
    return rows

def sget_job_usefulness(prompt):
    response = model.generate_content('you are being used in a website for filtering services , this is the usecase of user ['+prompt+'] and the service experiences of each person given below  ['+str(sget_jobs())+'] select the experiences of services suitable. The output should be experiences seperated by commas')
    return response.text.split(', ')

# Goods related functions
def get_goods():
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT name FROM goods")
    rows = c.fetchall()
    conn.close()
    return rows

def get_goods_info(name_title):
    conn = sqlite3.connect('services.db')
    c = conn.cursor()
    c.execute("SELECT * FROM goods WHERE name=?", (name_title,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_goods_usefulness(prompt):
    response = model.generate_content('you are being used in a website for filtering goods , this is the usecase of user ['+prompt+'] and these are service titles available ['+str(get_goods())+'] show output of the names of goods suitable. The output should be in the same format string seperated by commas')
    return response.text.split(', ')
