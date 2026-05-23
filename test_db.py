from database import engine

conn = engine.connect()

print("CONNECTED SUCCESSFULLY")

conn.close()