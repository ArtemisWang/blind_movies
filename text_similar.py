#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import srt_preprocess
import text_preprocess
from multiprocessing import Pool
import json
import time
import pickle
import srt_process_min as spm
import os

def f(text1, text2):
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?access_token=24.3c5a2f1f516112a5f524efebe6506656.2592000.1563890188.282335-16612200'
    body = {"text_1": text1, "text_2": text2, "model": "BOW"} ## model可选BOW,GRNN,CNN
    headers = {"content-type": "application/json"}
    #print type(body)
    #print type(json.dumps(body))
    # 这里有个细节，如果body需要json形式的话，需要做处理
    # 可以是data = json.dumps(body)
    # response = requests.post(url, data = json.dumps(body), headers = headers)
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    response = requests.post(url, json = body, headers = headers)
    # 返回信息
    # print(response.text)
    # # 返回响应头
    # print(response.status_code)
    return response.text

def del_temp():
    dirlist = os.listdir('temp')
    for path in dirlist:
        os.remove('temp/'+ path)
    print('--缓存文件已清理完毕--\n')

if __name__ == '__main__':
    pool = Pool(processes=2)
    # sp = srt_preprocess.SrtProcess() ### 从srt_preprocess中获取srt句子，原始短句
    # sp.process('data/inception.srt')
    # srt = sp.srt ## 获取未经分组的srt
    srt = spm.get_wordlist('data/inception.srt')## 从srt_process_min中获取srt句子，按照字幕间隔分组后的字幕句子
    # print(len(srt))
    tp = text_preprocess.TextProcess()
    tp.process('data/inception.txt')
    word = tp.word
    acc_list = []
    # print(len(word), len(srt), len(word_i))
    for ii, word_ii in enumerate(word[22:]):
        text_1 = word_ii
        word_acc = []
        for jj, srt_jj in enumerate(srt):
            text_2 = srt_jj
            acc = pool.apply_async(f, (text_1, text_2)).get()  ## 双进程获取相似度值
            # acc = f(text1=text_1, text2=text_2) ## 单进程取值，跟上面那句二选一
            time.sleep(0.1)
            try:
                acc = json.loads(acc)
            except:
                acc = 0
            try:
                # print(acc['score'])
                word_acc.append(acc['score'])
            except:
                # print(acc)
                word_acc.append(0)
        print(word_acc)
        with open('temp/word_acc.txt', 'a') as temp_file:
            temp_file.write(str(word_acc))
        acc_list.append(word_acc)
    # print('acc_list_len:', len(acc_list), len(acc_list[0]))
    data = {'acc_list': acc_list}
    with open('data/acc_whole_bow.pkl', 'wb') as f:
        pickle.dump(data, f)
    # del_temp()  ## 如果正确运行完，清除缓存文件
