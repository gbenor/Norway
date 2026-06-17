from pathlib import Path
import re, html
root=Path('/workspace/Norway')
md=(root/'lital_gilad_norway_trip_manuscript_v2.md').read_text()
parts=re.split(r'(?m)^# ', md)
intro=parts[0].strip()
chapters=[]
for p in parts[1:]:
    title=p.splitlines()[0].strip(); body='\n'.join(p.splitlines()[1:]).strip(); chapters.append((title,body))
# save content
content=root/'content'; content.mkdir(exist_ok=True)
slugs=['home','oslo','holmenkollen','hemsedal','fjord-country','flam','hardanger','trolltunga','rosendal','bergen','epilogue']
# combine chapter 8+9 for Rosendal
mapping={
'oslo':[1],'holmenkollen':[2],'hemsedal':[3],'fjord-country':[4],'flam':[5],'hardanger':[6],'trolltunga':[7],'rosendal':[8,9],'bergen':[10],'epilogue':[11]}
(content/'home.md').write_text(md.split('# Chapter 1')[0].strip()+"\n")
for slug,idxs in mapping.items():
    text='\n\n'.join('# '+chapters[i][0]+'\n\n'+chapters[i][1] for i in idxs)
    (content/f'{slug}.md').write_text(text+'\n')
route=['Oslo','Holmenkollen','Hemsedal','Borgund','Snow Road','Flåm','Nærøyfjord','Hardangervidda','Trolltunga','Rosendal','Bergen']
nav_pages=[('index.html','Home','home'),('oslo.html','Oslo','oslo'),('holmenkollen.html','Holmenkollen','holmenkollen'),('hemsedal.html','Hemsedal','hemsedal'),('fjord-country.html','Fjord Country','fjord-country'),('flam.html','Flåm','flam'),('hardanger.html','Hardanger','hardanger'),('trolltunga.html','Trolltunga','trolltunga'),('rosendal.html','Rosendal','rosendal'),('bergen.html','Bergen','bergen'),('epilogue.html','Epilogue','epilogue')]
subtitles={'oslo':'First impressions of a capital shaped by water, design and public life.','holmenkollen':'Nordmarka, skiing culture and Oslo from above.','hemsedal':'Entering mountain Norway through valleys, lakes and long June daylight.','fjord-country':'Borgund, Vindhellavegen, the Lærdal Tunnel, Aurlandsfjellet and Undredal.','flam':'The Flåm Railway, Nærøyfjord, Gudvangen and Voss.','hardanger':'Waterfalls, plateaus, Hardangerfjord and Norway’s hydroelectric imagination.','trolltunga':'The defining hike: effort, weather, questions and the tongue of rock.','rosendal':'Odda, ferry roads, Rosendal, Baroniet and the softer side of fjord country.','bergen':'The city between mountains and sea, and the finale of the journey.','epilogue':'Why this trip stayed with us.'}
photos={'oslo':['photos/day01/opera-house','photos/day01/vigeland','photos/day01/fram-museum','photos/day01/akershus'], 'holmenkollen':['photos/day02/holmenkollen','photos/day02/nordmarka'], 'hemsedal':['photos/day03/valdres','photos/day03/hemsedal'], 'fjord-country':['photos/day04/borgund','photos/day04/snow-road','photos/day04/undredal'], 'flam':['photos/day05/flam-railway','photos/day05/naeroyfjord','photos/day05/voss'], 'hardanger':['photos/day06/hardanger','photos/day06/voringsfossen','photos/day06/kinsarvik'], 'trolltunga':['photos/day07/trolltunga'], 'rosendal':['photos/day08/odda','photos/day08/rosendal','photos/day08/ferry'], 'bergen':['photos/day10/bryggen','photos/day10/fish-market','photos/day10/floyen','photos/day10/ulriken','photos/day10/lovstakken'], 'epilogue':['photos/epilogue']}

def md_to_html(text,slug):
    out=[]; paras=[]; gal_i=0
    def flush():
        nonlocal paras, gal_i
        if paras:
            p=' '.join(paras).strip(); paras=[]
            if p.startswith('[PHOTO PLACEHOLDER:'):
                folder=(photos.get(slug) or [f'photos/{slug}'])[min(gal_i,len(photos.get(slug,[0]))-1)] if photos.get(slug) else f'photos/{slug}'
                out.append(f'<section class="photo-block"><p class="placeholder-note">{html.escape(p[1:-1])}</p><div class="gallery" data-gallery-folder="{folder}"></div></section>')
                gal_i += 1
            elif '?' in p and (p.lower().startswith(('why','how','what','can','are','is','who')) or p.endswith('?')):
                out.append(f'<aside class="question-card"><span>Question we asked</span><p>{html.escape(p)}</p></aside>')
            else: out.append(f'<p>{html.escape(p)}</p>')
    for line in text.splitlines():
        line=line.rstrip()
        if not line: flush(); continue
        if line.startswith('# '): flush(); out.append(f'<h1>{html.escape(line[2:].strip())}</h1>')
        elif line.startswith('## '):
            flush(); h=line[3:].strip(); cls=' class="reflection-heading"' if any(w in h.lower() for w in ['reflection','thought','taught']) else ''
            out.append(f'<h2{cls}>{html.escape(h)}</h2>')
        else: paras.append(line)
    flush(); return '\n'.join(out)

def shell(title,body,slug,prev=None,next=None):
    links=''.join(f'<a href="{f}">{n}</a>' for f,n,s in nav_pages)
    route_html=''.join(f'<span class="{"current" if ((slug=="fjord-country" and r in ["Borgund","Snow Road"]) or (slug=="flam" and r in ["Flåm","Nærøyfjord"]) or (slug=="hardanger" and r=="Hardangervidda") or r.lower()==slug) else ""}">{r}</span>' for r in route)
    nav=''
    if slug!='home': nav=f'<nav class="chapter-nav"><a href="{prev or "index.html"}">← Previous chapter</a><a href="index.html">Back to home</a><a href="{next or "index.html"}">Next chapter →</a></nav>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | Lital & Gilad Explore Norway</title><meta name="description" content="{html.escape(subtitles.get(slug,'A personal Norway road trip journal and travel guide.'))}"><link rel="stylesheet" href="assets/css/styles.css"></head><body><div class="progress"></div><a class="skip" href="#main">Skip to content</a><header class="topbar"><nav class="nav"><a class="brand" href="index.html">Lital & Gilad</a><div class="links">{links}</div></nav></header>{body}<button class="top" aria-label="Back to top">↑</button><div class="lightbox" role="dialog" aria-modal="true"><button class="close">Close</button><img alt=""></div><footer class="footer"><div><strong>Lital & Gilad Explore Norway</strong><p>Personal travel journal and Norway road trip guide.</p></div></footer><script src="data/photo-manifest.js"></script><script src="assets/js/main.js"></script></body></html>'''
# home
home_body=f'''<section class="hero home-hero" style="--hero:url(photos/hero-norway.jpg)"><div><p class="eyebrow">Norway road trip journal · June 2026</p><h1>Lital & Gilad Explore Norway</h1><p>A Journey Through Fjords, Mountains and Norwegian Culture</p><div class="btns"><a class="btn" href="#origin">Begin the story</a><a class="btn ghost" href="#timeline">Explore the route</a></div></div></section><main id="main"><section class="wrap grid" id="origin"><div class="intro"><h2>Origin Story</h2><p>The idea for this trip did not begin as a classic holiday plan. It started because Lital had an EMDR conference in Oslo. Instead of treating the journey as a short professional trip, we decided to take advantage of being in Norway and continue into a full road trip across the country.</p><p>At first, the plan sounded simple: arrive in Oslo, see the famous fjords, experience something close to the classic “Norway in a Nutshell” route, and finish in Bergen. But very quickly the trip became much more than a list of attractions.</p></div><aside class="postcard-quote">“It often felt as though we were living inside a postcard.”</aside></section><section class="wrap" id="timeline"><h2>Route Overview</h2><div class="route-timeline">{''.join(f'<div>{r}</div>' for r in route)}</div></section><section class="wrap"><h2>Trip Highlights</h2><div class="highlights">{''.join(f'<a class="feature" href="{href}"><h3>{name}</h3><p>{desc}</p></a>' for name,href,desc in [('Trolltunga','trolltunga.html','The defining hike above Ringedalsvatnet.'),('Flåm Railway','flam.html','A mountain railway that makes engineering feel cinematic.'),('Snow Road','fjord-country.html','Aurlandsfjellet, snow walls and the descent toward the fjords.'),('Nærøyfjord','flam.html','A narrow fjord cruise through cliffs and waterfalls.'),('Bergen','bergen.html','The rain-bright finale between mountains and sea.'),('Steinsdalsfossen','rosendal.html','A waterfall you can walk behind on the road to Bergen.')])}</div></section><section class="wrap card"><h2>Photo naming rules</h2><p>Add <code>photo01.jpg</code>, <code>photo02.jpg</code>, <code>photo03.jpg</code> and onward into each gallery folder. The website tries those names automatically and shows “Photos coming soon.” when a folder is empty. No HTML edits are required.</p></section></main>'''
(root/'index.html').write_text(shell('Home',home_body,'home'))
# chapter pages
page_list=[p for p in nav_pages if p[2] != 'home']
for i,(file,label,slug) in enumerate(page_list):
    text=(content/f'{slug}.md').read_text(); title=re.search(r'^# (.+)',text,re.M).group(1)
    words=len(re.findall(r'\w+',text)); mins=max(1,round(words/220))
    extra=''
    if slug=='trolltunga': extra='<section class="wrap stats"><div><strong>Distance</strong><span>Long full-day hike</span></div><div><strong>Elevation gain</strong><span>Serious mountain climb</span></div><div><strong>Duration</strong><span>Most of the day</span></div><div><strong>Difficulty</strong><span>Demanding</span></div></section><section class="wrap"><h2>What We Wondered At Trolltunga</h2><details><summary>How was the trail built?</summary><p>Who Built the Trail? is answered in the story below.</p></details><details><summary>How did they move equipment?</summary><p>How Did They Bring Equipment? is answered in the story below.</p></details><details><summary>Why are there power lines?</summary><p>Why Are There Power Lines in Remote Places? is answered in the story below.</p></details></section>'
    if slug=='bergen': extra='<section class="wrap bergen-finale"><h2>Bergen Finale</h2><div class="cards"><div>Bryggen</div><div>Fish Market</div><div>Fløyen</div><div>Ulriken</div><div>Løvstakken</div></div></section>'
    prev='index.html' if i==0 else page_list[i-1][0]; nxt='index.html' if i==len(page_list)-1 else page_list[i+1][0]
    route_ctx=f'<div class="route-context">{route_html if False else ""}</div>'
    chapter_nav=f'<nav class="chapter-nav"><a href="{prev}">← Previous chapter</a><a href="index.html">Back to home</a><a href="{nxt}">Next chapter →</a></nav>'
    body=f'<section class="hero small {"troll-hero" if slug=="trolltunga" else ""}" style="--hero:url(photos/{slug}/cover.jpg)"><div><p class="eyebrow">{mins} minute read</p><h1>{html.escape(label)}</h1><p>{html.escape(subtitles.get(slug,""))}</p></div></section><main id="main"><div class="route-context">'+''.join(f'<span class="{"current" if label.split()[0] in r or (slug=="fjord-country" and r in ["Borgund","Snow Road"]) else ""}">{r}</span>' for r in route)+'</div>'+extra+f'<article class="wrap story">{md_to_html(text,slug)}{chapter_nav}</article></main>'
    (root/file).write_text(shell(label,body,slug,prev,nxt))
