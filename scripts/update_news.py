#!/usr/bin/env python3
"""Fetch attributed headlines, not article text. No API key or Wabi dependency."""
import email.utils, hashlib, json, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'news.json'
URL='https://news.google.com/rss/search?q=%22GTA+6%22+OR+%22GTA+VI%22+when:7d&hl=de&gl=DE&ceid=DE:de'
request=urllib.request.Request(URL,headers={'User-Agent':'GTA-VI-News-Fan-Feed/1.0 (+https://github.com/joe-design9/gta-vi-news)'})
with urllib.request.urlopen(request,timeout=45) as response:
    root=ET.fromstring(response.read())
items=root.findall('./channel/item')
if not items:
    raise RuntimeError('RSS returned no items; preserving the previous feed and timestamp.')
data=json.loads(PATH.read_text())
articles=data['articles']
known={a['sourceUrl'] for a in articles}
# Stable publisher+headline key reduces repeat headlines across RSS refreshes.
def key(title,source): return re.sub(r'\W+',' ',title.lower()).strip()+'|'+source.lower()
titles={key(a['title'],a.get('sourceName','')) for a in articles}
added=0
for item in items:
    title=(item.findtext('title') or '').strip()
    source=(item.findtext('source') or '').strip()
    link=(item.findtext('link') or '').strip()
    if not link.startswith('https://') or not re.search(r'\bGTA\s*(?:6|VI)\b|Grand Theft Auto (?:6|VI)',title,re.I): continue
    suffix=' - '+source
    if source and title.endswith(suffix): title=title[:-len(suffix)]
    identity=key(title,source)
    if link in known or identity in titles: continue
    try: published=email.utils.parsedate_to_datetime(item.findtext('pubDate')).astimezone(timezone.utc).isoformat()
    except (TypeError,ValueError): continue
    articles.append({'id':'rss-'+hashlib.sha256(link.encode()).hexdigest()[:20], 'title':title, 'summary':'', 'body':'', 'publishedAt':published, 'sourceName':source or 'Presse via Google News','sourceUrl':link,'category':'feed'})
    titles.add(identity);known.add(link);added+=1
# Preserve manually curated articles and retain at most 150 recent RSS headlines.
curated=[a for a in articles if a.get('category')!='feed']
feed=sorted([a for a in articles if a.get('category')=='feed'],key=lambda a:a.get('publishedAt',''),reverse=True)[:150]
# Curated articles remain the first editorial selections; latest press follows.
data['articles']=sorted(curated,key=lambda a:a.get('publishedAt',''),reverse=True)+feed
data['checkedAt']=datetime.now(timezone.utc).isoformat()
PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'RSS checked: {len(items)} items; {added} added; {len(data["articles"])} retained.')
