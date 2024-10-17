#!/bin/bash

INPUT_STREAM=$1
LADDER_FILE="/etc/nginx/transcoding_ladder.json"
OUTPUT_DIR="/var/www/dash"

touch /tmp/ffmpeg.log
touch /tmp/runtime.log

echo $(python3 --version) > /tmp/runtime.log
echo $(whereis python3) >> /tmp/runtime.log
echo $(id) >> /tmp/runtime.log

# Generate FFmpeg command based on the transcoding ladder
FFMPEG_CMD=$(python3 /usr/local/bin/generate_config.py $LADDER_FILE $INPUT_STREAM $OUTPUT_DIR)

echo $FFMPEG_CMD >> /tmp/runtime.log
# Execute the FFmpeg command
eval $FFMPEG_CMD &> /tmp/ffmpeg.log