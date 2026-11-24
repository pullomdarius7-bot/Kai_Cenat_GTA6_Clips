#!/usr/bin/env bash
# Fast-Track export: Kai Cenat GTA 6 Day 1 VOD (VZqAPdUvqnQ), Clips 1-5.
# For each clip: download only that time window (+5s padding each side),
# re-encode frame-accurately for CapCut (-14 LUFS), then make word-level .srt captions.
#
# Usage:   bash export_clips.sh            (all 5 clips)
#          bash export_clips.sh 1 3        (only clips 1 and 3)
# If YouTube blocks you, add browser cookies:  COOKIES=chrome bash export_clips.sh
set -euo pipefail
cd "$(dirname "$0")"

URL="https://www.youtube.com/live/VZqAPdUvqnQ"
WS="workspaces/VZqAPdUvqnQ"
mkdir -p "$WS"/{raw,artifacts,previews,exports,logs}

# name|download_start|download_end|trim_offset_sec|duration_sec
CLIPS=(
  "clip01_prayer|00:07:47|00:08:29|5.0|32.0"
  "clip02_adaptive_triggers|00:27:59|00:28:43|5.0|34.0"
  "clip03_new_zealand_fomo|00:03:43|00:04:43|5.0|50.0"
  "clip04_2k_basketball|01:33:36|01:34:11|5.0|25.0"
  "clip05_screen_narration|00:09:45|00:10:27|5.0|32.0"
)

COOKIE_ARGS=()
[ -n "${COOKIES:-}" ] && COOKIE_ARGS=(--cookies-from-browser "$COOKIES")

want() { [ $# -eq 0 ] && return 0; for n in "${SEL[@]}"; do [ "$n" = "$1" ] && return 0; done; return 1; }
SEL=("$@")

i=0
for entry in "${CLIPS[@]}"; do
  i=$((i+1))
  if [ ${#SEL[@]} -gt 0 ] && ! want "$i"; then continue; fi
  IFS="|" read -r NAME DL_START DL_END OFFSET DUR <<< "$entry"
  echo "=== Clip $i: $NAME"

  # 1. Download only this window (5s padding each side)
  if [ ! -s "$WS/raw/${NAME}_padded.mp4" ]; then
    yt-dlp "${COOKIE_ARGS[@]}" \
      --download-sections "*${DL_START}-${DL_END}" \
      -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
      --merge-output-format mp4 \
      -o "$WS/raw/${NAME}_padded.mp4" "$URL" 2>&1 | tee "$WS/logs/${NAME}_download.log" | grep -vE '^\[download\] +[0-9.]+%' || true
  fi
  [ -s "$WS/raw/${NAME}_padded.mp4" ] || { echo "Download failed for $NAME (see $WS/logs)"; continue; }

  # 2. Frame-accurate re-encode + -14 LUFS loudness for CapCut
  ffmpeg -y -nostdin -loglevel error \
    -ss "$OFFSET" -i "$WS/raw/${NAME}_padded.mp4" -t "$DUR" \
    -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
    -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 48000 \
    "$WS/exports/${NAME}_capcut.mp4"

  # 3. 16kHz mono WAV for Whisper
  ffmpeg -y -nostdin -loglevel error -i "$WS/exports/${NAME}_capcut.mp4" \
    -vn -ac 1 -ar 16000 "$WS/raw/${NAME}_16k.wav"

  # 4. Word-level .srt (max 3 words per caption) -- skipped if faster-whisper isn't installed
  #    (it usually can't install on Android/Termux; use CapCut's Auto Captions instead)
  if python3 -c "import faster_whisper" 2>/dev/null; then
    python3 make_srt.py "$WS/raw/${NAME}_16k.wav" "$WS/exports/${NAME}.srt"
  else
    echo "faster-whisper not installed -> skipping .srt (use CapCut Auto Captions)"
  fi

  # 5. Quick QA: resolution, duration, black frames
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height:format=duration \
    -of compact "$WS/exports/${NAME}_capcut.mp4" | tee "$WS/logs/${NAME}_qa.txt"
  ffmpeg -nostdin -i "$WS/exports/${NAME}_capcut.mp4" -vf blackdetect=d=0.5:pix_th=0.10 -an -f null - 2>&1 \
    | grep -c black_start | xargs -I{} echo "black segments: {}" | tee -a "$WS/logs/${NAME}_qa.txt"
done

echo "Done. CapCut files are in $WS/exports/"

# On Android (Termux), copy finished clips to the phone's Movies folder so CapCut can see them
if [ -d "$HOME/storage/shared" ]; then
  DEST="$HOME/storage/shared/Movies/KaiCenat_GTA6"
  mkdir -p "$DEST"
  cp "$WS"/exports/* "$DEST"/
  echo "Copied to phone: Movies/KaiCenat_GTA6"
fi
