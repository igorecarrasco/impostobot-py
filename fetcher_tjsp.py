import mechanize
import json
from collections import namedtuple

Entry = namedtuple('Entry', 'name source position allocation gross_pay net_pay active')

class Fetcher:
    _user_agent = 'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7'
    _url = 'http://www.tjsp.jus.br/RHF/PortalTransparenciaAPI/sema/FolhaPagamentoMagistrado/ListarTodosPorCargoMesAno'
    _max_results = 5000

    def fetch(self, year, month):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', self._user_agent)]
        result = []
        for active in False, True:
            print "Fetching from TJSP (active=%s)" % str(active)
            r = br.open(mechanize.Request(self._url, data=self._post_data(year, month, active)))
            data = json.loads(r.read())
            for e in data['data']:
                result.append(Entry(
                    name=e['nome'],
                    source='TJSP',
                    position=e['folhaMagistradoCargo']['descricao'],
                    allocation=e['lotacao'],
                    gross_pay=float(e['totalCredito']),
                    net_pay=float(e['rendimentoLiquido']),
                    active=int(active)))
        return result

    def _post_data(self, year, month, active):
        return { 'draw': '1',
                 'columns[0][data]': 'nome',
                 'columns[0][name]': '',
                 'columns[0][searchable]': 'true',
                 'columns[0][orderable]': 'false',
                 'columns[0][search][value]': '',
                 'columns[0][search][regex]': 'false',
                 'columns[1][data]': 'lotacao',
                 'columns[1][name]': '',
                 'columns[1][searchable]': 'true',
                 'columns[1][orderable]': 'false',
                 'columns[1][search][value]': '',
                 'columns[1][search][regex]': 'false',
                 'columns[2][data]': 'folhaMagistradoCargo.descricao',
                 'columns[2][name]': '',
                 'columns[2][searchable]': 'true',
                 'columns[2][orderable]': 'false',
                 'columns[2][search][value]': '',
                 'columns[2][search][regex]': 'false',
                 'columns[3][data]': 'totalCredito',
                 'columns[3][name]': '',
                 'columns[3][searchable]': 'true',
                 'columns[3][orderable]': 'false',
                 'columns[3][search][value]': '',
                 'columns[3][search][regex]': 'false',
                 'columns[4][data]': 'totalDebitos',
                 'columns[4][name]': '',
                 'columns[4][searchable]': 'true',
                 'columns[4][orderable]': 'false',
                 'columns[4][search][value]': '',
                 'columns[4][search][regex]': 'false',
                 'columns[5][data]': 'rendimentoLiquido',
                 'columns[5][name]': '',
                 'columns[5][searchable]': 'true',
                 'columns[5][orderable]': 'false',
                 'columns[5][search][value]': '',
                 'columns[5][search][regex]': 'false',
                 'columns[6][data]': 'remuneracaoOrgaoOrigem',
                 'columns[6][name]': '',
                 'columns[6][searchable]': 'true',
                 'columns[6][orderable]': 'false',
                 'columns[6][search][value]': '',
                 'columns[6][search][regex]': 'false',
                 'columns[7][data]': 'diarias',
                 'columns[7][name]': '',
                 'columns[7][searchable]': 'true',
                 'columns[7][orderable]': 'false',
                 'columns[7][search][value]': '',
                 'columns[7][search][regex]': 'false',
                 'columns[8][data]': '',
                 'columns[8][name]': '',
                 'columns[8][searchable]': 'true',
                 'columns[8][orderable]': 'false',
                 'columns[8][search][value]': '',
                 'columns[8][search][regex]': 'false',
                 'start': 0,
                 'length': self._max_results,
                 'search[value]': '',
                 'search[regex]': 'false',
                 'mes': month,
                 'ano': year,
                 'ativo': ['false', 'true'][int(active)],
                 'cargoId': '',
                 'nome': '' }
