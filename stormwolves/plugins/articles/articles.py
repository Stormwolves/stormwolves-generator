import os
import shutil
from PIL import Image

# TODO: All this stuff needs to be refactored as a class and have a better speed handling

def get_output_path(article):
    '''
    Return an output path

    :param article:
    :return:
    '''
    # TODO: DONT!
    return os.path.join(os.path.abspath("."), "output")


def make_header_image(path):
    '''
    Resize image to the restrictions.

    :param path:
    :return:
    '''
    size = 730, 730
    if os.path.exists(path):
        im = Image.open(path)
        im.thumbnail(size, Image.ANTIALIAS)
        w, h = im.size
        if h > 292:
            cut_h = (h - 292) / 2
            im.crop((0, cut_h, w, h - cut_h)).save(path, "JPEG")
        else:
            im.save(path, "JPEG")


def save_image(article):
    '''
    Save image to the article path.

    :param path:
    :return:
    '''
    article.web_path = os.path.join(os.path.dirname(article.save_as),
                                    article.settings.get('ARTICLE_PICTURES'),
                                    os.path.basename(article.header_image_src))
    header_image_save_as = os.path.join(get_output_path(article), article.web_path)
    if not os.path.exists(article.header_image_src):
        raise Exception('File "{0}" does not exists!'.format(article.header_image_src))
    if not os.path.exists(header_image_save_as):
        if not os.path.exists(os.path.dirname(header_image_save_as)):
            os.makedirs(os.path.dirname(header_image_save_as))
        shutil.copy(article.header_image_src, header_image_save_as)
        make_header_image(header_image_save_as)


def get_source_post_image(article):
    '''
    Get a source image for the post

    :param article:
    :return:
    '''
    all_images = article.settings.get('ARTICLE_PICTURES')
    default_image = article.settings.get('ARTICLE_DEFAULT_PICTURE')
    if not all_images or not default_image:
        raise Exception('This plugin requires that ARTICLE_PICTURES and ARTICLE_DEFAULT_PICTURE should be defined!')
    a_img_path = os.path.join(os.path.dirname(article.source_path), all_images)

    # First see if there is an explicit image filename in the article metadata
    article_image = None
    article_default_image_no_ext = ".".join(os.path.basename(article.source_path).split(".")[:-1])
    if hasattr(article, 'image'):
        article_image = os.path.join(a_img_path, os.path.sep.join(
            [pth for pth in article.image.split(os.path.sep) if pth]))

    # See if there is an image, named after article filename with the jpeg/jpg/png extensions
    if not article_image:
        for f_ext in ['jpeg', 'jpg', 'png']:
            article_image = os.path.join(a_img_path, '{0}.{1}'.format(article_default_image_no_ext, f_ext))
            if not os.path.exists(article_image):
                article_image = None
            else:
                break

    # Set just a default image
    if not article_image:
        article_image = os.path.join(a_img_path, default_image)
        article.default_image = True
    else:
        article.default_image = False

    return article_image


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

        if not getattr(article, "noimage", None):  # noimage: True  -- disables the header image completely
            article.header_image_src = get_source_post_image(article)
            save_image(article)


def register():
    '''
    Registration.
    '''
    from pelican import signals
    signals.article_generator_finalized.connect(contentor)
