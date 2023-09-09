import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import Label, Entry, Button, Frame, Text, messagebox

# Dicionário para armazenar ações já consultadas e sua formatação
acoes_consultadas = {}

# Função para obter os valores das ações ao pressionar o botão "Consultar"
def obter_valores_acoes():
    global acoes_consultadas  # Utilizamos o dicionário global

    # Obtém o texto da entrada, converte para maiúsculas e divide em ações separadas por espaços
    acoes = entrada_acoes.get().upper().split()
    
    valores_encontrados = False  # Flag para indicar se pelo menos um valor foi encontrado
    
    for acao in acoes:
        if acao in acoes_consultadas:
            # Se a ação já foi consultada, defina a cor de fundo como amarela
            acoes_consultadas[acao] = "yellow"
            resultados.tag_config(acao, background=acoes_consultadas[acao])
            valores_encontrados = True
            resultados.bind("<ButtonRelease-1>", remover_cor_de_fundo)
            continue
        
        # Constrói a URL de pesquisa no Google para a ação
        url = f'https://www.google.com/search?q={acao}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Seleciona os elementos HTML que contêm os valores das ações
        valor_elements = soup.select('.BNeawe.iBp4i.AP7Wnd')

        if len(valor_elements) >= 2:
            # Obtém o valor da ação (geralmente o segundo elemento)
            valor = valor_elements[1].text.split()[0]
            resultados_text = f'Valor da ação {acao}: R${valor}\n'
            valores_encontrados = True  # Indica que pelo menos um valor foi encontrado
            
            # Adiciona a ação consultada ao dicionário com a formatação de negrito
            acoes_consultadas[acao] = "bold"
        else:
            valores_encontrados = True
            # Exibe uma mensagem de erro se os dados não foram encontrados
            messagebox.showerror("ERRO", f'Não foi possível encontrar dados para "{acao}"\n')
            continue  
        
        # Habilita a edição do widget de texto para adicionar resultados
        resultados.config(state=tk.NORMAL)
        resultados.insert(tk.END, resultados_text)
        
        # Calcula o índice de início e término da ação no widget de texto
        start_index = resultados.search(acao, "1.0", tk.END)
        end_index = f"{start_index}+{len(acao)}c"
        
        # Aplica a formatação de negrito ao nome da ação
        resultados.tag_add(acao, start_index, end_index)
        resultados.tag_config(acao, font=("TkDefaultFont", 10, acoes_consultadas[acao]))
        
        # Desabilita a edição do widget de texto novamente
        resultados.config(state=tk.DISABLED)
        
    # Exibe o widget de texto apenas se pelo menos um valor for encontrado
    if valores_encontrados:
        resultados.pack()
        # Limpa o conteúdo da entrada após encontrar as ações
        entrada_acoes.delete(0, tk.END)
    else:
        # Exibe uma mensagem se nenhum valor for encontrado
        messagebox.showinfo("Nenhum valor encontrado", "Nenhum valor de ação foi encontrado.")

# Função para remover a cor de fundo das ações destacadas ao clicar nelas
def remover_cor_de_fundo(event):
    widget = event.widget
    index = widget.index(tk.CURRENT)
    tag_names = widget.tag_names(index)
    for tag_name in tag_names:
        if tag_name in acoes_consultadas:
            widget.tag_config(tag_name, background="")  # Remove a cor de fundo

# Cria uma instância da janela principal do aplicativo
app = tk.Tk()
app.title('Consultar Valores das Ações')

# Cria um frame para organizar os elementos da interface
frame = tk.Frame(app)
frame.pack(padx=20, pady=20)

# Label para instruções
Label(frame, text='Digite as ações (separadas por espaços):').pack()

# Campo de entrada de texto para inserir as ações
entrada_acoes = Entry(frame, width=30)
entrada_acoes.pack()

# Botão para acionar a consulta
btn_consultar = Button(frame, text='Consultar', command=obter_valores_acoes)
btn_consultar.pack()

# Widget de texto para exibir os resultados (inicialmente desabilitado)
resultados = Text(frame, width=40, height=10, state=tk.DISABLED)

app.mainloop()
