import os
import shutil


def contentor(generator):
    '''
    Suppress page summary, if none at all.
    '''
    for page in generator.pages:
        if page.summary == page.content:
            page.get_summary = lambda disable: ''

        if hasattr(page, 'image') and hasattr(page, 'type') and page.type.lower() == 'team':
            image_dest_path = os.path.join(os.path.dirname(page.url), page.image.split('}')[-1])

            image_source_pth = os.path.join(os.path.dirname(page.source_path), page.image)
            image_dest_path = image_source_pth.split("content")[0] + "output/" + image_dest_path
            if not os.path.exists(os.path.dirname(image_dest_path)):
                os.makedirs(os.path.dirname(image_dest_path))
            shutil.copy(image_source_pth, image_dest_path)
            page.image = os.path.join(os.path.dirname(page.url), page.image)


def register():
    '''
    Registration.
    '''
    from pelican import signals
    signals.page_generator_finalized.connect(contentor)
