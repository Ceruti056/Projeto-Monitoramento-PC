#Projeto-Monitoramento-PC

Funcionalidades 🚀
1. Navegação Lateral (Menu)
    Agora a interface possui uma barra lateral contendo os 4 módulos do sistema, permitindo transitar entre os diferentes "apps" da plataforma sem sair da página inicial.

2. Monitor em Tempo Real
    Utiliza a biblioteca psutil para consultar dados reais do seu hardware.
    Exibe métricas de uso de CPU, RAM e Disco C: com barras de progresso (estilo htop).
    A página se atualiza sozinha a cada 2 segundos.
    Cores Dinâmicas: Valores ficam vermelhos ao passarem de 80%.
    Alertas Virtuais (Toasts): Exibe balões na tela e blocos de alerta caso a CPU ou Memória passem de certos limites (ex: > 90%).

3. Gestão e Otimizador de Processos
    Exibe o "Top 10" de processos que mais estão usando Memória RAM e CPU.
    Implementado um Otimizador Automático (Manual seguro):
    Você pode digitar o PID de qualquer processo exibido na tabela.
    Ao clicar no botão Finalizar, o aplicativo encerrará a tarefa imediatamente e liberará o recurso.

4. Modo Gamer 🎮
    O app verifica secretamente os processos em execução em busca de grandes jogos (steam.exe, cs2.exe, valorant.exe, Minecraft.exe, gtav.exe, etc.).
    Exibe o impacto que aquele jogo está causando no hardware agora.
    Informa uma taxa de FPS Estimada se baseando no quão ocioso o seu computador está enquanto o jogo roda. 

5. Bibliotecas Utilizadas:
    • Streamlit: Cria a interface inteira em Python de forma simples e rapida.
    • psutil: Captura informacoes internas do hardware com maxima precisao.
    • Pandas & Matplotlib: Manipulam e plotam dados brutos transformando-os em informacoes visuais legiveis.
#
