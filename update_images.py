import sqlite3

db_path = 'db.sqlite3'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sql_command = """
UPDATE app_aps_geolocalizacao
SET image = 'media/images/satellitee_47IEPNA.jpg';
"""
cursor.execute(sql_command)
conn.commit()

cursor.close()
conn.close()
