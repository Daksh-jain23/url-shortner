from database import get_connection

conn = get_connection()

rows = conn.execute("SELECT * FROM urls").fetchall()

print("ID | Original URL")
print("-" * 50)

for row in rows:
    print(f"{row[0]}  | {row[1]}")

conn.close()