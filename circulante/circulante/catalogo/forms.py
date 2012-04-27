# coding: utf-8

from django.forms import ModelForm, ValidationError
from .isbn import validatedISBN10

from .models import Publicacao

class PublicacaoModelForm(ModelForm):
    class Meta:
        model = Publicacao
       
    def clean_id_padrao(self):
        dado=self.cleaned_data['id_padrao']
        if self.cleaned_data['tipo'] == 'livro':
            isbn = validatedISBN10(dado)
            if isbn:
                dado=isbn # para salvar sem hifens pois o validatedISBN10 os remove.
            else:
                msg= u'Para livros o id_padrao deve ser um ISBN válido.'
                raise ValidationError(msg)
        return dado
        
