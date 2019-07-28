class TextProcess:
    def __init__(self):
        self.name = []  ## 按顺序存放说话人名字的列表
        self.word = []  ## 按顺序存放说话人说的剧本台词的列表
        self.name_i = []  ## 按顺序存放台词在剧本中索引的列表，从0开始
        self.back = []  ## 按顺序存放解说或者背景或者非对话部分的剧本内容的列表
        self.back_i = []  ## 按顺序存放解说在剧本中索引序号的列表，与name_i正好互斥
        self.back_all = []

    def process(self, file):
        with open(file, 'r') as f:
            i = 0
            for line in f:
                line = line.strip('\n').strip('：')
                if line != '':
                    if line.find('：') != -1:
                        lines = line.split("：")
                        self.name.append(lines[0])
                        self.word.append(lines[1])
                        # liness = lines[1].replace('，', '。').split('。')
                        # while '' in liness:
                        #     liness.remove('')
                        # self.word = self.word + liness
                        self.name_i.append(i)
                        i += 1
                        self.back_all.append(None)
                    else:
                        self.back.append(line)
                        self.back_i.append(i)
                        self.back_all.append(line)
                        i += 1



if __name__ == '__main__':
    f = open('data/inception_text_cut.txt', 'r')
    name = [] ## 说话的人
    word = [] ## 台词
    name_i = []
    back = [] ## 解说
    back_i = []
    i = 0
    for line in f:
        line = line.strip('\n').strip('：')
        if line != '':
            if line.find('：') != -1:
                lines = line.split("：")
                name.append(lines[0])
                word.append(lines[1])
                # liness = lines[1].replace('，', '。').split('。')
                # while '' in liness:
                #     liness.remove('')
                # word = word + liness
                name_i.append(i)
                i += 1
            else:
                back.append(line)
                back_i.append(i)
                i += 1
    f.close
    # for i in range(len(back)):
    #     print(back_i[i], back[i])
    # for j in range(len(name)):
    #     print(j, name_i[j], word[j])
