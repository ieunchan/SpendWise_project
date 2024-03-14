# 메인페이지 구현. -> streamlit 사용
# 메인 페이지에는 2개의 selectbox가 필요
# 수입은 카테고리가 없게 지출은 4-5 카테고리 생성
# 지출 카테고리에 세부사항 입력 가능하게 구현
# 입력받은 데이터는 로컬환경에 텍스트 파일로 저장.
# 전체 지출과 수입을 표시
import streamlit as st
import pandas as pd
import os
def main():
    
    st.title("homemade 가계부")

    
    # file_name = "fianacial_records.csv"
    # file_path = os.path.join(os.getcwd(), file_name)
    # with open(file_path,"a",encoding="utf-8") as financial_file: 
    try:
        user_data = pd.read_csv("financial_records.csv")
    except FileNotFoundError:
        user_data = pd.DataFrame(columns=["날짜", "분류", "지출형식","금액"])

    selected_date = st.date_input("날짜를 선택하세요")
    st.write("선택한 날짜:", selected_date)

    option = st.selectbox('수입 혹은 지출 선택', ('수입', '지출'))
    if option == '지출':
        spend_option = st.selectbox('지출 형식을 입력하세요',('쇼핑', '술', '식사', '교통(택시포함)', '이체'))
    amount = st.text_input('금액을 입력하세요')

    if st.button("입력완료"):
        user_data = user_data.append({"날짜": [selected_date], "분류": [option], "금액": [int(amount)],"지출형식": [spend_option]}, ignore_index = True)
        user_data.to_csv("financial_records.csv", index=False)
        st.success("기록되었습니다.")
if __name__ == "__main__":
    main()
