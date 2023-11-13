import os
import time
import psycopg2

# ==================================================
# Allt som behövs för att kommunicera med databasen

class DatabaseConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="host.docker.internal",
            database="postgres",
            user="postgres",
            password="postgres",
            port=5433
        )

    def is_enabled(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT preferences_value FROM public.preferences WHERE preferences_key='enabled';")
            result = cur.fetchone()[0]
            print('enabled?', result)
            return result
        finally:
            cur.close()

    def exists(self, number):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM public.results WHERE original = " + str(number))
            result = cur.fetchall()
            return len(result) > 0
        finally:    
            cur.close()

    def add(self, original, factors):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO public.results (original, factors, producer) VALUES (%s, %s, 1)", (str(original), factors))
            self.conn.commit()
        finally:    
            cur.close()

# ==================================================

# ALGORITM FÖR ATT PRIMTALSFAKTORISERA
def factorize(tal):
    factors = []

    factor = 2
    while factor < tal:
        if tal % factor == 0:
            factors.append(str(factor))    
            tal = int(tal / factor)
        else:
            factor += 1
    if factor > 1:
        factors.append(str(factor))

    return '*'.join(factors) if factors else str(tal)

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
    
START_NUMBER = int(os.environ.get("START_NUMBER"))
STEP_NUMBER = int(os.environ.get("STEP_NUMBER", "1"))
number = START_NUMBER

while True:
    # Kontrollera först om detta tal redan räknats ut, hoppa över isåfall
    if database.exists(number):
        number += STEP_NUMBER
        continue

    if not database.is_enabled():
        time.sleep(1)
        continue

    # Faktorisera detta tal
    result = factorize(number)

    # Spara i databasen
    database.add(number, result)

    # Gå vidare till nästa tal
    number += STEP_NUMBER

# ==================================================
