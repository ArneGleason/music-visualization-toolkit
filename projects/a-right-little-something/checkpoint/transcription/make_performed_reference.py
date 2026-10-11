import json, pathlib, re
b=pathlib.Path('projects/a-right-little-something')
lines=(b/'lyrics/arranged.txt').read_text(encoding='utf-8').splitlines()
out=['Lyrics as performed','',
     'Reference for the current master (2026-10-03 2137). Arranged spelling and typos are retained. The two extra chorus repeats are included.','']
n=0
for line in lines:
    if line.startswith('['):
        out.append('['+re.split(r'\s+-\s*\d',line[1:-1],maxsplit=1)[0]+']')
    elif line.strip():
        n+=1
        if n==24:
            continue
        out.append(line)
        if n in (20,54):
            out.append('Out here in orbit.')
    elif out[-1]!='':
        out.append('')
out.extend(['Review notes: The rapid “in” sequence currently follows the arranged wording; its repetition count and interpolated timing still need listening review. The separate sheet line “Loose it.” has not been independently identified in the recording and is omitted here pending review.',''])
text='\n'.join(out)
(b/'lyrics/performed.txt').write_text(text,encoding='utf-8')
print(text)
