from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import *


def edit_and_delete_button(obj):
    edit_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.pk])
    delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])

    return format_html("""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-iBBXm8fW90+nuLcSKlbmrPcLa0OT92xO1BIsZ+ywDWZCvqsWgccV3gFoRBv0z+8dLJgyAHIhR35VZc2oM/gI1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        </head>
        <body>
            <a class="button" href="{}"><i class="fas fa-edit"></i></a>&nbsp;&nbsp;
            <a class="button" href="{}"><i class="fas fa-trash-alt"></i></a>
        </body>
        </html>""", edit_url, delete_url)


edit_and_delete_button.short_description = 'Action'


class article_admin(admin.ModelAdmin):
    list_display = ["id", "title", "body", "created_on", edit_and_delete_button]
    search_fields = ["title", "body"]
    actions = None
    list_display_links = None


class comment_admin(admin.ModelAdmin):
    list_display = ["id", "article", "text", "created_on", edit_and_delete_button]
    search_fields = ["text"]
    actions = None
    list_display_links = None


admin.site.register(Article, article_admin)
admin.site.register(Comment, comment_admin)

