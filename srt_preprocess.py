class SrtProcess:
    def __init__(self):
        self.srt = []
        self.timeline = []

    def process(self, file):
        f = open(file, 'r')
        i = 1
        j = 0
        for line in f:
            line = line.strip('\n')
            if line == str(i):
                i = i + 1
                j = 1
            elif j == 1:
                self.timeline.append(line)
                j = 2
            elif j == 2:
                self.srt.append(line)
                j = 0
        f.close()

if __name__ == '__main__':
    f = open('data/inception_cut.srt', 'r')
    i = 1
    j = 0
    srt = []
    timeline = []
    for line in f:
        line = line.strip('\n')
        if line == str(i):
            i = i + 1
            j = 1
        elif j == 1:
            timeline.append(line)
            j = 2
        elif j == 2:
            srt.append(line)
            j = 0
    f.close()
    for i in range(len(timeline)):
        print(str(i), timeline[i], srt[i])