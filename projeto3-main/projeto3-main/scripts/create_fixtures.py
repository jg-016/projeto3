import os
import sys
import django

# Ensure project root is on sys.path when running from scripts/ folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto3.settings')
django.setup()

from loja.models import Fabricante, Categoria, Produto

f1, _ = Fabricante.objects.get_or_create(fabricante='Dell')
f2, _ = Fabricante.objects.get_or_create(fabricante='Microsoft')
c1, _ = Categoria.objects.get_or_create(categoria='Hardware')
c2, _ = Categoria.objects.get_or_create(categoria='Software')

Produto.objects.get_or_create(produto='Notebook Dell', defaults={'preco':2500.00,'destaque':True,'promocao':False,'categoria':c1,'fabricante':f1})
Produto.objects.get_or_create(produto='Windows License', defaults={'preco':199.00,'destaque':False,'promocao':True,'msgPromocao':'Promo!','categoria':c2,'fabricante':f2})

print('fixtures created')
