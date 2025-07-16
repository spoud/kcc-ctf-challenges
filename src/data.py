import random
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from typing import List, Optional
from xml.dom import minidom

from faker import Faker


class Address:
    """
    Represents an address with street, city, state, zip, country, and country code.
    """
    def __init__(
        self,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
        country_code: str
    ):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.country_code = country_code

    def to_element(self, tag_name: str = "address") -> ET.Element:
        """
        Convert the Address object to an XML element.

        Args:
            tag_name: The name of the XML tag for the address element.

        Returns:
            An XML element representing the address.
        """
        address_elem = ET.Element(tag_name)

        street_elem = ET.SubElement(address_elem, "street")
        street_elem.text = self.street

        city_elem = ET.SubElement(address_elem, "city")
        city_elem.text = self.city

        state_elem = ET.SubElement(address_elem, "state")
        state_elem.text = self.state

        zip_elem = ET.SubElement(address_elem, "zip")
        zip_elem.text = self.zip_code

        country_elem = ET.SubElement(address_elem, "country")
        country_elem.text = self.country

        country_code_elem = ET.SubElement(address_elem, "country_code")
        country_code_elem.text = self.country_code

        return address_elem

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Address':
        """
        Create an Address object from an XML element.

        Args:
            element: The XML element containing address data.

        Returns:
            An Address object.
        """
        street = element.find("street").text
        city = element.find("city").text
        state = element.find("state").text
        zip_code = element.find("zip").text
        country = element.find("country").text
        country_code = element.find("country_code").text

        return cls(street, city, state, zip_code, country, country_code)


class Hotel:
    """
    Represents a hotel with a name and address.
    """
    def __init__(self, name: str, address: Address):
        self.name = name
        self.address = address

    def to_element(self) -> ET.Element:
        """
        Convert the Hotel object to an XML element.

        Returns:
            An XML element representing the hotel.
        """
        hotel_elem = ET.Element("hotel")

        name_elem = ET.SubElement(hotel_elem, "hotel")
        name_elem.text = self.name

        hotel_elem.append(self.address.to_element())

        return hotel_elem

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Hotel':
        """
        Create a Hotel object from an XML element.

        Args:
            element: The XML element containing hotel data.

        Returns:
            A Hotel object.
        """
        name = element.find("hotel").text
        address = Address.from_element(element.find("address"))

        return cls(name, address)


class Guest:
    """
    Represents a guest with name, email, phone, birthdate, and address.
    """
    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        birthdate: date,
        address: Address
    ):
        self.name = name
        self.email = email
        self.phone = phone
        self.birthdate = birthdate
        self.address = address

    def to_element(self) -> ET.Element:
        """
        Convert the Guest object to an XML element.

        Returns:
            An XML element representing the guest.
        """
        guest_elem = ET.Element("guest")

        name_elem = ET.SubElement(guest_elem, "name")
        name_elem.text = self.name

        email_elem = ET.SubElement(guest_elem, "email")
        email_elem.text = self.email

        phone_elem = ET.SubElement(guest_elem, "phone")
        phone_elem.text = self.phone

        birthdate_elem = ET.SubElement(guest_elem, "birthdate")
        birthdate_elem.text = self.birthdate.isoformat()

        guest_elem.append(self.address.to_element())

        return guest_elem

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Guest':
        """
        Create a Guest object from an XML element.

        Args:
            element: The XML element containing guest data.

        Returns:
            A Guest object.
        """
        name = element.find("name").text
        email = element.find("email").text
        phone = element.find("phone").text
        birthdate_str = element.find("birthdate").text
        birthdate = date.fromisoformat(birthdate_str)
        address = Address.from_element(element.find("address"))

        return cls(name, email, phone, birthdate, address)


class Payment:
    """
    Represents a payment with amount, currency, payment method, transaction ID, billing address, and optional voucher code.
    """
    def __init__(
        self,
        amount: float,
        currency: str,
        payment_method: str,
        transaction_id: str,
        billing_address: Address,
        voucher_code: Optional[str] = None
    ):
        self.amount = amount
        self.currency = currency
        self.payment_method = payment_method
        self.transaction_id = transaction_id
        self.billing_address = billing_address
        self.voucher_code = voucher_code

    def to_element(self) -> ET.Element:
        """
        Convert the Payment object to an XML element.

        Returns:
            An XML element representing the payment.
        """
        payment_elem = ET.Element("payment")

        amount_elem = ET.SubElement(payment_elem, "amount")
        amount_elem.text = str(self.amount)

        currency_elem = ET.SubElement(payment_elem, "currency")
        currency_elem.text = self.currency

        payment_method_elem = ET.SubElement(payment_elem, "payment_method")
        payment_method_elem.text = self.payment_method

        transaction_id_elem = ET.SubElement(payment_elem, "transaction_id")
        transaction_id_elem.text = self.transaction_id

        payment_elem.append(self.billing_address.to_element("billing_address"))

        if self.voucher_code:
            voucher_code_elem = ET.SubElement(payment_elem, "voucher_code")
            voucher_code_elem.text = self.voucher_code

        return payment_elem

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Payment':
        """
        Create a Payment object from an XML element.

        Args:
            element: The XML element containing payment data.

        Returns:
            A Payment object.
        """
        amount = float(element.find("amount").text)
        currency = element.find("currency").text
        payment_method = element.find("payment_method").text
        transaction_id = element.find("transaction_id").text
        billing_address = Address.from_element(element.find("billing_address"))

        voucher_code_elem = element.find("voucher_code")
        voucher_code = voucher_code_elem.text if voucher_code_elem is not None else None

        return cls(amount, currency, payment_method, transaction_id, billing_address, voucher_code)


class Booking:
    """
    Represents a hotel booking with confirmation number, booking source, booking date, checkin date, checkout date,
    hotel information, guests, payment information, and optional booking notes.
    """
    def __init__(
        self,
        confirmation_number: str,
        booking_source: str,
        booking_date: date,
        checkin_date: date,
        checkout_date: date,
        hotel: Hotel,
        guests: List[Guest],
        payment: Payment,
        booking_notes: Optional[List[str]] = None
    ):
        self.confirmation_number = confirmation_number
        self.booking_source = booking_source
        self.booking_date = booking_date
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date
        self.hotel = hotel
        self.guests = guests
        self.payment = payment
        self.booking_notes = booking_notes or []

    def to_element(self) -> ET.Element:
        """
        Convert the Booking object to an XML element.

        Returns:
            An XML element representing the booking.
        """
        booking_elem = ET.Element("booking")
        booking_elem.set("confirmation_number", self.confirmation_number)
        booking_elem.set("booking_source", self.booking_source)
        booking_elem.set("booking_date", self.booking_date.isoformat())

        checkin_elem = ET.SubElement(booking_elem, "checkin")
        checkin_elem.text = self.checkin_date.isoformat()

        checkout_elem = ET.SubElement(booking_elem, "checkout")
        checkout_elem.text = self.checkout_date.isoformat()

        booking_elem.append(self.hotel.to_element())

        guests_elem = ET.SubElement(booking_elem, "guests")
        for guest in self.guests:
            guests_elem.append(guest.to_element())

        booking_elem.append(self.payment.to_element())

        if self.booking_notes:
            booking_notes_elem = ET.SubElement(booking_elem, "booking_notes")
            for note in self.booking_notes:
                note_elem = ET.SubElement(booking_notes_elem, "note")
                note_elem.text = note

        return booking_elem

    @classmethod
    def from_element(cls, element: ET.Element) -> 'Booking':
        """
        Create a Booking object from an XML element.

        Args:
            element: The XML element containing booking data.

        Returns:
            A Booking object.
        """
        confirmation_number = element.get("confirmation_number")
        booking_source = element.get("booking_source")
        booking_date_str = element.get("booking_date")
        booking_date = date.fromisoformat(booking_date_str)

        checkin_date_str = element.find("checkin").text
        checkin_date = date.fromisoformat(checkin_date_str)

        checkout_date_str = element.find("checkout").text
        checkout_date = date.fromisoformat(checkout_date_str)

        hotel = Hotel.from_element(element.find("hotel"))

        guests = []
        guests_elem = element.find("guests")
        for guest_elem in guests_elem.findall("guest"):
            guests.append(Guest.from_element(guest_elem))

        payment = Payment.from_element(element.find("payment"))

        booking_notes = []
        booking_notes_elem = element.find("booking_notes")
        if booking_notes_elem is not None:
            for note_elem in booking_notes_elem.findall("note"):
                booking_notes.append(note_elem.text)

        return cls(
            confirmation_number,
            booking_source,
            booking_date,
            checkin_date,
            checkout_date,
            hotel,
            guests,
            payment,
            booking_notes
        )


def serialize_booking(booking: Booking) -> bytes:
    """
    Serialize a Booking object to XML bytes.

    Args:
        booking: The Booking object to serialize.

    Returns:
        The serialized XML as bytes.
    """
    booking_elem = booking.to_element()
    xml_str = ET.tostring(booking_elem, encoding='utf-8')

    # Pretty print the XML for better readability
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")

    return pretty_xml.encode('utf-8')


def deserialize_booking(xml_bytes: bytes) -> Booking:
    """
    Deserialize XML bytes to a Booking object.

    Args:
        xml_bytes: The XML bytes to deserialize.

    Returns:
        A Booking object.
    """
    root = ET.fromstring(xml_bytes)
    return Booking.from_element(root)


def random_booking() -> Booking:
    """
    Generate a random booking object with random data using Faker.

    The function creates a booking with random:
    - Confirmation number
    - Booking source (either "Online" or "POS")
    - Booking date (within the last 30 days)
    - Checkin date (within the next 30 days)
    - Checkout date (1-14 days after checkin)
    - Hotel information
    - 1-5 guests
    - Payment information
    - Optional booking notes

    Returns:
        A randomly generated Booking object.
    """
    fake = Faker()

    # Generate random booking details
    confirmation_number = fake.uuid4()
    booking_source = random.choice(["Online", "POS"])
    booking_date = date.fromisoformat(fake.date_between(start_date="-30d", end_date="today").isoformat())
    checkin_date = date.fromisoformat(fake.date_between(start_date="today", end_date="+30d").isoformat())
    checkout_date = checkin_date + timedelta(days=random.randint(1, 14))

    # Generate random hotel
    hotel_name = f"{fake.company()} Hotel"
    hotel_address = Address(
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip_code=fake.zipcode(),
        country=fake.country(),
        country_code=fake.country_code()
    )
    hotel = Hotel(name=hotel_name, address=hotel_address)

    # Generate random guests (1-5)
    num_guests = random.randint(1, 5)
    guests = []
    for _ in range(num_guests):
        guest_address = Address(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            zip_code=fake.zipcode(),
            country=fake.country(),
            country_code=fake.country_code()
        )
        guest = Guest(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            birthdate=date.fromisoformat(fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat()),
            address=guest_address
        )
        guests.append(guest)

    # Generate random payment
    billing_address = Address(
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip_code=fake.zipcode(),
        country=fake.country(),
        country_code=fake.country_code()
    )
    payment = Payment(
        amount=float(f"{random.uniform(100, 2000):.2f}"),
        currency=random.choice(["USD", "EUR", "GBP", "CAD", "AUD"]),
        payment_method=random.choice(["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]),
        transaction_id=f"TX{fake.uuid4().replace('-', '')[:12]}",
        billing_address=billing_address,
        voucher_code=f"VOUCHER{fake.random_number(digits=6)}" if random.random() < 0.3 else None
    )

    # Generate random booking notes (optional)
    booking_notes = []
    if random.random() < 0.7:  # 70% chance to have notes
        num_notes = random.randint(1, 3)
        note_options = [
            "Late check-in requested",
            "Early check-in requested",
            "Room with a view preferred",
            "Quiet room requested",
            "Extra pillows needed",
            "Allergic to feathers",
            "Celebrating anniversary",
            "Celebrating birthday",
            "Business trip",
            "Requires accessible room"
        ]
        booking_notes = random.sample(note_options, min(num_notes, len(note_options)))

    # Create and return the booking
    return Booking(
        confirmation_number=confirmation_number,
        booking_source=booking_source,
        booking_date=booking_date,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        hotel=hotel,
        guests=guests,
        payment=payment,
        booking_notes=booking_notes
    )
