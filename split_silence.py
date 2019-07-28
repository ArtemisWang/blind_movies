import ffmpeg


# 全抽帧
def get_frames():
    input_file = '/Users/didi/Desktop/ffmpeg/test.mp4'
    output_file = '/Users/didi/Desktop/ffmpeg/image/image-%5d.jpg'
    out, err = (
        ffmpeg
            .input(input_file)
            .output(output_file)
            .run(quiet=False, overwrite_output=True)
    )
    if out == b'':
        print('do nothing')


# 按一定的频率抽帧
def get_frames_by_rate():
    input_file = 'data/inception_cut.mkv'
    output_file = 'image-%5d.jpg'
    out, err = (
        ffmpeg
            .input(input_file, ss=0)
            # .output(output_file, r='1', f='image2')
            .output(output_file, vf='fps=1/30', f='image2')
            .run(quiet=True, overwrite_output=True) ## quiet指是否在控制台中显示具体信息，True为不显示
    )
    if out == b'':
        print('do nothing')


# 按指定时间片段抽帧
def get_frames_by_times():
    times = [1, 5, 8, 10]
    for time in times:
        input_file = '/Users/didi/Desktop/ffmpeg/test.mp4'
        output_file = '/Users/didi/Desktop/ffmpeg/image/image-' + str(time) + '.jpg'
        out, err = (
            ffmpeg
                .input(input_file, ss=time)
                .output(output_file, vframes='1', f='image2')
                .run(quiet=False, overwrite_output=True)
        )
        if out == b'':
            print('do nothing')


if __name__ == '__main__':
    get_frames_by_rate()