from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alunos/', views.lista_alunos, name='lista_alunos'),  # Corrigido para lista_alunos
    path('alunos/cadastro/', views.cadastro_aluno, name='cadastro_aluno'),  # URL para o formulário de cadastro
    path('alunos/editar/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    path('alunos/excluir/<int:aluno_id>/', views.excluir_aluno, name='excluir_aluno'),
    path('livros/', views.lista_livros, name='lista_livros'),  # Corrigido para lista_livros
    path('livros/cadastro/', views.cadastro_livro, name='cadastro_livro'),  # URL para o formulário de cadastro de livros
    path('livros/editar/<int:livro_id>/', views.editar_livro, name='editar_livro'),
    path('livros/excluir/<int:livro_id>/', views.excluir_livro, name='excluir_livro'),
    path('emprestimos/', views.lista_emprestimos, name='lista_emprestimos'),  # Corrigido para lista_emprestimos
    path('emprestimos/registrar/', views.registrar_emprestimo, name='registrar_emprestimo'),
    path('historico/', views.lista_historico, name='lista_historico'),  # Corrigido para lista_historico
    path('autores/', views.autores, name='autores'),
    path('emprestimos/devolver/<int:emprestimo_id>/', views.devolver_emprestimo, name='devolver_emprestimo'),
]