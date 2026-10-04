"""Small bottom lyrics and word highlights from the existing frame timing."""

def timestamp(frame, fps):
    # ASS stores centiseconds. Floor so a cue is active on its intended
    # video frame rather than slipping one frame later after rounding up.
    centis = int(frame*100//fps)
    hours, remainder = divmod(centis, 360000)
    minutes, remainder = divmod(remainder, 6000)
    seconds, hundredths = divmod(remainder, 100)
    return f'{hours}:{minutes:02}:{seconds:02}.{hundredths:02}'


def escape(text):
    return text.replace('\\', '＼').replace('{', '［').replace('}', '］').replace('\n', '\\N')


def write_lyrics(data, style, path):
    fps = data['fps']
    header = f'''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyrics,{style['font']},{style['fontSize']},&H00F2F1EB,&H00F2F1EB,&H0017100B,&H8017100B,0,0,0,0,100,100,0.6,0,1,1.5,1,2,90,90,{style['bottomMargin']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    events = []
    for phrase in data['phrases']:
        start, end = phrase['startFrame']-1, phrase['endFrameExclusive']-1
        words = []
        cursor = 0
        for word in phrase['words']:
            offset = phrase['text'].find(word['text'], cursor)
            if offset < 0:
                continue
            cursor = offset+len(word['text'])
            words.append((max(start, word['startFrame']-1), min(end, word['endFrameExclusive']-1), offset, cursor))
        boundaries = sorted({start, end, *(f for a,b,_,_ in words for f in (a,b) if start <= f <= end)})
        for a,b in zip(boundaries, boundaries[1:]):
            if b <= a:
                continue
            active = next((w for w in words if w[0] <= a < w[1]), None)
            text = phrase['text']
            if active:
                _,_,left,right = active
                text = escape(text[:left])+r'{\c&HFFE5A3&}'+escape(text[left:right])+r'{\c&HF2F1EB&}'+escape(text[right:])
            else:
                text = escape(text)
            events.append(f'Dialogue: 0,{timestamp(a,fps)},{timestamp(b,fps)},Lyrics,,0,0,0,,{text}')
    path.write_text(header+'\n'.join(events)+'\n', encoding='utf-8')
