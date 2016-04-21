import os
import shutil
from PIL import Image
from pelican import signals, contents



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
    img_pth = os.path.join(os.path.dirname(article.source_path), article.settings.get('ARTICLE_PICTURES'))
    images_to_copy = ([(False, os.path.join(img_pth, img),) for img in article.metadata.get('_embedded_images', list())] +
                      [(True, article.header_image_src,)])

    for crop, img_src in images_to_copy:
        article.web_path = os.path.join(os.path.dirname(article.save_as),
                                        article.settings.get('ARTICLE_PICTURES'),
                                        os.path.basename(img_src))
        img_save_as = os.path.join(get_output_path(article), article.web_path)
        if not os.path.exists(img_src):
            raise Exception('File "{0}" does not exists!'.format(img_src))
        if not os.path.exists(img_save_as):
            if not os.path.exists(os.path.dirname(img_save_as)):
                os.makedirs(os.path.dirname(img_save_as))
            shutil.copy(img_src, img_save_as)
            if crop:
                make_header_image(img_save_as)


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
        article.formatted_date = article.date.strftime("%Y.%m.%d")
        article.lead = article.content.split('</p>')[0].replace('<p>', '')
        article.content_no_lead = "</p>".join(article.content.split('</p>')[1:])
        if not getattr(article, "_summary", None):
            article._summary = ""

        if hasattr(article, 'gallery'):
            article.template = 'gallery'
            continue

        if not getattr(article, "noimage", None):  # noimage: True  -- disables the header image completely
            article.header_image_src = get_source_post_image(article)
            save_image(article)


class ArticleContentParser(object):
    def __init__(self, content):
        self.content = content

    def parse(self):
        if not isinstance(self.content, contents.Article):
            return
        self.render_tags()

    def _untag(self, data):
        out = list()
        for elm in data.split(">"):
            elm = elm.split("<")[0]
            if elm:
                out.append(elm)

        return ' '.join(out)

    def _render_youtube_tag(self, tag):
        '''
        Render YouTube tag.

        :param tag:
        :return:
        '''
        template = """<div class="videocontainer">
        <iframe src="//www.youtube.com/embed/{video_id}"
                frameborder="0" class="videoport" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
    </div>"""
        return template.format(video_id=tag.split("{youtube}")[-1])

    def _render_vimeo_tag(self, tag):
        '''
        Render Vimeo tag.

        :param tag:
        :return:
        '''
        template = """<div class="videocontainer">
            <iframe src="//player.vimeo.com/video/{video_id}?portrait=0&color=333"
                    frameborder="0" class="videoport" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
        </div>"""
        return template.format(video_id=tag.split("{vimeo}")[-1])

    def _render_image_tag(self, tag):
        '''
        Render image tag.

        :param tag:
        :return:
        '''
        template = """<div class="article-image-container"><img src="{image_path}" class="article-image"/></div>"""
        image_path = os.path.sep.join([self.content.settings['SITEURL'],
                                      os.path.dirname(self.content.save_as),
                                      tag.split("{image}")[-1]])
        self._push_image(image_path)
        return template.format(image_path=image_path)

    def _push_image(self, path):
        '''
        Register source image for further processing.

        :param path:
        :return:
        '''
        if '_embedded_images' not in self.content.metadata:
            self.content.metadata['_embedded_images'] = list()
        self.content.metadata['_embedded_images'].append(os.path.basename(path))

    def render_tags(self):
        '''
        Render video tags for Vimeo player.
        :return:
        '''
        body = list()
        for line in (self.content._content or '').split(os.linesep):
            if line.find('{vimeo}') > -1:
                line = self._render_vimeo_tag(self._untag(line))
            elif line.find('{youtube}') > -1:
                line = self._render_youtube_tag(self._untag(line))
            elif line.find('{image}') > -1:
                line = self._render_image_tag(self._untag(line))
            body.append(line)
        self.content._content = os.linesep.join(body)


def article_content_parser(content):
    ArticleContentParser(content).parse()


def register():
    '''
    Registration.
    '''
    signals.content_object_init.connect(article_content_parser)
    signals.article_generator_finalized.connect(contentor)
