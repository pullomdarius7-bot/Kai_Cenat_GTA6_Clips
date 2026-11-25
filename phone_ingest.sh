#!/usr/bin/env bash
# Termux: grab a stream's audio + YouTube captions, find the loudest moments,
# and drop the transcript files in your phone's Download folder to send to Claude.
#
# Usage:  bash phone_ingest.sh                 (uses the default stream below)
#         bash phone_ingest.sh <YouTube URL>   (any other stream/VOD)
cd "$(dirname "$0")" || exit 1

URL="${1:-https://www.youtube.com/watch?v=6r62rTzESks}"
# Pull the 11-character video ID out of the link (works for /live/, watch?v=, youtu.be)
VID=$(echo "$URL" | sed -E 's#.*(v=|/live/|youtu\.be/|/shorts/)([A-Za-z0-9_-]{11}).*#\2#')
WS="workspaces/$VID"
DEST="$HOME/storage/shared/Download/clip_ingest_$VID"

# 1) Phone storage must be connected so the results can land in Download
if [ ! -d "$HOME/storage/shared" ]; then
  echo "Phone storage not connected. Run: termux-setup-storage  (tap Allow), then run this again."
  exit 1
fi

# 2) Install tools only if they're missing (python, ffmpeg, node for YouTube's JS check)
for p in python ffmpeg nodejs; do
  bin=$p; [ "$p" = nodejs ] && bin=node
  command -v "$bin" >/dev/null || pkg install -y "$p"
done
# Always update yt-dlp: YouTube breaks old versions often
pip install -q -U "yt-dlp[default]" || pip install -q -U yt-dlp

mkdir -p "$WS" "$DEST"
JS_ARGS=""; command -v node >/dev/null && JS_ARGS="--js-runtimes node"

echo "Downloading audio + captions for $VID (audio only, so it's much smaller than the video)..."
# Pass the JS runtime flag through a yt-dlp config file so the ingest script picks it up
CONF="$HOME/.config/yt-dlp/config"; mkdir -p "$(dirname "$CONF")"
if [ -n "$JS_ARGS" ] && ! grep -q -- "--js-runtimes" "$CONF" 2>/dev/null; then
  echo "$JS_ARGS" >> "$CONF"
fi

ok=0
for attempt in 1 2 3; do
  if python tools/ingest_and_transcribe.py "$URL" --out-dir "$WS" --skip-whisper \
       > "$WS/ingest.log" 2>&1 && [ -s "$WS/transcript_readable.txt" ]; then
    ok=1; break
  fi
  echo "Attempt $attempt didn't finish. Last lines:"; tail -3 "$WS/ingest.log"
  [ $attempt -lt 3 ] && { echo "Retrying in 30s..."; sleep 30; }
done

if [ $ok -ne 1 ]; then
  echo "FAILED. The full log is at $WS/ingest.log"
  echo "If it says 'Sign in to confirm you're not a bot', turn Wi-Fi off and try on mobile data."
  exit 1
fi

# 3) The big WAV file isn't needed anymore (the render step downloads its own piece)
rm -f "$WS/audio_16k.wav"

cp "$WS"/transcript_readable.txt "$WS"/transcript_words.json "$WS"/audio_peaks.json "$DEST"/
[ -f "$WS/meta.json" ] && cp "$WS/meta.json" "$DEST"/
command -v termux-media-scan >/dev/null && termux-media-scan -r "$DEST" >/dev/null 2>&1

echo
echo "DONE. Lines in transcript: $(wc -l < "$WS/transcript_readable.txt")"
echo "Send Claude these files from Download/clip_ingest_$VID:"
echo "  transcript_readable.txt   audio_peaks.json   (and meta.json if it's there)"
