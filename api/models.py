from django.db import models
from django.core.exceptions import ValidationError

class Member(models.Model):

    # Family Information
    family_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    spouse_name = models.CharField(max_length=100, blank=True, null=True)

    # Photos
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)

    # Communication Address
    address = models.CharField(max_length=255)
    # address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)

    # Contact Details
    mobile_1 = models.CharField(max_length=15)
    mobile_2_spouse = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_no_1 = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_no_2 = models.CharField(max_length=15, blank=True, null=True)
    email_id_1 = models.EmailField()
    email_id_2 = models.EmailField(blank=True, null=True)

    # Additional Information
    pulli_id = models.CharField(max_length=50, unique=True)
    native = models.CharField(max_length=100)
    karai = models.CharField(max_length=100)

    # Custom Columns
    token_year = models.PositiveIntegerField(null=True)
    token_number = models.PositiveIntegerField(null=True)
    custom_column_1 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.family_name})"

class YelamProduct(models.Model):
    name = models.CharField(max_length=200)
    member = models.ForeignKey(Member,on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"
    

class Yelam(models.Model):
    INHOUSE = 'inhouse'
    EXTERNAL = 'external'

    BIDDER_TYPE_CHOICES = [
        (INHOUSE, 'Inhouse'),
        (EXTERNAL, 'External'),
    ]

    product = models.ForeignKey('YelamProduct', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.PROTECT, null=True, blank=True)
    bidder_type = models.CharField(
        max_length=10,
        choices=BIDDER_TYPE_CHOICES,
        default=INHOUSE,
    )
    bidder_name = models.CharField(max_length=100, null=True, blank=True)  # For external bidders
    bid_amount = models.CharField(max_length=100)
    pending_amount = models.CharField(max_length=100)

    def clean(self):
        # Ensure `member` is provided for inhouse bidders
        if self.bidder_type == self.INHOUSE and not self.member:
            raise ValidationError({'member': 'Member must be provided for inhouse bids.'})

        # Ensure `bidder_name` is provided for external bidders
        if self.bidder_type == self.EXTERNAL and not self.bidder_name:
            raise ValidationError({'bidder_name': 'Bidder name must be provided for external bids.'})

        # Ensure `member` is still referenced for external bids
        if self.bidder_type == self.EXTERNAL and not self.member:
            raise ValidationError({'member': 'Reference member must be provided for external bids.'})

    def save(self, *args, **kwargs):
        # Run the custom validations before saving
        self.clean()
        super().save(*args, **kwargs)

class Token(models.Model):
    number = models.IntegerField()
    year = models.IntegerField()
    member = models.ForeignKey(Member,on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"