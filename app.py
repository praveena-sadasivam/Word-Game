from flask import Flask,render_template,request,jsonify
from nltk.corpus import wordnet as word_net
import json
import random
from logging.handlers import RotatingFileHandler

word_dict=dict()
random_wrd=str()
correct_word=set()
score=0
number_of_question_attend=1
meaning=dict()


# Opening JSON file that has 4 letter english words
with open('word_dictionary.json', 'r') as openfile:
    # Reading from json file 
    json_object = json.load(openfile)


#flask object
app=Flask(__name__,
template_folder="clients/templates",
static_folder="clients/static")

file_handler = RotatingFileHandler("error.log", maxBytes=1024 * 1024 * 100)
app.logger.addHandler(file_handler)


@app.errorhandler(500)
def handle_500_error(exception):
    app.logger.error(exception)
    return "Internal Server Error"

@app.errorhandler(404)
def handle_404_error(exception):
    app.logger.error(exception)
    return "Not Found"


#function to get random words
def get_random_word():
    rand_num = random.randint(0,len(json_object)-1)
    rand_word=json_object[rand_num]
    print("\ngetting random word\n")
    return rand_word

#function to shuffle the target word
def get_jumbled_word():
    rand_word=get_random_word()
    # sample() method shuffling the characters of the word 
    jubled_word_list = random.sample(rand_word, len(rand_word)) 
   
    # join() method join the elements
    jumbled = ''.join(jubled_word_list)
    print("\ngetting jumbled word\n")
    return [jumbled,rand_word]



#function to get html page
@app.route("/")
def get_html():
    print("\nopening web page\n")
    return render_template("word_game.html")

#function to send target word to web page 
@app.route("/api/jumbled_word")
def jumbled_word():
    global random_wrd
    words=get_jumbled_word()
    jum_word=words[0]
    random_wrd=words[1]
    correct_word.add(random_wrd)
    print("\njumbled word: ",jum_word)
    print("\nrandom word: ",random_wrd)
    print("\nsending a jumbled word to webpage")
    return jsonify(jum_word)

#function to check user input
@app.route("/api/checker",methods=['GET'])
def check_word():
    global number_of_question_attend
    number_of_question_attend+=1
    print("\nchecking user input\n")
    global score
    answer = request.args.get("answer")
    answer=answer.split(" ")
    for word in answer:
        if word in json_object:
            correct_word.add(word)
            score+=1
            print("\nvalid answer !\n")
    global random_wrd
    words=get_jumbled_word()
    jum_word=words[0]
    random_wrd=words[1]
    correct_word.add(random_wrd)
    print("\njumbled word: ",jum_word)
    print("\nrandom word: ",random_wrd)
    print("\nsending a jumbled word to webpage\n")
    return jsonify(jum_word)

#function to return result page
@app.route("/api/result")
def result():
    return render_template("result.html")

#function to display score
@app.route("/api/score")
def get_score():
    print("\n number of question attend: ",number_of_question_attend)
    print("\nscore: ",score)
    return jsonify([score,number_of_question_attend])

# function to return correct word 
@app.route("/api/words")
def get_word():
    return jsonify(list(correct_word))

#function to display meaning
@app.route("/api/meaning",methods=['GET'])
def word_meaning():
    print("\nword with meaning\n")
    answer = request.args.get("word")
    syn = word_net.synsets(answer)[0]
    meaning=syn.definition()
    print(answer+': '+meaning+'\n')
    return jsonify([meaning,answer])
#function to restart game
@app.route("/api/restart")
def restart():
    global number_of_question_attend
    number_of_question_attend=1
    global score 
    score= 0
    global correct_word
    correct_word=set()
    print("\nback to game\n")
    return render_template("word_game.html")

if __name__ == '__main__':
    app.run(port=3000)
