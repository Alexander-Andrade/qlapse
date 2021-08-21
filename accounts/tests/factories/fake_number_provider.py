from faker.providers.phone_number.en_US import Provider


class CustomPhoneProvider(Provider):
    # Twilio numbers format
    # +1 929 334 3259 - New York City Zone, NY
    # +1 628 227 5972 - San Francisco, CA
    def phone_number(self):
        return self.numerify('+1##########')
