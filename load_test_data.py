import os
import psycopg2
from unidecode import unidecode

conn = psycopg2.connect('postgres://jwimexnlvgbllw:o_wLus3ozh00LEr1_3MBqV_AMo@ec2-54-227-255-240.compute-1.amazonaws.com:5432/dfbuq9u9fol693')
cur = conn.cursor()
#cur.execute('create table test(t varchar(200));')


with open('/home/jsegura/5.txt') as f:
 
    name = 'despertar_hombre.txt'
    url = 'http://sdsfdfdfs.gfd'
    content = unidecode(f.read().replace("'",'').replace('"','')).casefold()
    content_hash = 'teyeduedgwuedguwgd'
    cur.execute("INSERT INTO documents (name,content,url,content_hash) VALUES ('{}','{}','{}','{}')".format(name,content,url,content_hash));
#    cur.execute("INSERT INTO test  VALUES ('{}')".format(i.strip()));

conn.commit()
conn.close()
