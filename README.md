# Super Dashboard PC - Monitoramento Avançado

O **Super Dashboard PC** é uma aplicação interativa desenvolvida em Python (via Streamlit) voltada para o monitoramento avançado de hardware, gestão de processos e visualização de métricas de desempenho. A plataforma conta com um menu lateral que permite transitar entre quatro módulos principais.

Abaixo, detalhamos cada módulo de acordo com o código presente no `app.py`, focando nas **funcionalidades técnicas**, **exemplos de uso no código** e no **impacto social** de cada uma dessas inovações.

---

## Funcionalidades Técnicas e Impacto

### 1. Dashboard Histórico
- **Funcionalidade Técnica:** Este módulo utiliza a biblioteca `pandas` para ler e carregar um grande volume de dados (`Big_data_dataset.csv`). Em seguida, emprega o `matplotlib` para plotar gráficos visuais complexos, processando métricas históricas para encontrar as médias exatas do comportamento da máquina.
- **Exemplo de Uso no `app.py`:** A função `load_csv_data()` faz a ingestão segura do arquivo CSV. Com os dados carregados, o sistema exibe cartões numéricos (`st.metric`) com a média exata da CPU, RAM e Temperatura. Além disso, plota um gráfico de linha comparando o uso de "CPU vs Memória" de uma amostra de 100 registros e gera um histograma com a "Distribuição de Temperaturas".
- **Impacto Social na Sociedade:** Ajuda profissionais de TI e pesquisadores a analisarem o comportamento de máquinas ao longo do tempo. Esse monitoramento contribui diretamente para a otimização de servidores e datacenters, o que reduz drasticamente o consumo desnecessário de energia elétrica e prolonga a vida útil dos equipamentos. Assim, minimiza-se a geração de lixo eletrônico (e-waste), promovendo uma TI mais verde e sustentável no mundo corporativo e acadêmico.

### 2. Monitor em Tempo Real
- **Funcionalidade Técnica:** Faz uso intensivo da biblioteca `psutil` para extrair dados do hardware no exato segundo em que estão ocorrendo (CPU, Memória RAM Virtual e capacidade do Disco C:). A interface se atualiza automaticamente em um loop através de comandos como `time.sleep(2)` e `st.rerun()`. A plataforma também reage dinamicamente mudando cores para vermelho ou ativando pop-ups caso os limites de uso passem dos 80% ou 90%.
- **Exemplo de Uso no `app.py`:** A função `get_live_metrics()` varre o percentual de uso num intervalo de 0.1s. A interface exibe barras de progresso (`st.progress`). Se a CPU passar de 90%, o código dispara instantaneamente alertas visuais via `st.toast("⚠️ ALERTA: CPU muito alta!")` e exibe mensagens de erro em tela para capturar a atenção imediata.
- **Impacto Social na Sociedade:** Democratiza o acesso à informação técnica. Essa funcionalidade permite que qualquer cidadão comum ou pessoa leiga compreenda a "saúde" de seu computador através de barras coloridas e alertas simples, sem precisar abrir terminais de comando complexos. Isso ajuda pessoas comuns a evitarem falhas de sistema que poderiam levar à perda irreparável de documentos importantes, fotos de família ou trabalhos escolares e acadêmicos.

### 3. Gestão & Otimizador de Processos
- **Funcionalidade Técnica:** Inspeciona todo o sistema operacional mapeando as tarefas que rodam no fundo através da função `psutil.process_iter()`. Ele agrupa os dados de PID (identificação do processo), nome, consumo de memória e CPU. Esses dados são organizados pelo `pandas` em ordem decrescente, permitindo ao usuário encontrar facilmente os "ralos" de desempenho e encerrá-los seletivamente.
- **Exemplo de Uso no `app.py`:** A tela se divide em duas colunas exibindo o "Top 10 - Maior Uso de RAM" e o "Top 10 - Maior Uso de CPU". Na parte inferior, há um otimizador seguro onde o usuário digita o número da tarefa (PID) e, ao clicar em "Finalizar", o código aciona a função de nível de sistema `psutil.Process(pid_to_kill).terminate()` para abater o processo e liberar recursos da máquina.
- **Impacto Social na Sociedade:** Empodera digitalmente o cidadão ao devolver-lhe o controle sobre a performance do seu próprio computador. Em ambientes educacionais ou famílias de baixa renda, otimizar recursos eliminando processos inúteis frequentemente significa dar uma sobrevida digna a computadores mais antigos. O app atua como um facilitador da inclusão digital, aliviando a urgência de famílias ou pequenas escolas gastarem dinheiro na compra de hardware novo e mais potente.

### 4. Modo Gamer 🎮
- **Funcionalidade Técnica:** Varre passivamente as tarefas em segundo plano buscando padrões em uma lista de strings conhecida (`game_list = ['steam.exe', 'csgo.exe', 'valorant.exe', ...]`). Ao identificar que o PC está processando jogos, o software entra em um estado de análise diferenciada de gargalo, cruzando a carga térmica, memória disponível e capacidade da CPU para inferir por regra matemática qual a entrega de frames provável.
- **Exemplo de Uso no `app.py`:** O aplicativo exibe uma mensagem de sucesso avisando qual jogo foi detectado ("Impacto atual no sistema..."). Em seguida, o código aplica uma lógica simples (se CPU < 60% e RAM < 70%, o `fps_est` = 144) para projetar uma estimativa de quadros por segundo ("FPS Estimado"), devolvendo a informação para o jogador através de um banner de informação.
- **Impacto Social na Sociedade:** Os jogos eletrônicos representam, hoje, a maior e mais influente plataforma de socialização, criatividade e desenvolvimento de habilidades cognitivas entre jovens em escala global. O "Modo Gamer" auxilia jovens gamers — especialmente os que operam em PCs mais modestos — a avaliarem rapidamente se a máquina tem margem para aguentar suas partidas, estimulando um ambiente virtual mais lúdico, engajador e nivelando as oportunidades no emergente cenário de entretenimento e e-sports.

---

## Principais Tecnologias Utilizadas no `app.py`
- **Streamlit (`import streamlit as st`):** Framework poderoso responsável pela construção de toda a interface visual amigável e reativa de forma nativa em Python.
- **PSUtil (`import psutil`):** Biblioteca essencial e de baixo nível usada para interfacear os chamados do sistema operacional, colhendo métricas reais das peças de hardware.
- **Pandas e Matplotlib (`import pandas`, `import matplotlib.pyplot`):** Dupla utilizada para ingestão, manipulação, limpeza e visualização gráfica de dezenas de milhares de logs de desempenho.
- **NumPy e Time (`import numpy`, `import time`):** Utilizados para processamento numérico e pausas sistemáticas (`sleep`) essenciais no loop contínuo do Monitoramento em Tempo Real.
