import os
import psycopg2
from unidecode import unidecode


conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

with open('/home/jsegura/1.txt') as f:
 
    name = 'despertar_hombre.txt'
    path = 'http://sdsfdfdfs.gfd'
    mime = 'plain/text'
    utility = 'load_test'
    pages = 3
    content = unidecode(f.read().replace("'",'').replace('"','')).casefold()
    chash = 'teyeduedgwuedguwgd'
    cur.execute("INSERT INTO documents (name,path,mime,utility,pages,content,chash) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(name,path,mime,utility,pages,content,chash));
#    cur.execute("INSERT INTO test  VALUES ('{}')".format(i.strip()));

conn.commit()
conn.close()
