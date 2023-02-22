from payload.core.person import PersonPayload


class OwnerPayload(PersonPayload):
    RELATIONAL_PROPS = []

    def __init__(self, **kwargs):
        super(OwnerPayload, self).__init__(**kwargs)
        self.type = kwargs.get('type', 'Owner')
        self.legalName = kwargs.get('legalName', '')
        self.isCompany = kwargs.get('isCompany', False)
        self.address = kwargs.get('address', {})
        self.delivery_address = kwargs.get('delivery_address', {})
        self.telephone = kwargs.get('telephone', '')

    @property
    def legalName(self) -> str:
        return self._legalName

    @legalName.setter
    def legalName(self, legalName: str) -> None:
        self._legalName = legalName

    @property
    def isCompany(self) -> bool:
        return self._isCompany

    @isCompany.setter
    def isCompany(self, isCompany: bool) -> None:
        self._isCompany = isCompany

    @property
    def address(self) -> dict:
        return self._address

    @address.setter
    def address(self, address: dict) -> None:
        self._address = address

    @property
    def delivery_address(self) -> dict:
        return self._delivery_address

    @delivery_address.setter
    def delivery_address(self, delivery_address: dict) -> None:
        self._delivery_address = delivery_address

    @property
    def telephone(self) -> str:
        return self._telephone

    @telephone.setter
    def telephone(self, telephone: str) -> None:
        self._telephone = telephone

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, image: str) -> None:
        self._image = image
