# Dashboard de Monitoramento de PC - Monitoramento Avançado

O **Dashboard de Monitoramento de PC** é uma aplicação interativa desenvolvida em Python (via Streamlit) voltada para o monitoramento avançado de hardware, gestão de processos e visualização de métricas de desempenho. A plataforma conta com um menu lateral que permite transitar entre seis módulos principais.

Abaixo, detalhamos cada módulo de acordo com o código presente no `app.py`, focando nas **funcionalidades técnicas**, **exemplos de uso no código** e no **impacto social** de cada uma dessas inovações.

## Impacto Social na Sociedade
O sistema contribui para a democratização do acesso à informação técnica e para o empoderamento digital dos usuários, permitindo que pessoas leigas monitorem facilmente a saúde e o desempenho de seus computadores por meio de interfaces simples e intuitivas. Isso ajuda a prevenir falhas, evitar a perda de dados importantes e otimizar o uso dos recursos do equipamento. Além disso, ao possibilitar a identificação e eliminação de processos desnecessários, prolonga a vida útil de computadores e servidores, reduzindo o consumo de energia elétrica, a geração de lixo eletrônico (e-waste) e os custos com substituição de hardware. Dessa forma, a solução promove a inclusão digital, beneficia ambientes educacionais e famílias de baixa renda, e incentiva práticas de TI mais sustentáveis nos setores corporativo e acadêmico.

---

## Funcionalidades Técnicas e Impacto

### 1. Dashboard Histórico
- **Funcionalidade Técnica:** Este módulo utiliza a biblioteca `pandas` para ler e carregar um grande volume de dados (`Big_data_dataset.csv`). Em seguida, emprega o `matplotlib` para plotar gráficos visuais complexos, processando métricas históricas para encontrar as médias exatas do comportamento da máquina.
- **Exemplo de Uso no `app.py`:** A função `load_csv_data()` faz a ingestão segura do arquivo CSV. Com os dados carregados, o sistema exibe cartões numéricos (`st.metric`) com a média exata da CPU, RAM e Temperatura. Além disso, plota um gráfico de linha comparando o uso de "CPU vs Memória" de uma amostra de 100 registros e gera um histograma com a "Distribuição de Temperaturas".
  ```python
  def load_csv_data():
      try:
          return pd.read_csv('Big_data_dataset.csv')
      except:
          return None

  # Exemplo de exibição em tela:
  with col1: st.metric("Média CPU", f"{df['cpu_utilization'].mean():.2f}%")
  ```

### 2. Monitor em Tempo Real
- **Funcionalidade Técnica:** Faz uso intensivo da biblioteca `psutil` para extrair dados do hardware no exato segundo em que estão ocorrendo (CPU, Memória RAM Virtual e capacidade do Disco C:). A interface se atualiza automaticamente em um loop através de comandos como `time.sleep(2)` e `st.rerun()`. A plataforma também reage dinamicamente mudando cores para vermelho ou ativando pop-ups caso os limites de uso passem dos 80% ou 90%.
- **Exemplo de Uso no `app.py`:** A função `get_live_metrics()` varre o percentual de uso num intervalo de 0.1s. A interface exibe barras de progresso (`st.progress`). Se a CPU passar de 90%, o código dispara instantaneamente alertas visuais via `st.toast("⚠️ ALERTA: CPU muito alta!")` e exibe mensagens de erro em tela para capturar a atenção imediata.
  ```python
  def get_live_metrics():
      cpu = psutil.cpu_percent(interval=0.1)
      ram = psutil.virtual_memory()
      disk = psutil.disk_usage('/')
      return cpu, ram, disk

  # Alertas dinâmicos:
  if cpu_live > 90:
      st.toast(f"⚠️ ALERTA: CPU muito alta! ({cpu_live}%)", icon="🔥")
      st.error(f"CPU atingiu nível crítico: {cpu_live}%")
  ```

### 3. Gestão & Otimizador de Processos
- **Funcionalidade Técnica:** Inspeciona todo o sistema operacional mapeando as tarefas que rodam no fundo através da função `psutil.process_iter()`. Ele agrupa os dados de PID (identificação do processo), nome, consumo de memória e CPU. Esses dados são organizados pelo `pandas` em ordem decrescente, permitindo ao usuário encontrar facilmente os "ralos" de desempenho e encerrá-los seletivamente.
- **Exemplo de Uso no `app.py`:** A tela se divide em duas colunas exibindo o "Top 10 - Maior Uso de RAM" e o "Top 10 - Maior Uso de CPU". Na parte inferior, há um otimizador seguro onde o usuário digita o número da tarefa (PID) e, ao clicar em "Finalizar", o código aciona a função de nível de sistema `psutil.Process(pid_to_kill).terminate()` para abater o processo e liberar recursos da máquina.
  ```python
  st.write("Digite o PID do processo que deseja encerrar:")
  pid_to_kill = st.number_input("PID", min_value=0, step=1)
  
  if st.button("Finalizar"):
      try:
          p = psutil.Process(pid_to_kill)
          p.terminate()
          st.success(f"Processo {pid_to_kill} finalizado com sucesso!")
      except Exception as e:
          st.error(f"Erro ao finalizar processo: {e}")
  ```

### 4. Sistema e Logs (Temperatura) 🌡️
- **Funcionalidade Técnica:** Este módulo é dividido em duas seções. A primeira realiza a leitura da temperatura do processador consultando o sensor térmico do Windows via `wmic` (Windows Management Instrumentation Command-line). Os valores brutos retornados em décimos de Kelvin são convertidos para graus Celsius pela fórmula `(valor / 10) - 273.15`. As temperaturas coletadas ao longo do tempo são armazenadas no `st.session_state` do Streamlit para que o histórico não se perca entre atualizações de tela. A segunda seção busca os 10 erros mais recentes registrados no "Visualizador de Eventos" do Windows usando um comando `powershell` com `Get-EventLog`, retornando os dados em formato JSON para exibição em tabela. Caso o sensor físico não esteja disponível (o que exige execução como Administrador), o sistema aplica um **fallback inteligente**, estimando a temperatura com base no percentual de uso da CPU em tempo real.
- **Exemplo de Uso no `app.py`:** A função `read_temp_wmic()` executa o comando de sistema e parseia a saída. O botão "Coletar Temperatura" aciona um loop que coleta N amostras (configuráveis de 5 a 60), exibindo uma barra de progresso a cada leitura. Ao final, o `matplotlib` plota um gráfico estilizado com pontos coloridos por severidade (verde, amarelo, vermelho) e linhas de alerta tracejadas nos limites de 60°C e 75°C.
  ```python
  def read_temp_wmic():
      """Lê a temperatura via WMIC e retorna lista de °C ou None."""
      try:
          cmd = 'wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature'
          r = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=5)
          lines = [l.strip() for l in r.stdout.strip().splitlines() if l.strip()]
          values = []
          for l in lines[1:]:
              if l.isdigit():
                  values.append((int(l) / 10.0) - 273.15)
          return values if values else None
      except Exception:
          return None

  # Linhas de alerta no gráfico:
  ax.axhline(y=75, color='#ff4b4b', linestyle='--', linewidth=1.2, label='Crítico (75°C)')
  ax.axhline(y=60, color='#f0a500', linestyle='--', linewidth=1.2, label='Alerta (60°C)')

  # Busca de logs de erro via PowerShell:
  cmd = 'powershell "Get-EventLog -LogName System -EntryType Error -Newest 10 | Select-Object TimeGenerated, Source, Message | ConvertTo-Json"'
  result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
  ```

### 5. Atualização do Sistema 🔄
- **Funcionalidade Técnica:** Integra-se diretamente ao **winget** (Gerenciador de Pacotes do Windows), a ferramenta oficial da Microsoft para instalação e atualização de softwares via linha de comando. O módulo disponibiliza dois botões de ação: o primeiro executa `winget upgrade` para listar todos os programas com atualizações pendentes, e o segundo dispara `winget upgrade --all` com as flags `--accept-package-agreements` e `--accept-source-agreements` para realizar a atualização silenciosa e em lote de todos os softwares instalados, sem precisar confirmar cada um manualmente. Toda a saída do terminal é capturada via `subprocess.run(capture_output=True)` e exibida em tempo real numa caixa de texto rolável.
- **Exemplo de Uso no `app.py`:** Ao clicar no botão, um `st.spinner` indica que o processo está em andamento (pois pode demorar alguns minutos). O resultado completo da execução do `winget` é exibido num `st.text_area` de altura generosa, permitindo ao usuário ler quais programas foram atualizados e verificar possíveis erros.
  ```python
  if st.button("Executar: winget upgrade --all"):
      with st.spinner("Atualizando programas..."):
          try:
              cmd = "winget upgrade --all --accept-package-agreements --accept-source-agreements"
              result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
              st.text_area("Resultado da Atualização:", result.stdout, height=300)
          except Exception as e:
              st.error(f"Erro ao executar comando: {e}")
  ```

### 6. Limpeza e Manutenção 🧹
- **Funcionalidade Técnica:** Agrupa três ferramentas nativas e poderosas do Windows, todas acionadas via `subprocess.run()` com os comandos de sistema adequados. A primeira executa o **SFC** (`sfc /scannow`), que varre todos os arquivos protegidos do sistema em busca de corrupção e os restaura automaticamente a partir de uma cópia armazenada em cache. A segunda aciona o **DISM** (`DISM /Online /Cleanup-Image /RestoreHealth`), que repara a própria imagem do Windows conectando-se ao Windows Update para baixar os componentes corretos e substituir arquivos danificados em um nível mais profundo que o SFC. A terceira função executa `pnputil /scan-devices`, que instrui o gerenciador Plug and Play do Windows a varrer todos os barramentos de hardware reconhecendo dispositivos novos, reiniciando drivers com falha e atualizando as associações de driver sem precisar reiniciar o computador.
- **Exemplo de Uso no `app.py`:** Cada ferramenta possui seu próprio bloco de botão e `st.spinner`. Após a execução — que pode levar vários minutos para o SFC e DISM — a saída completa do terminal é capturada e exibida num `st.text_area`, permitindo ao usuário auditar o que foi corrigido. Um aviso (`st.markdown` com **Requer Administrador**) orienta o usuário sobre a necessidade de elevar os privilégios para que os comandos funcionem corretamente.
  ```python
  # SFC:
  if st.button("Executar SFC"):
      with st.spinner("Executando sfc /scannow..."):
          result = subprocess.run("sfc /scannow", capture_output=True, text=True, shell=True)
          st.text_area("Saída do SFC:", result.stdout, height=200)

  # DISM:
  if st.button("Executar DISM"):
      with st.spinner("Executando DISM..."):
          result = subprocess.run("DISM /Online /Cleanup-Image /RestoreHealth", capture_output=True, text=True, shell=True)
          st.text_area("Saída do DISM:", result.stdout, height=200)

  # Reinicialização de Drivers:
  if st.button("Reiniciar Drivers / Escanear Hardware"):
      with st.spinner("Processando..."):
          result = subprocess.run("pnputil /scan-devices", capture_output=True, text=True, shell=True)
          st.success("Escaneamento de dispositivos concluído.")
          st.text_area("Detalhes:", result.stdout, height=150)
  ```
---

## Principais Tecnologias Utilizadas no `app.py`
- **Streamlit (`import streamlit as st`):** Framework poderoso responsável pela construção de toda a interface visual amigável e reativa de forma nativa em Python.
- **PSUtil (`import psutil`):** Biblioteca essencial e de baixo nível usada para interfacear os chamados do sistema operacional, colhendo métricas reais das peças de hardware (CPU, RAM, Disco e Processos).
- **Pandas e Matplotlib (`import pandas`, `import matplotlib.pyplot`):** Dupla utilizada para ingestão, manipulação, limpeza e visualização gráfica de dezenas de milhares de logs de desempenho, além de plotar o gráfico histórico de temperatura com alertas visuais dinâmicos.
- **Subprocess (`import subprocess`):** Módulo nativo do Python que permite a execução de comandos do sistema operacional diretamente a partir do código, sendo o motor por trás dos módulos de Temperatura (WMIC), Logs (PowerShell), Atualização (winget), Manutenção (SFC, DISM) e Reinicialização de Drivers (pnputil).
- **JSON (`import json`):** Utilizado para parsear a saída estruturada dos logs de erro do sistema retornados pelo PowerShell, convertendo-os em um DataFrame exibível em tabela.
- **NumPy e Time (`import numpy`, `import time`):** Utilizados para processamento numérico e pausas sistemáticas (`sleep`) essenciais no loop contínuo do Monitoramento em Tempo Real e na coleta sequencial de amostras de temperatura.
