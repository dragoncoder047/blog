#! /usr/bin/env python3
import base64
import zlib
import schemascii
import html.parser
from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor

# PORT = 8080
# BIND = "192.168.1.158"
# SITEURL = f"http://{BIND}:{PORT}"

AUTHOR = "dragoncoder047"
SITENAME = "dragoncoder047&rsquo;s blog"
SITESUBTITLE = "random thoughts about nonrandom things"
SITEURL = "https://dragoncoder047.github.io/blog"
LOGO = "/images/yazani/yazani_1_extracted_bg.png"
LOGO_AREA_HTML = (f'<a href="{SITEURL}" class="flex-row">'
                  '<div class="flex-row">'
                  f'<img src="{LOGO}" style="max-height:10em" '
                  'id="banner-image" />'
                  '<div id="sitename-text">'
                  f'<h1>{SITENAME}</h1><h2>{SITESUBTITLE}</h2>'
                  '</div></div></a>')
ICON = "/images/yazani/yazani_1_extracted_bg_big_eyes_cropped.png"
ICON_MIMETYPE = "image/png"
THEME_CSS_FILE = "/static/css/theme.css"
THEME_MAIN_CSS = "/static/css/main.css"
THEME_STATIC_DIR = "static/"
EXTRA_JS = ("/static/misc.js",)

GOOGLE_TAG = "G-XR0F89CCGK"  # cSpell: ignore ccgk

PATH = "markdown/"
OUTPUT_PATH = "docs/"

GISCUS = {
    "repo": "dragoncoder047/blog",
    "repo-id": "R_kgDOHCL60w",
    "category": "Post Comments",
    "category-id": "DIC_kwDOHCL6084CRxCW",
    "mapping": "og:title",
    "lang": "en",
}

TIMEZONE = "America/New_York"

DEFAULT_LANG = "en_US"

# maybe later...
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

SEO_REPORT = True

DISPLAY_PAGES_ON_MENU = True

ARTICLE_URL = "{date:%Y}/{slug}"
ARTICLE_SAVE_AS = ARTICLE_URL + "/index.html"
PAGE_URL = "page/{slug}"
PAGE_SAVE_AS = PAGE_URL + "/index.html"
AUTHOR_SAVE_AS = AUTHOR_URL = ""  # "author/{slug}.html" # I am the only author
AUTHORS_SAVE_AS = ""  # "authors.html"
DRAFT_URL = "_draft/{slug}"
DRAFT_SAVE_AS = DRAFT_URL + "/index.html"
DRAFT_PAGE_URL = "_draft_page/{slug}"
DRAFT_PAGE_SAVE_AS = DRAFT_PAGE_URL + "/index.html"
TAG_URL = "tag/{slug}"
TAG_SAVE_AS = TAG_URL + "/index.html"
TAGS_URL = "tags"
TAGS_SAVE_AS = "tags/index.html"
ARCHIVES_URL = "archives"
ARCHIVES_SAVE_AS = "archives/index.html"

# I don't use categories
CATEGORY_URL = CATEGORY_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""
DISPLAY_CATEGORIES_ON_MENU = False
USE_CATEGORIES = False

# Blogroll
LINKS = (
    ("Conwaylife.com Forums", "https://www.conwaylife.com/"),
    ("Python", "https://www.python.org/"),
    ("uLisp", "http://www.ulisp.com/"),
)

# Social
SOCIAL = (
    (f"{AUTHOR} on GitHub", f"https://github.com/{AUTHOR}"),
    (f"{AUTHOR} on YouTube", f"https://youtube.com/@{AUTHOR}"),
    (f"{AUTHOR} on Instagram", f"https://instagram.com/{AUTHOR}/"),
)

MENUITEMS = (
    ("Archives", f"{SITEURL}/{ARCHIVES_URL}"),
    ("By tag", f"{SITEURL}/{TAGS_URL}"),
    ("Site root", "/"),
    ("Projects", "#", (
        ("Thuepaste", f"https://{AUTHOR}.github.io/thuepaste"),
        ("Armdroid", f"https://{AUTHOR}.github.io/armdroid"),
        ("Langton's Ant Music", f"https://{AUTHOR}.github.io/langton-music"),
        ("Schemascii", f"https://{AUTHOR}.github.io/schemascii"),
        ("Parasite", f"https://{AUTHOR}.github.io/parasite"),
    )),
)

DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = 3
PAGINATION_PATTERNS = (
    (1, "{url}", "{save_as}"),
    (2, "{base_name}/page{number}", "{base_name}/page{number}/index.html"),
)

THEME = "./pelicantheme"

READERS = {"html": None}


def lv_fence(source, language, css_class, options, md, **kwargs):
    return ('<div class="lifeviewer"><textarea>'
            + f'{source.replace("AUTOSTART", "")}'
            + '\n[[ EXCLUSIVEPLAY ]]</textarea><canvas height="'
            + f'{options.get("height", 400)}"'
            + 'width="{options.get("width", 600)}"></canvas></div>')


def kroki_fence(source, language, css_class, options, md, classes, attrs,
                **kwargs):
    data = base64.urlsafe_b64encode(zlib.compress(
        source.encode("utf-8"), 9)).decode("ascii")
    lang = options.get("type", options.get("name", "svgbob"))
    attr = ""
    if "width" in options and "height" in options:
        attr = f' width="{options["width"]}" height="{options["height"]}"'
    if classes:
        divopen = "<div class=\"" + " ".join(classes) + "\">"
        divclose = "</div>"
    else:
        divopen = divclose = ""
    attr += "".join(f'{k}="{v}"' for k, v in attrs.items())
    return (divopen +
            f'<img src="https://kroki.io/{lang}/svg/{data}"{attr} />' +
            divclose)


def named_kroki(name):
    def named_fence(source, language, css_class, options, md, **kwargs):
        return kroki_fence(source, language, css_class,
                           options | {"type": name}, md, **kwargs)
    return {"name": name, "class": name, "format": named_fence}


def schemascii_fence(source, lang, cls, opts, md, attrs, **kwargs):
    try:
        return schemascii.render("markdown-block", source, **attrs)
    except (schemascii.Error, Exception) as err:
        import traceback
        traceback.print_exception(err)
        return f"<code style=\"color: red\">Schemascii error:\n{err!r}</code>"


class SocialExtension(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(SocialEmbed(md), "social", -1)


class SocialEmbed(Postprocessor):
    def run(self, src: str):
        # cSpell: ignore insta
        if "<youtube" not in src and "<insta" not in src:
            return src
        # Seems like a kludge to not use a Treeprocessor.
        # But I tried, it doesn't work. ¯\_(ツ)_/¯ Weird!
        # And you can't use xml.etree.ElementTree either
        # because it's *cough cough* not valid XML...
        magic = SocialMagic()
        magic.feed(src)
        magic.close()
        return magic.out


class SocialMagic(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]):
        func = getattr(self, "handle_" + tag, None)
        if not callable(func):
            self.out += self.get_starttag_text()
        else:
            self.out += func(dict(attrs))
    handle_startendtag = handle_starttag

    def handle_youtube(self, attrs: dict[str, str]) -> str:
        if "short" in attrs:
            url = "https://youtube.com/embed/" + attrs["short"]
            ratio = "9/16"
            width = "40%"
        elif "id" in attrs:
            url = "https://youtube.com/embed/" + attrs["id"]
            ratio = "16/9"
            width = "60%"
        elif "list" in attrs:
            url = ("https://youtube.com/embed?listType=playlist&list="
                   + attrs["list"])
            ratio = "16/9"
            width = "60%"
        else:
            raise ValueError(
                "must have one of 'short', 'id', 'list' attribute")
        # add global attributes
        # cSpell: ignore enablejsapi
        if "?" in url:
            url += "&"
        else:
            url += "?"
        url += "cc_load_policy=1&cc_lang_pref=en&rel=0&enablejsapi=1"
        attrs = {
            "style": ("display:block;margin-left:auto;margin-right:auto;"
                      f"aspect-ratio:{ratio};width:{width};"
                      "max-width:90vw"),
            "src": url,
            "allow": ("accelerometer;autoplay;"
                      "clipboard-write;encrypted-media;"
                      "gyroscope;picture-in-picture;"
                      "web-share"),
            "allowfullscreen": True}

        return f"<iframe{"".join(f" {k}=\"{v}\"" for k,
                                 v in attrs.items())}></iframe>"

    def handle_instagram(self, attrs: dict[str, str]) -> str:
        permalink = html.escape(f"https://www.instagram.com/p/{
            attrs["post"]}/?utm_source=ig_embed")
        # cSpell: ignore instgrm
        return f"""<blockquote class="instagram-media"{
            "" if not bool(attrs.get("caption", True))
            else " data-instgrm-captioned"}
    data-instgrm-permalink="{permalink}"
    data-instgrm-version="14">
    <a href="{permalink}">View this post on Instagram</a>
    </blockquote>""".replace("\n", "")
    handle_insta = handle_instagram

    def handle_endtag(self, tag: str):
        func = getattr(self, "handle_" + tag, None)
        if not callable(func):
            self.out += f"</{tag}>"

    def handle_data(self, data):
        self.out += data

    def handle_comment(self, comment):
        self.out += f"<!--{comment}-->"

    def handle_decl(self, decl):
        self.out += f"<!{decl}>"

    def unknown_decl(self, decl):
        self.out += f"<!{decl}>"

    def handle_pi(self, foo):
        self.out += f"<?{foo}>"

    def handle_entityref(self, ref):
        self.out += f"&{ref};"

    def handle_charref(self, ref):
        self.out += f"&#{ref};"


MARKDOWN = {
    "extension_configs": {
        "meta": {},
        "pymdownx.extra": {},
        "pymdownx.caret": {},
        "pymdownx.details": {},
        "pymdownx.highlight": {
            "use_pygments": False,  # I use Prism.js
        },
        "pymdownx.inlinehilite": {},
        "pymdownx.superfences": {
            "custom_fences": [
                # covered by kroki, but needed for compatibility with github
                named_kroki("mermaid"),
                named_kroki("svgbob"),
                {
                    "name": "lifeviewer",
                    "class": "lifeviewer",
                    "format": lv_fence
                },
                {
                    "name": "kroki",
                    "class": "kroki",
                    "format": kroki_fence
                },
                {
                    "name": "schemascii",
                    "class": "schemascii",
                    "format": schemascii_fence
                }
            ]
        },
        "pymdownx.saneheaders": {},
        "pymdownx.magiclink": {},
        "pymdownx.smartsymbols": {},
        "smarty": {},
        "pymdownx.tabbed": {},
        "pymdownx.tasklist": {},
        "pymdownx.tilde": {},
        "sane_lists": {},
        "admonition": {},
        "abbr": {},
        "def_list": {},
        "toc": {},
        "footnotes": {},
        "attr_list": {},
        "markdown_figcap": {},
        "python_markdown_comments:CommentsExtension": {},
        "mdx_include": {
            "syntax_left": r"<{2,}\s+i(?:nc(?:lude))",
            "syntax_right": r">{2,}",
        },
        "build:SocialExtension": {},
    },
    "output_format": "html5",
}

PLUGINS = [
    # "seo",
    "pelican.plugins.share_post",
    # "sitemap",
    "pelican.plugins.related_posts",
    "minchin.pelican.plugins.nojekyll",
    "pelican.plugins.read_more",
    "jinja2content",
    "series",
    "pelican.plugins.neighbors"
]

# oops!!!
READ_MORE_LINK_FORMAT = '<a href="/blog/{url}">{text}</a>'


if __name__ == "__main__":
    import os
    import shlex
    os.system(f"""pelican {
        shlex.quote(PATH)
    } -o {
        shlex.quote(OUTPUT_PATH)
    } -s {
        shlex.quote(__file__)}""")
