import os

def get_snippet(article):
    return "Here is an article snippet."

def contentor(generator):
    '''
    Create slugs by file creation
    '''
    for article in generator.articles:
        if not getattr(article, "_summary", None):
            article._summary = ""
        article.formatted_date = article.date.strftime("%Y.%m.%d")
        article.lead = article.content.split('</p>')[0].replace('<p>', '')
        article.content_no_lead = "</p>".join(article.content.split('</p>')[1:])


def register():
    '''
    Registration.
    '''
    from pelican import signals
    signals.article_generator_finalized.connect(contentor)
