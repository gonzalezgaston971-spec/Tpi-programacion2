class FoodStoreError(Exception):
    pass


class DatoInvalidoError(FoodStoreError):
    pass


class TipoDatoInvalidoError(FoodStoreError):
    pass


class StockInsuficienteError(FoodStoreError):
    pass


class EntidadNoEncontradaError(FoodStoreError):
    pass


class DuplicadoError(FoodStoreError):
    pass


class OperacionNoPermitidaError(FoodStoreError):
    pass


class CredencialesInvalidasError(FoodStoreError):
    pass
