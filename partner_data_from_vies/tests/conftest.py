# © 2020 Andrei Levin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoolib
from config import config


class OdooAccess:
    def __init__(self, config):
        # Prepare the connection to the server
        self.connection = odoolib.get_connection(
            hostname=config.hostname, database=config.database,
            login=config.username, password=config.password,
            protocol=config.protocol
        )

    def execute(self, *args, **kwargs):
        return self.connection.execute(*args, **kwargs)

    def env(self, *args, **kwargs):
        return self.connection.get_model(*args, **kwargs)


odoo_c = OdooAccess(config)
