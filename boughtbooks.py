# coding = utf-8

import random


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
get_books()