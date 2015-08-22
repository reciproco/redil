import os
import psycopg2
from unidecode import unidecode
from faker import Faker
fake = Faker('es_ES')

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
#cur.execute('create table test(t varchar(200));')


with open('definiti.txt') as f:

  for i in range(1000):
    name = unidecode(fake.name()).casefold()
    url = fake.url()
    content = unidecode(fake.address()).casefold()
    content_hash = 'teyeduedgwuedguwgd'
    cur.execute("INSERT INTO documents (name,content,url,content_hash) VALUES ('{}','{}','{}','{}')".format(name,content,url,content_hash));
#    cur.execute("INSERT INTO test  VALUES ('{}')".format(i.strip()));

conn.commit()
conn.close()
