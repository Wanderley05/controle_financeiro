import streamlit as st
import pandas as pd
import plotly.express as px

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

# Inicialização
create_tables()

st.set_page_config(
    page_title="Finance Manager",
    layout="wide"
)

if "logged" not in st.session_state:
    st.session_state.logged = False

# Título
st.title("💰 Finance Manager")

# Menu principal
menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Cadastro"]
)

# ==========================
# CADASTRO
# ==========================

if menu == "Cadastro":

    st.subheader("Criar Conta")

    novo_usuario = st.text_input("Usuário")

    nova_senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Cadastrar"):

        try:

            senha_hash = hash_password(
                nova_senha
            )

            add_user(
                novo_usuario,
                senha_hash
            )

            st.success(
                "Usuário criado com sucesso!"
            )

        except:

            st.error(
                "Usuário já existe."
            )

# ==========================
# LOGIN
# ==========================

if menu == "Login":

    usuario = st.text_input("Usuário")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        user = get_user(usuario)

        if user:

            senha_banco = user[2]

            if verify_password(
                senha,
                senha_banco
            ):

                st.session_state.logged = True
                st.session_state.user_id = user[0]
                st.session_state.usuario = user[1]

                st.success(
                    "Login realizado"
                )

            else:

                st.error(
                    "Senha incorreta"
                )

        else:

            st.error(
                "Usuário não encontrado"
            )

# ==========================
# ÁREA LOGADA
# ==========================

if st.session_state.logged:

    st.success(
        "Bem-vindo ao sistema!"
    )
    st.info(
        f"Usuário logado: {st.session_state.usuario}"
    )

    aba = st.sidebar.radio(
        "Navegação",
        [
            "Dashboard",
            "Nova Transação"
        ]
    )

    # ==========================
    # NOVA TRANSAÇÃO
    # ==========================

    if aba == "Nova Transação":

        st.header("Nova Transação")

        descricao = st.text_input(
            "Descrição"
        )

        valor = st.number_input(
            "Valor",
            min_value=0.01
        )

        categoria = st.selectbox(
            "Categoria",
            [
                "Alimentação",
                "Transporte",
                "Moradia",
                "Lazer",
                "Salário",
                "Outros"
            ]
        )

        tipo = st.radio(
            "Tipo",
            [
                "Receita",
                "Despesa"
            ]
        )

        if st.button("Salvar Transação"):

            add_transaction(
                st.session_state.user_id,
                descricao,
                valor,
                categoria,
                tipo,
            )

            add_log(
                f"Transação criada: {descricao}"
            )

            st.success(
                "Transação cadastrada com sucesso!"
            )

    # ==========================
    # DASHBOARD
    # ==========================

    if aba == "Dashboard":

        dados = get_transactions(st.session_state.user_id)

        if not dados:

            st.info(
                "Nenhuma transação cadastrada."
            )

        else:

            df = pd.DataFrame(
                dados,
                columns=[
                    "ID",
                    "Descrição",
                    "Valor",
                    "Categoria",
                    "Tipo",
                    "Data"
                ]
            )

            st.header(
                "Dashboard Financeiro"
            )

            categoria_filtro = st.selectbox(
                "Categoria",
                ["Todas"] +
                list(df["Categoria"].unique())
            )

            tipo_filtro = st.selectbox(
                "Tipo",
                ["Todos"] +
                list(df["Tipo"].unique())
            )

            if categoria_filtro != "Todas":

                df = df[
                    df["Categoria"]
                    == categoria_filtro
                ]

            if tipo_filtro != "Todos":

                df = df[
                    df["Tipo"]
                    == tipo_filtro
                ]

            receitas = df[
                df["Tipo"] == "Receita"
            ]["Valor"].sum()

            despesas = df[
                df["Tipo"] == "Despesa"
            ]["Valor"].sum()

            saldo = receitas - despesas

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Receitas",
                f"R$ {receitas:,.2f}"
            )

            c2.metric(
                "Despesas",
                f"R$ {despesas:,.2f}"
            )

            c3.metric(
                "Saldo",
                f"R$ {saldo:,.2f}"
            )

            st.subheader(
                "Histórico"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            despesas_df = df[
                df["Tipo"] == "Despesa"
            ]

            if not despesas_df.empty:

                fig = px.pie(
                    despesas_df,
                    names="Categoria",
                    values="Valor",
                    title="Gastos por Categoria"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            evolucao = (
                df.groupby("Data")["Valor"]
                .sum()
                .reset_index()
            )

            fig2 = px.line(
                evolucao,
                x="Data",
                y="Valor",
                title="Evolução Financeira"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            st.subheader(
                "Excluir Transação"
            )

            excluir = st.number_input(
                "ID da transação",
                min_value=1
            )

            if st.button(
                "Excluir Registro"
            ):

                delete_transaction(
                    excluir
                )

                add_log(
                    f"Transação {excluir} removida"
                )

                st.success(
                    "Registro removido"
                )

                st.rerun()