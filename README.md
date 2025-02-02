## Resumo das Funcionalidades da Aplicação "PopupTeclas"
A aplicação "PopupTeclas" é uma ferramenta que visa facilitar a manipulação e o gerenciamento de textos copiados para a área de transferência (clipboard) do sistema, oferecendo uma interface gráfica interativa e funcionalidades extras. Em resumo, suas principais funcionalidades são:
**1. Captura e Exibição de Texto:**
- Monitora a área de transferência (clipboard) e detecta quando um texto é copiado usando `Ctrl+C`.
- Abre um popup (janela flutuante) exibindo o texto copiado, pronto para edição.
- Permite que o usuário visualize e edite o texto em um widget de texto com rolagem (ScrolledText).
**2. Edição e Formatação de Texto:**
- Permite a edição direta do texto no popup.
- Suporta formatação básica de texto, como quebras de linha (newlines).
**3. Histórico de Textos Copiados:**
- Armazena os últimos 4 textos copiados em um histórico.
- Permite navegar pelo histórico usando as setas "←" e "→" (ou as teclas de seta do teclado).
- Atualiza o histórico em tempo real enquanto o usuário edita o texto no popup.
**4. Ações com o Texto:**
- **Salvar:** Permite salvar o texto editado em um arquivo `.txt` no local desejado pelo usuário.
- **Enviar:** Cola o texto editado no campo ativo do sistema utilizando `Ctrl+V`, simulando a ação de colar, também utilizando a área de transferência.
**5. Interface Personalizável:**
- Janela com bordas 3D, cores personalizadas e botões com design limpo.
- Possui scroll para textos maiores.
- Permite arrastar o popup para reposicionar na tela.
- Adapta a altura do popup com base no tamanho do texto para melhor visualização.
**6. Atalhos de Teclado:**
- `ESC`: Fecha o popup.
- `Ctrl+C`: Captura o texto copiado e abre o popup.
- `←` e `→`: Navega pelo histórico de textos.
- `↑`: Envia o texto editado para o campo ativo.
- `↓`: Salva o texto editado.
**7. Tratamento de Texto:**
- Filtra o texto capturado, removendo linhas vazias, URLs, referências (como "fonte", "source"), etc.
**8. Design Responsivo:**
- O popup ajusta seu tamanho automaticamente de acordo com a quantidade de linhas do texto exibido.
- A janela é centralizada na tela ao ser aberta pela primeira vez.
-arraste com clique
