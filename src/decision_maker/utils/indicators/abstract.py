from injector import singleton
from pandas import DataFrame


@singleton
class AbstractIndicatorFactory:
    def __init__(self, quotation_data: DataFrame):
        self.quotations = quotation_data
