from django import forms
from django.core.exceptions import ValidationError
from .models import *



class EntradaForm(forms.ModelForm):
	class Meta:
		model =DatoEntrada

		fields=[
			'horas',
			'des',
			
			
		]

		labels={
			'horas': 'horas',
			'des':'Descripcion',
			
		}


		widgets={
			'horas': forms.NumberInput(attrs={'class':'form-control'}),
			'des':forms.TextInput(attrs={'class':'form-control'}),
			
		}

	class EmpleadoForm(forms.ModelForm):
		class Meta:
			model = empleado
			fields = '__all__'
