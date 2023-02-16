#! /usr/bin/env python3
import base64
import zlib
import schemascii

PORT = 8080
BIND = '192.168.1.158'
SITEURL = f'http://{BIND}:{PORT}'

AUTHOR = 'dragoncoder047'
SITENAME = 'dragoncoder047&rsquo;s blog'
SITESUBTITLE = 'random thoughts about nonrandom things'
SITEURL = 'https://dragoncoder047.github.io/blog'
LOGO = '/images/patrick.svg'
LOGO_AREA_HTML = f'<a href="{SITEURL}"><div class="flex-row"><img src="{LOGO}" width="141" alt="Patrick the purple dragon" height="85" /><div id="sitename-text" class="flex-column"><h1>{SITENAME}</h1><h2>{SITESUBTITLE}</h2></div></div></a>'
ICON = '/images/patrick_head_silhouette.svg'
ICON_MIMETYPE = 'image/svg+xml'
THEME_CSS_FILE = '/static/css/theme.css'
THEME_MAIN_CSS = '/static/css/main.css'
THEME_STATIC_DIR = 'static/'
EXTRA_JS = '/static/misc.js'
USE_FOLDER_AS_CATEGORY = True

PATH = 'aaaa/'
OUTPUT_PATH = './'

GISCUS = {
    'repo': 'dragoncoder047/blog',
    'repo-id': 'R_kgDOHCL60w',
    'category': 'Post Comments',
    'category-id': 'DIC_kwDOHCL6084CRxCW',
    'mapping': 'og:title',
    'lang': 'en',
}

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en_US'

# maybe later...
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

SEO_REPORT = True

DISPLAY_PAGES_ON_MENU = DISPLAY_CATEGORIES_ON_MENU = True

ARTICLE_SAVE_AS = ARTICLE_URL = 'post/{date:%Y-%m-%d}-{slug}.html'
PAGE_URL = PAGE_SAVE_AS = 'page/{slug}.html'
AUTHOR_SAVE_AS = AUTHOR_URL = 'author/{slug}.html'
DRAFT_URL = DRAFT_SAVE_AS = 'draft/{slug}.html'
DRAFT_PAGE_URL = DRAFT_PAGE_SAVE_AS = 'page/draft/{slug}.html'
AUTHORS_SAVE_AS = 'authors.html'
CATEGORY_SAVE_AS = CATEGORY_URL = 'category/{slug}.html'
CATEGORIES_SAVE_AS = 'categories.html'  # cSpell:ignore catg
TAG_SAVE_AS = TAG_URL = ''  # 'tag/{slug}.html'
TAGS_SAVE_AS = ''  # 'tags.html' # I don't use tags
ARCHIVES_SAVE_AS = 'archives.html'

PATH_METADATA = r'(?P<category>.*)/.*'

# Blogroll
LINKS = (
    ('Conwaylife', 'https://www.conwaylife.com/'),
    ('Python', 'https://www.python.org/'),
)

# Social
SOCIAL = (
    (f'{AUTHOR} on GitHub', f'https://github.com/{AUTHOR}'),
)

MENUITEMS = (
    ('Archives', f'{SITEURL}/{ARCHIVES_SAVE_AS}'),
    ('Site root', '/'),
    ('Projects', '#', (
        ('Phoo', f'https://phoo-lang.github.io/'),
        ('Thuepaste', f'https://{AUTHOR}.github.io/thuepaste'),
        ('Armdroid', f'https://{AUTHOR}.github.io/armdroid'),
        ('Langton\'s Ant Music', f'https://{AUTHOR}.github.io/langton-music'),
        ('Schemascii', f'https://github.com/dragoncoder047/schemascii'),
    )),
)

DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = 3
PAGINATION_PATTERNS = (
    (1, '{name}{extension}', '{name}{extension}'),
    (2, '{name}_{number}{extension}', '{name}_{number}{extension}'),
)

THEME = './pelicantheme'

READERS = {'html': None}


def lv_fence(source, language, css_class, options, md, **kwargs):
    return f'<div class="lifeviewer"><textarea>{source.replace("AUTOSTART", "")}\n[[ EXCLUSIVEPLAY ]]</textarea><canvas height="{options.get("height", 400)}" width="{options.get("width", 600)}"></canvas></div>'


def kroki_fence(source, language, css_class, options, md, **kwargs):
    data = base64.urlsafe_b64encode(zlib.compress(
        source.encode('utf-8'), 9)).decode('ascii')
    lang = options.get('type', options.get('name', 'svgbob'))
    attr = ''
    if 'width' in options and 'height' in options:
        attr = f' width="{options["width"]}" height="{options["height"]}"'
    return f'<img src="https://kroki.io/{lang}/svg/{data}"{attr} />'


def named_kroki(name):
    def named_fence(source, language, css_class, options, md, **kwargs):
        return kroki_fence(source, language, css_class, options | {'type': name}, md, **kwargs)
    return {'name': name, 'class': name, 'format': named_fence}


def schemascii_fence(source, language, css_class, options, md, attrs, **kwargs):
    try:
        return schemascii.render("markdown-block", source, **attrs)
    except (schemascii.Error, Exception) as err:
        import traceback
        traceback.print_exception(err)
        return f"<code style=\"color: red\">Schemascii error:\n{err!r}</code>"


MARKDOWN = {
    'extension_configs': {
        'meta': {},
        'pymdownx.extra': {},
        'pymdownx.caret': {},
        'pymdownx.details': {},
        'pymdownx.highlight': {
            'use_pygments': False,  # I use Prism.js
        },
        'pymdownx.inlinehilite': {},
        "pymdownx.superfences": {
            "custom_fences": [
                # covered by kroki, but needed for compatibility with github
                named_kroki('mermaid'),
                named_kroki('svgbob'),
                {
                    'name': 'lifeviewer',
                    'class': 'lifeviewer',
                    'format': lv_fence
                },
                {
                    'name': 'kroki',
                    'class': 'kroki',
                    'format': kroki_fence
                },
                {
                    'name': 'schemascii',
                    'class': 'schemascii',
                    'format': schemascii_fence
                }
            ]
        },
        'pymdownx.saneheaders': {},
        'pymdownx.magiclink': {},
        'pymdownx.smartsymbols': {},
        'smarty': {},
        'pymdownx.tabbed': {},
        'pymdownx.tasklist': {},
        'pymdownx.tilde': {},
        'sane_lists': {},
        'admonition': {},
        'abbr': {},
        'def_list': {},
        'toc': {},
        'footnotes': {},
        'attr_list': {},
        'markdown_figcap': {},
        'python_markdown_comments:CommentsExtension': {},
        'mdx_include': {
            'syntax_left': r'<{2,}\s+i(?:nc(?:lude))',
            'syntax_right': r'>{2,}',
        }
    },
    'output_format': 'html5',
}

PLUGINS = [
    # 'seo',
    'pelican.plugins.share_post',
    # 'sitemap',
    'pelican.plugins.related_posts',
    'minchin.pelican.plugins.nojekyll',
    'pelican.plugins.read_more',
    'jinja2content',
    'series',
    'pelican.plugins.more_categories',
    'pelican.plugins.neighbors'
]

if __name__ == '__main__':
    import os
    os.system(f'pelican {PATH} -o {OUTPUT_PATH} -s {__file__}')
