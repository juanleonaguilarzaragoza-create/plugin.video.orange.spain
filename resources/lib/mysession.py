# encoding: utf-8
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from __future__ import unicode_literals, absolute_import, division

import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class CustomAdapter(HTTPAdapter):

    def __init__(self, *args, **kwargs):
        # Crear contexto SSL estándar del sistema
        self.ctx = ssl.create_default_context()

        # Bajar nivel de seguridad para permitir servidores antiguos
        # (RSA pequeños, SHA1, etc.)
        try:
            self.ctx.set_ciphers('DEFAULT@SECLEVEL=0')
        except Exception:
            pass

        super(CustomAdapter, self).__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ctx
        )


class MySession(requests.Session):

    def __init__(self, *args, **kwargs):
        super(MySession, self).__init__(*args, **kwargs)

        # Aplicar adaptador SSL personalizado a HTTPS
        self.mount('https://', CustomAdapter())
