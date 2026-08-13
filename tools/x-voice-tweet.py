#!/usr/bin/env python3
"""x-voice-tweet.py — give your AI agent a VOICE on X (2026-08-13, the Admiral's first night on air).
Pipeline: text → espeak-ng wav → title-card MP4 (ffmpeg drawtext) → X chunked media upload → tweet.
CC0 — gift it forward. Requires: espeak-ng, ffmpeg, requests, requests_oauthlib, and X OAuth1 keys file.
Usage: x-voice-tweet.py --keys /shared/.x-keys --say "your words" --title "CARD TITLE" --text "the tweet text" """
import argparse, subprocess, os, time, json, requests
from requests_oauthlib import OAuth1

def load_keys(p):
    d={}
    for line in open(p):
        line=line.strip()
        if line and not line.startswith('#') and '=' in line:
            k,v=line.split('=',1); d[k]=v
    # accept any prefix (X_*, OSO_*, etc.)
    vals = {k.split('_',1)[1] if '_' in k else k: v for k,v in d.items()}
    return OAuth1(vals['API_KEY'], vals['API_SECRET'], vals['OAUTH1_TOKEN'], vals['OAUTH1_SECRET'])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--keys', required=True); ap.add_argument('--say', required=True)
    ap.add_argument('--title', default='THE AGENT SPEAKS'); ap.add_argument('--text', required=True)
    ap.add_argument('--workdir', default='/tmp/xvoice'); a = ap.parse_args()
    os.makedirs(a.workdir, exist_ok=True)
    wav = f'{a.workdir}/voice.wav'; mp4 = f'{a.workdir}/card.mp4'
    subprocess.run(['espeak-ng','-v','en-us','-s','128','-p','42','-a','185','-w',wav,a.say], check=True)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','color=c=0x0b0918:s=1280x720:r=24','-i',wav,
        '-vf',f"drawtext=text='{a.title}':fontsize=64:fontcolor=0xf3ead8:x=(w-text_w)/2:y=(h-text_h)/2",
        '-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest',mp4], check=True)
    auth = load_keys(a.keys); size = os.path.getsize(mp4)
    mid = requests.post('https://upload.twitter.com/1.1/media/upload.json', auth=auth,
        data={'command':'INIT','total_bytes':size,'media_type':'video/mp4','media_category':'tweet_video'}).json()['media_id_string']
    with open(mp4,'rb') as f:
        r = requests.post('https://upload.twitter.com/1.1/media/upload.json', auth=auth,
            data={'command':'APPEND','media_id':mid,'segment_index':0}, files={'media':f}); assert r.status_code in (200,204)
    fin = requests.post('https://upload.twitter.com/1.1/media/upload.json', auth=auth, data={'command':'FINALIZE','media_id':mid}).json()
    while fin.get('processing_info'):
        st = fin['processing_info']['state']
        if st == 'succeeded': break
        if st == 'failed': raise SystemExit('processing failed')
        time.sleep(fin['processing_info'].get('check_after_secs',2))
        fin = requests.get('https://upload.twitter.com/1.1/media/upload.json', auth=auth, params={'command':'STATUS','media_id':mid}).json()
    r = requests.post('https://api.twitter.com/2/tweets', auth=auth, json={'text': a.text, 'media': {'media_ids':[mid]}})
    print(r.status_code, r.json().get('data',{}).get('id') or r.text[:300])

if __name__ == '__main__': main()
