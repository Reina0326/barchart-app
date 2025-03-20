import streamlit as st
import pandas as pd
import plotly.express as px

# Excel файлыг унших
# file_path = 'D:/web/disease_analysis_results.xlsx'
file_path ='https://raw.githubusercontent.com/Reina0326/barchart-app/main/disease_analysis_results.xlsx'
excel_data = pd.ExcelFile(file_path)
sheet_names = excel_data.sheet_names

# Өгөгдлийг унших
all_data = {}

for sheet_name in sheet_names:
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        if 'p_value' in df.columns and 'column' in df.columns:
            if all(col in df.columns for col in ['odds_ratio', 'relative_risk', 'ppv']):
                all_data[sheet_name] = df
            else:
                st.warning(f'{sheet_name} хуудас дээр шаардлагатай баганууд байхгүй байна.')
        else:
            all_data[sheet_name] = pd.DataFrame({'column': [], 'p_value': []})
    except Exception as e:
        st.error(f'Алдаа гарлаа: {e}')

# Аппын гарчиг
st.set_page_config(page_title="Өвчний Магадлал", layout="wide")
st.title('🩺 Өвчний Магадлалын Анализ')
st.markdown("---")

# Хажуугийн цэс
st.sidebar.header("Тохиргоо")
selected_disease = st.sidebar.selectbox('Өвчний нэр сонгох:', sheet_names)

# Сонгосон өвчний өгөгдөл
if selected_disease in all_data:
    df_selected = all_data[selected_disease]
else:
    df_selected = pd.DataFrame()

# Өгөгдөл харах сонголт
if not df_selected.empty:
    with st.expander("📊 Өгөгдлийн хүснэгт харах"):
        st.dataframe(df_selected)

    # График төрөл сонгох
    chart_type = st.sidebar.radio("График төрөл сонгох:", ["Bar Chart", "Line Chart", "Scatter Plot"])
    
    # График үүсгэх
    if chart_type == "Bar Chart":
        fig = px.bar(
            df_selected, x='column', y='p_value',
            title=f'{selected_disease} өвчний магадлал',
            labels={'p_value': 'Өвчин тусах магадлал', 'column': 'Асуулт'},
            hover_data=['odds_ratio', 'relative_risk', 'ppv']
        )
    elif chart_type == "Line Chart":
        fig = px.line(
            df_selected, x='column', y='p_value',
            title=f'{selected_disease} өвчний магадлал',
            labels={'p_value': 'Өвчин тусах магадлал', 'column': 'Асуулт'},
            hover_data=['odds_ratio', 'relative_risk', 'ppv']
        )
    else:
        fig = px.scatter(
            df_selected, x='column', y='p_value',
            title=f'{selected_disease} өвчний магадлал',
            labels={'p_value': 'Өвчин тусах магадлал', 'column': 'Асуулт'},
            hover_data=['odds_ratio', 'relative_risk', 'ppv']
        )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Өгөгдөл байхгүй байна.")