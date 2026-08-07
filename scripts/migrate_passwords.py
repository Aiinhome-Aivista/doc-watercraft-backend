import os
import sys

# Ensure the project root is on the Python path so we can import the database module
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import bcrypt
from database.db_connection import get_db_connection

def migrate():
    """Migrate clear‑text passwords to bcrypt hashes.

    This script reads all rows from the `users` table, skips passwords that are already
    bcrypt hashes (identified by the `$2b$` prefix), hashes the remaining clear‑text
    passwords, and updates the rows in‑place.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users")
    for user_id, clear_pw in cursor.fetchall():
        # If the password column already contains a bcrypt hash, leave it unchanged
        if isinstance(clear_pw, str) and clear_pw.startswith("$2b$"):
            continue

        # Convert possible non‑string values to string before hashing
        clear_pw_str = str(clear_pw)
        hashed = bcrypt.hashpw(clear_pw_str.encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            "UPDATE users SET password=%s WHERE id=%s",
            (hashed, user_id),
        )
    conn.commit()
    conn.close()
    print("Migration complete")

if __name__ == "__main__":
    migrate()
