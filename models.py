from dataclasses import dataclass, field


@dataclass
class Counterparty:
    name: str = ""
    inn: str = ""
    account: str = ""
    bank: str = ""
    bik: str = ""
    address: str = ""

    def to_table_rows(self) -> list[list[str]]:
        """
        Собирает в массив. Неуказанные пропускаются (покупатель отличается по кол-ву данных от продавца)
        """
        rows = []
        if self.name:
            rows.append(["Контрагент:", self.name])
        if self.inn:
            rows.append(["ИНН:", self.inn])
        if self.account:
            rows.append(["Р/с:", self.account])
        if self.bank:
            rows.append(["Банк:", self.bank])
        if self.bik:
            rows.append(["БИК:", self.bik])
        if self.address:
            rows.append(["Адрес:", self.address])
        return rows


@dataclass
class ServiceItem:
    number: str
    name: str
    quantity: str
    price: str
    total: str

    def to_row(self) -> list[str]:
        return [self.number, self.name, self.quantity, self.price, self.total]


@dataclass
class Invoice:
    invoice_number: str
    date: str
    seller: Counterparty = field(default_factory=Counterparty)
    buyer: Counterparty = field(default_factory=Counterparty)
    items: list[ServiceItem] = field(default_factory=list)
    subtotal: str = ""
    vat: str = ""
    grand_total: str = ""

    def get_items_table(self) -> list[list[str]]:
        """
        Возвращает счет под таблицу.
        """
        header = ["№", "Наименование", "Кол-во", "Цена", "Сумма"]
        rows = [header]
        
        for i, item in enumerate(self.items, 1):
            rows.append(item.to_row())
        
        # Итоги
        if self.subtotal:
            rows.append(["", "", "", "Итого:", self.subtotal])
        if self.vat:
            rows.append(["", "", "", "НДС:", self.vat])
        if self.grand_total:
            rows.append(["", "", "", "К оплате:", self.grand_total])
        
        return rows



if __name__ == "__main__":
    # переписать пример на более нейтральный
    seller = Counterparty(
        name='ООО "Ромашка"',
        inn="1234567890",
        account="40702810000000000000",
        bank="ПАО Сбербанк",
        bik="044525225"
    )

    buyer = Counterparty(
        name="ИП Иванов И.И.",
        inn="987654321012",
        address="г. Москва, ул. Примерная, д. 1"
    )

    items = [
        ServiceItem("1", "Разработка сайта", "1", "50 000", "50 000"),
        ServiceItem("2", "Техническая поддержка", "3", "5 000", "15 000"),
    ]

    invoice = Invoice(
        invoice_number="123",
        date="27.03.2026",
        seller=seller,
        buyer=buyer,
        items=items,
        subtotal="65 000",
        vat="Без НДС",
        grand_total="65 000 руб."
    )

    print("Продавец:", invoice.seller.to_table_rows())
    print("Покупатель:", invoice.buyer.to_table_rows())
    print("Товары:", invoice.get_items_table())
