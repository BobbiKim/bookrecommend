from flask import Flask
from flask import render_template
import SingleProductCF
import recommend
import random

app = Flask(__name__)
book_file='data/booknovel'
success_file='data/booksucceed'
economy_file='data/bookeconomy'
technology_file='data/booktechnology'
picture=['../static/xiaoshuo.jpg','../static/keji.jpg','../static/lizhi.jpg','../static/jingji.jpg']

allnovelbooklist=recommend.redfile(book_file)
allnovelbookdict=recommend.changedict(allnovelbooklist)

allsuccesslist=recommend.redfile(success_file)
allsuccessdict=recommend.changedict(allsuccesslist)

alleconomylist=recommend.redfile(economy_file)
alleconomydict=recommend.changedict(alleconomylist)

alltechnologylist=recommend.redfile(technology_file)
alltechnologydict=recommend.changedict(alltechnologylist)

def get_books():
    # 用户及其购买过的书的信息

    users = [i for i in range(1, 2001)]
    books = [i for i in range(0, 15)]
    user_book = set()
    for i in range(0, 20001):
        user = users[random.randint(0, 200)]
        book = books[random.randint(0, 14)]
        item = str(user) + " " + str(book)
        print(item)
        user_book.add(item)
    print(len(user_book))
    with open("data/information.txt", "w") as f:
        for item in user_book:
            precetage = random.randint(1, 10)
            user, book = item.split(" ")
            f.write(str(user) + '\t' + str(book) + '\t' + str(precetage) + '\n')
@app.route("/")
def index():
    return render_template('index.html')
@app.route('/bookclass/<index>')
def bookclass(index):
    if(index=='novel'):
        result = allnovelbookdict
        hot=recommend.recommend(allnovelbooklist,3)
        tupian=picture[0]
    elif(index=='success'):
        result = allsuccessdict
        hot=recommend.recommend(allsuccesslist,1)
        tupian=picture[2]
    elif(index=='economy'):
        result=alleconomydict
        hot=recommend.recommend(alleconomylist,1)
        tupian=picture[3]
    elif(index=='technology'):
        result=alltechnologydict
        hot=recommend.recommend(alltechnologylist,0)
        tupian=picture[1]
    return render_template('bookclass.html', novel_info=result,hot=hot,tupian=tupian)
@app.route('/bookdetail/<kind>/<index>')
def bookdetail(kind,index):
    get_books()
    strindex=index
    index=int(index)
    showbook={}
    if(kind=='novel'):
        for item in allnovelbookdict:
            if item==index:
                showbook[index]=allnovelbookdict[item]
                print(showbook)
        result = recommend.recommend(allnovelbooklist, index)
        like = SingleProductCF.SingleProductCF().recommend("data/information.txt", strindex, allnovelbookdict)
    elif(kind=='success'):
        for item in allsuccessdict:
            if item==index:
                showbook[index]=allsuccessdict[item]
                print(showbook)
        result = recommend.recommend(allsuccesslist, index)
        like = SingleProductCF.SingleProductCF().recommend("data/information.txt", strindex, allsuccessdict)
    elif(kind=='economy'):
        for item in alleconomydict:
            if item==index:
                showbook[index]=alleconomydict[item]
                print(showbook)
        result = recommend.recommend(alleconomylist, index)
        like = SingleProductCF.SingleProductCF().recommend("data/information.txt", strindex, alleconomydict)
    elif(kind=='technology'):
        for item in alltechnologydict:
            if item == index:
                showbook[index] = alltechnologydict[item]
                print(showbook)
        result = recommend.recommend(alltechnologylist, index)
        like = SingleProductCF.SingleProductCF().recommend("data/information.txt", strindex, alltechnologydict)
        for item in like:
            for key in item:
                print(item[key][1])
    return render_template('bookdetail.html', novel_info=result,showbook=showbook,index=index,like=like)

if __name__ == "__main__":
    app.run(debug=True)
