import os
import psycopg2
from faker import Faker
fake = Faker('es_ES')

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
#cur.execute('create table test(t varchar(200));')

for i in range (1000):
    name = fake.name()
    url = fake.uri()
    content = fake.text()
    content_hash = fake.name()
    cur.execute("INSERT INTO documents (name,content,url,content_hash) VALUES ('{}','{}','{}','{}')".format(name,content,url,content_hash));

conn.commit()
conn.close()
