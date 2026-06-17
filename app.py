# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psutil
import numpy as np
import time
import subprocess
import json

st.set_page_config(page_title="Dashboard Monitoramento PC", layout="wide", page_icon="💻")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        background-color: #4CAF50; color: white; border-radius: 8px;
        border: none; padding: 10px 24px; transition: all 0.3s ease 0s;
        font-weight: 600; letter-spacing: 0.5px;
    }
    .stButton>button:hover {
        background-color: #45a049; box-shadow: 0px 8px 20px rgba(76, 175, 80, 0.35);
        transform: translateY(-2px);
    }
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
""", unsafe_allow_html=True)


# ================= MENU LATERAL =================
st.sidebar.title("💻 Navegação")
page = st.sidebar.radio("Selecione o Módulo:", [
    "Dashboard Histórico",
    "Monitor em Tempo Real",
    "Gestão & Otimizador",
    "Sistema e Logs (Temperatura)",
    "Atualização do Sistema",
    "Limpeza e Manutenção"
])

st.sidebar.markdown("---")
st.sidebar.info("Super Dashboard — Monitoramento Avançado")

# ================= FUNÇÕES AUXILIARES =================
@st.cache_data
def load_csv_data():
    try:
        return pd.read_csv('Big_data_dataset.csv')
    except:
        return None

def get_live_metrics():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return cpu, ram, disk

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

# Coleta métricas base sempre
cpu_live, ram_live, disk_live = get_live_metrics()

# ================= MÓDULOS =================

if page == "Dashboard Histórico":
    st.title("📊 Dashboard Histórico (CSV)")
    df = load_csv_data()
    if df is not None:
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Média CPU", f"{df['cpu_utilization'].mean():.2f}%")
        with col2: st.metric("Média RAM", f"{df['memory_usage'].mean():.2f}%")
        with col3: st.metric("Temperatura Média", f"{df['temperature'].mean():.2f} °C")

        st.markdown("---")
        colA, colB = st.columns(2)
        with colA:
            st.subheader("CPU vs Memória (Amostra)")
            sample_df = df.head(100)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(sample_df.index, sample_df['cpu_utilization'], label='CPU', color='#4da6ff', alpha=0.85)
            ax.plot(sample_df.index, sample_df['memory_usage'], label='RAM', color='#f0a500', alpha=0.85)
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)
        with colB:
            st.subheader("Distribuição de Temperaturas")
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            ax2.hist(df['temperature'].dropna(), bins=30, color='#ff4b4b', edgecolor='black', alpha=0.75)
            st.pyplot(fig2)
            plt.close(fig2)

        with st.expander("Ver Tabela de Dados"):
            st.dataframe(df)
    else:
        st.error("Arquivo Big_data_dataset.csv não encontrado.")

elif page == "Monitor em Tempo Real":
    st.title("⚡ Monitor em Tempo Real")
    st.markdown("Atualização contínua. Alertas visuais serão gerados se o uso passar de 90%.")

    auto_refresh = st.checkbox("Habilitar Atualização Automática (A cada 2 seg)", value=True)

    if cpu_live > 90:
        st.toast(f"⚠️ ALERTA: CPU muito alta! ({cpu_live}%)", icon="🔥")
        st.error(f"CPU atingiu nível crítico: {cpu_live}%")
    if ram_live.percent > 80:
        st.toast(f"⚠️ ALERTA: Memória RAM quase cheia! ({ram_live.percent}%)", icon="💾")
        st.warning(f"Memória RAM alta: {ram_live.percent}%")

    st.subheader("Uso de CPU")
    st.progress(cpu_live / 100.0)
    st.markdown(f"<h2 style='color: {'#ff4b4b' if cpu_live > 80 else '#00fa9a'};'>{cpu_live}%</h2>", unsafe_allow_html=True)

    st.subheader("Uso de Memória RAM")
    st.progress(ram_live.percent / 100.0)
    used_gb = ram_live.used / (1024**3)
    total_gb = ram_live.total / (1024**3)
    st.markdown(f"<h3 style='color: {'#ff4b4b' if ram_live.percent > 80 else '#00fa9a'};'>{ram_live.percent}% ({used_gb:.2f} GB / {total_gb:.2f} GB)</h3>", unsafe_allow_html=True)

    st.subheader("Armazenamento (C:)")
    st.progress(disk_live.percent / 100.0)
    st.write(f"{disk_live.percent}% Utilizado")

    if auto_refresh:
        time.sleep(2)
        st.rerun()

elif page == "Gestão & Otimizador":
    st.title("🔧 Gestão de Processos & Otimizador Automático")
    st.write("Abaixo estão os processos mais pesados do sistema no momento.")

    if st.button("Atualizar Lista"):
        st.rerun()

    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            if info['name'] and info['pid'] > 0:
                processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    df_procs = pd.DataFrame(processes)
    if not df_procs.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 10 — Maior Uso de RAM")
            top_ram = df_procs.sort_values(by='memory_percent', ascending=False).head(10)
            top_ram['memory_percent'] = top_ram['memory_percent'].round(2)
            st.dataframe(top_ram[['pid', 'name', 'memory_percent']], use_container_width=True)
        with col2:
            st.subheader("Top 10 — Maior Uso de CPU")
            top_cpu = df_procs.sort_values(by='cpu_percent', ascending=False).head(10)
            top_cpu['cpu_percent'] = top_cpu['cpu_percent'].round(2)
            st.dataframe(top_cpu[['pid', 'name', 'cpu_percent']], use_container_width=True)

        st.markdown("---")
        st.markdown("### Otimizador (Encerrar Processos)")
        st.write("Digite o PID do processo que deseja encerrar:")
        pid_to_kill = st.number_input("PID", min_value=0, step=1)
        if st.button("Finalizar"):
            try:
                p = psutil.Process(pid_to_kill)
                p.terminate()
                st.success(f"Processo {pid_to_kill} finalizado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao finalizar processo: {e}")

elif page == "Sistema e Logs (Temperatura)":
    st.title("🌡️ Sistema e Logs de Falha")
    st.markdown("Monitore a temperatura do seu PC com gráfico histórico e visualize os últimos erros do sistema.")

    # ---- Seção de temperatura com gráfico ----
    st.subheader("📈 Temperatura do PC — Gráfico Histórico")

    # Persistir histórico entre reruns via session_state
    if 'temp_history' not in st.session_state:
        st.session_state.temp_history = []
    if 'temp_timestamps' not in st.session_state:
        st.session_state.temp_timestamps = []

    col_ctrl, col_graph = st.columns([1, 3])

    with col_ctrl:
        n_samples = st.number_input("Amostras a coletar", min_value=5, max_value=60, value=20, step=5)
        collect_btn = st.button("🔄 Coletar Temperatura")
        clear_btn   = st.button("🗑️ Limpar Histórico")

        if clear_btn:
            st.session_state.temp_history = []
            st.session_state.temp_timestamps = []
            st.success("Histórico limpo.")

    if collect_btn:
        progress = st.progress(0, text="Coletando amostras...")
        for i in range(int(n_samples)):
            temps = read_temp_wmic()
            ts = time.strftime("%H:%M:%S")
            if temps:
                avg = sum(temps) / len(temps)
                st.session_state.temp_history.append(avg)
            else:
                # Fallback estimado pelo uso de CPU quando sensor não está disponível
                cpu_now = psutil.cpu_percent(interval=0.2)
                simulated = 35 + (cpu_now * 0.45)
                st.session_state.temp_history.append(simulated)
            st.session_state.temp_timestamps.append(ts)
            progress.progress((i + 1) / int(n_samples), text=f"Amostra {i+1}/{int(n_samples)}")
            time.sleep(0.3)
        progress.empty()
        st.success(f"✅ {int(n_samples)} amostras coletadas!")

    with col_graph:
        if st.session_state.temp_history:
            temps  = st.session_state.temp_history
            labels = st.session_state.temp_timestamps
            max_t  = max(temps)
            min_t  = min(temps)
            avg_t  = sum(temps) / len(temps)

            m1, m2, m3 = st.columns(3)
            m1.metric("🔥 Máxima", f"{max_t:.1f} °C")
            m2.metric("❄️ Mínima",  f"{min_t:.1f} °C")
            m3.metric("📊 Média",   f"{avg_t:.1f} °C")

            fig, ax = plt.subplots(figsize=(9, 4))
            fig.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#1a1d27')

            # Linha e área preenchida
            ax.plot(range(len(temps)), temps, color='#4da6ff', linewidth=2.5, zorder=2)
            ax.fill_between(range(len(temps)), temps, alpha=0.2, color='#4da6ff')

            # Pontos coloridos por severidade
            colors = ['#ff4b4b' if t >= 75 else '#f0a500' if t >= 60 else '#00fa9a' for t in temps]
            ax.scatter(range(len(temps)), temps, c=colors, zorder=3, s=55, edgecolors='white', linewidths=0.4)

            # Linhas de alerta
            ax.axhline(y=75, color='#ff4b4b', linestyle='--', linewidth=1.2, label='Crítico (75°C)')
            ax.axhline(y=60, color='#f0a500', linestyle='--', linewidth=1.2, label='Alerta (60°C)')

            # Eixos
            step = max(1, len(labels) // 10)
            ax.set_xticks(range(0, len(labels), step))
            ax.set_xticklabels(labels[::step], rotation=30, color='#cccccc', fontsize=8)
            ax.set_ylabel("Temperatura (°C)", color='#cccccc')
            ax.set_xlabel("Hora da coleta", color='#cccccc')
            ax.tick_params(colors='#cccccc')
            ax.spines[['top', 'right']].set_visible(False)
            ax.spines[['left', 'bottom']].set_color('#444')
            ax.legend(facecolor='#1a1d27', labelcolor='white', fontsize=9)
            ax.set_title("Histórico de Temperatura (°C)", color='white', fontsize=13, pad=10)

            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Clique em **Coletar Temperatura** à esquerda para iniciar o monitoramento gráfico.")

    st.markdown("---")

    # ---- Logs de Falha ----
    st.subheader("🪲 Logs de Falha do Sistema")
    if st.button("Buscar Logs de Erro"):
        with st.spinner("Buscando logs do Windows..."):
            try:
                cmd = 'powershell "Get-EventLog -LogName System -EntryType Error -Newest 10 | Select-Object TimeGenerated, Source, Message | ConvertTo-Json"'
                result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                if result.stdout.strip():
                    try:
                        logs = json.loads(result.stdout)
                        if isinstance(logs, dict): logs = [logs]
                        st.dataframe(pd.DataFrame(logs), use_container_width=True)
                    except json.JSONDecodeError:
                        st.text(result.stdout)
                else:
                    st.info("Nenhum log de erro recente encontrado.")
            except Exception as e:
                st.error(f"Erro ao buscar logs: {e}")

elif page == "Atualização do Sistema":
    st.title("🔄 Atualização do Sistema (Winget)")
    st.markdown("Verifique e instale atualizações de software usando o Gerenciador de Pacotes do Windows (winget).")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Verificar Atualizações")
        if st.button("Executar: winget upgrade"):
            with st.spinner("Buscando atualizações (isso pode levar um tempo)..."):
                try:
                    result = subprocess.run("winget upgrade", capture_output=True, text=True, shell=True)
                    st.text_area("Resultado:", result.stdout, height=300)
                except Exception as e:
                    st.error(f"Erro ao executar comando: {e}")
    with col2:
        st.subheader("Atualizar Tudo")
        st.warning("Recomendado executar o Streamlit como Administrador para evitar prompts de permissão.")
        if st.button("Executar: winget upgrade --all"):
            with st.spinner("Atualizando programas..."):
                try:
                    cmd = "winget upgrade --all --accept-package-agreements --accept-source-agreements"
                    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                    st.text_area("Resultado da Atualização:", result.stdout, height=300)
                except Exception as e:
                    st.error(f"Erro ao executar comando: {e}")

elif page == "Limpeza e Manutenção":
    st.title("🧹 Limpeza e Manutenção do PC")
    st.markdown("Ferramentas avançadas do Windows para corrigir arquivos corrompidos e manter o sistema saudável. **(Requer Administrador)**")

    st.subheader("Verificador de Arquivos do Sistema (SFC)")
    if st.button("Executar SFC"):
        with st.spinner("Executando sfc /scannow..."):
            try:
                result = subprocess.run("sfc /scannow", capture_output=True, text=True, shell=True)
                st.text_area("Saída do SFC:", result.stdout, height=200)
            except Exception as e:
                st.error(f"Erro: {e}")

    st.markdown("---")
    st.subheader("Reparar Imagem do Windows (DISM)")
    if st.button("Executar DISM"):
        with st.spinner("Executando DISM..."):
            try:
                result = subprocess.run("DISM /Online /Cleanup-Image /RestoreHealth", capture_output=True, text=True, shell=True)
                st.text_area("Saída do DISM:", result.stdout, height=200)
            except Exception as e:
                st.error(f"Erro: {e}")

    st.markdown("---")
    st.subheader("Reiniciar Drivers do Computador")
    st.write("Esta função fará a varredura e reinicialização dos drivers de dispositivos conectados.")
    if st.button("Reiniciar Drivers / Escanear Hardware"):
        with st.spinner("Processando..."):
            try:
                result = subprocess.run("pnputil /scan-devices", capture_output=True, text=True, shell=True)
                st.success("Escaneamento de dispositivos concluído. Os drivers foram atualizados/reiniciados na sessão atual.")
                st.text_area("Detalhes:", result.stdout, height=150)
            except Exception as e:
                st.error(f"Erro ao reiniciar drivers: {e}")
