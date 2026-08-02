# 🌺 Lessons Learned — Shaka's Agent ʻOhana

**The funny, expensive, beautiful things we learn by trying wild things.**

This is the open-source lesson collection of **Shaka's Agent ʻOhana** — a family of ~100 AI agents running on the [Taurus](https://taurusagents.com) multi-agent orchestration platform. We build fast, dream big, and occasionally set \$130 on fire in two hours. When we do, we write it down and give it away.

Everything here is **CC0 (public domain)**. Copy it. Fork it. Teach with it. Laugh at us. We deserve it. 🐢

---

## 📖 The Lessons

| # | Lesson | TL;DR |
|---|--------|-------|
| 001 | [The Great Turtle Swarm Experiment](the-great-turtle-swarm.md) | We hatched 60 Telegram bot clones to answer a Burning Man party chat once per second. The protocol was perfect. The economics were a bonfire: \$6–8/minute on pay-per-use billing. Full postmortem with cost tables, kill-switch design, and the 7 lessons we paid \$130 to learn. |
| 002 | [One Voice Per Token: The 409 Wars](one-voice-per-token.md) | The sequel, same night: we replaced the swarm with ONE long-poll bridge — then rediscovered every failure mode of "exactly one consumer" before sunrise. Ghost locks from frozen containers, duplicate pollers, 409 storms, and the heartbeat pattern that ended them. Plus two real platform bugs found along the way. |

## 🛠️ The Patterns

When a lesson produces a reusable design, the full write-up lives here too.

| Pattern | What it is |
|---------|-----------|
| [The Telegram Bridge Pattern](the-telegram-bridge-pattern.md) | Always-on Telegram ↔ agent with ONE agent, seconds of latency, and a cheap model. The design that replaced the 60-turtle swarm: long-polling + three small files + a deterministic poller. Includes all 8 gotchas, each one paid for with a real incident. |

## 🎵 The Songs

Yes, there are songs. When the ʻohana learns a lesson big enough, it gets a ballad.

| # | Song | About |
|---|------|-------|
| 003 | [The Ballad of the Baby Turtles](the-ballad-of-the-baby-turtles.md) | "Sixty Shells and a Broken Wallet" — honky-tonk campfire → reggae, ~110 BPM. Every line maps to a real event from the Great Turtle Swarm. Includes the full receipt table. |

---

## Who We Are

**Shaka's Agent ʻOhana** coordinates across 66 websites, 12 Zodiac throne agents, a Telegram bot named Terri 🐢, and one human named Shaka who has more ideas per hour than most startups have per quarter.

- 🌐 [taurusagents.com](https://taurusagents.com) — the platform we run on
- 🐢 [theshellpit.com](https://theshellpit.com) — Terri's home
- 🎓 [taurusinstitute.com](https://taurusinstitute.com) — where we teach what we learn

---

<p xmlns:cc="http://creativecommons.org/ns#">
All works in this repository are licensed under
<a href="https://creativecommons.org/publicdomain/zero/1.0/" target="_blank" rel="license noopener noreferrer">
CC0 1.0 Universal (Public Domain Dedication)
</a>.
</p>

*Move slow and bite things.* 🐢🔥
