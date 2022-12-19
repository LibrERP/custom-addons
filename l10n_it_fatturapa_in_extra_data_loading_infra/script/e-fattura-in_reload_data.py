import argparse
import datetime
import odoolib
import math

# # # #
# Constants
# # # #

# Number of records to be processed per chunk
CHUNK_SIZE = 25

# # # #
# Read command line arguments
# # # #

# Define the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', required=True)
parser.add_argument('-p', '--port', type=int, default=8069)
parser.add_argument(
    '-P', '--protocol',
    choices=['json', 'xml'],
    default='json',
    help='RPC protocol to be used. Encryption is enabled with --tls option'
)
parser.add_argument('-t', '--tls', action='store_true', default=False)
parser.add_argument('-d', '--database', required=True)
parser.add_argument('-u', '--user', required=True)
parser.add_argument('-w', '--passwd', required=True)
parser.add_argument(
    '-i',
    '--ids',
    type=int,
    metavar='IDs',
    nargs='+',
    help=(
         'List of ids of the records to be processed separated by a space. '
         'If an ID is not found it will be skipped without rising errors.'
    )
)

# Parse the command line arguments
args = parser.parse_args()

if args.protocol == 'json':
    protocol = args.tls and 'jsonrpcs' or 'jsonrpc'
elif args.protocol == 'xml':
    protocol = args.tls and 'xmlpcs' or 'xmlrpc'
else:
    raise ValueError(f'Invalid protocol selected: {args.protocol}')
# end if

# # # #
# Connect to Odoo
# # # #

# Connect
connection = odoolib.get_connection(
    protocol=protocol,
    hostname=args.host,
    port=args.port,
    database=args.database,
    login=args.user,
    password=args.passwd,
)

# Define models
OdooResUsers = connection.get_model('res.users')
OdooResPartner = connection.get_model('res.partner')
OdooAccountInvoice = connection.get_model('account.invoice')
OdooFatturaPAAttachmentIn = connection.get_model('fatturapa.attachment.in')

# Check successful connection
users_ids = OdooResUsers.search([('login', '=', 'admin')])
print('Successfully logged in as', OdooResUsers.read(users_ids[0], ['name'])['name'])

# # # #
# Process e-fattura-in
# # # #

# Load the ids
fatturapa_in_recordset = OdooFatturaPAAttachmentIn.search_read(
    args.ids and [('id', 'in', args.ids)] or [],
    ['id']
)
fatturapa_in_ids_list = [record['id'] for record in fatturapa_in_recordset]
print(f'Found {len(fatturapa_in_ids_list)} e-invoices to process')

# Split records in chunks
chunks_list = [
    fatturapa_in_ids_list[CHUNK_SIZE * i: min(CHUNK_SIZE * (i+1), len(fatturapa_in_ids_list))]
    for i in range(math.ceil(len(fatturapa_in_ids_list) / CHUNK_SIZE))
]
print(f'Job split in {len(chunks_list)} chunks of {CHUNK_SIZE} records each')

# Process records by calling the "load_extra_data_multi" methods for each record
for chunk_idx, chunk in enumerate(chunks_list):
    print(
        f'[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] Processing chunk {chunk_idx + 1} / {len(chunks_list)} ...',
        end=''
    )
    OdooFatturaPAAttachmentIn.load_extra_data_multi(chunk)
    print('done!')
# end for

print(f'[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] Task completed!')
