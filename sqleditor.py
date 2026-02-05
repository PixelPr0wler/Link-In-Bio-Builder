import sqlite3

conn=sqlite3.connect('app.db')
cursor=conn.cursor()

cursor.execute("DROP")

conn.commit()
conn.close()