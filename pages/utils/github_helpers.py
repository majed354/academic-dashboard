import streamlit as st
import requests
import pandas as pd
from io import StringIO, BytesIO

@st.cache_data(ttl=3600)
def list_github_dir_contents(dir_path):
    pat = st.secrets["GITHUB_PAT"]
    owner = st.secrets["GITHUB_OWNER"]
    repo = st.secrets["GITHUB_REPO"]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{dir_path}"
    headers = {'Authorization': f'token {pat}', 'Accept': 'application/vnd.github.v3+json'}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"GitHub API error: {e}")
        return None

@st.cache_data(ttl=3600)
def get_github_file_content(file_path):
    pat = st.secrets["GITHUB_PAT"]
    owner = st.secrets["GITHUB_OWNER"]
    repo = st.secrets["GITHUB_REPO"]
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}"
    headers = {'Authorization': f'token {pat}'}
    try:
        response = requests.get(raw_url, headers=headers)
        response.raise_for_status()
        if file_path.lower().endswith('.csv'):
            return pd.read_csv(StringIO(response.text))
        elif file_path.lower().endswith('.pdf'):
            return response.content
        elif file_path.lower().endswith(('.xlsx', '.xls')):
            return pd.read_excel(BytesIO(response.content))
        else:
            return response.text
    except Exception as e:
        st.error(f"Error fetching file: {e}")
        return None

def get_available_years(program_code):
    data_path = f"data/{program_code}/yearly_data"
    contents = list_github_dir_contents(data_path) or []
    years, mapping = [], {}
    for item in contents:
        if item.get('type')=='file' and item['name'].lower().endswith('.csv'):
            try:
                yr = int(item['name'].split('_')[0]); years.append(yr); mapping[yr]=item['path']
            except: pass
    years.sort(reverse=True)
    return years, mapping

def get_available_reports(program_code):
    path = f"data/{program_code}/reports"
    contents = list_github_dir_contents(path) or []
    reports = {}
    for item in contents:
        nm = item.get('name','')
        if item.get('type')=='file' and (nm.startswith('تقرير_') or nm.startswith('توصيف_')):
            reports[nm]=item['path']
    return reports
