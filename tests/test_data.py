import pytest
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data import random_booking, serialize_booking, deserialize_booking, Booking


def test_booking_serialization_deserialization():
    """
    Test that bookings can be serialized to XML and deserialized back to Booking objects.
    
    This test:
    1. Generates a few random bookings
    2. Serializes each booking to XML
    3. Prints the serialized XML to the terminal for visual verification
    4. Deserializes the XML back to a Booking object
    5. Verifies that the deserialized booking has the same properties as the original
    """
    # Number of random bookings to generate and test
    num_bookings = 3
    
    for i in range(num_bookings):
        print(f"\n\n{'='*80}\nTesting booking {i+1} of {num_bookings}\n{'='*80}")
        
        # Generate a random booking
        original_booking = random_booking()
        
        # Serialize the booking to XML
        xml_bytes = serialize_booking(original_booking)
        
        # Print the serialized XML for visual verification
        print(f"\nSerialized XML for booking {i+1}:\n")
        print(xml_bytes.decode('utf-8'))
        
        # Deserialize the XML back to a Booking object
        deserialized_booking = deserialize_booking(xml_bytes)
        
        # Verify that the deserialized booking has the same properties as the original
        assert isinstance(deserialized_booking, Booking), "Deserialized object is not a Booking"
        
        # Check basic properties
        assert deserialized_booking.confirmation_number == original_booking.confirmation_number
        assert deserialized_booking.booking_source == original_booking.booking_source
        assert deserialized_booking.booking_date == original_booking.booking_date
        assert deserialized_booking.checkin_date == original_booking.checkin_date
        assert deserialized_booking.checkout_date == original_booking.checkout_date
        
        # Check hotel
        assert deserialized_booking.hotel.name == original_booking.hotel.name
        assert deserialized_booking.hotel.address.street == original_booking.hotel.address.street
        assert deserialized_booking.hotel.address.city == original_booking.hotel.address.city
        assert deserialized_booking.hotel.address.state == original_booking.hotel.address.state
        assert deserialized_booking.hotel.address.zip_code == original_booking.hotel.address.zip_code
        assert deserialized_booking.hotel.address.country == original_booking.hotel.address.country
        assert deserialized_booking.hotel.address.country_code == original_booking.hotel.address.country_code
        
        # Check guests
        assert len(deserialized_booking.guests) == len(original_booking.guests)
        for j, (orig_guest, deser_guest) in enumerate(zip(original_booking.guests, deserialized_booking.guests)):
            assert deser_guest.name == orig_guest.name, f"Guest {j+1} name mismatch"
            assert deser_guest.email == orig_guest.email, f"Guest {j+1} email mismatch"
            assert deser_guest.phone == orig_guest.phone, f"Guest {j+1} phone mismatch"
            assert deser_guest.birthdate == orig_guest.birthdate, f"Guest {j+1} birthdate mismatch"
            assert deser_guest.address.street == orig_guest.address.street, f"Guest {j+1} address street mismatch"
            assert deser_guest.address.city == orig_guest.address.city, f"Guest {j+1} address city mismatch"
            assert deser_guest.address.state == orig_guest.address.state, f"Guest {j+1} address state mismatch"
            assert deser_guest.address.zip_code == orig_guest.address.zip_code, f"Guest {j+1} address zip mismatch"
            assert deser_guest.address.country == orig_guest.address.country, f"Guest {j+1} address country mismatch"
            assert deser_guest.address.country_code == orig_guest.address.country_code, f"Guest {j+1} address country code mismatch"
        
        # Check payment
        assert deserialized_booking.payment.amount == original_booking.payment.amount
        assert deserialized_booking.payment.currency == original_booking.payment.currency
        assert deserialized_booking.payment.payment_method == original_booking.payment.payment_method
        assert deserialized_booking.payment.transaction_id == original_booking.payment.transaction_id
        assert deserialized_booking.payment.voucher_code == original_booking.payment.voucher_code
        assert deserialized_booking.payment.billing_address.street == original_booking.payment.billing_address.street
        assert deserialized_booking.payment.billing_address.city == original_booking.payment.billing_address.city
        assert deserialized_booking.payment.billing_address.state == original_booking.payment.billing_address.state
        assert deserialized_booking.payment.billing_address.zip_code == original_booking.payment.billing_address.zip_code
        assert deserialized_booking.payment.billing_address.country == original_booking.payment.billing_address.country
        assert deserialized_booking.payment.billing_address.country_code == original_booking.payment.billing_address.country_code
        
        # Check booking notes
        assert len(deserialized_booking.booking_notes) == len(original_booking.booking_notes)
        for j, (orig_note, deser_note) in enumerate(zip(original_booking.booking_notes, deserialized_booking.booking_notes)):
            assert deser_note == orig_note, f"Booking note {j+1} mismatch"
        
        print(f"\nBooking {i+1} serialization/deserialization test passed!")
    
    print("\nAll booking serialization/deserialization tests passed!")