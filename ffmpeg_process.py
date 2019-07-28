import ffmpeg
import os
import insert_process
import speech_synthesis as ss

# probe = ffmpeg.probe('data/inception_cut.mkv')
# print(probe)
# video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
# print(video_stream)

### 从视频中每隔50s提取一张图片
# stream = ffmpeg.input('data/inception_cut.mkv')
# stream = ffmpeg.output(stream, 'image-%5d.jpg', vf='fps=1/50', f='image2')
# ffmpeg.run(stream, quiet=True, overwrite_output=True)

def get_segment_times():
    insert_dict = insert_process.insert_dict
    rank = list(insert_dict)
    segment_times = str(insert_dict[rank[0]]['start_time'])
    for rank_i in rank[1:]:
        start_time = str(insert_dict[rank_i]['start_time'])
        segment_times += ','+start_time
    # print(segment_times)
    print('--已获取切割时间--\n')
    return segment_times

def segment_video(filename, segment_times):
    cmd = 'ffmpeg -re -i '+filename+' -c copy -f segment -segment_format mp4 -segment_times '+segment_times+' -reset_timestamps 1 temp/inception_cut_%d.mp4'
    ## 切割视频的命令行
    os.system(cmd)
    print('--视频已切割--\n')

def if_mp4(filename):
    is_mkv = 'mkv' in filename
    if is_mkv:
        # cmd = 'ffmpeg -re -i '+filename+' -filter_complex [0:v][0:s]overlay[v] -map [v] -map 0:a -acodec copy '+filename.replace('mkv','mp4')
        # cmd = 'ffmpeg -re -i '+filename+' -acodec copy '+filename.replace('mkv','mp4')
        cmd = 'ffmpeg -i '+filename+' -map 0:2 '+filename.replace('mkv','ass')
        os.system(cmd)
        ### 将ass字幕从mkv视频中提取出来
        cmd = 'ffmpeg -i '+filename+' -vf ass='+filename.replace('mkv','ass')+' -f mp4 '+filename.replace('mkv', 'mp4')
        os.system(cmd)
        ### 将mkv格式视频转为MP4格式的命令行，字幕烧录进去
        filename = filename.replace('mkv', 'mp4')
        os.remove(filename.replace('mkv','ass')) ## 删除字幕缓存
        print('--已创建MP4格式视频--\n')
    else:
        print('--该视频为MP4格式--\n')
    return filename

def speech_synthesis():
    insert_dict = insert_process.insert_dict
    rank = list(insert_dict)
    audio_length = []
    for i, rank_i in enumerate(rank):
        text = insert_dict[rank_i]['content']
        savename = 'temp/audio_'+str(i)+'.mp3'
        # print(savename, text)
        length = ss.speech_synthesis(text, savename)
        audio_length.append(length)
    print('--语音合成完毕--\n')
    return audio_length

def concat_video(audio_length):
    insert_dict = insert_process.insert_dict
    rank = list(insert_dict)
    with open('temp/filelist.txt', 'w') as f:
        f.write('file \'inception_cut_0.mp4\'')
    for i, audio_i in enumerate(audio_length):
        cmd = 'ffmpeg -i temp/audio_'+str(i)+'.mp3 -filter_complex [0:a][0:a][0:a][0:a][0:a][0:a]amerge=inputs=6[aout] -map [aout] temp/audio_'+str(i)+'_.mp3'
        os.system(cmd)
        ## 将mp3转为5.1立体声
        cmd = 'ffmpeg -i temp/audio_'+str(i)+'_.mp3 -af volume=0.2 temp/audio_'+str(i)+'__.mp3'
        os.system(cmd)
        ## 将mp3音量减小
        cmd = 'ffmpeg -r 16975/708 -f image2 -loop 1 -i data/1.png -i temp/audio_'+str(i)+'__.mp3 -s 1280*720 -pix_fmt yuv420p -t '+str(audio_i+1)+' -ar 48000 -vcodec libx264 temp/audio_'+str(i)+'_.mp4'
        os.system(cmd)
        ## 将mp3与图片生成mp4
        with open('temp/filelist.txt', 'a') as f:
            f.write('\nfile \'audio_'+str(i)+'_.mp4\'')
            f.write('\nfile \'inception_cut_'+str(i+1)+'.mp4\'')
        ## 写filelist文件
    cmd = 'ffmpeg -f concat -i temp/filelist.txt -c copy result/output.mp4'
    os.system(cmd)
    ## 拼接mp4
    print('--解说视频制作完毕--\n')

def del_temp():
    dirlist = os.listdir('temp')
    for path in dirlist:
        os.remove('temp/'+ path)
    print('--缓存文件已清理完毕--\n')


filename = 'data/inception_cut.mkv'
filename = if_mp4(filename) ## 将mkv格式视频转为MP4格式，并生成新的文件名
segment_times = get_segment_times()  ## 获取分割时间字符串
segment_video(filename, segment_times)  ## 将视频文件按照分割时间分隔开并储存在temp文件夹中
audio_length = speech_synthesis() ## 将剧本中的句子语音合成
concat_video(audio_length)
del_temp() ## 清除缓存


