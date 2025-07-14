import os
import django
import random
from faker import Faker

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "temple_admin_api.settings")

# Initialize Django
django.setup()

from api.models import Member  # Replace `api` with the name of your Django app

faker = Faker()

def generate_fake_mobile_number():
    """Generate a 10-digit realistic mobile number."""
    return f"{random.randint(6000000000, 9999999999)}"

def generate_fake_members(num_members=10):
    for _ in range(num_members):
        family_name = faker.last_name()
        name = faker.first_name()
        spouse_name = faker.first_name() 
        address_line_1 = faker.street_address()
        address_line_2 = faker.secondary_address() 
        city = faker.city()
        state = faker.state()
        pin_code = faker.zipcode()
        mobile_1 = generate_fake_mobile_number()
        mobile_2_spouse = generate_fake_mobile_number() if spouse_name else None
        whatsapp_no_1 = mobile_1 if random.choice([True, False]) else generate_fake_mobile_number()
        whatsapp_no_2 = mobile_2_spouse if mobile_2_spouse else None
        email_id_1 = faker.email()
        email_id_2 = faker.email() if random.choice([True, False]) else None
        pulli_id = faker.unique.uuid4()
        native = faker.city()
        karai = faker.word()
        custom_column_1 = faker.text(max_nb_chars=200) if random.choice([True, False]) else None

        # Create and save the Member object
        member = Member(
            family_name=family_name,
            name=name,
            spouse_name=spouse_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            pin_code=pin_code,
            mobile_1=mobile_1,
            mobile_2_spouse=mobile_2_spouse,
            whatsapp_no_1=whatsapp_no_1,
            whatsapp_no_2=whatsapp_no_2,
            email_id_1=email_id_1,
            email_id_2=email_id_2,
            pulli_id=pulli_id,
            native=native,
            karai=karai,
            custom_column_1=custom_column_1,
        )
        member.save()
        print(f"Member {name} {family_name} created.")

# Run the script
if __name__ == "__main__":
    generate_fake_members(20)  # Change the number of members as needed
