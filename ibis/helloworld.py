import ibis
import os

gphost     = os.environ.get('PGHOST')
gpdatabase = os.environ.get('PGDATABASE')
gppassword = os.environ.get('PGPASSWORD')
gpuser     = os.environ.get('PGUSER')
gpport     = 5432;

con = ibis.postgres.connect(
   user=gpuser,
   database=gpdatabase,
   port=gpport,
   password=gppassword,
   host=gphost
   )

table = con.table('news_people').limit(10)
p = table['people_csv']
results = p.execute()
for row in results:
    print(row)


