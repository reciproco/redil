import os
import psycopg2
from unidecode import unidecode

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

with open('/home/sistemas/datos/1.txt') as f:
 
    name = 'despertar_hombre.txt'
    url = 'http://sdsfdfdfs.gfd'
    content = unidecode(f.read().replace("'",'').replace('"','')).casefold()
    content_hash = 'teyeduedgwuedguwgd'
    cur.execute("INSERT INTO documents (name,content,url,content_hash) VALUES ('{}','{}','{}','{}')".format(name,content,url,content_hash));
#    cur.execute("INSERT INTO test  VALUES ('{}')".format(i.strip()));

conn.commit()
conn.close()
