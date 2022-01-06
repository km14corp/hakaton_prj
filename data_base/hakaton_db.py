import time

from data_base.db_help_class import db_help, connect_close, connect_dec


class data_base(db_help):
    def add_coach(self, name, cost, tg_id):
        db_help.add_info(self, 'coach', '*', [name, cost, tg_id])

    def add_tools(self, name, cost):
        db_help.add_info(self, 'tools', '*', [name, cost])

    def add_basket(self, name, cost_of_order):
        db_help.add_info(self, 'basket', '*', [name, cost_of_order])
        self.start_basket(name)

    def start_basket(self, name):
        time.sleep(15 * 60)
        db_help.delete_info(self, 'name', name)

    @connect_dec
    def return_cost(self, name_of_table, name_of_thing):
        return self.cursor.execute(f"SELECT cost_of_order FROM {name_of_table} WHERE name='{name_of_thing}'")

    @connect_close
    def add_to_basket(self, name, cost_of_order):
        now = self.return_cost('basket', name)[0]
        self.cursor.execute("UPDATE basket SET cost_of_order = {cost} WHERE name = {name}".format(
            cost=now + ', ' + str(cost_of_order), name=name))

    def return_basket_order(self, name):
        text = self.return_cost('basket', name)[0]
        arr_of_orders = ['Цена {} заказа {}'.format(i, j) for i, j in enumerate(text.split(', '))]
        return '\n'.join(arr_of_orders)
