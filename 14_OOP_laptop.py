class Laptop:    
    def __init__(self, brand, processor, generation, ram_gb, storage):
        self.brand = brand
        self.processor = processor
        self.generation = generation
        self._ram_gb = ram_gb           # protected
        self.storage =storage    
    
    def show_configuration(self):
        return f"""
        Brand     : {self.brand}
        Processor : {self.processor}
        Generation: {self.generation}
        Ram       : {self._ram_gb}
        Storage   : {self.storage}        
        """
    def run_code(self):
        return "Code is working fine!"

    def get_ram(self):
        return self._ram_gb
    def set_ram(self, new_ram):
        if new_ram > 64:
            return f"{new_ram}Gb ram is not supported"
        else:
            self._ram_gb = new_ram
        