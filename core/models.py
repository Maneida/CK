from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
import uuid
from uuid import UUID

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id or not isinstance(self.id, uuid.UUID):
            self.id = uuid.uuid4()
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)
        
    def generate_slug(self):
        """
        Generate a unique slug for the model instance.
        Override this method in subclasses to provide custom behaviour.
        """
        base_slug = slugify(str(self))
        unique_slug = base_slug
        num = 1
        while self.__class__.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        return unique_slug

    def to_dict(self):
        """Returns a dictionary containing all key/values of the instance."""
        new_dict = {
            field.name: field.value_from_object(self)
            for field in self._meta.fields
        }
        
        datetime_format = '%Y-%m-%dT%H:%M:%S.%f'
        
        for field in self._meta.fields:
            if isinstance(field, (models.DateTimeField, models.DateField)) and field.name in new_dict:
                if new_dict[field.name]:
                    new_dict[field.name] = new_dict[field.name].strftime(datetime_format)
            elif isinstance(new_dict[field.name], UUID):
                new_dict[field.name] = str(new_dict[field.name])
        
        new_dict["__class__"] = self.__class__.__name__
        return new_dict
    
    def get_absolute_url(self):
        """
        Returns the URL to access a particular instance of the model.
        Override this method in subclasses to provide custom behavior.
        """
        return reverse(f'{self._meta.model_name}_detail', kwargs={'slug': self.slug})


class Category(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    def generate_slug(self):
        return slugify(self.name)
    

class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def generate_slug(self):
        return slugify(self.name)


class Post(BaseModel):
    title = models.CharField(max_length=255)
    # title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = CKEditor5Field('Content', config_name='extends')
    post_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    preview = models.TextField(blank=True,
                               help_text="Optional preview text for the post.",
                               validators=[MaxLengthValidator(limit_value=500)])
    post_image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    @property
    def category_name(self):
        return self.category.name if self.category else None
    
    @property
    def title_tag(self):
        return f"{self.title} | {self.author} | {self.category}" 

    def __str__(self):
        return self.title

    def generate_slug(self):
        return slugify(self.title)

