from odoo import models, fields, api
from odoo.models import NewId
from odoo.exceptions import UserError

# Alternative simpler approach using session storage
# class SaleOrderSessionManager:
class SaleOrderNewIdManager:
    """Alternative approach using Odoo's session for NewId persistence"""

    @classmethod
    def store_order_in_session(cls, session, order):
        """Store order in user session"""
        if not isinstance(order.id, NewId):
            return None

        # Generate a unique key for this order
        import time
        import random
        session_key = f"newid_order_{int(time.time())}_{random.randint(1000, 9999)}"

        # Store in session (if available)
        if session:
            # Store essential order data in session
            order_cache = dict(order._cache)
            lines_cache = [dict(line._cache) for line in order.order_line]

            session[session_key] = {
                'order_cache': order_cache,
                'lines_cache': lines_cache,
                'model': order._name,
            }

            return session_key

        return None

    @classmethod
    def get_order_from_session(cls, env, session, session_key):
        """Retrieve order from session"""
        if not session_key or not session:
            return None

        session_data = session.get(session_key)
        if not session_data:
            return None

        # Recreate order
        order_cache = session_data.get('order_cache', {})
        lines_cache = session_data.get('lines_cache', [])

        # Create new order
        order = env['sale.order'].new(order_cache)

        # Add lines
        for line_cache in lines_cache:
            line = env['sale.order.line'].new(line_cache)
            order.order_line = order.order_line + line

        return order
