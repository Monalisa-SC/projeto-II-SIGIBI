from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Aluno, Livro, Emprestimo
from .forms import AlunoForm, LivroForm  # Importe os formulários AlunoForm e LivroForm do mesmo arquivo
from .forms import RegistrarEmprestimoForm
from django.utils import timezone
from django.db.models import Sum


def index(request):
    total_alunos = Aluno.objects.count()
    total_livros = Livro.objects.aggregate(total=Sum('quantidade'))['total'] or 0
    total_emprestimos = Emprestimo.objects.filter(data_devolucao__isnull=True).count()

    context = {
        'total_alunos': total_alunos,
        'total_livros': total_livros,
        'total_emprestimos': total_emprestimos,
    }

    return render(request, 'index.html', context)

def lista_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, 'alunos/lista_alunos.html', {'alunos': alunos})

def cadastro_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno cadastrado com sucesso!')
            return redirect('lista_alunos')
        else:
            messages.error(request, 'Erro ao cadastrar aluno.')
    else:
        form = AlunoForm()
    return render(request, 'alunos/cadastro_aluno.html', {'form': form})

def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('lista_alunos')
        else:
            messages.error(request, 'Erro ao atualizar aluno.')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'alunos/editar_aluno.html', {'form': form, 'aluno': aluno})

def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso!')
        return redirect('lista_alunos')
    return render(request, 'alunos/excluir_aluno_confirm.html', {'aluno': aluno})

def lista_livros(request):
    livros = Livro.objects.all()
    return render(request, 'livros/lista_livros.html', {'livros': livros})

def cadastro_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)  # Use LivroForm
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro cadastrado com sucesso!')
            return redirect('lista_livros')
        else:
            messages.error(request, 'Erro ao cadastrar livro.')
    else:
        form = LivroForm()
    return render(request, 'livros/cadastro_livro.html', {'form': form})

def editar_livro(request, livro_id):
    """
    View para editar um livro existente.
    Args:
        request: O objeto HttpRequest.
        livro_id: O ID do livro a ser editado.
    Returns:
        Um HttpResponse que renderiza o template 'editar_livro.html' com o formulário,
        ou redireciona para a lista de livros após a edição bem-sucedida.
    """
    livro = get_object_or_404(Livro, pk=livro_id)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)  # Use LivroForm
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('lista_livros')
        else:
            messages.error(request, 'Erro ao atualizar livro.')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livros/editar_livro.html', {'form': form, 'livro': livro})

def excluir_livro(request, livro_id):
    """
    View para excluir um livro existente.
    Args:
        request: O objeto HttpRequest.
        livro_id: O ID do livro a ser excluído.
    Returns:
        Um HttpResponse que renderiza o template 'excluir_livro.html' para confirmação,
        ou redireciona para a lista de livros após a exclusão bem-sucedida.
    """
    livro = get_object_or_404(Livro, pk=livro_id)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso!')
        return redirect('lista_livros')
    return render(request, 'livros/excluir_livro.html', {'livro': livro})

def lista_emprestimos(request):
    alunos = Aluno.objects.all()
    livros = Livro.objects.all()
    emprestimos = Emprestimo.objects.filter(data_devolucao__isnull=True)

    context = {
        'alunos': alunos,
        'livros': livros,
        'emprestimos': emprestimos,
    }
    return render(request, 'emprestimos/lista_emprestimos.html', context)

def registrar_emprestimo(request):
    if request.method == 'POST':
        form = RegistrarEmprestimoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empréstimo registrado com sucesso!')
            return redirect('lista_emprestimos')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('lista_emprestimos')
    return redirect('lista_emprestimos')


def devolver_emprestimo(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id)
    if not emprestimo.data_devolucao:
        emprestimo.data_devolucao = timezone.now()
        emprestimo.save()
        
        livro = emprestimo.livro
        livro.quantidade += 1
        livro.disponivel = True
        livro.save()
        
        messages.success(request, 'Livro devolvido com sucesso!')
    else:
        messages.warning(request, 'Este empréstimo já foi devolvido.')
    return redirect('lista_emprestimos')

def lista_historico(request):
    emprestimos = Emprestimo.objects.all()
    return render(request, 'historico/lista_historico.html', {'emprestimos': emprestimos})

def autores(request):
    return render(request, 'autores.html')
