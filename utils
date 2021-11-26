from ffmpeg_streaming import Formats, FFProbe
import sys, os, datetime

def monitor(ffmpeg, duration, time_, time_left, process):
    """
    Handling proccess.

    Examples:
    1. Logging or printing ffmpeg command
    logging.info(ffmpeg) or print(ffmpeg)

    2. Handling Process object
    if "something happened":
        process.terminate()

    3. Email someone to inform about the time of finishing process
    if time_left > 3600 and not already_send:  # if it takes more than one hour and you have not emailed them already
        ready_time = time_left + time.time()
        Email.send(
            email='someone@somedomain.com',
            subject='Your video will be ready by %s' % datetime.timedelta(seconds=ready_time),
            message='Your video takes more than %s hour(s) ...' % round(time_left / 3600)
        )
       already_send = True

    4. Create a socket connection and show a progress bar(or other parameters) to your users
    Socket.broadcast(
        address=127.0.0.1
        port=5050
        data={
            percentage = per,
            time_left = datetime.timedelta(seconds=int(time_left))
        }
    )

    :param ffmpeg: ffmpeg command line
    :param duration: duration of the video
    :param time_: current time of transcoded video
    :param time_left: seconds left to finish the video process
    :param process: subprocess object
    :return: None
    """
    per = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s left [%s%s]" %
        (per, datetime.timedelta(seconds=int(time_left)), '#' * per, '-' * (100 - per))
    )
    sys.stdout.flush()

def probe():

    ffprobe = FFProbe('video.mp4')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ffprobe.save_as_json(os.path.join(current_dir, 'probe.json'))

    all_media = ffprobe.all()

    video_format = ffprobe.format()

    streams = ffprobe.streams().all()
    videos = ffprobe.streams().videos()
    audios = ffprobe.streams().audios()

    first_stream = ffprobe.streams().first_stream()
    first_video = ffprobe.streams().video()
    first_audio = ffprobe.streams().audio()

    print("all:")
    print(all_media)

    print("format:")
    print(video_format)

    print("streams:")
    print(streams)

    print("videos:")
    for video in videos:
        print(video)

    print("audios:")
    for audio in audios:
        print(audio)

    print("first stream:")
    print(first_stream)

    print("first video:")
    print(first_video)

    print("first audio:")
    print(first_audio)

    print("duration: {}".format(str(datetime.timedelta(seconds=float(video_format.get('duration', 0))))))
    # duration: 00:00:10.496

    print("size: {}k".format(round(int(video_format.get('size', 0)) / 1024)))
    # size: 290k

    print("overall bitrate: {}k".format(round(int(video_format.get('bit_rate', 0)) / 1024)))
    # overall bitrate: 221k

    print("dimensions: {}x{}".format(first_video.get('width', "Unknown"), first_video.get('height', "Unknown")))
    # dimensions: 480x270

    print("video bitrate: {}k".format(round(int(first_video.get('bit_rate', 0)) / 1024)))
    # video bitrate: 149k

    print("audio bitrate: {}k".format(round(int(first_audio.get('bit_rate', 0)) / 1024)))
    # audio bitrate: 64k