import time

from data_base.db_help_class import db_help, connect_close, connect_dec


class data_base(db_help):
    def add_coach(self, name, cost, tg_id):
        """Add coach name, cost, telegram id to the database"""
        db_help.add_info(self, 'coach', '*', [name, str(cost), str(tg_id)])

    def add_tools(self, name, cost):
        """Add tool name, cost to the database"""
        db_help.add_info(self, 'tools', '*', [name, str(cost)])

    def add_basket(self, name, cost_of_order):
        """Add basket row to the database
        - name - name of man who have done the order
        - cost_of_order - cost of first men order"""
        db_help.add_info(self, 'basket', '*', [name, str(cost_of_order)])
        self.start_basket(name)

    def start_basket(self, name):
        """Delete row before 15 minutes"""
        time.sleep(15)
        db_help.delete_info(self, 'basket', ['name'], [name])

    @connect_dec
    def return_cost(self, name_of_table, name_of_thing):
        """Returning cost of thing
        - name of table - table where thing exists
        - name_of_thing - name of existing thing"""
        name_of_cost = 'cost' if name_of_table != 'basket' else 'cost_of_order'
        try:
            return self.cursor.execute(
                    f"SELECT {name_of_cost} FROM {name_of_table} WHERE name='{name_of_thing}'").fetchall()[0]
        except Exception as e:
            print(e)
            return False

    @connect_close
    def add_to_basket(self, name, cost_of_order):
        """Method to add new order to the existing row in the baskets table"""
        now = self.return_cost('basket', name)
        if not now:
            return False
        now = now[0]
        self.cursor.execute("UPDATE basket SET cost_of_order = '{cost}' WHERE name = '{name}'".format(
            cost=str(now) + ', ' + str(cost_of_order), name=name))

    def return_basket_order(self, name):
        """Method to return text with costs of every order
        - name - name of man who has this order"""
        text = self.return_cost('basket', name)
        if not text:
            return False
        text = text[0]
        arr_of_orders = ['Цена {} заказа {}'.format(i + 1, j) for i, j in enumerate(text.split(', '))]
        return '\n'.join(arr_of_orders)

    def return_basket_price(self, name):
        """Method to return price of order
        - name - name of man who has this order"""
        text = self.return_cost('basket', name)
        if not text:
            return False
        text = text[0]
        return sum([int(i) for i in text.split(', ')])
