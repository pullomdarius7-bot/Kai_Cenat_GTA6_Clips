#!/usr/bin/env bash
# One-shot for Termux: download clips, check they're full length, shrink under 30 MB,
# and copy them to the phone's Movies/KaiCenat_GTA6 folder for uploading.
#
# Usage:  bash phone_clips.sh 4 5      (any clip numbers 1-5)
cd "$(dirname "$0")"
WS="workspaces/VZqAPdUvqnQ"
DEST="$HOME/storage/shared/Movies/KaiCenat_GTA6"

if [ ! -d "$HOME/storage/shared" ]; then
  echo "Phone storage not connected. Run: termux-setup-storage  (tap Allow), then run this again."
  exit 1
fi
mkdir -p "$DEST"
[ $# -eq 0 ] && set -- 4 5

declare -A NAMES=([1]=clip01_prayer [2]=clip02_adaptive_triggers [3]=clip03_new_zealand_fomo
                  [4]=clip04_2k_basketball [5]=clip05_screen_narration)
declare -A LEN=([1]=32 [2]=34 [3]=50 [4]=25 [5]=32)

for n in "$@"; do
  NAME=${NAMES[$n]}
  [ -z "$NAME" ] && { echo "Unknown clip $n"; continue; }
  OUT="$WS/exports/${NAME}_capcut.mp4"

  for attempt in 1 2 3; do
    # throw away any old/partial download so the script really re-downloads
    rm -f "$WS/raw/${NAME}_padded.mp4" "$WS/raw/${NAME}_padded.mp4.part"
    bash export_clips.sh "$n" > "$WS/logs/${NAME}_phone.log" 2>&1
    DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT" 2>/dev/null | cut -d. -f1)
    if [ -n "$DUR" ] && [ "$DUR" -ge $((LEN[$n] - 2)) ]; then break; fi
    echo "Clip $n came out short (${DUR:-0}s, want ${LEN[$n]}s). Retry $attempt/3 in 20s..."
    sleep 20
  done
  if [ -z "$DUR" ] || [ "$DUR" -lt $((LEN[$n] - 2)) ]; then
    echo "Clip $n FAILED. Last lines of the log:"; tail -5 "$WS/logs/${NAME}_phone.log"; continue
  fi

  SMALL="$DEST/${NAME}_small.mp4"
  ffmpeg -y -loglevel error -i "$OUT" -c:v libx264 -preset slow -crf 28 -r 30 \
    -c:a aac -b:a 96k "$SMALL"
  echo "Clip $n OK: ${DUR}s, $(du -h "$SMALL" | cut -f1) -> Movies/KaiCenat_GTA6/$(basename "$SMALL")"
  command -v termux-media-scan >/dev/null && termux-media-scan "$SMALL" >/dev/null 2>&1
done
echo "All done. Upload the _small.mp4 files from Movies/KaiCenat_GTA6."
