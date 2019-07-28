import srt
import datetime


def HandleWithFile(filename):
    f = open(filename, 'r', encoding='utf-8')
    file = f.read()
    f.close()
    subtitle_generator = srt.parse(file)
    subtitles = list(subtitle_generator)
    return subtitles


def TimeDeltaList(subtitles):
    timedelta_list = []
    num = 0
    time_const = datetime.timedelta(seconds=1)
    try:
        while subtitles[num].index:
            time_delta = subtitles[num + 1].start - subtitles[num].end
            if time_delta > time_const:
                timedelta_list.append(str(time_delta))
            else:
                timedelta_list.append(0)
            num += 1
    except IndexError:
        timedelta_list = timedelta_list
        # print("时间差子程序已经进行到了最后一步")
    return timedelta_list


def isNextZero(point, timedelta_list):
    # print(point)
    try:
        if timedelta_list[point + 1] != 0:
            return point
        else:
            point = point + 1
            return isNextZero(point, timedelta_list)
    except IndexError:
        return point


def HandleDiff(timedelta_list,valve=True):
    diff_list = []
    point = 0
    while point < len(timedelta_list):
        if timedelta_list[point] != 0 and (point == len(timedelta_list) - 1 or timedelta_list[point+1] != 0):
            diff_list.append([timedelta_list[point]])
            # print(diff_list)
            point += 1
        else:
            point_prev = point
            point_next = isNextZero(point, timedelta_list)
            diff_list.append(list(timedelta_list[point_prev:(point_next + 1)]))
            point = point_next + 1
    if valve:
        for num in range(len(diff_list)):
            if len(diff_list[num]) > 5:
                innerList = diff_list.pop(num)
                # print('innerlist:', innerList)
                i = len(innerList) // 3
                j = len(innerList) % 3
                if j != 0:
                    for t in range(i):
                        diff_list.insert(num + t, innerList[3 * t:3 * t + 3])
                    diff_list.insert(num + i, innerList[3 * (t + 1):])
                    # print(innerList[3 * (t + 1):])
                elif j == 0:
                    for t in range(i):
                        diff_list.insert(num + t, innerList[3 * t:3 * t + 3])
                else:
                    pass
        return diff_list
    else:
        return diff_list


def showData(diff_list, subtitles):
    diff_dict = {}
    point_index = 0
    for num in range(len(diff_list)):
        point_index_prev = point_index + 1
        point_index = point_index + len(diff_list[num])
        try:
            if len(diff_list[num]) == 1:
                if num == 0:
                    # index = str(subtitles[point_index_prev].index - 2) + ' - ' + str(subtitles[point_index].index - 1)
                    index = str([i for i in range(subtitles[point_index_prev].index - 2, subtitles[point_index].index)])
                    # print(index)
                    subtitle_content = str(subtitles[point_index_prev - 1].content) + ',' + str(
                        subtitles[point_index].content)
                    diff_start = subtitles[point_index_prev - 1].start
                    diff_end = subtitles[point_index].end
                    diff_dict[index] = {'diff_time': diff_list[num], 'diff_start': diff_start,
                                        'diff_end': diff_end, 'subtitle_content': subtitle_content}
                elif diff_list[num][0] == 0:
                    # index = str(subtitles[point_index].index-1)
                    index = str([subtitles[point_index].index-1])
                    subtitle_content = str(subtitles[point_index_prev-1].content) + ',' + str(
                        subtitles[point_index].content)
                    diff_start = subtitles[point_index_prev-1].start
                    diff_end = subtitles[point_index].end
                    diff_dict[index] = {'diff_time': diff_list[num], 'diff_start': diff_start,
                                        'diff_end': diff_end, 'subtitle_content': subtitle_content}
                else:
                    # index = str(subtitles[point_index].index-1)
                    index = str([subtitles[point_index].index-1])
                    subtitle_content = str(subtitles[point_index].content)
                    diff_start = subtitles[point_index].start
                    diff_end = subtitles[point_index].end
                    diff_dict[index] = {'diff_time': diff_list[num], 'diff_start': diff_start,
                                        'diff_end': diff_end, 'subtitle_content': subtitle_content}

            elif len(diff_list[num]) == 2:
                # index = str(subtitles[point_index_prev].index-1) + ' - ' + str(subtitles[point_index].index-1)
                index = str([i for i in range(subtitles[point_index_prev].index-1, subtitles[point_index].index)])
                subtitle_content = str(subtitles[point_index_prev].content) + ',' + str(
                    subtitles[point_index_prev+1].content)
                diff_start = subtitles[point_index_prev].start
                diff_end = subtitles[point_index].end
                diff_dict[index] = {'diff_time': diff_list[num], 'diff_start': diff_start,
                                    'diff_end': diff_end, 'subtitle_content': subtitle_content}
            else:
                # index = str(subtitles[point_index_prev].index-1) + ' - ' + str(subtitles[point_index].index-1)
                index = str([i for i in range(subtitles[point_index_prev].index-1, subtitles[point_index].index)])
                subtitle_content = str(subtitles[point_index_prev].content)
                for i in range(subtitles[point_index].index - subtitles[point_index_prev].index):
                    subtitle_content = subtitle_content + ',' + str(subtitles[point_index_prev + i + 1].content)
                diff_start = subtitles[point_index_prev].start
                diff_end = subtitles[point_index].end
                diff_dict[index] = {'diff_time': diff_list[num], 'diff_start': diff_start,
                                    'diff_end': diff_end, 'subtitle_content': subtitle_content}
        except IndexError:
            print("子程序完成")
    return diff_dict

def get_diff_dict(filename):
    subtitles = HandleWithFile(filename)
    timedelta_list = TimeDeltaList(subtitles)
    # print(timedelta_list)
    diff_list = HandleDiff(timedelta_list)
    # print(diff_list, len(diff_list))
    diff_dict = showData(diff_list, subtitles=subtitles)
    return diff_dict

def get_wordlist(filename):
    diff_dict = get_diff_dict(filename)
    srt_list = []
    for a in diff_dict:
        # print(diff_dict[a]['subtitle_content'])  ## 提取字典中的文字部分的方法
        srt_list.append(diff_dict[a]['subtitle_content'])
    return srt_list


if __name__ == '__main__':
    subtitles = HandleWithFile('data/inception_cut.srt')
    time_const = datetime.timedelta(seconds=1)
    timedelta_list = TimeDeltaList(subtitles)
    # print(timedelta_list, len(timedelta_list))
    diff_list = HandleDiff(timedelta_list)
    # print(diff_list, len(diff_list))
    diff_dict = showData(diff_list, subtitles=subtitles)
    # print(diff_dict.keys(), diff_list)
    srt_list = []
    for a in diff_dict:
        # print(diff_dict[a]['subtitle_content'])  ## 提取字典中的文字部分的方法
        srt_list.append(diff_dict[a]['subtitle_content'])

