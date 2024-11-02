import json
import mysql.connector
import random

def fn_Connect_SQL():
    global cursor
    mysql_config = {
        'user': 'krzysztof',
        'password': 'krzysztof',
        'host': 'localhost',
        'database': 'Quiz',
    }
    try:
        connection = mysql.connector.connect(**mysql_config)
        print("Połączono z bazą danych!")

        # Tworzenie kursora
        cursor = connection.cursor()

        # Wykonywanie zapytania
        cursor.execute("SELECT DATABASE();")

        # Pobieranie wyników
        result = cursor.fetchone()
        print("Połączono z bazą:", result)
        return connection, cursor
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
    return None, None

def ImportQuestion(connection,cursor,filename='questions.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        questions = json.load(file)

    for question in questions:
        id = question["id"]
        content = question["question"]
        category = question["category"]
        query = """
               INSERT INTO Questions (id, Content, Category)
               VALUES (%s, %s, %s)
               """
        data = (id, content, category)

        cursor.execute(query, data)
        for answer in question["answers"]:
            a_content = answer["answer"]
            a_correct = answer["is_correct"]
            a_query = """
                          INSERT INTO Answers (Content, IsCorrect,IDQuestions)
                          VALUES (%s, %s, %s)
                          """
            a_data = (a_content, a_correct,id)

            cursor.execute(a_query, a_data)
        connection.commit()
connection, cursor = fn_Connect_SQL()

ImportQuestion(connection,cursor)