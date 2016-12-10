# coding: gbk

"""�����л�Ʊ�鿴��

Usage:
    tickets [-dgktz] <from> <to> <date>

Options:
    -h, --help �鿴����
    -d         ����
    -g         ����
    -k         ����
    -t         �ؿ�
    -z         ֱ��

Examples:
    tickets �Ϻ� ���� 2016-10-10
    tickets -dg �ɶ� �Ͼ� 2016-10-10
"""

import requests
from docopt import docopt
from prettytable import PrettyTable
from colorama import init, Fore
from hello import hello


init()

class TrainsCollection:

    header = '���� ��վ ʱ�� ��ʱ һ�� ���� ���� Ӳ�� Ӳ�� ����'.split()

    def __init__(self, available_trains, options):
        """��ѯ���Ļ𳵰�μ���

        :param available_trains: һ���б�, �����ɻ�õĻ𳵰��, ÿ��
                                 �𳵰����һ���ֵ�
        :param options: ��ѯ��ѡ��, �����, ����, etc...
        """
        self.available_trains = available_trains
        self.options = options

    def _get_duration(self, raw_train):
        duration = raw_train.get('lishi').replace(':', 'Сʱ') + '��'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property   #װ����
    def trains(self):
        for raw_train in self.available_trains:
            train_no = raw_train['station_train_code']
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + raw_train['from_station_name'] + Fore.RESET,
                               Fore.RED + raw_train['to_station_name'] + Fore.RESET]),
                    '\n'.join([Fore.GREEN + raw_train['start_time'] + Fore.RESET,
                               Fore.RED + raw_train['arrive_time'] + Fore.RESET]),
                    self._get_duration(raw_train),
                    raw_train['zy_num'],
                    raw_train['ze_num'],
                    raw_train['rw_num'],
                    raw_train['yw_num'],
                    raw_train['yz_num'],
                    raw_train['wz_num'],
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def cli():
    """Command-line interface"""
    arguments = docopt(__doc__)
    from_hello = hello.get(arguments['<from>'])
    to_hello = hello.get(arguments['<to>'])
    date = arguments['<date>']
    url = ('https://kyfw.12306.cn/otn/lcxxcx/query?'
           'purpose_codes=ADULT&queryDate={}&'
           'from_station={}&to_station={}').format(
                date, from_hello, to_hello
           )
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])
    r = requests.get(url, verify=False)
    available_trains = r.json()['data']['datas']
    TrainsCollection(available_trains, options).pretty_print()


if __name__ == '__main__':
    cli()