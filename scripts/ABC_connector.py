from abc import ABC, abstractmethod


class abc_reference_conector (ABC):

    @property
    @abstractmethod
    def data_type(self):
        pass

    @property
    @abstractmethod
    def platform_name(self):
        pass


    @property
    @abstractmethod
    def search_url (self, platform_name):
        pass 

    @property
    @abstractmethod
    def  search_string(self):
        """Note, this section can be linked to the SimPhoNy backend as discussed before"""
        pass
    
    @abstractmethod
    def searching(self):
        pass

    @abstractmethod
    def return_results(self):
        pass

    @abstractmethod
    def version_api(self,version):
        pass