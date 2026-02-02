from flask import Flask, render_template , request 
app = Flask(__name__)

menu = ["Установка", "Первое приложение", "Обратная связь"]

@app.route('/', methods=["POST", "GET"]) 
def hello():
    if request.method == 'POST':
        print(request.form)
    return render_template('index.html', title="INDEX HTML", menu=menu)


@app.route('/about') 
def about():
    return render_template('about.html')


@app.route('/generalpage') 
def mainpage():
    return render_template('generalpage.html')


if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5000, debug=True)