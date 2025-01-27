from django.db import models

class Member(models.Model):
    pulli_id = models.CharField(primary_key=True, max_length=50, unique=True)
    family_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    husband_photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    wife_photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    mobile_1 = models.CharField(max_length=15)
    mobile_2_spouse = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_no_1 = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_no_2 = models.CharField(max_length=15, blank=True, null=True)
    email_id_1 = models.EmailField()
    email_id_2 = models.EmailField(blank=True, null=True)
    native = models.CharField(max_length=100)
    karai = models.CharField(max_length=100)
    token_year = models.PositiveIntegerField(null=True)
    token_number = models.PositiveIntegerField(null=True)
    custom_column_1 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.family_name})"


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Yelam(models.Model):
    INHOUSE = 'inhouse'
    EXTERNAL = 'guest'

    BIDDER_TYPE_CHOICES = [
        (INHOUSE, 'inhouse'),
        (EXTERNAL, 'guest'),
    ]

    manual_book_srno = models.CharField(max_length=100)
    remarks = models.CharField(max_length=1000, null=True, blank=True)
    product = models.CharField(max_length=1000)
    # product = models.ForeignKey('Product', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.PROTECT)
    bid_amount = models.CharField(max_length=100, null=True, blank=True)
    bidder_type = models.CharField(max_length=10, choices=BIDDER_TYPE_CHOICES, default=INHOUSE)
    balance_amount = models.CharField(max_length=100, null=True, blank=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_whatsapp = models.CharField(max_length=100, null=True, blank=True)
    guest_native = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Yelam {self.manual_book_srno} ({self.bidder_type})"


class Token(models.Model):
    number = models.IntegerField()
    year = models.IntegerField()
    member = models.ForeignKey(Member, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('number', 'year', 'member')

    def __str__(self):
        return f"Token {self.number}/{self.year} for {self.member}"
