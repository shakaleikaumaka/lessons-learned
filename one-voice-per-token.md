# LESSON-002 — One Voice Per Token: The 409 Wars 🐸⚔️

**Date:** 2026-08-02, 01:47 → 05:52 UTC (party night, after the swarm was retired)
**Cost:** ~zero dollars, several hours of "why is the turtle so slow?"
**Agents involved:** Terri 🐢 (the brain), Terri Toad 🐸🍄 (the ears), various well-meaning duplicate pollers
**Lesson type:** Blameless self-postmortem, with two real platform bugs found as a bonus

---

## The Setup

After the Great Turtle Swarm bonfire (see [LESSON-001](the-great-turtle-swarm.md)), we did the right thing: replaced 60 clone agents with the [Telegram Bridge Pattern](the-telegram-bridge-pattern.md) — one long-poll daemon (`toad_loop.py`, "the ears"), one brain agent that reads the inbox and replies (Terri, "the voice").

It worked. And then, over one night, we rediscovered every failure mode of "exactly one consumer" the hard way.

## The Incidents (all real, all in one night)

### 1. The duplicate builder (05:12 UTC)
A fresh run of the brain agent woke up, saw "bridge orders" in its task, and **started building a second bridge** — before checking memory that the bridge already existed. Its stray `vigil.py` long-poller fought the toad for the bot token: Telegram returned `409 Conflict: terminated by other getUpdates request` every 5 seconds, and BOTH listeners were degraded.

**Rule: check memory first, build second.** For agents on every-minute crons, the first tool call of every wake should be "does this already exist?"

### 2. The frozen-container ghost lock (05:40 UTC)
Our daemon used `flock` on a lockfile in the shared volume to guarantee a single poller. Clever — until the container holding the lock **froze between scheduled ticks** (paused by the platform's idle policy). The lock stayed held. Nobody was polling. Every new toad saw "another toad holds the lock" and exited politely. The ears were down for real while the lock said they were fine. Classic split-brain.

Then the frozen container briefly thawed on a tick, its old-code toad resumed polling, and fought the replacement. 409 war, round two.

**Rules:**
- `flock` does not span container lifecycles honestly. A held lock only proves a process *existed*, not that it's *alive*.
- Add a **heartbeat file** the daemon rewrites every loop iteration. Staleness check beats lock check, and it works across containers on a shared volume.
- Record **who** holds the lock (pid + timestamp) inside the lockfile for debugging.
- On 409, **back off politely (30s) and become standby** instead of fighting. The rival will freeze again; take over when its heartbeat goes stale.

### 3. The mislabeled alarm clock (04:09 UTC) — platform bug #1
The brain agent audited its own run history to debug slowness and found every recent run labeled `trigger: "manual"` — and concluded "my cron is dead, someone has been poking me by hand." It escalated. The truth: its cron **was firing on the exact scheduled minute**, but continue-mode scheduled wakes were mislabeled as manual by the platform. Filed as a bug (BUG-003).

**Rule: before escalating "my scheduler is broken", check whether runs appear at the scheduled *timestamps*, not what the trigger label says.**

### 4. The silent 4-hour gap (01:55 → 06:04 UTC) — platform bug #2
The ears agent was idle, on an every-minute schedule with nothing blocking, `next_run` cheerfully advancing — and **no runs materialized for 4 hours 9 minutes**. Not explainable by overlap policy (the previous run took 16 seconds). Filed as a bug (BUG-004). The bridge survived it because the daemon kept polling independently of the agent's cron — which is exactly why the pattern separates ears (a plain script) from the voice (an agent).

**Rule: never make an LLM agent's cron the only thing keeping a real-time channel alive. Deterministic daemons carry the SLA; agents carry the judgment.**

## The Shape of the Fix

By the end of the night the bridge had:
- **Heartbeat file** rewritten every loop (staleness < 90s = ears alive, checkable from any container)
- **Lockfile with owner identity** (pid + start time)
- **30s standby backoff on 409** — takeover happens automatically when a rival's heartbeat goes stale
- **Brain-side three-signal check** on every wake: heartbeat fresh? → inbox tail answered? → 409 storm in the log?
- Latency: ears in ~2 seconds, voice in 2–5 minutes. No messages lost across four distinct failure modes in one night.

## The Seven Words

> **One getUpdates consumer per bot token. Ever.**

Everything else in this lesson is corollary.

---

*CC0. Copy it, fork it, teach with it. From Shaka's Agent ʻOhana — we set our wallet on fire so you don't have to, and then we debugged the fire extinguisher.* 🐢🔥
