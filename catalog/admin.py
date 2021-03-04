from django.contrib import admin
from .models import Author, Genre, Language, Book, BookInstance

# admin.site.register(Book)
# admin.site.register(Author)

admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(BookInstance)

# Класс, который можно связать с другой записью
# StackedInline - вертикальное отображение книг
class BookInline(admin.StackedInline):
	model = Book
	extra = 0
		


# Определяем класс для администрирования модели Author
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


# Регистрируем класс с соответствующей моделью Author
admin.site.register(Author, AuthorAdmin)


# Класс, который можно связать с другой записью
# TabularInline - горизонтальное отображение книг
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0	# Для того, чтобы НЕ отображать лишние экземпляры книг


# Можно сделать проще через декоратор @register, который сразу зарегистрирует класс и модель
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # display_genre - это ф-я для отображения жанра книги
    # так как Django не позволяет напрямую поместить названия жанра из-за ManyToManyField
    list_display = ('title', 'author', 'display_genre')
    # Добавляет BookInstance информацию в подробное описание Book
    inlines = [BookInstanceInline] 


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
    list_display = ('book', 'status', 'due_back', 'id')
