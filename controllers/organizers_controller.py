from core.persistance.organizer_store import OrganizerStore
from models.organizer_model import Organizer
from views.organizers_view import OrganizersView
from core.exceptions.user_exit_exception import UserExitException


class OrganizersController:
    def __init__(self, controllers_manager):
        self.__controllers_manager = controllers_manager
        self.view = OrganizersView()
        self.__store = OrganizerStore()

    def get_organizers(self):
        return self.__store.list()

    def get_organizer_by_cpf(self, cpf):
        return self.__store.get(cpf)

    def add_organizer(self, cpf, name, birthday, cep, street, number, complement):
        organizer = Organizer(cpf, name, birthday, cep,
                              street, number, complement)
        self.__store.add(organizer)

    def edit_organizer(self, cpf, name, birthday, cep, street, number, complement):
        organizer = self.get_organizer_by_cpf(cpf)

        organizer.name = name
        organizer.birthday = birthday
        organizer.address.cep = cep
        organizer.address.street = street
        organizer.address.number = number
        organizer.address.complement = complement

        self.__store.update(organizer)

    def remove_organizer(self, cpf):
        self.__store.remove(cpf)

    def open_organizers_menu(self):
        try:
            while True:
                bindings = {
                    'register_organizer': self.open_register_organizer,
                    'edit_organizer': self.open_edit_organizer,
                    'remove_organizer': self.open_remove_organizer,
                    'list_organizers': self.open_organizers_list,
                    'find_organizer': self.open_find_organizer
                }

                option = self.view.show_organizers_menu()
                bindings[option]()
        except UserExitException:
            return

    def open_register_organizer(self):
        try:
            organizer_data = None

            organizer_correct_data = False
            first_loop = True
            while not organizer_correct_data:
                organizer_data = self.view.show_organizer_register(
                    remount=first_loop)
                first_loop = False

                already_has_organizer = self.get_organizer_by_cpf(
                    organizer_data['cpf'])
                if (already_has_organizer != None):
                    self.view.show_error_message('Esse CPF ja foi cadastrado!')
                    continue

                organizer_correct_data = True

            self.view.close()

            address_data = self.__controllers_manager.address.view.show_register_address()
            self.__controllers_manager.address.view.close()

            self.add_organizer(
                organizer_data["cpf"],
                organizer_data["name"],
                organizer_data["birthday"],
                address_data["cep"],
                address_data["street"],
                address_data["number"],
                address_data["complement"],
            )

            self.view.show_message('Organizador adicionado!')
        except UserExitException:
            self.view.close()
            return

    def open_edit_organizer(self):
        try:
            organizer = self.open_select_organizer()

            organizer_data = self.view.show_organizer_register(
                organizer.to_raw(address_str=False))

            address_data = self.__controllers_manager.address.view.show_register_address(
                organizer.address.to_raw())
            self.__controllers_manager.address.view.close()

            self.edit_organizer(
                organizer.cpf,
                organizer_data["name"],
                organizer_data["birthday"],
                address_data["cep"],
                address_data["street"],
                address_data["number"],
                address_data["complement"],
            )

            self.view.close()
            self.view.show_message('Organizador editado!')
        except UserExitException:
            self.view.close()
            return

    def open_remove_organizer(self):
        try:
            organizer = self.open_select_organizer()

            self.remove_organizer(organizer.cpf)

            self.view.show_message('Organizador deletado!')
        except UserExitException:
            self.view.close()
            return

    def open_organizers_list(self):
        organizers = self.get_organizers()

        organizers_data = []
        for key in organizers:
            organizer = organizers[key]
            organizers_data.append(organizer.to_raw())

        self.view.show_organizers_list(organizers_data)

    def open_find_organizer(self):
        try:
            organizer = self.open_select_organizer()
            self.view.show_organizer_details(organizer.to_raw())
        except UserExitException:
            self.view.close()
            return

    def open_select_organizer(self):
        while True:
            input_find = self.view.show_find_organizer()
            self.view.close()

            organizer = self.get_organizer_by_cpf(input_find['cpf'])

            if (organizer):
                return organizer
            else:
                self.view.show_message('Organizador n??o encontrado!')

    def open_select_many_organizers(self):
        organizers = []
        raw_organizers = []

        while True:
            button, values = self.view.show_find_many_organizers(
                raw_organizers)
            self.view.close()

            if (button == 'confirm'):
                return organizers

            organizer = self.get_organizer_by_cpf(values['cpf'])

            if (organizer):
                organizers.append(organizer)
                raw_organizers.append(organizer.to_raw())
            else:
                self.view.show_message('Organizador n??o encontrado!')
