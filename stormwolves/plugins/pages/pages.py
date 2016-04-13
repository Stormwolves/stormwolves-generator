def contentor(generator):
    '''
    Suppress page summary, if none at all.
    '''
    for page in generator.pages:
        if page.summary == page.content:
            page.get_summary = lambda disable: ''


def register():
    '''
    Registration.
    '''
    from pelican import signals
    signals.page_generator_finalized.connect(contentor)
