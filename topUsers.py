import sqlite3

def sort_users():
        try:
            conn = sqlite3.connect('memes.db')
            cursor = conn.cursor()
            update_top_users = "SELECT username, count(username) as repeticoes FROM memes_sent GROUP BY username ORDER BY repeticoes DESC LIMIT 5"
            cursor.execute(update_top_users)
            lines = cursor.fetchall()
 
        except sqlite3.Error as error:
            print(error)

        finally:
            conn.close()
            print("DB Connection Closed")
        
        return lines
