import requests
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .API import fn_GetQuestion,fn_CheckCorrect

def my_view(request):
    return HttpResponse("Hello, Django!")

def quiz_start(request):
    return render(request, 'index.html')


# your_app/views.py


from django.shortcuts import render, redirect
from django.http import HttpResponse


def get_question(request):
    message = ''
    if request.method == "POST":
        print("POST request received")

        try:
            category = int(request.POST.get('category'))
            answer = request.POST.get('answer')
            int_answer = int(answer)
        except (TypeError, ValueError) as e:
            print(f"Error parsing category or answer: {e}")
            return redirect('/')

        correct = fn_CheckCorrect(int_answer)

        if correct == '1':
            category += 100
            if category > 1000:
                return render(request,'win.html')
            else:
                message = 'Dobrze kolejne pytanie!'
                question_json = fn_GetQuestion(category)

            if not question_json or 'Answers' not in question_json or 'content' not in question_json:
                print("Error: fn_GetQuestion returned invalid data.")
                return HttpResponse("Error retrieving question data.", status=500)


            answers = question_json['Answers']
            question = question_json['content']
            print('pytanie')
            print(question)
            return render(request, 'question.html', {'answers': answers, 'question': question, 'category': category, 'message':message})
        else:
            print("Answer is incorrect, redirecting to home")
            return redirect('/')
    else:
        print("GET request received")
        category = 100
        question_json = fn_GetQuestion(category)

        if not question_json or 'Answers' not in question_json or 'content' not in question_json:
            print("Error: fn_GetQuestion returned invalid data on GET request.")
            return HttpResponse("Error retrieving question data.", status=500)

        answers = question_json['Answers']
        question = question_json['content']
        return render(request, 'question.html', {'answers': answers, 'question': question, 'category': category,'message':message})
