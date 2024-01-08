from faker import Faker

fake = Faker(locale='de')
class UserParams(object):
    def __init__(self, f_name=None, l_name=None, dob=None,
                 email=None, address=None, phone=None):

        self.f_name = f_name if f_name is not None else fake.first_name()
        self.l_name = l_name if l_name is not None else fake.last_name()
        fake_dob = fake.date_of_birth(minimum_age=18, maximum_age=65)
        self.dob = dob if dob is not None else fake_dob.strftime('%Y-%m-%d')
        self.email = email if email is not None else fake.email()
        self.address = address if address is not None else fake.address()
        self.phone = phone if phone is not None else fake.phone_number()

    def gen_user_data(self) -> dict:
        user_data = {
            "f_name": self.f_name,
            "l_name": self.l_name,
            "dob": self.dob,
            "email": self.email,
            "address": self.address,
            "phone": self.phone
        }
        return user_data