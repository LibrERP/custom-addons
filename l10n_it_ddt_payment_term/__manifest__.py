{
    'name': 'Termini di pagamento in DDT',
    'version': '12.0.1.0.1',
    'category': 'Localization/Italy',
    'summary': (
        'Il modulo aggiunge nei DDT i Termini di Pagamento'
    ),
    'author': 'Didotech srl',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'l10n_it_ddt',
    ],
    'data': [
        'views/stock.xml',
    ],
    'installable': True
}
