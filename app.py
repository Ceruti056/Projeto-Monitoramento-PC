import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psutil
import numpy as np
import time

st.set_page_config(page_title="Super Dashboard PC", layout="wide")



# ================= MENU LATERAL =================
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione o Módulo:", [
    "Dashboard Histórico", 
    "Monitor em Tempo Real", 
    "Gestão & Otimizador", 
    "Modo Gamer",
    "Modo HUD"
])

st.sidebar.markdown("---")
st.sidebar.info("Super Dashboard - Monitoramento Avançado")

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



# Coleta sempre no background silencioso quando roda a página
cpu_live, ram_live, disk_live = get_live_metrics()

# ================= MÓDULOS =================

if page == "Dashboard Histórico":
    st.title("Dashboard Histórico (CSV)")
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
            fig, ax = plt.subplots(figsize=(8,4))
            ax.plot(sample_df.index, sample_df['cpu_utilization'], label='CPU', color='blue', alpha=0.7)
            ax.plot(sample_df.index, sample_df['memory_usage'], label='RAM', color='orange', alpha=0.7)
            ax.legend()
            st.pyplot(fig)
        with colB:
            st.subheader("Distribuição de Temperaturas")
            fig2, ax2 = plt.subplots(figsize=(8,4))
            ax2.hist(df['temperature'].dropna(), bins=30, color='red', edgecolor='black', alpha=0.7)
            st.pyplot(fig2)
        
        with st.expander("Ver Tabela de Dados"):
            st.dataframe(df)
    else:
        st.error("Arquivo Big_data_dataset.csv não encontrado.")

elif page == "Monitor em Tempo Real":
    st.title("Monitor em Tempo Real")
    st.markdown("Atualização contínua. Alertas visuais serão gerados se o uso passar de 90%.")
    
    auto_refresh = st.checkbox("Habilitar Atualização Automática (A cada 2 seg)", value=True)
    
    # Alertas
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
    st.title("Gestão de Processos & Otimizador Automático")
    st.write("Abaixo estão os processos mais pesados do sistema no momento.")
    
    if st.button("Atualizar Lista"):
        st.rerun()
        
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            # Filtrar alguns dados nulos ou system idle
            if info['name'] and info['pid'] > 0:
                processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    df_procs = pd.DataFrame(processes)
    if not df_procs.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 - Maior Uso de RAM")
            top_ram = df_procs.sort_values(by='memory_percent', ascending=False).head(10)
            # Normalizar os valores de porcentagem
            top_ram['memory_percent'] = top_ram['memory_percent'].round(2)
            st.dataframe(top_ram[['pid', 'name', 'memory_percent']])
            
        with col2:
            st.subheader("Top 10 - Maior Uso de CPU")
            top_cpu = df_procs.sort_values(by='cpu_percent', ascending=False).head(10)
            top_cpu['cpu_percent'] = top_cpu['cpu_percent'].round(2)
            st.dataframe(top_cpu[['pid', 'name', 'cpu_percent']])
            
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

elif page == "Modo Gamer":
    st.title("🎮 Modo Gamer")
    st.write("Verificando se jogos populares estão em execução...")
    
    game_list = ['steam.exe', 'csgo.exe', 'cs2.exe', 'valorant.exe', 'League of Legends.exe', 'gtav.exe', 'r5apex.exe', 'Roblox.exe', 'Minecraft.exe']
    running_games = []
    
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in [g.lower() for g in game_list]:
                running_games.append(proc.info['name'])
        except:
            pass
            
    if running_games:
        st.success(f"Jogo(s) detectado(s): {', '.join(set(running_games))}")
        st.markdown("### Status do Sistema: ALTA PERFORMANCE ATIVA")
        
        st.write(f"**Impacto atual no sistema:** CPU {cpu_live}% | RAM {ram_live.percent}%")
        
        fps_est = 144 if cpu_live < 60 and ram_live.percent < 70 else (60 if cpu_live < 85 else 30)
        st.info(f"FPS Estimado (simulação baseada em folga de sistema): **{fps_est} FPS**")
        
    else:
        st.info("Nenhum jogo conhecido detectado no momento.")
        st.write("Abra a Steam, CS2, Valorant, Minecraft ou GTA V para ativar este modo.")
        
    if st.button("Re-Verificar"):
        st.rerun()

elif page == "Modo HUD":
    # Layout ultra minimalista para overlay
    st.markdown(
        """
        <style>
        .hud-text { font-family: 'Courier New', Courier, monospace; font-size: 80px; font-weight: bold; line-height: 1.2; text-shadow: 2px 2px 5px black;}
        .hud-cpu { color: #ff4b4b; }
        .hud-ram { color: #00fa9a; }
        </style>
        """, unsafe_allow_html=True
    )
    
    st.markdown("<div style='text-align: center; margin-top: 100px;'>", unsafe_allow_html=True)
    st.markdown(f"<div class='hud-text hud-cpu'>CPU: {cpu_live}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hud-text hud-ram'>RAM: {ram_live.percent}%</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("")
    st.caption("HUD Overlay - Atualização a cada 3 segundos. Ideal para manter minimizado num segundo monitor.")
    
    time.sleep(3)
    st.rerun()
