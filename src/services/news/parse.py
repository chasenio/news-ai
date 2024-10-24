import typing as t
import pytz

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from utils.time import datetime_utc

from models.news import SourceType

from .data import New


def parse_news(html: str, source_type: SourceType) -> t.Iterator[New]:
    """
    解析新闻网页, 返回新闻可迭代对象
    """
    soup = BeautifulSoup(html, 'html.parser')
    news_parser = get_parser(source_type)
    for article in news_parser(soup):
        yield article

def get_parser(source_type: SourceType) -> t.Callable[[BeautifulSoup], t.Iterator[New]]:
    if source_type == SourceType.BLOOMBERG:
        return parse_bloomberg
    if source_type == SourceType.BARRONS:
        return parse_barrons
    else:
        raise ValueError(f"Unknown source type: {source_type}")

def make_time(time_str: str) -> datetime:
    """
    将类似 "1 hr ago" 的时间字符串转换为 datetime 对象
    """
    now = datetime_utc()
    dur, unit, _ = time_str.split(' ')
    if unit.lower() == "min":
        factor = timedelta(minutes=int(dur))
    elif unit.lower() in ("hr", "hours"):
        factor = timedelta(hours=int(dur))
    elif unit.lower() in ("day", "days"):
        factor = timedelta(days=int(dur))
    else:
        raise ValueError(f"Unknown time unit: {unit}")

    return now - factor

# 解析 barrons latest news
def parse_barrons(soup: BeautifulSoup) -> t.Iterator[New]:
    prefix = "https://www.barrons.com"
    # 找到所有 article 标签
    articles = soup.find_all('article')
    for article in articles:

        # 在子标签中找到时间 p 标签
        p = article.find("p")
        if p:
            time_str = article.find('p').text
            published_at = make_time(time_str)
        else:
            published_at = datetime_utc()
        # 找到标题标签
        title_tag_a = article.find('a')
        title = title_tag_a.text
        url = title_tag_a['href']

        yield New(title=title, source_type=SourceType.BARRONS,
                  published_at=published_at, article_url=url)



# 解析 bloomberg latest news
def parse_bloomberg(soup: BeautifulSoup) -> t.Iterator[New]:
    prefix = "https://www.bloomberg.com"
    # 找到 class 是 LineupContentArchive_itemContainer__jXMs_ LineupContentArchive_fullWidthItemContainer__Har_N 的 div
    article_class = 'LineupContentArchive_itemContainer__jXMs_ LineupContentArchive_fullWidthItemContainer__Har_N'
    articles = soup.find_all('div', class_=article_class)

    for article in articles:
        # 找到 time 标签
        time_str = article.find('time').text

        # 找到 title 标签
        title_tag_a = article.find('a')
        title = title_tag_a.text
        url = title_tag_a['href']

        # 找到文章 image url
        image_url = article.find('img')['src']
        yield New(title=title, source_type=SourceType.BLOOMBERG,
                  published_at=make_time(time_str), article_url="".join([prefix, url]),
                  image_url=image_url)
