import json
import sys

def generate_ffmpeg_command(ladder_file, input_stream, output_dir):
    with open(ladder_file, 'r') as f:
        ladder = json.load(f)

    video_params = []
    for i, profile in enumerate(ladder):
        video_params.append(
            f"-filter:v:{i} scale=-2:{profile['height']} "
            f"-c:v:{i} libx264 -b:v:{i} {profile['bitrate']}k "
            f"-maxrate:v:{i} {profile['bitrate'] * 2}k -bufsize:v:{i} {profile['bitrate'] * 4}k "
            f"-g:v:{i} {profile['keyframe_interval']} -keyint_min:v:{i} {profile['keyframe_interval']} "
            f"-sc_threshold:v:{i} 0 -b_strategy:v:{i} 0 "
            f"-c:a:{i} aac -b:a:{i} {profile['audio_bitrate']}k"
        )

    video_params_str = " ".join(video_params)

    ffmpeg_cmd = (
        f"ffmpeg -i rtmp://localhost/live/{input_stream} "
        f"{video_params_str} "
        f"-f dash "
        f"-use_template 1 -use_timeline 1 "
        f"-seg_duration 4 -adaptation_sets \"id=0,streams=v id=1,streams=a\" "
        f"-init_seg_name init-\$RepresentationID\$.m4s -media_seg_name chunk-\$RepresentationID\$-\$Number%05d\$.m4s "
        f"{output_dir}/manifest.mpd"
    )

    return ffmpeg_cmd

if __name__ == "__main__":
    ladder_file, input_stream, output_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    print(generate_ffmpeg_command(ladder_file, input_stream, output_dir))