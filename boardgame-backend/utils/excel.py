import pandas as pd
import os
import re
from utils.db import save_salary_report

BASE_SALARY = 23000

# Tính hệ số lương từ chuỗi ca
def get_shift_multiplier(shift_info):
    if 'x2' in shift_info:
        return 2.0
    elif 'x1.5' in shift_info:
        return 1.5
    elif re.search(r'[ABC]/2', shift_info):
        return 0.5
    return 1.0

# Kiểm tra nếu là AB, BC thì vẫn trả đủ 1 ca
def is_half_shift(shift_info):
    return bool(re.search(r'AB|BC', shift_info))

# Trích xuất tên nhân viên từ ô
def extract_names(cell):
    if pd.isna(cell):
        return []
    names = re.split(r'[\n,/\\]+', str(cell))
    return [name.strip() for name in names if name.strip()]

def process_salary(file):
    df = pd.read_excel(file, header=None)
    employees = 

    for i in range(df.shape[1]):
        if df.iloc[1, i] == 'Thứ 2':
            start_col = i
            break
    else:
        raise ValueError("Không tìm thấy cột 'Thứ 2'")

    shifts = ['Ca A', 'Ca B', 'Ca C']
    current_shift = None

    for i in range(2, df.shape[0]):
        first_cell = str(df.iloc[i, 0]).strip()
        if any(s in first_cell for s in shifts):
            current_shift = first_cell
            continue

        for j in range(start_col, start_col + 7):  # 7 ngày trong tuần
            cell_value = df.iloc[i, j]
            if pd.isna(cell_value):
                continue

            names = extract_names(cell_value)
            if not names:
                continue

            raw_text = str(cell_value)
            shift_multiplier = get_shift_multiplier(raw_text)

            if is_half_shift(raw_text):
                shift_multiplier = 1.0  # AB/BC là 1 ca

            base_pay = BASE_SALARY * shift_multiplier
            per_person_pay = base_pay / len(names)

            for name in names:
                employees[name] = employees.get(name, 0) + per_person_pay

    report_path = os.path.join("outputs", "salary_report.xlsx")
    os.makedirs("outputs", exist_ok=True)
    result_df = pd.DataFrame(employees.items(), columns=['Tên', 'Tổng lương'])
    result_df.to_excel(report_path, index=False)

    # Save report to database
    from datetime import datetime
    report_data = []
    report_date = datetime.now().strftime("%Y-%m-%d")
    for _, row in result_df.iterrows():
        report_data.append({
            "name": row['Tên'],
            "total_salary": row['Tổng lương'],
            "report_date": report_date
        })

    save_salary_report(report_data)
    return report_path
