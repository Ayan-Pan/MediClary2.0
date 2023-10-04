from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# loading the saved models
diabetes_model = pickle.load(open("Saved_Models/diabetes_model.sav", "rb"))
heart_disease_model = pickle.load(open("Saved_Models/heart_disease_model.sav", "rb"))
parkinsons_model = pickle.load(open("Saved_Models/parkinsons_model.sav", "rb"))


def validate(request, model, msg_lst):
    msg = "Let's check!"
    color = "info"

    if request.method == "POST":
        data = np.array(request.form.getlist("data"))
        if len(data[data == ""]) > 0:
            msg = "Please enter all the fields!"
            color = "warning"
        else:
            num_data = [eval(i) for i in data]
            prediction = model.predict([num_data])

            if prediction[0] == 1:
                msg = msg_lst[0]
                color = "danger"
            else:
                msg = msg_lst[1]
                color = "success"

    return msg, color


@app.route("/", methods=["GET", "POST"])
def diabetes():
    msg_lst = ["The person is diabetic!", "The person is not diabetic!"]
    msg, color = validate(request, diabetes_model, msg_lst)
    return render_template("diabetes.html", msg=msg, color=color)


@app.route("/heart", methods=["GET", "POST"])
def heart():
    msg_lst = [
        "The person is having heart disease!",
        "The person does not have heart disease!",
    ]
    msg, color = validate(request, heart_disease_model, msg_lst)
    return render_template("heart.html", msg=msg, color=color)


@app.route("/parkinson", methods=["GET", "POST"])
def parkinson():
    msg_lst = [
        "The person has Parkinson's disease!",
        "The person does not have Parkinson's disease!",
    ]
    msg, color = validate(request, parkinsons_model, msg_lst)
    return render_template("parkinson.html", msg=msg, color=color)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
