from flask import Flask
import time
import os
import psycopg2

DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'
PORT = os.environ.get('PORT')

class DatabaseConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="host.docker.internal",
            database="postgres",
            user="postgres",
            password="postgres",
            port=5433
        )

    def close(self):
        self.conn.close()

    def count(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM public.results WHERE producer = 1;")
            alpha_count = cur.fetchone()
            cur.execute("SELECT COUNT(*) FROM public.results WHERE producer = 2;")
            beta_count = cur.fetchone()
            return alpha_count[0], beta_count[0]
        except:
            return None, None
        finally:    
            cur.close()

    def latest(self):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT MAX(saved) FROM results;"
            )
            result = cur.fetchone()
            return result[0]
        except:
            return None
        finally:
            cur.close()

    def largest(self):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT original, factors, producer, saved FROM results ORDER BY original DESC LIMIT 1;"
            )
            result = cur.fetchone()
            return result[0], result[1], result[2], result[3]
        except:
            return None, None, None, None
        finally:    
            cur.close()

    def toggle(self):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE public.preferences SET preferences_value = 1 - preferences_value WHERE preferences_key='enabled';"
            )
            self.conn.commit()
        finally:
            cur.close()


app = Flask(__name__)

# Koppla upp mot databasen
database = None
while True:
    print('database?')
    try:
        database = DatabaseConnection()
        print('connected')
        break
    except:
        time.sleep(1)

 
@app.route('/')
def index():
    with open("index.html") as f:
        data = f.read()
    return data


@app.get('/stats')
def stats():
    global database

    if not database:
        return {
            'status': 'DB offline'
        }

    alpha_count, beta_count = database.count()
    largest_original, largest_factors, largest_producer, largest_saved = database.largest()
    latest = database.latest()

    return {
        'status': 'OK',
        'alpha_count': alpha_count,
        'beta_count': beta_count,
        'latest': latest,
        'largest_original': largest_original,
        'largest_factors': largest_factors,
        'largest_producer': largest_producer,
        'largest_saved': largest_saved,
    }
    

@app.get('/toggle')
def toggle():
    if not database:
        return {
            'status': 'DB offline'
        }

    database.toggle()
    print('toggled')
    return "OK"
 
 
if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=int(PORT))