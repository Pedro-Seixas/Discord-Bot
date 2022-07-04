import mysql.connector
from mysql.connector import Error

def sort_users():
        try:
            connection = mysql.connector.connect(host='remotemysql.com', database='lQcUi31XZz', user='lQcUi31XZz', password='8nIEHO3Rx3')
            update_top_users_table = "SELECT autor, count(autor) as repeticoes FROM top_users GROUP BY autor ORDER BY repeticoes DESC LIMIT 5"
            cursor = connection.cursor()
            cursor.execute(update_top_users_table)
            linhas = cursor.fetchall()
 
        except Error as erro:
            print(erro)

        finally:
            if(connection.is_connected()):
                connection.close()
                print("Conexao ao MySQL finalizada")
        
        return linhas
