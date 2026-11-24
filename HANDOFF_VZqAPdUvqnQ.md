# Claude Code Handoff: Kai Cenat GTA 6 Day 1 VOD (`VZqAPdUvqnQ`) — Full 5-Clip Blueprint

Copy and paste this document into **Claude Code**. It includes verified metadata, verbatim transcripts for all 5 clips, full Phase 2 Cut-by-Cut Editing Blueprints for Clips 1–5, exact `yt-dlp` + `ffmpeg` + `faster-whisper` commands to export CapCut-ready slices and `.srt` files, your Voice Card rules, and the full 5-stage local VOD scan spec. Pair this with `post.md` for ready-to-paste TikTok, Instagram, and YouTube posts, hashtags, and creator shout-outs.

## Instructions for Claude Code

1. **Immediate Track (Clips 1–5 Fast Export):** Run the Fast-Track commands below to range-download Clips 1–5 from [Kai Cenat Live — PLAYING GTA 6 FOR THE FIRST TIME (DAY 1)](https://www.youtube.com/live/VZqAPdUvqnQ), re-encode each frame-accurately (`libx264 -crf 18 -pix_fmt yuv420p`, `-14 LUFS`), and run `faster-whisper` (`compute_type="int8"`, `word_timestamps=True`, max 3 words/cue) to export editable `.srt` files into `workspaces/VZqAPdUvqnQ/exports/`.
2. **CapCut (ClipCut) Interactive Walkthrough:** After the MP4 slices and `.srt` files are ready, ask me which clip (1–5) I want to edit first, then guide me through CapCut **one step at a time** using that clip's Cut-by-Cut Blueprint below. Wait for me to reply `done` after each step before giving the next one.
3. **Full VOD Scan Track (Optional / Background):** Only if I confirm, run the Stage 1–5 deterministic pipeline across hours 2–11 of the 11h 35m VOD to pull buried peaks that were not in the initial transcript sample.

## Verified Source Metadata & Creator Credits

| Field | Value |
| :--- | :--- |
| **Title** | 🌴PLAYING GTA 6 FOR THE FIRST TIME🌴 (DAY 1) |
| **Original Creator** | Kai Cenat (`@KaiCenatLive` on [YouTube](https://www.youtube.com/@KaiCenatLive) / `KaiCenat` on [Twitch](https://streamscharts.com/channels/kaicenat) / `@kai_cenat` on TikTok / `@kaicenat` on Instagram) |
| **Source VOD URL** | [https://www.youtube.com/live/VZqAPdUvqnQ](https://www.youtube.com/live/VZqAPdUvqnQ) |
| **Video ID** | `VZqAPdUvqnQ` |
| **Publish Date** | 2026-11-19 |
| **Duration** | `11:35:56` (`41,756s`) |
| **Views / Likes** | 12,487,887 views / 110,223 likes |
| **On-Screen Credit Pill** | `Source: @KaiCenatLive (YouTube / Twitch)` — place in upper corner or above center safe zone; never in the bottom 25% UI dead zone. |

## Voice & Copy Rules (Darius Pullom — `@viralclipppps` / `@viralclipppps31`)

- **Tone:** Direct, grounded, honest, plain-spoken. Talk like a real person—never scripted influencer hype or corporate jargon.
- **Structure:** Short to medium sentences, natural contractions (`I'm`, `don't`, `he's`), jump straight to the point.
- **Banned Words (Never Use):** `no fluff`, `fluff`, corporate filler (`delve`, `leverage`, `utilize`, `synergy`, `game-changer`).

## Phase 1: Viral Timestamp Extraction (All 5 Verified Clips)

| Clip # & Working Title | Source Timestamps (Edited Runtime) | Archetype | Expectation Gap (Hook) vs. Payoff | Retention Score | Key Cut Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. The 13-Year Prayer Before Loading GTA 6** | `00:07:52 – 00:08:24` (`22s`) | **A — Deadpan / Tension-Payoff** | **Hook:** Starts a genuine prayer thanking God for 13 years. **Payoff:** Accidentally curses mid-prayer, panics, and speed-runs the Lord's Prayer. | **9/10** | Preserve 0.6s panic beat after the slip; hard-cut on "Amen." |
| **2. Adaptive Triggers Ruined His First Robbery** | `00:28:04 – 00:28:38` (`22s`) | **B — Reaction / Narrated Split-Screen** | **Hook:** Hyped watching Lucia pull a stick-up. **Payoff:** PS5 adaptive triggers lock up mid-robbery and he spirals yelling to turn them off. | **8.5/10** | Cut the silent gap around `00:28:26` so tension snaps straight into the trigger rant. |
| **3. Changed Servers to New Zealand to Beat FOMO** | `00:03:48 – 00:04:38` (`24s`) | **C — High-Velocity Storytelling** | **Hook:** Opens dead serious: "We in New Zealand, don't even ask." **Payoff:** Admits he couldn't sleep, felt like Christmas, and swapped servers shirtless at 8 AM. | **8/10** | Strip every "um" and pause; cut every 1.5–2.5s onto punchlines. |
| **4. GTA 6 vs. 2K Basketball ("Oh Hell No")** | `01:33:41 – 01:34:06` (`18s`) | **B — Reaction / Narrated Split-Screen** | **Hook:** Loads up in-game basketball hyped ("2K you're finished"). **Payoff:** Realizes he can't cross over and yells "oh hell no" six times. | **8/10** | Keep gameplay + facecam locked 40/60; hard-cut on the final "oh hell no." |
| **5. 13 Years of Hype Ruined by Screen Narration** | `00:09:50 – 00:10:22` (`20s`) | **A — Deadpan / Tension-Payoff** | **Hook:** Claps it up shirtless after waiting 13 years ("here we go, I'm scared"). **Payoff:** First thing GTA 6 blasts at him is "press square to enable screen narration" and he panics spamming "OFF OFF OFF." | **8.5/10** | Keep the raw hype buildup clean, then punch-in 180% when the narration prompt interrupts him. |

## Verbatim Video Transcripts (Clips 1–5)

### Clip 1 Transcript (`00:07:52 – 00:08:24`)
```text
[00:07:52] i'm scared bro um let me go
[00:07:59] ahead and say god thank you so much for this moment i waited 13 years god thank you so much
[00:08:03] for making me survive this long god thank you so much for making me come this long please thank you
[00:08:06] so much we don't have to use anymore before gta um shits any uh joke anymore i didn't mean to
[00:08:11] curse god um our father who are in heaven hallowed be thy name thy kingdom come thy will be done
[00:08:15] on earth is in heaven give us this day our daily bread forgive us our trespasses as we forgive those
[00:08:18] who trespass against us and lead us not into temptation but deliver us from evil amen
```

### Clip 2 Transcript (`00:28:04 – 00:28:38`)
```text
[00:28:04] where are you got it oh she like that oh oh lucia like that oh this oh she like oh
[00:28:11] shit okay oh she this is a stick up hands up stop the fucking stick up
[00:28:26] moment don't
[00:28:33] hands up wait adaptive triggers adapt adaptive adaptive triggers is on turn this bullshit the fuck off no no no
```

### Clip 3 Transcript (`00:03:48 – 00:04:38`)
```text
[00:03:48] first things first i want to go ahead and tell y'all bro we in new zealand bitch okay don't even
[00:03:55] ask now bro all right listen okay um first things first this is what i want to say chat this
[00:04:02] is what i want to say i did not sleep tonight bro this is the first time in a long
[00:04:07] time where it felt like christmas my my nigga that ass like this is the first time bro this gave
[00:04:13] me memories of like but i was in my bed and i was just i was just on like social
[00:04:20] media but as i was on social media i'm seeing hell of shit i'm just seeing gta 6 is out
[00:04:27] everybody booing it up i got fomo immediately so what did i did i changed servers immediately bro that i
[00:04:34] hopped on that flight and and did what i had to do no shirt no i'm off the wake up
[00:04:38] like chat it's 8 a.m what are you doing wake up what are you doing
```

### Clip 4 Transcript (`01:33:41 – 01:34:06`)
```text
[01:33:41] oh my god okay let's see basketball
[00:13:50 -> 01:33:50] oh one 2k your finish okay i can't cross over or nothing
[01:34:00] oh hell no oh hell no hell no hell no hell no oh hell no you can't quit me whipping
[01:34:06] w the neighborhood
```

### Clip 5 Transcript (`00:09:50 – 00:10:22`)
```text
[00:09:50] we've been waiting 13 years holy shit holy shit okay here we go i'm done talking everybody clap it up here we go oh
[00:09:57] my god i'm scared and i got a fire i got a fire monitor i have the best monitor so
[00:10:02] everything like i'm going to see i have no shirt on that is his bitch do i sound li
[00:10:12] oh my fucking god
[00:10:15] oh my god oh my god press square to enable screen narration no off screen square off off off off
```

## Phase 2: Full Cut-by-Cut Editing Blueprints (Clips 1–5)

### Blueprint — Clip 1: The 13-Year Prayer Before Loading GTA 6

- **Target Runtime:** `22s` | **Archetype:** `A — Deadpan / Tension-Payoff`
- **Frame Layout:** Full-bleed `9:16` (`1080x1920`) facecam crop, eyes locked at **38% from top** across all zooms.
- **Persistent Hook Banner (`0:00–0:22`):** Upper third safe zone (20% from top), white rounded box, bold black sans-serif: `HE PRAYED BEFORE LOADING GTA 6...`
- **Native UI / Credit Layer:** Live chat strip cropped top-right + subtle credit pill `Source: @KaiCenatLive (YouTube / Twitch)` below hook banner.

| Edited Time | Source Time | Visual, Framing & Zoom % | Captions, Status Tags & Overlays | Audio, BGM & SFX | Retention Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0:00–0:03` | `00:07:52–00:07:55` | `100%` baseline 9:16 facecam (eyes at 38%). Cut phone-drop dead air and "um." | Hook banner locked. Center white/black-stroke captions: `I'm scared bro.` -> `God, thank you` | Dry speech only. | Zero-Second Entry / Hook |
| `0:03–0:09` | `00:07:59–00:08:05` | Hold `100% -> 108%` slow creep zoom. **Zero hard cuts.** | `waited 13 YEARS` (`13 YEARS` yellow) -> `making me survive this long` + tag `*GENUINELY LOCKED IN*` | Soft solo piano fades in low (`-24 LUFS`). | Tension Buildup |
| `0:09–0:13` | `00:08:06–00:08:10` | **MIDPOINT SPIKE:** Hold on "before GTA... shits", then **hard cut to `180%` punch-in** (eyes locked at 38%). **PRESERVE** 0.6s panic beat. | Shift red/yellow: `before GTA... SHITS` -> `I DIDN'T MEAN TO CURSE GOD` + tag `*INSTANT REGRET*` | Hard-cut piano to silence on `SHITS` + single subtle bass thump SFX (`-14 LUFS`). | Midpoint Spike (45%) |
| `0:13–0:21` | `00:08:11–00:08:21` | Pull back to `120%` tight crop (eyes at 38%). Strip breaths `> 0.3s`. | Rapid center captions: `Our Father...` -> `deliver us from evil` + tag `*DAMAGE CONTROL*` | Dry voice or faint choir sting (`-26 LUFS`). | Payoff Escalation |
| `0:21–0:22` | `00:08:21–00:08:22` | Snap to `160%` punch-in (eyes at 38%). | Oversized white/yellow: `AMEN.` | Hard-cut immediately on final syllable of `Amen` (8 frames max). | Abrupt Outro / Loop |

**Audit:** [x] Reveal held past 40% | [x] Zero intro/outro lag | [x] Bottom 25% clear + eyeline locked | [x] No ping-ponging or SFX spam | [x] Transformative framing + credit pill.

### Blueprint — Clip 2: Adaptive Triggers Ruined His First Robbery

- **Target Runtime:** `22s` | **Archetype:** `B — Reaction / Narrated Split-Screen`
- **Frame Layout:** `40/60` vertical split-screen (`1080x768` facecam on top, `1080x1152` GTA 6 robbery gameplay on bottom). Facecam eyes locked at **20% from top**.
- **Persistent Hook Banner (`0:00–0:22`):** Bold white-on-black matte bar at top safe zone: `PS5 CONTROLLERS RUINED HIS FIRST GTA 6 ROBBERY`
- **Native UI / Credit Layer:** Subtle `Source: @KaiCenatLive` pill pinned right below the top bar; active captions centered directly on the `40/60` split-screen seam.

| Edited Time | Source Time | Visual, Framing & Zoom % | Captions, Status Tags & Overlays | Audio, BGM & SFX | Retention Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0:00–0:04` | `00:28:04–00:28:08` | `40/60` split-screen (`100%` facecam top / `100%` gameplay bottom). Open frame 0 on vocal spike. | Seam captions: `OH LUCIA LIKE THAT` (`LUCIA` cyan) + tag `*LOCKED IN*` | Raw game audio + Kai's voice, dry (no BGM). | Zero-Second Entry / Setup |
| `0:04–0:10` | `00:28:09–00:28:16` | Hold `40/60` split-screen; slight `110%` zoom on bottom gameplay showing the stick-up action. | `THIS IS A STICK UP` -> `HANDS UP` (yellow) | Keep raw robbery tension audio; strip dead air after `00:28:16`. | Action Momentum |
| `0:10–0:11` | `00:28:17–00:28:32` | **CUT** the dead air between `00:28:17` and `00:28:32` (keep only `0.3s` transition beat if Lucia aims). | Brief flash tag: `*TRIGGER LOCKS UP*` | Clean hard cut into the panic vocal spike. | Pacing Tightening |
| `0:11–0:18` | `00:28:33–00:28:37` | **MIDPOINT SPIKE:** Keep `40/60` split, punch top facecam to `175%` (eyes locked at 20% height) as he realizes adaptive triggers are on. | Red/yellow kinetic seam captions: `WAIT... ADAPTIVE TRIGGERS?!` -> `TURN THIS OFF` + tag `*PANICKING*` | Quick bass drop / alert ping SFX on `ADAPTIVE TRIGGERS`, then raw yelling at `-14 LUFS`. | Midpoint Spike (50%) |
| `0:18–0:22` | `00:28:37–00:28:38` | Punch top facecam to `200%` (eyes locked at 20% height) on final panic yell. | Oversized red text on seam: `NO NO NO!` | Hard-cut abruptly mid-final `NO` (zero trailing breath). | Abrupt Outro / Loop |

**Audit:** [x] Reveal held past 45% | [x] Dead gap cleanly stripped | [x] Seam captions avoid bottom 25% | [x] No camera ping-ponging | [x] Transformative split-screen + credit pill.

### Blueprint — Clip 3: Changed Servers to New Zealand to Beat FOMO

- **Target Runtime:** `24s` | **Archetype:** `C — High-Velocity Storytelling`
- **Frame Layout:** Full-bleed `9:16` (`1080x1920`) facecam crop, eyes locked at **36% from top** across all jump cuts.
- **Persistent Hook Banner (`0:00–0:24`):** White rounded box in upper third: `BRO REALLY CHANGED TIME ZONES FOR GTA 6`
- **Native UI / Credit Layer:** Small `8:00 AM • NEW ZEALAND SERVER` location/time chyron pill in upper-right + `Source: @KaiCenatLive` credit pill.

| Edited Time | Source Time | Visual, Framing & Zoom % | Captions, Status Tags & Overlays | Audio, BGM & SFX | Retention Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0:00–0:03` | `00:03:48–00:03:52` | `115%` medium facecam (eyes at 36%). Strip "first things first" lead-in—enter right on `bro we in New Zealand`. | Center captions: `WE IN NEW ZEALAND` (`NEW ZEALAND` yellow) -> `DON'T EVEN ASK` | Dry speech + light upbeat trap/lo-fi groove enters softly (`-24 LUFS`). | Zero-Second Entry / Curiosity Gap |
| `0:03–0:09` | `00:04:02–00:04:09` | **CUT** `00:03:53–00:04:01` filler. Hard cut to `105%` (eyes at 36%). Strip all "um"s and restarts. | `I DID NOT SLEEP TONIGHT` -> `FELT LIKE CHRISTMAS` (`CHRISTMAS` cyan) | Keep light groove steady under voice. | High-Velocity Setup |
| `0:09–0:15` | `00:04:15–00:04:27` | Hard cut to `130%` tighter crop (eyes at 36%). Cut straight from `in my bed` -> `seeing GTA 6 is out` -> `got FOMO immediately`. | `GTA 6 IS OUT` -> `GOT FOMO IMMEDIATELY` (red highlight) + tag `*ZERO SELF CONTROL*` | Slight rhythmic bass rise into the FOMO admission. | Midpoint Escalation (45%) |
| `0:15–0:21` | `00:04:28–00:04:36` | **MIDPOINT SPIKE:** Hard cut to `170%` punch-in (eyes locked at 36%) on `changed servers immediately` -> `hopped on that flight`. | `CHANGED SERVERS IMMEDIATELY` -> `NO SHIRT, OFF THE WAKE UP` (yellow) | Quick airplane-chime or whoosh SFX (`-18 LUFS`) strictly on `hopped on that flight`. | Payoff Punchline |
| `0:21–0:24` | `00:04:37–00:04:39` | Snap to `190%` tight reaction crop (eyes at 36%). | `IT'S 8 AM — WAKE UP!` (white/yellow) | Hard-cut music + voice directly on final `WAKE UP!` | Abrupt Outro |

**Audit:** [x] 100% dead air stripped | [x] Cuts every 2–3s onto punchlines | [x] Eyelines locked at 36% | [x] Bottom 25% clear | [x] Transformative pacing + credit pill.

### Blueprint — Clip 4: GTA 6 vs. 2K Basketball ("Oh Hell No")

- **Target Runtime:** `18s` | **Archetype:** `B — Reaction / Narrated Split-Screen`
- **Frame Layout:** `40/60` vertical split-screen (`1080x768` facecam top / `1080x1152` GTA 6 basketball court gameplay bottom). Facecam eyes locked at **20% from top**.
- **Persistent Hook Banner (`0:00–0:18`):** Bold outlined text in upper third: `HE THOUGHT GTA 6 WAS GOING TO END NBA 2K...`
- **Native UI / Credit Layer:** Subtle `Source: @KaiCenatLive` pill top-left; seam captions centered on the split line.

| Edited Time | Source Time | Visual, Framing & Zoom % | Captions, Status Tags & Overlays | Audio, BGM & SFX | Retention Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0:00–0:04` | `01:33:41–01:33:46` | `40/60` split-screen (`100%` facecam / `100%` court). Open frame 0 on `okay let's see basketball`. | Seam captions: `OKAY LET'S SEE BASKETBALL` (`BASKETBALL` orange/yellow) | Raw game + voice audio, dry. | Zero-Second Entry / Expectation Gap |
| `0:04–0:09` | `01:33:50–01:33:55` | Hold `40/60` split; slight `110%` zoom on bottom player dribbling. Cut any silent loading pause between `01:33:46` and `01:33:50`. | `2K YOU'RE FINISHED!` (cyan) -> `I CAN'T CROSS OVER OR NOTHING` + tag `*REALIZATION HITTING*` | Soft comedic record-scratch or dead-air beat as he realizes he can't dribble. | Midpoint Twist (45%) |
| `0:09–0:15` | `01:34:00–01:34:04` | **MIDPOINT SPIKE:** Punch top facecam to `180%` (eyes locked at 20% height) while keeping bottom gameplay visible so viewers see the clunky shot/dribble. | Rapid red/white stacking seam captions: `OH HELL NO` x4 + tag `*2K IS SAFE*` | Raw yelling normalized to `-14 LUFS`; optional faint sad-trombone or comedic bass thump under first `OH HELL NO`. | Comedic Payoff |
| `0:15–0:18` | `01:34:04–01:34:06` | Snap top facecam to `200%` (eyes locked at 20% height) on final repetition. | Oversized red text: `OH HELL NO!` | Hard-cut abruptly right after the 6th `OH HELL NO` (cut before `you can't quit me`). | Abrupt Outro / Comment Bait |

**Audit:** [x] Reveal held until 45% mark | [x] Gameplay + reaction visible together | [x] Seam captions clear of bottom 25% | [x] Zero dead tail | [x] Transformative edit + credit pill.

### Blueprint — Clip 5: 13 Years of Hype Ruined by Screen Narration

- **Target Runtime:** `20s` | **Archetype:** `A — Deadpan / Tension-Payoff`
- **Frame Layout:** `40/60` split-screen (`1080x768` facecam top / `1080x1152` GTA 6 launch screen bottom), switching to full-bleed `9:16` facecam if the launch screen is black. Eyes locked at **22% from top** in split-screen (or **38%** if full-bleed).
- **Persistent Hook Banner (`0:00–0:20`):** White rounded box in upper third: `WAITED 13 YEARS FOR GTA 6 JUST FOR THIS TO HAPPEN`
- **Native UI / Credit Layer:** Live chat strip or `Source: @KaiCenatLive` pill in upper corner; captions on center/seam.

| Edited Time | Source Time | Visual, Framing & Zoom % | Captions, Status Tags & Overlays | Audio, BGM & SFX | Retention Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0:00–0:05` | `00:09:50–00:09:56` | `100%` baseline framing. Enter frame 0 on `we've been waiting 13 years`. Keep the clap-it-up hype intact. | `WAITING 13 YEARS` (`13 YEARS` yellow) -> `EVERYBODY CLAP IT UP!` | Dramatic/cinematic swelling synth pad enters low (`-24 LUFS`) to exaggerate the epic moment. | Zero-Second Entry / Hype Setup |
| `0:05–0:10` | `00:09:57–00:10:04` | Slow `100% -> 112%` creep zoom. Cut `got a fire monitor` tangent cleanly (`00:09:58–00:10:01`) so it jumps straight from `I'm scared` to `I have no shirt on`. | `I'M SCARED` -> `I HAVE NO SHIRT ON` + tag `*PEAK HYPE*` | Swell synth pad slightly louder (`-20 LUFS`) right before the game loads. | Tension Buildup |
| `0:10–0:14` | `00:10:12–00:10:16` | **MIDPOINT SPIKE:** Hold as he yells `oh my god`, then **hard-cut to `180%` punch-in** (eyes locked) the exact second the robotic voice reads `Press square to enable screen narration`. | Cyan robotic-font caption: `[PRESS SQUARE TO ENABLE SCREEN NARRATION]` + tag `*MOOD KILLED*` | **Audio whiplash:** Hard-cut the epic synth pad to dead silence the exact frame the robotic narration starts. | Midpoint Spike (50%) |
| `0:14–0:20` | `00:10:17–00:10:21` | Snap to `200%` tight facecam (eyes locked) as he panics spamming the button. | Rapid red/white pop-ins: `NO! OFF!` -> `OFF! OFF! OFF!` | Raw frantic yelling at `-14 LUFS`. Hard-cut abruptly on the final `OFF!` | Abrupt Outro / Loop |

**Audit:** [x] Epic buildup vs. comedic interruption past 50% | [x] Monitor tangent trimmed | [x] Audio whiplash cleanly timed | [x] Safe caption zones + eyeline lock | [x] Transformative edit + credit pill.

## Fast-Track Commands for Claude Code (Export All 5 Clips + SRTs)

```bash
mkdir -p workspaces/VZqAPdUvqnQ/{raw,artifacts,previews,exports,logs}

# Array of clips: name|dl_start|dl_end|trim_offset|duration
CLIPS=(
  "clip01_prayer|00:07:47|00:08:29|5.0|32.0"
  "clip02_adaptive_triggers|00:27:59|00:28:43|5.0|34.0"
  "clip03_new_zealand_fomo|00:03:43|00:04:43|5.0|50.0"
  "clip04_2k_basketball|01:33:36|01:34:11|5.0|25.0"
  "clip05_screen_narration|00:09:45|00:10:27|5.0|32.0"
)

for entry in "${CLIPS[@]}"; do
  IFS="|" read -r NAME DL_START DL_END OFFSET DUR <<< "$entry"

  # 1. Lazy range-download with 5s padding
  yt-dlp --extractor-args "youtube:player_client=android,web" \
    --download-sections "*${DL_START}-${DL_END}" \
    -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
    --merge-output-format mp4 \
    -o "workspaces/VZqAPdUvqnQ/raw/${NAME}_padded.mp4" \
    "https://www.youtube.com/live/VZqAPdUvqnQ"

  # 2. Frame-accurate re-encode + -14 LUFS loudness normalization for CapCut
  ffmpeg -y -nostdin -loglevel error \
    -ss "${OFFSET}" -i "workspaces/VZqAPdUvqnQ/raw/${NAME}_padded.mp4" -t "${DUR}" \
    -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
    -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 48000 \
    "workspaces/VZqAPdUvqnQ/exports/${NAME}_capcut.mp4"

  # 3. 16kHz mono WAV for word-level faster-whisper SRT generation
  ffmpeg -y -nostdin -loglevel error \
    -i "workspaces/VZqAPdUvqnQ/exports/${NAME}_capcut.mp4" \
    -vn -ac 1 -ar 16000 "workspaces/VZqAPdUvqnQ/raw/${NAME}_16k.wav"
done
```

After running the loop:
1. Run `faster-whisper` (`compute_type="int8"`, `vad_filter=True`, `word_timestamps=True`, max 3 words per subtitle cue) on each `workspaces/VZqAPdUvqnQ/raw/*_16k.wav` and save `workspaces/VZqAPdUvqnQ/exports/<name>.srt`.
2. Verify A/V sync drift `<= 50 ms` and `blackdetect` = 0 via `ffprobe` / `ffmpeg`.
3. Ask me which clip (1–5) to edit first and walk me through CapCut one step at a time.

## Optional Full 11.5-Hour VOD Scan Spec (Stages 1–5 — Hours 2–11)

Only run this if I confirm I want buried moments from hours 2–11:
- **Stage 1:** Audio-only 16kHz mono WAV via `yt-dlp -x --audio-format wav` + `--write-subs --sub-langs live_chat` normalized line-by-line into `raw/chat_normalized.jsonl`. Strict O(1) RAM.
- **Stage 2:** Stream 1s RMS/dBFS bins (`Z_audio >= 2.5`, `delta_dB >= 6.0`, `L_t > -30.0 dBFS`) + 10s Anscombe chat velocity (`Z_chat >= 3.0`, `M_chat >= 2.5`, `C_raw >= 5`), backward lag alignment `tau` (`2–15s`), fused score `H(t) >= 3.2`, pad `-45s / +25s` (cap `150s`).
- **Stage 3–5:** Scoped `faster-whisper` on candidate windows -> LLM editorial scoring (`>= 7.5`) -> lazy range-download + QA gate.
