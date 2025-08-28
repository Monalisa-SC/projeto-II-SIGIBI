from django import forms
from .models import Aluno, Livro, Emprestimo
from django.utils import timezone

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'turma', 'matricula']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do aluno'}),
            'turma': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Turma'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}),
        }


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'ano', 'quantidade']  # Inclui o campo quantidade
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autor'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ano de Publicação'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),  # Widget para o campo quantidade
        }



class RegistrarEmprestimoForm(forms.Form):
    """
    Formulário para registrar um novo empréstimo de livro para um aluno.
    """
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        label="Aluno",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    livro = forms.ModelChoiceField(
        queryset=Livro.objects.filter(disponivel=True),
        label="Livro",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    data_devolucao = forms.DateField(
        label="Data de Devolução (Opcional)",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        help_text="Informe a data prevista para devolução do livro."
    )

    def clean_livro(self):
        """
        Valida se o livro selecionado está disponível para empréstimo.
        """
        livro = self.cleaned_data['livro']
        if not livro.disponivel:
            raise forms.ValidationError("Este livro não está disponível para empréstimo.")
        return livro

    def clean_data_devolucao(self):
        """
        Valida se a data de devolução é posterior à data de empréstimo.
        """
        data_devolucao = self.cleaned_data['data_devolucao']
        if data_devolucao and data_devolucao < timezone.now().date():
            raise forms.ValidationError("A data de devolução deve ser posterior à data atual.")
        return data_devolucao

    def save(self):
        """
        Cria um novo objeto Emprestimo com os dados validados do formulário.
        """
        aluno = self.cleaned_data['aluno']
        livro = self.cleaned_data['livro']
        data_devolucao = self.cleaned_data.get('data_devolucao')

        emprestimo = Emprestimo.objects.create(
            aluno=aluno,
            livro=livro,
            data_emprestimo=timezone.now().date(),
            data_devolucao=data_devolucao
        )
        livro.quantidade -= 1
        if livro.quantidade <= 0:
           livro.disponivel = False
        livro.save()
        return emprestimo
