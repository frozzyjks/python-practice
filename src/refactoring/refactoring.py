from datetime import date, datetime

from bs4 import BeautifulSoup

# Константы вынесены наверх, их так легко найти и изменить при новых требованиях
_BASE_URL = "https://spimex.com"
_LINK_CLASS = "accordeon-inner__item-title link xls"
_HREF_PREFIX = "/upload/reports/oil_xls/oil_xls_"
_DATE_FORMAT = "%Y%m%d"
_DATE_LENGTH = 8


def parse_page_links(
    html: str,
    start_date: date,
    end_date: date,
) -> list[tuple[str, date]]:
    """Парсит ссылки на xls-бюллетени с одной страницы и фильтрует по диапазону дат."""
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_=_LINK_CLASS)

    for link in links:
        href = link.get("href")
        if not href:
            continue

        href = href.split("?")[0]

        if _HREF_PREFIX not in href or not href.endswith(".xls"):
            continue

        try:
            raw_date = href.split(_HREF_PREFIX)[1][:_DATE_LENGTH]
            date = datetime.strptime(raw_date, _DATE_FORMAT).date()

            if start_date <= date <= end_date:
                url = href if href.startswith("http") else f"{_BASE_URL}{href}"
                results.append((url, date))
            else:
                print(f"Ссылка {href} вне диапазона дат")

        except (IndexError, ValueError) as e:
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")

    return results

    # TODO: рассмотреть возможность возврата датакласса вместо tuple
    #       когда появятся новые поля (например имя файла, размер)
