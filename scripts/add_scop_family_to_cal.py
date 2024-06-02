#!/usr/bin/python3

Doms = set()
DomToFam = {}
for Line in open("../data/scop_lookup.tsv"):
    Fields = Line[:-1].split('\t')
    assert len(Fields) == 2
    Dom = Fields[0]
    Fam = Fields[1]
    Doms.add(Dom)
    DomToFam[Dom] = Fam

f = open("../reseek_db/scop40_family.cal", "w")
notfound = set()
n = 0
for line in open("../reseek_db/scop40.cal"):
    if line.startswith('>'):
        n += 1
        Dom = line[1:-1]
        try:
            Fam = DomToFam[Dom]
        except:
            notfound.add(Dom)
            continue
        f.write(">" + Dom + "/" + Fam + "\n")
    else:
        f.write(line)

print("%d / %d domains not found" % (len(notfound), n))