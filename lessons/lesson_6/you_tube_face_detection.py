import cv2
import dlib
import ffmpeg
import sys
import pytube
import pytube.exceptions
from matplotlib import pyplot as plt
import urllib.error
from multiprocessing import Pool
from discomp import Pool as DPool
import time

UNKNOWN_FRAME_RATE = "unknown frame rate"
UNKNOWN_NUM_FRAMES = "unknown number of frames"

URLS = [
    'https://www.youtube.com/watch?v=SLD9xzJ4oeU',
    'https://www.youtube.com/watch?v=puQ2-aVdxOA',
    'https://www.youtube.com/watch?v=C0aWrDcM988',
    'https://www.youtube.com/watch?v=HdNn5TZu6R8',
    'https://www.youtube.com/watch?v=tBozgYVgeDE',
    'https://www.youtube.com/watch?v=1dTEXh4lxfA',
    'https://www.youtube.com/watch?v=CPKq9sDIs2M',
    'https://www.youtube.com/watch?v=X8T1UzeoPto',
    'https://www.youtube.com/watch?v=gDtISrPdmCM',
    'https://www.youtube.com/watch?v=T52EZ7bMa9w',
    'https://www.youtube.com/watch?v=cRGrIn2VHTE',
    'https://www.youtube.com/watch?v=vFippyIh5fk',
    'https://www.youtube.com/watch?v=CduA0TULnow',
    'https://www.youtube.com/watch?v=CH1XGdu-hzQ',
    'https://www.youtube.com/watch?v=udKE1ksKWDE',
    'https://www.youtube.com/watch?v=alMZceP3RF8',
    'https://www.youtube.com/watch?v=XVhcvMaEoeA',
    'https://www.youtube.com/watch?v=hLjqVP6PPtg',
    'https://www.youtube.com/watch?v=-RCA8Shtzjw',
    'https://www.youtube.com/watch?v=g9aXpJCOPHk',
    'https://www.youtube.com/watch?v=0dbUQx5xFPM',
    'https://www.youtube.com/watch?v=KSlLWy3nf3o',
    'https://www.youtube.com/watch?v=wccsj712fgs',
    'https://www.youtube.com/watch?v=0hgfLoI-UDA',
    'https://www.youtube.com/watch?v=xWx3R7WaAQY',
    'https://www.youtube.com/watch?v=43Rnv96Crsw',
    'https://www.youtube.com/watch?v=Rzn8zu-XT2U',
    'https://www.youtube.com/watch?v=q6K_ENzZNUw',
    'https://www.youtube.com/watch?v=L-jNrDzoYr4',
    'https://www.youtube.com/watch?v=HuTE7v3l4nA',
    'https://www.youtube.com/watch?v=7sVf7L44zeI',
    'https://www.youtube.com/watch?v=WZwHhk0hPl0',
    'https://www.youtube.com/watch?v=UEzr4EWzido',
    'https://www.youtube.com/watch?v=9VVlfsE9iZI',
    'https://www.youtube.com/watch?v=sBKjVxLVrA0',
    'https://www.youtube.com/watch?v=_F4KLGdG7-Y',
    'https://www.youtube.com/watch?v=4bkahpkzRKM',
    'https://www.youtube.com/watch?v=tSSjliHrttQ',
    'https://www.youtube.com/watch?v=G09dfRrUxUM',
    'https://www.youtube.com/watch?v=7Y5HSB3p5zk',
    'https://www.youtube.com/watch?v=imKYrbS_c5Y',
    'https://www.youtube.com/watch?v=77d9DE5yB9I',
    'https://www.youtube.com/watch?v=AYVirkvNYco',
]


def parse_args():
    """
    Parse arguments
        argv[1] in_file
    :return: args
    """
    arg = ""
    try:
        arg = sys.argv[1]
    except IndexError:
        pass

    if "youtube" in arg:
        # user asked for a specific url
        urls = [arg]
    else:
        try:
            num_vids = int(arg)
            num_vids = min(num_vids, len(URLS))
            urls = URLS[:num_vids]
        except ValueError:
            urls = URLS

    print(f"Urls to handle {len(urls)}")
    return urls


def get_detector():
    """
    :return: A face detector.
    """
    return dlib.get_frontal_face_detector()


def count_faces(frame, detector):
    """
    Use detector to count number of faces recognized in an image.
    :param frame: Frame image to process
    :param detector: Face detector
    :return: number of faces found
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)

    return len(rects)


def frames_per_sec(in_video_path):
    """
    probe a video file for frame rate and number of frames
    :param in_video_path: Path to video to probe
    :return: frame rate (per sec), total number of frames
    """
    try:
        for ch in ffmpeg.probe(in_video_path)['streams']:
            if ch['codec_type'] == 'video' and 'avg_frame_rate' in ch.keys():
                return eval(ch['avg_frame_rate']), eval(ch['nb_frames'])
    except:
        pass

    return UNKNOWN_FRAME_RATE, UNKNOWN_NUM_FRAMES


def video_face_detection(in_video_path, preferred_data_rate=3):
    """
    produce a time series data of number of images along the video.
    :param in_video_path: Path to input video
    :param preferred_data_rate: number of frames per second to run face
                                detection on
    :return: an array of values, frames per seconds
    """
    print(f'Detect faces {in_video_path}')

    detector = get_detector()

    frame_rate, num_frames = frames_per_sec(in_video_path)

    print(f'Num frames {num_frames}.')

    sample_rate = max(round(frame_rate/preferred_data_rate), 1)
    data_rate = frame_rate/sample_rate
    print(f'frame rate {frame_rate} sample rate {sample_rate}, data rate {data_rate}')
    cap = cv2.VideoCapture(in_video_path)
    frame_count = 0
    face_count = []
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break
        frame_count += 1
        if frame_count % 500 == 0:
            print(f'Progress: {frame_count}/{num_frames}')
        if frame_count % sample_rate != 0:
            # Run face recognition at data_rate
            continue
        face_count.append(count_faces(frame, detector))
        if frame_count > 3000:
            print("stopping due to frame count limit")
            # for this example don't process too long videos
            break

    # Release capture devices
    cap.release()
    print(f'Detect faces {in_video_path} DONE')
    return face_count, data_rate


def download_from_you_tube(url):
    print(f'download {url}')

    yt = pytube.YouTube(url)
    file_name = yt.streams\
                  .filter(progressive=True, file_extension='mp4')\
                  .order_by('resolution')\
                  .desc()\
                  .first()\
                  .download(filename=f'face_count_'
                                     f'{url.split("=")[1].split("&")[0]}.mp4')

    print(f'download {url} DONE')
    return file_name


def plot_faces(faces_time_series, frame_rate, uid):
    print(f'plot faces {uid}')
    y = faces_time_series
    if frame_rate == UNKNOWN_FRAME_RATE or frame_rate == 0:
        x = [i for i in range(len(y))]
    else:
        x = [i/frame_rate for i in range(len(y))]
    fig = plt.figure()
    plt.plot(x, y)
    fig.savefig(f'{uid}_faces_plot.png', dpi=fig.dpi)
    plt.close("all")
    print(f'plot faces {uid} DONE')


def handle_url(url):

    try:
        video_file = download_from_you_tube(url)
    except urllib.error.HTTPError as e:
        print(f'{e} {url}')
        return [0], 1
    except KeyError as e:
        print(f'{e} {url}')
        return [0], 1
    except pytube.exceptions.VideoUnavailable as e:
        print(f'{e} {url}')
        return [0], 1
    except:
        print('Unknown error')
        print(f' {url}')
        return [0], 1

    faces_time_series, frame_rate = video_face_detection(video_file)
    return faces_time_series, frame_rate


def handle_urls_mp(urls):
    start = time.time()
    print(f"multi process {len(urls)} urls")
    thread_pool = Pool()
    res = thread_pool.map(handle_url, urls)
    end = time.time()
    print(f'multi process {len(urls)} urls took {end - start} sec')
    return res


# main
def main_mp():
    urls = parse_args()
    res = handle_urls_mp(urls)
    for uid, (faces_time_series, frame_rate) in enumerate(res):
        plot_faces(faces_time_series, frame_rate, uid)


def main_discomp():
    thread_pool = DPool()
    urls = parse_args()
    res = thread_pool.map(handle_url, urls)

    for uid, (faces_time_series, frame_rate) in enumerate(res):
        plot_faces(faces_time_series, frame_rate, uid)


def main_discomp_mp(batch_size=2):
    thread_pool = DPool()
    urls = parse_args()
    batches = [urls[i*batch_size:(i+1)*batch_size]
               for i in range(len(urls)//batch_size+1)]
    print(f'batch size {batch_size}, num batches {len(batches)}')

    res = thread_pool.map(handle_urls_mp, batches)
    all_res = []

    print(f'all batches returned')

    for r in res:
        all_res += r

    for uid, (faces_time_series, frame_rate) in enumerate(all_res):
        plot_faces(faces_time_series, frame_rate, uid)


def main_single_thread():
    urls = parse_args()
    for uid, url in enumerate(urls):
        faces_time_series, frame_rate = handle_url(url)
        plot_faces(faces_time_series, frame_rate, uid)


if __name__ == "__main__":
    main_start = time.time()
    main_single_thread()
    main_end = time.time()
    print(f'main compute took {main_end - main_start} sec')

