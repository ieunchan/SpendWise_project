# 메인페이지 구현. -> streamlit 사용
# 메인 페이지에는 2개의 selectbox가 필요
# 수입은 카테고리가 없게 지출은 4-5 카테고리 생성
# 지출 카테고리에 세부사항 입력 가능하게 구현
# 입력받은 데이터는 로컬환경에 텍스트 파일로 저장.
# 전체 지출과 수입을 표시
import streamlit as st
from pages import home, category_expenses, monthlyExpenseVariation

if 'page' not in st.session_state:
    st.session_state['page'] = 'HOME'

menues = {"HOME": home, "이번달 지출유형": category_expenses,"전월대비 지출량": monthlyExpenseVariation}

with st.sidebar:
    for menu in menues.keys():
        if st.button(menu, use_container_width=True, type='primary' if st.session_state['page']==menu else 'secondary'):
            st.session_state['page']=menu
            st.rerun() 

for menu in menues.keys():
    if st.session_state['page']==menu:
        menues[menu]()
