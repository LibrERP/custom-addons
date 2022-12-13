{
    'name': 'Fattturazione da DDT: controlli avanzati',
    'version': '12.0.3.1.2',
    'category': 'Localization/Italy',
    'summary': (
        'Al momento della fatturazione da DDT è possibile scegliere se'
        ' usare lo sconto memorizzato nella riga del DDT o quello della '
        'riga dell\'ordine di vendita (sale.order)'
    ),
    'author': 'Didotech srl',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'l10n_it_ddt',
    ],
    'data': [
        'data/res_config_settings.xml',
        'views/res_config_settings.xml',
    ],
    'installable': True
}
