import visual
import srt_process_min as spm
import text_preprocess

def determineInsert(rank): ## 将需要插入的剧本解说的文字和时间轴封装进一个字典中，字典的key表示该插入剧本解说的字幕的组号的值，在该条字幕后面插入这句解说
    ## 字典内每条内包含解说的起始时间和结束时间以及解说文字
    insert_dict = {}
    diff_dict = spm.get_diff_dict('data/inception.srt')
    tp = text_preprocess.TextProcess()
    tp.process('data/inception_text_cut.txt')
    # print(len(list(diff_dict)))
    for i in range(len(rank)-1):
        if rank[i] == rank[i+1]-1:
            # print(diff_dict[list(diff_dict)[rank[i]]]['diff_end'])
            name_now = tp.name_i[i]
            name_next = tp.name_i[i+1]
            if name_next-name_now > 1:
                j = name_next-name_now
                insert_content = ''
                while j > 1:
                    insert_content = tp.back_all[j-1+name_now] + insert_content
                    j -= 1
                insert_dict[rank[i]] = {'start_time': diff_dict[list(diff_dict)[rank[i]]]['diff_end'],
                                        'end_time': diff_dict[list(diff_dict)[rank[i+1]]]['diff_start'],
                                        'content': insert_content}
    return insert_dict






rank = visual.rank_rank
insert_dict = determineInsert(rank)