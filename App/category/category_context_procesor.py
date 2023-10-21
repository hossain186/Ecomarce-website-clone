from .models import Category

def menu_links(requlest):

    links = Category.objects.all()

    return dict(links = links)