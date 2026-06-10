import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from database import (
    create_tables,
    add_user,
    get_user,
    add_transaction,
    get_transactions,
    delete_transaction,
    add_log
)

from auth import (
    hash_password,
    verify_password
)


create_tables()

st.set_page_config(
    page_title="💸 FinanceFlow",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

/* ---- RESET E BASE ---- */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 50%, #1a0533 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, #001a3a 0%, transparent 50%),
                radial-gradient(ellipse at 50% 80%, #0a1a0a 0%, transparent 50%),
                #0a0a0f !important;
}

/* ---- PARTÍCULAS ANIMADAS NO FUNDO ---- */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(139, 92, 246, 0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 70%, rgba(59, 130, 246, 0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 10%, rgba(16, 185, 129, 0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 50%, rgba(245, 158, 11, 0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 90%, rgba(239, 68, 68, 0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 30%, rgba(139, 92, 246, 0.3) 0%, transparent 100%),
        radial-gradient(2px 2px at 20% 40%, rgba(59, 130, 246, 0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 80%, rgba(16, 185, 129, 0.4) 0%, transparent 100%);
    background-size: 600px 600px;
    animation: particleFloat 20s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes particleFloat {
    0%   { transform: translateY(0px) translateX(0px); }
    25%  { transform: translateY(-30px) translateX(15px); }
    50%  { transform: translateY(-10px) translateX(-10px); }
    75%  { transform: translateY(-40px) translateX(20px); }
    100% { transform: translateY(0px) translateX(0px); }
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #0a0a14 100%) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.3) !important;
    box-shadow: 4px 0 30px rgba(139, 92, 246, 0.15) !important;
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #8b5cf6, #3b82f6, #10b981, #f59e0b, #ef4444, #8b5cf6);
    background-size: 200% 100%;
    animation: rainbowSlide 3s linear infinite;
}

@keyframes rainbowSlide {
    0%   { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

/* ---- TÍTULO PRINCIPAL ---- */
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 800 !important;
    font-size: 3rem !important;
    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 30%, #10b981 60%, #f59e0b 100%) !important;
    background-size: 300% 300% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: titleGradient 4s ease infinite, titlePulse 2s ease-in-out infinite !important;
    text-align: center !important;
    letter-spacing: -1px !important;
    margin-bottom: 0.5rem !important;
}

@keyframes titleGradient {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes titlePulse {
    0%, 100% { filter: drop-shadow(0 0 8px rgba(139, 92, 246, 0.5)); }
    50%       { filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.9)); }
}

/* ---- SUBTÍTULOS ---- */
h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: #c4b5fd !important;
    border-left: 3px solid #8b5cf6 !important;
    padding-left: 12px !important;
    animation: borderPulse 2s ease-in-out infinite !important;
}

@keyframes borderPulse {
    0%, 100% { border-left-color: #8b5cf6; }
    33%       { border-left-color: #3b82f6; }
    66%       { border-left-color: #10b981; }
}

/* ---- BOTÕES ---- */
.stButton > button {
    background: linear-gradient(135deg, #8b5cf6, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 0; height: 0;
    background: rgba(255,255,255,0.25);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.5s ease, height 0.5s ease;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 0 15px 40px rgba(139, 92, 246, 0.7) !important;
    background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
}

.stButton > button:hover::before {
    width: 300px;
    height: 300px;
}

.stButton > button:active {
    transform: translateY(-1px) scale(0.98) !important;
}

/* ---- INPUTS ---- */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.25), 0 0 20px rgba(139, 92, 246, 0.2) !important;
    background: rgba(139, 92, 246, 0.08) !important;
    outline: none !important;
}

/* ---- MÉTRICAS (CARDS) ---- */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 16px !important;
    padding: 1.2rem !important;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    animation: cardEntrance 0.6s ease forwards !important;
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #8b5cf6, #3b82f6, #10b981);
    background-size: 200% 100%;
    animation: rainbowSlide 2s linear infinite;
}

[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(139,92,246,0.06) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.4s;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-6px) scale(1.02) !important;
    border-color: rgba(139, 92, 246, 0.6) !important;
    box-shadow: 0 20px 50px rgba(139, 92, 246, 0.3) !important;
}

[data-testid="stMetric"]:hover::after { opacity: 1; }

@keyframes cardEntrance {
    from { opacity: 0; transform: translateY(30px) scale(0.9); }
    to   { opacity: 1; transform: translateY(0)    scale(1);   }
}

[data-testid="stMetricLabel"] {
    color: #a78bfa !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.8rem !important;
    background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    animation: fadeIn 0.8s ease !important;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---- ALERTAS ---- */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 4px !important;
    animation: slideInLeft 0.4s ease !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* ---- RADIO ---- */
.stRadio label {
    color: #c4b5fd !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    transition: color 0.2s ease !important;
}

.stRadio label:hover { color: #a78bfa !important; }

/* ---- SELECTBOX ---- */
[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

[data-baseweb="select"] > div:hover {
    border-color: rgba(139, 92, 246, 0.7) !important;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.2) !important;
}

/* ---- SEPARADOR ANIMADO ---- */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, #8b5cf6, #3b82f6, #10b981, transparent) !important;
    background-size: 200% 100% !important;
    animation: rainbowSlide 3s linear infinite !important;
    margin: 1.5rem 0 !important;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(#8b5cf6, #3b82f6);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: #a78bfa; }

/* ---- LABEL DOS CAMPOS ---- */
label, .stSelectbox label, .stTextInput label, .stNumberInput label {
    color: #a78bfa !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    font-weight: 600 !important;
}

/* ---- LOADING SPINNER ---- */
.stSpinner > div {
    border-top-color: #8b5cf6 !important;
}

/* ---- ENTRADA ESCALONADA DOS ELEMENTOS ---- */
.element-container:nth-child(1)  { animation-delay: 0.05s; }
.element-container:nth-child(2)  { animation-delay: 0.10s; }
.element-container:nth-child(3)  { animation-delay: 0.15s; }
.element-container:nth-child(4)  { animation-delay: 0.20s; }
.element-container:nth-child(5)  { animation-delay: 0.25s; }
.element-container:nth-child(6)  { animation-delay: 0.30s; }
.element-container {
    animation: fadeIn 0.5s ease both;
}
</style>
""", unsafe_allow_html=True)



if "logged" not in st.session_state:
    st.session_state.logged = False



st.title("💸 FinanceFlow")

st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(139,92,246,0.15) 0%, rgba(59,130,246,0.1) 50%, rgba(16,185,129,0.1) 100%);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: fadeIn 1s ease forwards;
">
    <p style='font-size:1.4rem; font-weight:700; color:#e8e8f0; margin:0'>Controle financeiro inteligente e moderno</p>
    <p style='font-size:0.9rem; color:#a78bfa; margin-top:0.4rem; font-family:monospace'>// acompanhe receitas · despesas · saldo em tempo real</p>
</div>
""", unsafe_allow_html=True)



if not st.session_state.logged:
    menu = st.sidebar.selectbox("🔐 Acesso", ["Login", "Cadastro"])
else:
    st.sidebar.markdown(f"""
    <div style='
        background: rgba(139,92,246,0.15);
        border: 1px solid rgba(139,92,246,0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        text-align: center;
    '>
        <div style='font-size:1.5rem'>👤</div>
        <div style='color:#c4b5fd; font-weight:700; font-size:1rem'>{st.session_state.usuario}</div>
        <div style='color:#6b7280; font-size:0.75rem; font-family:monospace'>logado</div>
    </div>
    """, unsafe_allow_html=True)
    menu = "logado"



if not st.session_state.logged and menu == "Cadastro":
    st.subheader("✨ Criar Conta")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        novo_usuario = st.text_input("Usuário", placeholder="seu_usuario")
        nova_senha = st.text_input(
            "Senha", type="password", placeholder="••••••••")
        if st.button("🚀 Criar Conta", use_container_width=True):
            if not novo_usuario or not nova_senha:
                st.error("⚠️ Preencha todos os campos.")
            elif len(nova_senha) < 6:
                st.error("⚠️ Senha deve ter ao menos 6 caracteres.")
            else:
                try:
                    add_user(novo_usuario, hash_password(nova_senha))
                    st.success("✅ Conta criada! Vá para Login.")
                except:
                    st.error("❌ Usuário já existe.")



if not st.session_state.logged and menu == "Login":
    st.subheader("🔑 Entrar")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        usuario = st.text_input("Usuário", placeholder="seu_usuario")
        senha = st.text_input("Senha", type="password", placeholder="••••••••")
        if st.button("⚡ Entrar", use_container_width=True):
            user = get_user(usuario)
            if user and verify_password(senha, user[2]):
                st.session_state.logged = True
                st.session_state.user_id = user[0]
                st.session_state.usuario = user[1]
                st.success("✅ Login realizado!")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos.")



if st.session_state.logged:

    aba = st.sidebar.radio(
        "📌 Navegar",
        ["📊 Dashboard", "➕ Nova Transação"]
    )

    if st.sidebar.button("🚪 Sair", use_container_width=True):
        st.session_state.logged = False
        st.rerun()

    
    if aba == "➕ Nova Transação":
        st.subheader("➕ Nova Transação")

        col1, col2 = st.columns(2)
        with col1:
            descricao = st.text_input(
                "Descrição", placeholder="Ex: Aluguel, Salário...")
            valor = st.number_input(
                "Valor (R$)", min_value=0.01, step=0.01, format="%.2f")
        with col2:
            categoria = st.selectbox("Categoria", [
                "🍔 Alimentação", "🚗 Transporte", "🏠 Moradia",
                "🎮 Lazer", "💼 Salário", "📦 Outros"
            ])
            tipo = st.radio(
                "Tipo", ["💚 Receita", "🔴 Despesa"], horizontal=True)

        st.markdown("---")

        if st.button("💾 Salvar Transação", use_container_width=True):
            if not descricao.strip():
                st.error("⚠️ Descrição obrigatória.")
            else:
                tipo_limpo = "Receita" if "Receita" in tipo else "Despesa"
                categoria_limpa = categoria.split(" ", 1)[-1]
                add_transaction(
                    st.session_state.user_id,
                    descricao, valor, categoria_limpa, tipo_limpo
                )
                add_log(f"Transação criada: {descricao}")
                
                st.success(f"✅ Transação **{descricao}** salva com sucesso!")


    if aba == "📊 Dashboard":

        dados = get_transactions(st.session_state.user_id)

        if not dados:
            st.info("📭 Nenhuma transação ainda. Adicione sua primeira transação!")
        else:
            df = pd.DataFrame(
                dados, columns=["ID", "Descrição", "Valor", "Categoria", "Tipo", "Data"])
            df["Data"] = pd.to_datetime(df["Data"])

            st.subheader("📊 Dashboard Financeiro")

            
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                categoria_filtro = st.selectbox(
                    "🏷️ Categoria", ["Todas"] + sorted(df["Categoria"].unique().tolist()))
            with col_f2:
                tipo_filtro = st.selectbox(
                    "📂 Tipo", ["Todos", "Receita", "Despesa"])
            with col_f3:
                ordem = st.selectbox(
                    "🔃 Ordenar por", ["Mais recente", "Mais antigo", "Maior valor", "Menor valor"])

            df_filtrado = df.copy()
            if categoria_filtro != "Todas":
                df_filtrado = df_filtrado[df_filtrado["Categoria"]
                                    == categoria_filtro]
            if tipo_filtro != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_filtro]

            order_map = {
                "Mais recente":  ("Data", False),
                "Mais antigo":   ("Data", True),
                "Maior valor":   ("Valor", False),
                "Menor valor":   ("Valor", True),
            }
            col_ord, asc_ord = order_map[ordem]
            df_filtrado = df_filtrado.sort_values(col_ord, ascending=asc_ord)

            
            st.markdown("---")
            receitas = df_filtrado[df_filtrado["Tipo"]
                            == "Receita"]["Valor"].sum()
            despesas = df_filtrado[df_filtrado["Tipo"]
                            == "Despesa"]["Valor"].sum()
            saldo = receitas - despesas
            n_transac = len(df_filtrado)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💚 Receitas",   f"R$ {receitas:,.2f}")
            c2.metric("🔴 Despesas",   f"R$ {despesas:,.2f}")
            c3.metric("💰 Saldo",      f"R$ {saldo:,.2f}",
                    delta=f"{'positivo' if saldo >= 0 else 'negativo'}")
            c4.metric("📋 Transações", f"{n_transac}")

            st.markdown("---")

            
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                desp_df = df_filtrado[df_filtrado["Tipo"] == "Despesa"]
                if not desp_df.empty:
                    fig_pie = px.pie(
                        desp_df, names="Categoria", values="Valor",
                        title="🥧 Gastos por Categoria",
                        color_discrete_sequence=px.colors.sequential.Plasma_r,
                        hole=0.45
                    )
                    fig_pie.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#e8e8f0", family="Space Grotesk"),
                        title_font=dict(size=16, color="#c4b5fd"),
                        legend=dict(font=dict(color="#e8e8f0"))
                    )
                    fig_pie.update_traces(textfont_color="#e8e8f0")
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("Sem despesas para exibir no gráfico.")

            with col_g2:
                df_linha = df_filtrado.copy()
                df_linha["DataStr"] = df_linha["Data"].dt.strftime("%d/%m/%Y")
                evolucao = df_linha.groupby(["DataStr", "Tipo"])[
                    "Valor"].sum().reset_index()
                fig_bar = px.bar(
                    evolucao, x="DataStr", y="Valor", color="Tipo",
                    title="📈 Receitas vs Despesas por Data",
                    color_discrete_map={
                        "Receita": "#10b981", "Despesa": "#ef4444"},
                    barmode="group"
                )
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e8e8f0", family="Space Grotesk"),
                    title_font=dict(size=16, color="#c4b5fd"),
                    legend=dict(font=dict(color="#e8e8f0")),
                    xaxis=dict(gridcolor="rgba(139,92,246,0.1)",
                            color="#a78bfa"),
                    yaxis=dict(gridcolor="rgba(139,92,246,0.1)",
                            color="#a78bfa")
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            
            st.subheader("📋 Histórico")
            df_show = df_filtrado[["ID", "Descrição",
                                "Valor", "Categoria", "Tipo", "Data"]].copy()
            df_show["Data"] = df_show["Data"].dt.strftime("%d/%m/%Y %H:%M")
            df_show["Valor"] = df_show["Valor"].apply(lambda v: f"R$ {v:,.2f}")
            st.dataframe(df_show, use_container_width=True, hide_index=True)

            
            st.markdown("---")
            st.subheader("🗑️ Excluir Transação")
            ids_disponiveis = df["ID"].tolist()
            col_d1, col_d2 = st.columns([3, 1])
            with col_d1:
                excluir = st.number_input(
                    "ID da transação", min_value=1, step=1)
            with col_d2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Excluir", use_container_width=True):
                    if int(excluir) in ids_disponiveis:
                        delete_transaction(int(excluir))
                        add_log(f"Transação {excluir} removida")
                        st.success(f"✅ Transação #{int(excluir)} removida.")
                        st.rerun()
                    else:
                        st.error("❌ ID não encontrado.")
