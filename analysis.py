# analyze_excel.py
import pandas as pd
import sqlite3
import re
from collections import Counter
import matplotlib.pyplot as plt

def process_excel_to_db(excel_path, db_path):
    """Process Excel file and store in SQLite database"""
    df = pd.read_excel(excel_path)
    df['Requirements'] = df['Requirements'].fillna('') + ' ' + df['Responsibilities'].fillna('')
    df['Requirements'] = df['Requirements'].str.replace('<highlighttext>', '').str.replace('</highlighttext>', '')
    
    conn = sqlite3.connect(db_path)
    df.to_sql('vacancies', conn, if_exists='replace', index=False)
    conn.close()

def analyze_data(db_path):
    """Enhanced analysis with responsibilities tracking"""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM vacancies", conn)
    conn.close()
    
    # Skills extraction (same as before)
    skills = [
        # Core Languages
        'SQL', 'СКЮэЛ', 'Python', 'Пайтон', 'R', 'Java', 'Джава', 'Scala', 'Скала',
        # Data Processing
        'Pandas', 'Пандас', 'NumPy', 'НамПай', 'Spark', 'Спарк', 'Hadoop', 'Хадуп', 'ETL', 'ЕТЛ',
        # Machine Learning
        'Machine Learning', 'Машинное обучение', 'ML', 'МЛ', 'Deep Learning', 'Глубокое обучение',
        'TensorFlow', 'ТензорФлоу', 'PyTorch', 'ПайТорч', 'Scikit-learn', 'Скит-лерн',
        'XGBoost', 'ИксДжиБуст', 'Computer Vision', 'Компьютерное зрение', 'CV', 'КВ',
        'NLP', 'Обработка естественного языка',
        # Visualization & BI
        'Excel', 'Эксель', 'Tableau', 'Табло', 'Power BI', 'Пауэр Би Ай', 'BI', 'Бизнес-аналитика',
        'Matplotlib', 'Матплотлиб', 'Seaborn', 'Сиборн', 'Plotly', 'Плотли',
        'Data Visualization', 'Визуализация данных',
        # Databases
        'PostgreSQL', 'ПостгреСQL', 'MySQL', 'МайSQL', 'ClickHouse', 'КликХаус',
        'MongoDB', 'Монго ДБ', 'Redis', 'Редис',
        # Cloud & Big Data
        'AWS', 'Амазон Веб Сервисы', 'Azure', 'Азур', 'Google Cloud', 'Гугл Клауд',
        'Yandex Cloud', 'Яндекс Облако', 'Kafka', 'Кафка', 'Airflow', 'Эйрфлоу',
        'Big Data', 'Большие данные',
        # Analytics & Stats
        'Data Analysis', 'Анализ данных', 'Data Mining', 'Добыча данных',
        'Statistics', 'Статистика', 'A/B Testing', 'А/Б тестирование',
        'Predictive Analytics', 'Прогнозная аналитика',
        # Russian Tools
        '1C', 'Yandex Metrica', 'Яндекс.Метрика', 'Yandex Direct', 'Яндекс.Директ',
        # MLOps
        'Docker', 'Докер', 'Kubernetes', 'Кубернетес', 'MLflow', 'ЭмЭлфлоу'
    ]
    
    def extract_skills(text):
        found_skills = []
        for skill in skills:
            if re.search(rf'\b{re.escape(skill)}\b', str(text), re.IGNORECASE):
                found_skills.append(skill)
        return found_skills
    
    df['skills'] = df['Requirements'].apply(extract_skills)
    
    # Responsibility patterns analysis
    responsibility_patterns = [
        ('Data Analysis', r'анализ данных|data analysis'),
        ('Reporting', r'отчетность|reporting'),
        ('Dashboard Creation', r'создание дашбордов|dashboard creation'),
        ('Model Development', r'разработка моделей|model development'),
        ('Data Pipeline', r'data pipeline|ETL'),
        ('Business Recommendations', r'рекомендации бизнесу|business recommendations'),
        ('Automation', r'автоматизация|automation'),
        ('Team Leadership', r'руководство командой|team leadership')
    ]
    
    def extract_responsibilities(text):
        responsibilities = []
        for name, pattern in responsibility_patterns:
            if re.search(pattern, str(text), re.IGNORECASE):
                responsibilities.append(name)
        return responsibilities
    
    df['responsibilities'] = df['Responsibilities'].apply(extract_responsibilities)
    
    # Generate statistics
    all_skills = [skill for sublist in df['skills'] for skill in sublist]
    skill_counts = Counter(all_skills)
    top_skills = dict(skill_counts.most_common(15))
    
    all_responsibilities = [resp for sublist in df['responsibilities'] for resp in sublist]
    responsibility_counts = Counter(all_responsibilities)
    top_responsibilities = dict(responsibility_counts.most_common(8))
    
    # Salary and seniority analysis (same as before)
    df['Salary From'] = pd.to_numeric(df['Salary From'], errors='coerce')
    df['Salary To'] = pd.to_numeric(df['Salary To'], errors='coerce')
    df['avg_salary'] = df[['Salary From', 'Salary To']].mean(axis=1)
    salary_by_region = df.groupby('Region')['avg_salary'].median().sort_values(ascending=False).head(10)
    
    def detect_seniority(title):
        if not isinstance(title, str):
            return 'Unknown'
        title = title.lower()
        if any(word in title for word in ['junior', 'младший', 'начальный']):
            return 'Junior'
        elif any(word in title for word in ['middle', 'средний']):
            return 'Middle'
        elif any(word in title for word in ['senior', 'старший', 'ведущий']):
            return 'Senior'
        elif any(word in title for word in ['lead', 'руководитель']):
            return 'Lead'
        return 'Unknown'
    
    df['seniority'] = df['Job Title'].apply(detect_seniority)
    seniority_counts = df['seniority'].value_counts()
    
    # Create visualizations
    plt.figure(figsize=(20, 16))
    
    # Chart 1: Top Required Skills
    plt.subplot(2, 2, 1)
    plt.barh(list(top_skills.keys()), list(top_skills.values()))
    plt.title('Top 15 Required Skills')
    plt.xlabel('Number of Mentions')
    plt.gca().invert_yaxis()
    
    # Chart 2: Salary by Region
    plt.subplot(2, 2, 2)
    salary_by_region.plot(kind='bar')
    plt.title('Average Salary by Region (Top 10)')
    plt.xlabel('Region')
    plt.ylabel('Salary (RUB)')
    plt.xticks(rotation=45)
    
    # Chart 3: Seniority Level Distribution
    plt.subplot(2, 2, 3)
    seniority_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Seniority Level Distribution')
    plt.ylabel('')
    
    # Chart 4: Common Responsibilities
    plt.subplot(2, 2, 4)
    plt.barh(list(top_responsibilities.keys()), list(top_responsibilities.values()))
    plt.title('Most Common Responsibilities')
    plt.xlabel('Number of Mentions')
    plt.gca().invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('dashboard/visualizations.png')
    plt.close()
    
    # Prepare data for dashboard
    with open('dashboard/data.js', 'w', encoding="utf-8") as f:
        f.write(f"const skillData = {str(top_skills)};\n")
        f.write(f"const salaryData = {str(salary_by_region.to_dict())};\n")
        f.write(f"const seniorityData = {str(seniority_counts.to_dict())};\n")
        f.write(f"const responsibilityData = {str(top_responsibilities)};\n")

if __name__ == '__main__':
    process_excel_to_db('collected_vacancies.xlsx', 'jobs.db')
    analyze_data('jobs.db')