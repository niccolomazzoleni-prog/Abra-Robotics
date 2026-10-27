import sys
rows=[
"................",
"................",
".......#.#......",
".......#.#......",
".......###......",
".......###......",
"..########.###..",
".##....###...##.",
".......###...##.",
"..#######....##.",
".##...###....##.",
".##...###....##.",
".##...###....##.",
"..#######.####..",
"................",
"................",
]
def svg(rows,bg,fg,title):
    rects=''.join(f'<rect x="{x}" y="{y}" width="1" height="1"/>' for y,r in enumerate(rows) for x,c in enumerate(r) if c=='#')
    # merge runs horizontally
    out=[]
    for y,r in enumerate(rows):
        x=0
        while x<16:
            if r[x]=='#':
                s=x
                while x<16 and r[x]=='#': x+=1
                out.append(f'M{s} {y}h{x-s}v1h-{x-s}z')
            else: x+=1
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" role="img" aria-labelledby="t"><title id="t">{title}</title><rect width="16" height="16" rx="2" fill="{bg}"/><path fill="{fg}" d="{"".join(out)}"/></svg>\n'
open(sys.argv[1],'w').write(svg(rows,'#2F3337','#F7F6F2','Abra, favicon 16 px'))
open(sys.argv[2],'w').write(svg(rows,'#000000','#FFFFFF','Abra, favicon 16 px monocromo'))
