from aip import AipSpeech
from mutagen.mp3 import MP3
from multiprocessing import Pool
import time

""" 你的 APPID AK SK """
APP_ID = '16610547'
API_KEY = 'LdUcmubzpwpK8c2G7GHqn6Qn'
SECRET_KEY = 'YqSK2gx4VKUjYlQzh0uTIZ31NVvqWwT6'

def speech_synthesis(text, savename):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(text, 'zh', 1, {'vol': 5, 'per':0})
    # client.synthesis('', )
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(savename, 'wb') as f:
            f.write(result)
    audio = MP3(savename)
    return audio.info.length

# speech_synthesis('一支来复枪的枪杆在这个胡子拉碴的男人后背挑翻检寻。一名日本保安俯视着他，然后朝海岸上面靠着吉普车的同事叫喊。他们身后是悬崖，而海滩上面矗立着一座日本式城堡。内景，日本城堡内，奢华的餐厅，稍后保安候着，一位侍者对坐在餐桌旁的一位年长的日本男子报告。他背对着我们。', 'temp/audio_0.mp3')



# ## 单核计算
# audio = MP3('auido5.mp3')
# print(audio.info.length)


# 多核计算
# def f(name):
#     # time.sleep(3)
#     return MP3(name).info.length
# pool = Pool(processes=2) # start 2 worker processes
# # apply_async好处是不会阻塞进程，参数1就是目标函数名，参数2是函数所接受的参数
#
#
#
# start2 = time.time()
# result = pool.apply_async(f, ('result/auido9.mp3',))  # evaluate "f(10)" asynchronously in a single process
# end2 = time.time()
# print('time:', end2-start2)
# print(result.get(timeout=1))  # prints "100" unless your computer is *very* slow
#
#
# ## 映射版本的输出，这个比较适合多个采纳数的时候使用
#
# pool.close()
# pool.join()