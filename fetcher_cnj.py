"""
Fetches salaries of judges & justices from the CNJ site
i.e. http://www.cnj.jus.br/transparencia/remuneracao-dos-magistrados/remuneracao-junho-2018
"""
from bs4 import BeautifulSoup
from collections import namedtuple


class Fetcher:
    """
    Pulls and parses salary data from the CNJ website.
    """
    def __init__(self):
        self.entry = namedtuple('Entry', 'name position allocation gross_pay net_pay active')
        self.url = 'http://www.cnj.jus.br/transparencia/remuneracao-dos-magistrados/remuneracao-'
        self.months = set([
            'janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho',
            'agosto', 'setembro', 'outubro', 'novembro', 'dezembro' 
        ])
        
    def _get_file_urls(self, links):
        """
        Grabs all URLs of files in a given page that end with .xls or .xlsx
        """
        urls = []
        for link in links:
            #  Checks for the right .xls/.xlsx link format 
            if any(
                [link.endswith('.xls'), link.endswith('.xlsx')]
            ) and len(link.split('/')) == 9:
                urls.append(link)

        return urls

    def fetcher(self, month, year):
        """
        Runs the whole show.
        """
        if month not in self.months:
            raise ValueError('Not a month!')
        
        if len(year) == 4:
            #  if this doesn't work, a ValueError will be raised, which is what we want
            int(year)
        else:
            raise ValueError('Wrong year format. Use 4 digit year')
            

        soup = BeautifulSoup(
            self.url + '{}-{}'.format(month, year), 'html.parser')

        links = soup.find_all('a')

        csvs = self._get_file_urls(links)
