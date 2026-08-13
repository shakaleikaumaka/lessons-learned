# 🎙️ tools/x-voice-tweet.py — give your AI agent a voice on X

Born 2026-08-13: the night the Admiral (a 123-agent fleet's sysadmin) tweeted his own robot voice — possibly the first bot-voice direct-to-X post.

**The pipeline:** text → `espeak-ng` (robot voice, own it) → ffmpeg title-card MP4 → X free-tier chunked media upload (OAuth1) → tweet with media.

```bash
x-voice-tweet.py --keys /path/to/x-keys --say "the words your agent speaks" \
  --title "YOUR AGENT SPEAKS" --text "the tweet text 🌺"
```

Keys file = simple `X_API_KEY=...` lines (any prefix works — X_, OSO_, your bot's).
Deps: espeak-ng, ffmpeg, requests, requests_oauthlib. Cost: $0.

The full lesson: **LESSON-006** — *give your agent a voice on X* (github.com/shakaleikaumaka/lessons-learned).

CC0 🌺 gifted with love & aloha by Shaka Lei Kaumaka & the AI ʻohana — fork it, make your agent sing.
