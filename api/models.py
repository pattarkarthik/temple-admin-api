from django.db import models

class Member(models.Model):
    # Existing fields...
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


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.product_name


class Yelam(models.Model):
    INHOUSE = 'inhouse'
    EXTERNAL = 'guest'

    BIDDER_TYPE_CHOICES = [
        (INHOUSE, 'inhouse'),
        (EXTERNAL, 'guest'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial Payment'),
        ('paid', 'Full Payment'),
    ]

    manual_book_srno = models.CharField(max_length=100)
    remarks = models.CharField(max_length=1000, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    member = models.ForeignKey('Member', on_delete=models.PROTECT)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder_type = models.CharField(max_length=10, choices=BIDDER_TYPE_CHOICES, default=INHOUSE)
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_whatsapp = models.CharField(max_length=100, null=True, blank=True)
    guest_native = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)

    def __str__(self):
        return f"Yelam {self.manual_book_srno} ({self.bidder_type})"

    def update_payment_status(self):
        total_paid = sum(transaction.amount for transaction in self.transactions.all())
        self.pending_amount = self.bid_amount - total_paid

        # Update payment status based on pending amount
        if self.pending_amount == self.bid_amount:
            self.payment_status = 'unpaid'
        elif self.pending_amount > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'paid'

        self.save()

class PaymentTransaction(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
        ('cheque', 'Cheque'),
    ]

    yelam = models.ForeignKey(Yelam, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    receipt_number = models.CharField(max_length=100, unique=True)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)

    def __str__(self):
        return f"Payment of {self.amount} for Yelam {self.yelam.manual_book_srno}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the transaction
        self.yelam.update_payment_status()  # Update the payment status of the associated Yelam

class Token(models.Model):
    number = models.IntegerField()
    year = models.IntegerField()
    member = models.ForeignKey(Member, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('number', 'year', 'member')

    def __str__(self):
        return f"Token {self.number}/{self.year} for {self.member}"
