import datetime
from pathlib import Path
from urllib.parse import urlencode

import scrapy
from rows.utils.date import date_range, today

from .cities import STATE_CODES
from .parser import IbamaPdfExtractor


def define_years(start_year, end_year):
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    if end_date > today():
        end_date = today()
    return start_date, end_date


class AutuacoesSpider(scrapy.Spider):
    name = "autuacoes"
    start_year = 1980
    end_year = datetime.datetime.now().year
    base_url = "https://servicos.ibama.gov.br/ctf/publico/areasembargadas/ConsultaPublicaAreasEmbargadas.php"

    def __init__(self, download_path, start_year=None, end_year=None):
        super().__init__()

        self.download_path = Path(download_path)
        if not self.download_path.exists():
            self.download_path.mkdir(parents=True)
        self.start_date, self.end_date = define_years(
            int(start_year) if start_year else self.start_year,
            int(end_year) if end_year else self.end_year,
        )

    def start_requests(self):
        for date in date_range(
            self.start_date, self.end_date + datetime.timedelta(days=365), "yearly"
        ):
            end_date = datetime.date(date.year, 12, 31)
            for code in STATE_CODES.keys():
                request = self.make_request(code, date, end_date)
                if request is not None:  # if it's cached, it's None
                    yield request

    def make_request(self, state_code, start_date, end_date):
        # Since `start_date` will be always `{some_year}-01-01` and `end_date`
        # will be always `{some_year}-12-31` (same year), then the PDF being
        # downloaded is for the whole year, thus the filename contains only the
        # year (and not the complete start/end dates).
        state = STATE_CODES[state_code]
        filename = self.download_path / f"{state}-{start_date.year}.pdf"
        meta = {"row": {"filename": filename}}

        # If the file was downloaded already, use the downloaded version, but
        # download again and overwrite the file if it's for the current year
        # (could be changed since last download).
        if filename.exists() and start_date.year != today().year:
            url = "file://" + str(filename.absolute())
        else:
            start = start_date.strftime("%d/%m/%Y")
            end = end_date.strftime("%d/%m/%Y")
            query = {
                "modulo": "publico/areasembargadas/ConsultaPublicaAutuacoesAmbientais_pdf.php",
                "$bvars": f",,,{state_code},,{start},{end}",
                "ajax": "1",
                "fpdf": "1",
            }
            url = self.base_url + "?" + urlencode(query)
        return scrapy.Request(url, meta=meta)

    def parse(self, response):
        if b"foi encontrado registros para esse" in response.body:
            return

        filename = response.meta["row"]["filename"]
        with filename.open(mode="wb") as fobj:
            fobj.write(response.body)

        for row in IbamaPdfExtractor(filename, logger=self.logger):
            yield row


if __name__ == "__main__":
    import argparse

    from rows.utils import CsvLazyDictWriter
    from scrapy import signals
    from scrapy.crawler import CrawlerProcess
    from scrapy.signalmanager import dispatcher

    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--start-year", type=int)
    parser.add_argument("--end-year", type=int)
    parser.add_argument("download_path")
    parser.add_argument("output_filename")
    args = parser.parse_args()

    writer = CsvLazyDictWriter(args.output_filename)
    def receive_item(signal, sender, item, response, spider):
        writer.writerow(item)
    dispatcher.connect(receive_item, signal=signals.item_passed)

    process = CrawlerProcess(settings={"LOG_LEVEL": args.log_level})
    process.crawl(
        AutuacoesSpider,
        download_path=args.download_path,
        start_year=args.start_year,
        end_year=args.end_year,
    )
    process.start()
    writer.close()
