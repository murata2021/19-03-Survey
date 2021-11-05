from flask import Flask,request,render_template,redirect,flash
from surveys import Question,Survey,satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension



app=Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"              ##DebugToolbar configuration
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


RESPONSES=[]                                           ##initialization of responses
resp_dict={str(q_num): " " for q_num in range(len(satisfaction_survey.questions))}


@app.route("/")
def show_homepage():

    return render_template("home.html",title=satisfaction_survey.title,instructions=satisfaction_survey.instructions)


@app.route("/questions/<q_number>")
def show_question1(q_number):

    if list(resp_dict.values()).count(" ")==0:         ##if all questions are answered, user will be redirected to thank you page!!!
        return redirect("/thanks")
    
    if q_number.isnumeric()==False:

        flash("Not numeric, you will be redirected to the first non-answered question if there any otherwise you will be redirected to thanks page!")

        for i in resp_dict:
            if resp_dict[i]==" ":
                q_number=i
                return render_template("question1.html",q_num=int(q_number),title=satisfaction_survey.title,question=satisfaction_survey.questions[int(q_number)].question,answers=satisfaction_survey.questions[int(q_number)].choices,listLength=len(satisfaction_survey.questions))

        return redirect("/thanks")

    
    elif int(q_number)>=len(satisfaction_survey.questions) or int(q_number)<0:

        flash("invalid question numbers but don't worry! you will be redirected to the first non-answered question if there any otherwise you will be redirected to thanks page!")

        for i in resp_dict:
            if resp_dict[i]==" ":
                q_number=i
                return render_template("question1.html",q_num=int(q_number),title=satisfaction_survey.title,question=satisfaction_survey.questions[int(q_number)].question,answers=satisfaction_survey.questions[int(q_number)].choices,listLength=len(satisfaction_survey.questions))
                
            
        return redirect("/thanks")
    
    else:

        return render_template("question1.html",q_num=int(q_number),title=satisfaction_survey.title,question=satisfaction_survey.questions[int(q_number)].question,answers=satisfaction_survey.questions[int(q_number)].choices,listLength=len(satisfaction_survey.questions))

@app.route("/questions/<q_number>",methods=["POST"])
def answer_question1(q_number):
    choice=request.form["choice"]
    
    RESPONSES.append({q_number:choice})
    resp_dict[str(int(q_number)-1)]=choice
    return redirect(f"/questions/{int(q_number)}")


@app.route("/thanks")
def thank_you():
    flash("ALL DONE! Thank you!")
    msg=f"Thank You, your responses are {RESPONSES} and {resp_dict}"
    return msg



