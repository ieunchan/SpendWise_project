import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime


def home():
    
    st.title("가계부")

    try:
        user_data = pd.read_csv("financial_records.csv")
    except FileNotFoundError:
        user_data = pd.DataFrame(columns=["날짜", "분류", "지출형식","금액"])
    
    user_data['날짜'] = pd.to_datetime(user_data['날짜'].str.split().str[0], format='%Y-%m-%d') # '날짜' 열을 datetime 타입으로 변경

    # 메인화면에 날짜 선택
    selected_date = st.date_input("날짜를 선택하세요")
    st.write("선택한 날짜:", selected_date)

    # 이번달 총 지출금액 추출
    expense_amounts = user_data[(user_data['분류'] == '지출') & (user_data['날짜'].dt.month == selected_date.month)]['금액']
    total_expense = expense_amounts.sum()
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
        spend_option = st.selectbox('지출 형식을 입력하세요',('쇼핑', '술', '식사', '교통', '이체', '기타'))
        if spend_option == '기타':
            etc = st.text_input("지출내용입력")
        elif spend_option != '기타':
            etc = None
    else:
        spend_option = None
        etc = None

    # 금액 입력
    amount = st.text_input('금액을 입력하세요')

    if st.button("입력완료"):
        new_row = pd.DataFrame({"날짜": [selected_date], "분류": [option], "금액": [int(amount)], "지출형식": [spend_option],"기타":[etc]})
        user_data = pd.concat([user_data, new_row], ignore_index=True)
        user_data.to_csv("financial_records.csv", index=False)
        st.success("기록되었습니다.")
        st.rerun()

# 한글 폰트 import
from matplotlib import font_manager, rc
def category_expenses():

    st.title("세부 지출내용")

    # 한글 폰트 적용
    font_path = "c:\WINDOWS\Fonts\MALGUN.TTF"
    font = font_manager.FontProperties(fname=font_path).get_name() 
    rc('font', family=font)

    # 사용자 데이터를 읽어와서 지출 금액을 빼옴
    user_data = pd.read_csv("financial_records.csv")
    spend_category_amount = user_data.groupby("지출형식")['금액'].sum()

    # 원형 그래프를 그리는 로직
    # 람다 함수를 사용하여 퍼센트가 아닌 금액으로 표현하게 만들었음. 천단위마다 콤마 추가함.
    total_amount = int(spend_category_amount.sum())
    plt.pie(spend_category_amount, labels=spend_category_amount.index, autopct=lambda pct: f"{pct:.0f}%\n({round(pct/100 * total_amount):,.0f}원)") # 소수점으로 나오는거 방지하려고 반올림 적용
    plt.gca().set_title(f"지출형식별 금액\n(총합: {total_amount:,.0f}원)")
    plt.axis('equal')
    plt.savefig('원형그래프.png')
    
    image = Image.open("원형그래프.png")
    st.image(image)

    st. markdown("***이번달 지출 순위***")
    expense_type = spend_category_amount.to_dict()
    expense_type = {key: value for key, value in sorted(expense_type.items(), key= lambda x:x[1], reverse=True)} # 값을 기준으로 내림차순으로 정렬

    rank = 1
    for category, amount in expense_type.items():
        st.markdown(f"{rank}. {category}: {amount:,.0f}원")
        rank += 1
def monthlyExpenseVariation():
    st.title("전월대비 지출량 변화")
    pass