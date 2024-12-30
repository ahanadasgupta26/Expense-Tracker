import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

if "expenses" not in st.session_state:
    st.session_state.expenses=pd.DataFrame(columns=["Date","Category","Amount","Description"])

def add_exp(date,category,amount,description):
    new_exp=pd.DataFrame([[date,category,amount,description]],columns=st.session_state.expenses.columns)
    st.session_state.expenses=pd.concat([st.session_state.expenses,new_exp],ignore_index=True)

def load_exp():
    up_file=st.file_uploader("Choose a file",type=['csv'])
    if up_file is not None:
        st.session_state.expenses=pd.read_csv(up_file)

def save_exp():
   st.session_state.expenses.to_csv("expenses.csv",index=False)
   st.success("Expenses successfully saved!")

def visualize_exp():
    if not st.session_state.expenses.empty:
        fig,ax=plt.subplots()
        sns.barplot(data=st.session_state.expenses,x='Category',y='Amount',ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    else:
        st.warning("No expenses to visualize!")

def edit_exp(index,date,category,amount,description):
    st.session_state.expenses.at[index,'Date']=date
    st.session_state.expenses.at[index,'Category']=category
    st.session_state.expenses.at[index,'Amount']=amount
    st.session_state.expenses.at[index,'Description']=description

def delete_exp(index):
    st.session_state.expenses=st.session_state.expenses.drop(index).reset_index(drop=True)

st.title("Expense Tracker")

with st.sidebar:
    st.header("Add expense")
    date=st.date_input("Date")
    category=st.selectbox("Category",['Food','Transport','Entertainment','Utilities','Others'])
    amount=st.number_input("Amount",min_value=0.0,format="%.2f")
    description=st.text_input("Description")

    if st.button("Add"):
        add_exp(date,category,amount,description)
        st.success("Expense successfully added!")

    st.header("File operations")

    if st.button("Save expenses"):
        save_exp()

    if st.button("Load expenses"):
        load_exp()

st.header("Expenses")
st.write(st.session_state.expenses)

st.header("Edit or Delete Expenses")
if not st.session_state.expenses.empty:
    exp_index = st.number_input("Select Expense Index",min_value=0,max_value=len(st.session_state.expenses)-1,step=1)
    selected_expense=st.session_state.expenses.iloc[exp_index]

    edit_date=st.date_input("Edit Date",value=pd.to_datetime(selected_expense['Date']))

    edit_category=st.selectbox("Edit Category",['Food','Transport','Entertainment','Utilities','Others'],index=['Food','Transport','Entertainment','Utilities','Others'].index(selected_expense['Category']))

    edit_amount=st.number_input("Edit Amount",min_value=0.0,format="%.2f",value=selected_expense['Amount'])

    edit_description=st.text_input("Edit Description",value=selected_expense['Description'])

    if st.button("Save changes"):
        st.session_state.expenses.at[exp_index,'Date']=edit_date
        st.session_state.expenses.at[exp_index,'Category']=edit_category
        st.session_state.expenses.at[exp_index,'Amount']=edit_amount
        st.session_state.expenses.at[exp_index,'Description']=edit_description
        st.success("Expense successfully edited!")

    if st.button("Delete expense"):
        st.session_state.expenses=st.session_state.expenses.drop(exp_index).reset_index(drop=True)
        st.success("Expense successfully deleted!")

st.header("Visualization")

if st.button("Visualize expenses"):
    visualize_exp()
    

