from django.db import models
from django.urls import reverse
import uuid


class Genre(models.Model):
    """
    Модель для представления жанра книги.
    """
    name = models.CharField(max_length=100, help_text="Enter a book genre")

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Модель для представления книги (но не физического экземпляра).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к определенному экземпляру книги.
        """
        return reverse('book_detail', args=[str(self.id)])

    def display_genre(self):
        """
        Создаёт строку для жанра книги. Требуется для отображения жанра в Админке.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Модель для представления экземпляра книги.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text="Book availability")

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    """
    Модель для представления автора той или иной книги.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
    Возвращает URL для доступа к определенному автору.
    """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Language(models.Model):
    """
    Модель для представления языка.
    """
    name = models.CharField(max_length=100, help_text="Enter a language the book was written in")

    def __str__(self):
        return f"{self.name}"
