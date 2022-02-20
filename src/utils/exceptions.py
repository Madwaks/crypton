class NotAvailableException(Exception):
    code = 404

    @property
    def message(self):
        return self.args[0]
