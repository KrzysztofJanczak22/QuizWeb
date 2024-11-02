from flask import Flask, jsonify, request
import mysql.connector
import random
app = Flask(__name__)

def fn_Connect_SQL():
    global cursor
    mysql_config = {
        'user': 'krzysztof',
        'password': 'krzysztof',
        'host': 'localhost',  # np. 'localhost'
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

def fn_GetQuestion(cursor, v_category):
    query_question = f'SELECT ID, Content FROM Questions WHERE Category = {v_category} '
    cursor.execute(query_question)
    result_question = cursor.fetchall()
    id_rand = random.randint(0,len(result_question)-1)
    return result_question[id_rand][0],result_question[id_rand][1]


def fn_GetAnswer(cursor, v_idQuestion):
    query_answer = f'SELECT ID,Content FROM Answers WHERE IDQuestions = {v_idQuestion} '
    cursor.execute(query_answer)
    result_question = cursor.fetchall()
    return result_question

def fn_ReturnCorrect(cursor, v_id):
    query_correct = f'SELECT IsCorrect FROM Answers WHERE id = {v_id}'
    cursor.execute(query_correct)
    result_correct = cursor.fetchmany(1)
    return result_correct[0][0]



# Prosta trasa GET
@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})


@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()
    return jsonify({"received_data": data}), 201

@app.route('/api/Question/<int:category>', methods=['GET'])
def fn_SendQuesion(category):
    global cursor
    v_id,v_content = fn_GetQuestion(cursor,category)
    tab_answers = fn_GetAnswer(cursor,v_id)
    data = {
        'id': v_id,
        'content': v_content,
        'Answers': tab_answers
    }
    return jsonify(data)

@app.route('/api/Answer/<int:idQuestion>', methods = ['POST'])
def fn_SendAnswer(idQuestion):
    result = fn_ReturnCorrect(cursor,idQuestion)
    if result[0][0] == 1:
        correct = True
    else: correct = False
    data = {
        'correct':correct
    }
    return jsonify(data)

@app.route('/api/Correct/<int:idAnswer>',methods = ['GET'])
def fn_SendCorrect(idAnswer):
    global cursor
    v_correct = fn_ReturnCorrect(cursor,idAnswer)
    data = v_correct
    return str(data)



# Uruchomienie aplikacji
if __name__ == '__main__':
    connection, cursor = fn_Connect_SQL()
    fn_GetQuestion(cursor,200)
    app.run(debug=True)
