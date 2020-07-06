from flask import Flask,render_template,request,jsonify
from nltk.corpus import wordnet as word_net
import json
import random
word_dict=dict()
random_wrd=str()
correct_word=list()
score=0


# Opening JSON file that has 4 letter english words
with open('word_dictionary.json', 'r') as openfile:
    # Reading from json file 
    json_object = json.load(openfile)


#flask object
app=Flask(__name__,
template_folder="clients/templates",
static_folder="clients/static")

#function to get random words
def get_random_word():
    rand_num = random.randint(0,len(json_object)-1)
    rand_word=json_object[rand_num]
    print("random function")
    return rand_word

#function to shuffle the target word
def get_jumbled_word():
    rand_word=get_random_word()
    # sample() method shuffling the characters of the word 
    jubled_word_list = random.sample(rand_word, len(rand_word)) 
   
    # join() method join the elements
    jumbled = ''.join(jubled_word_list)
    print("jumbled function")
    return [jumbled,rand_word]



#function to get html page
@app.route("/")
def get_html():
    print("html page")
    return render_template("word_game.html")

#function to send target word to web page 
@app.route("/api/jumbled_word")
def jumbled_word():
    global random_wrd
    words=get_jumbled_word()
    jum_word=words[0]
    random_wrd=words[1]
    correct_word.append(random_wrd)
    print("jumbled: ",jum_word)
    print("random: ",random_wrd)
    print("got word")
    return jsonify(jum_word)

#function to check user input
@app.route("/api/checker",methods=['GET','POST'])
def check_word():
    print("check method")
    global score
    answer = request.args.get("answer")
    answer=answer.split(" ")
    for word in answer:
        if word in json_object:
            score+=1
            
    return jsonify(score)

#function to return result page
@app.route("/api/result")
def result():
    return render_template("result.html")

#function to display score
@app.route("/api/score")
def get_score():
    print("score: ",score)
    return jsonify(score)

# function to return correct word 
@app.route("/api/words")
def get_word():
    print(correct_word)
    return jsonify(correct_word)

#function to display meaning on click
@app.route("/api/meaning",methods=['GET'])
def word_meaning():
    word = request.args.get("words")
    print(word)
    syn = word_net.synsets(word)[0]
    meaning=syn.definition()
    return jsonify(meaning)

if __name__ == '__main__':
    app.run(debug=True,port=3000)
