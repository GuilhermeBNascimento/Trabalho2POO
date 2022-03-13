from views.locals_view import LocalsView
from models.local_model import Local
from core.exceptions.user_exit_exception import UserExitException
from core.persistance.local_store import LocalStore


class LocalsController:
    def __init__(self, controllers_manager):
        self.__controllers_manager = controllers_manager
        self.view = LocalsView()
        self.store = LocalStore()

    def get_locals(self):
        return self.store.list()

    def get_local_by_name(self, name):
        return self.store.get(name)

    def add_local(self, name, cep, street, number, complement):
        local = Local(name, cep, street, number, complement)
        self.store.add(local)

    def edit_local(self, name, cep, street, number, complement):
        local = self.get_local_by_name(name)

        local.address.cep = cep
        local.address.street = street
        local.address.number = number
        local.address.complement = complement

        self.store.update(local)

    def delete_local(self, name):
        self.store.remove(name)

    def open_locals_menu(self):
        try:
            while True:
                bindings = {
                    'register_local': self.open_register_local,
                    'edit_local': self.open_edit_local,
                    'remove_local': self.open_remove_local,
                    'list_locals': self.open_local_list,
                    'find_local': self.open_find_local
                }

                option = self.view.show_locals_menu()
                bindings[option]()
        except UserExitException:
            return

    def open_register_local(self):
        local_data = self.view.show_register_local()
        address_data = self.__controllers_manager.address.view.show_register_address()
        self.__controllers_manager.address.view.close()

        self.add_local(
            local_data['name'],
            address_data['cep'],
            address_data['street'],
            address_data['number'],
            address_data['complement']
        )

        self.view.show_message('Local adicionado!')

    def open_edit_local(self):
        local = self.open_select_local()
        address_data = self.__controllers_manager.address.view.show_register_address()

        self.edit_local(
            local.name,
            address_data['cep'],
            address_data['street'],
            address_data['number'],
            address_data['complement']
        )

        self.view.show_message('Local editado!')

    def open_remove_local(self):
        local = self.open_select_local()
        self.delete_local(local.name)
        self.view.show_message('Local deletado!')

    def open_local_list(self):
        locals = self.get_locals()
        print(locals)

        locals_data = []
        for key in locals:
            local = locals[key]
            locals_data.append(local.to_raw())

        self.view.show_locals_list(locals_data)

    def open_find_local(self):
        local = self.open_select_local()
        self.view.show_local(local.to_raw())

    def open_select_local(self):
        while True:
            values = self.view.show_find_local()
            self.view.close()

            local = self.get_local_by_name(values['name'])

            if (local):
                return local
            else:
                self.view.show_message('Local não encontrado!')
