from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    email = models.EmailField(unique=True)

    # Log in with email instead of username
    USERNAME_FIELD = "email"
    # Prompted by `createsuperuser` (excludes USERNAME_FIELD and password)
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        # Stop "Ada@x.com" and "ada@x.com" from being two different accounts
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class SlugMixin(models.Model):
    """Auto-generates a unique slug from `slug_source` on first save."""

    slug = models.SlugField(unique=True, blank=True)
    slug_source = "name"  # override in subclasses

    class Meta:
        abstract = True

    def _generate_unique_slug(self):
        base = slugify(getattr(self, self.slug_source)) or "item"
        slug, n = base, 2
        qs = type(self).objects.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)


class Category(SlugMixin):
    name = models.CharField(max_length=100)
    slug_source = "name"

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Course(SlugMixin):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="courses"
    )
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_index=True,
    )
    description = models.TextField(blank=True)
    slug_source = "title"

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title