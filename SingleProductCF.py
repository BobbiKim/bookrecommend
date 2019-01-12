from operator import itemgetter

# 基于单品购买的推荐算法

# 获取书籍信息 字典类型
def book_factory():
    index = 0
    book = {}
    f = open('data/booknovel')
    for line in f.readlines():
        item = line.strip().split(' ')
        book.setdefault(index, [])
        book[index] = item
        index = index + 1
    f.close()
    return book


class SingleProductCF:
    '''
    基于单品推荐算法
    购买过此商品的用户还买过什么商品
    根据用户购买人数和好评加权推荐五本书籍给用户
    '''

    def __init__(self):
        self.num_rec_book = 5
        # 买过该书用户买过其他书的数据集合
        self.dataset = {}

    def get_data(self, filename):
        f = open(filename)
        for line in f.readlines():
            # 一个用户对一本书的评价
            user, book, score = line.split("	")
            self.dataset.setdefault(user, set())
            self.dataset[user].add(book)

    def rec_book(self, base_book):
        # 推荐的书籍
        n = self.num_rec_book
        other_book = {}
        # 把书籍放入存储容器时，弃掉当前的目标书籍
        # 因为不会推荐同一本书
        for user, books in self.dataset.items():
            if base_book not in books:
                continue
            else:
                for book in books:
                    other_book.setdefault(book, 0)
                    other_book[book] += 1
        # 将书籍按次数排序
        topn_dic = sorted(other_book.items(), key=itemgetter(1), reverse=True)[0:n]
        rec_result = []
        for dic in topn_dic:
            rec_result.append(dic[0])
        return rec_result

    def recommend(self, filename, book_id, books):
        result_dict = []
        self.get_data(filename)
        result=self.rec_book(book_id)
        for index, i in enumerate(result):
            result_dict.append({})
            result_dict[index].setdefault(i, [])
            result_dict[index][i] = books[int(i)]
        # 返回的是一个列表，里面每一项是一个字典
        # 字典的key是编号，value是商品信息
        return result_dict
