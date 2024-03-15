import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

def home():
    
    st.title("가계부")

    try:
        user_data = pd.read_csv("financial_records.csv")
    except FileNotFoundError:
        user_data = pd.DataFrame(columns=["날짜", "분류", "지출형식","금액"])
    
    # 메인화면에 날짜 선택
    selected_date = st.date_input("날짜를 선택하세요")
    st.write("선택한 날짜:", selected_date)

    # 이번달 총 지출금액 추출
    expense_amounts = user_data[user_data['분류'] == '지출']['금액']
    total_expense = expense_amounts.sum()
    total_expense = "{:,.0f}".format(total_expense) # 금액을 천단위마다 콤마추가
    st.write('이번달 총 지출: ', total_expense,"원")

    # 이번달 총 수입 추출
    income_amounts = user_data[user_data['분류'] == '수입']['금액']
    total_imcome = income_amounts.sum()
    total_imcome = "{:,.0f}".format(total_imcome) # 금액을 천단위마다 콤마추가
    st.write('이번달 총 수입: ',total_imcome,'원')

    # 메인화면에 수입, 지출 선택
    option = st.selectbox('수입 혹은 지출 선택', ('수입', '지출'))
    if option == '지출':
        spend_option = st.selectbox('지출 형식을 입력하세요',('쇼핑', '술', '식사', '교통(택시포함)', '이체', '기타'))
        if spend_option == '기타':
            etc = st.text_input("지출내용입력")
        elif spend_option != '기타':
            etc = None
    else:
        spend_option = None

    # 금액 입력
    amount = st.text_input('금액을 입력하세요')

    if st.button("입력완료"):
        new_row = pd.DataFrame({"날짜": [selected_date], "분류": [option], "금액": [int(amount)], "지출형식": [spend_option],"기타":[etc]})
        user_data = pd.concat([user_data, new_row], ignore_index=True)
        user_data.to_csv("financial_records.csv", index=False)
        st.success("기록되었습니다.")
        st.rerun()


def category_expenses():
    st.title("이번달 지출유형")
    category_expenses_graph = pd.read_csv("financial_records.csv")
    expensed = category_expenses_graph[category_expenses_graph['분류'] == '지출']['금액']
    expensed_category = category_expenses_graph[category_expenses_graph['분류'] == '지출']['지출형식']
    expensed_category_series = pd.Series(expensed_category)
    sizes = expensed / expensed.sum()
    labels = expensed_category_series.unique()
    plt.figure(figsize=(6, 6))
    sb.set_palette("pastel")
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    st.pyplot()
def monthlyExpenseVariation():
    st.title("전월대비 지출량 변화")
    pass