import os

def get_snippet(article):
    return "Here is an article snippet."

def contentor(generator):
    '''
    Create slugs by file creation
    '''
    for article in generator.articles:
        pass


def register():
    '''
    Registration.
    '''
    from pelican import signals
    signals.article_generator_finalized.connect(contentor)
