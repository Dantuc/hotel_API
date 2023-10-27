import sqlite3

connection = sqlite3.connect('hotel_database.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS hotels (hotel_id text PRIMARY KEY,\
      name text, stars real, daily real, city text)"

cursor.execute(create_table)
connection.commit()
connection.close()