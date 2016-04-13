import random

ipsum = """
Lorem ipsum dolor sit amet, et mel aliquid philosophia contentiones. Nec ea liber necessitatibus. Vel ei ubique ignota sanctus, ne scripta quaerendum definitiones vim, nihil persecuti posidonium mel in. Ad vix discere appellantur. Ei etiam noster nostro vel.

Vix viderer detraxit ne. Ei vix porro disputationi signiferumque, possim tibique scaevola vim at. Alienum definiebas et mei, veri dicat altera has an, his vide epicurei dissentiunt ex. Tacimates similique in his. Cu vim platonem definiebas intellegam, sed stet brute debet ea.

Legimus periculis hendrerit an eos, nostrud facilis mei ei. Fabulas debitis adolescens sea ad. Nam admodum principes et, an alia appareat ponderum eos. Quem assentior quaerendum ad ius, est ea purto docendi. Qui congue semper eruditi cu.

Eius corpora evertitur et his, aliquid minimum disputationi nec eu. Vivendo explicari in his, te duo sanctus molestiae. Everti vocibus habemus sit ne, ea vim habeo inermis, mea ad novum partiendo deseruisse. Nec purto aliquip at, enim zril scaevola has eu. Platonem signiferumque ad vis, ius eu recteque sadipscing.

Facer dolore detracto duo et. Affert laudem primis no vel, graeco admodum percipit vel ut. Id munere alienum molestiae usu, ut pri dico impetus neglegentur, at cum accumsan reformidans. Augue platonem consectetuer ius id. Ut audiam utroque eum. Ex est soleat feugiat.

Id vis eros probatus necessitatibus, at stet natum nostro quo. Ancillae detracto salutatus quo at, ius tota nostrum praesent te. Eam suscipit reformidans ad, ea has nulla putant. Te putent adolescens conclusionemque est, quo idque animal cotidieque id, ad prompta bonorum dissentias vim. In vix sint inermis iudicabit, scripta conceptam efficiendi ei his, fabulas accommodare consectetuer te mel.

Diam ignota ex vis, ex tation audiam cotidieque mei. Suas paulo tritani in est. Erant quaeque maiestatis ei mei, mei quem philosophia ne, vel quas tation mentitum cu. Commune electram ad nam, eu mea intellegam mediocritatem, usu movet insolens oportere an.

His in duis possim, movet dolorum ei pro. Purto omnesque appellantur ut vis. Adhuc reprehendunt an his. Qui ad minim molestiae, ex eos agam augue.

Mel ut integre elaboraret, agam cotidieque est et. Ut nullam inimicus reprimique usu, mea impedit menandri cu. Sumo nibh voluptatibus ut cum, te usu diceret antiopam dignissim. Ea vis minim noluisse.

Cu porro harum civibus eos, suas postulant nam ea. Prima invidunt mei in, iusto fuisset consectetuer sed ex, ex solum fierent mea. Ea nostro appellantur est. Eos mazim aliquando id, ad solum nonumy invenire pri, vel ex posse pertinax.
"""

ipsum_text = ipsum.split("\n\n")
ipsum_titles = [t.split(",")[0].strip() for t in ipsum.replace("\n", " ").split(".")]
taken_titles = dict()
taken_dates = dict()

def gen_title():
    while True:
        title = random.choice(ipsum_titles)
        if title not in taken_titles:
            taken_titles[title] = None
            return title

def gen_date():
    while True:
        year = random.randint(2000, 2016)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 24)
        mm = random.randint(0, 60)
        ret = (year, month, day, hour, mm)
        if ret not in taken_dates:
            taken_dates[ret] = None
            return ret

def generate():
    year, month, day, hour, mm = gen_date()
    name = '{y}-{m}-{d}-{h}-{mm}'.format(y=year, m=month, d=day, h=hour, mm=mm)
    text = '\n\n'.join(ipsum_text[:random.randint(1, len(ipsum_text))])

    f = open('{0}.md'.format(name), 'w')
    f.write('Title: {0}\n'.format(gen_title()))
    f.write('Date: {y}-{m}-{d} {h}:{mm}\n'.format(y=year, m=month, d=day, h=hour, mm=mm))
    f.write('{0}\n'.format(text))
    f.close()
 

if __name__ == '__main__':
    random.seed()
    for x in range(50):
        generate()
