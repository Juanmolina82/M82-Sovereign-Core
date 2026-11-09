import os, datetime, pandas as pd, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
output_dir = os.path.expanduser('~/M82')
os.makedirs(output_dir, exist_ok=True)
excel_path = os.path.join(output_dir, 'm82_aapl_refinitiv_metrics_2026.xlsx')
data = {'Métrica': ['Ticker','Precio Spot ($)','Market Cap ($T)','P/E TTM','Forward P/E','EPS TTM ($)','Q4 FY26 Revenue ($B)','Q4 EPS ($)','Target Price ($)','Consenso'],'Valor': ['AAPL.O',222.91,3.39,34.12,30.15,6.53,114.50,2.10,245.50,'Strong Buy'],'Fuente': ['LSEG Workspace','LSEG Live','LSEG Live','LSEG Calc','LSEG Est','LSEG Calc','Q4 Report','Q4 Report','LSEG Consensus','32 Buy / 12 Hold']}
df = pd.DataFrame(data)
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "AAPL Refinitiv Audit"
font_header = Font(name='Calibri', size=11, bold=True, color='FFFFFF'); font_title = Font(name='Calibri', size=13, bold=True, color='1F497D')
fill_navy = PatternFill(start_color='1F497D', end_color='1F497D', fill_type='solid'); fill_accent = PatternFill(start_color='DCE6F1', end_color='DCE6F1', fill_type='solid')
thin_border = Border(left=Side(style='thin', color='D9D9D9'), right=Side(style='thin', color='D9D9D9'), top=Side(style='thin', color='D9D9D9'), bottom=Side(style='thin', color='D9D9D9'))
ws['A1'] = "M82 SOVEREIGN CORE :: APPLE INC. (AAPL.O) REFINITIV AUDIT"; ws['A1'].font = font_title
ws['A2'] = f"Account: jmmp@molina82.com | Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
ws.append([]); headers = ["Métrica / KPI", "Valor Registrado", "Fuente / Contexto"]; ws.append(headers)
for col_num, header in enumerate(headers, 1):
    cell = ws.cell(row=4, column=col_num); cell.font, cell.fill, cell.alignment = font_header, fill_navy, Alignment(horizontal='center', vertical='center')
for r_idx, row in df.iterrows():
    row_num = r_idx + 5
    ws.cell(row=row_num, column=1, value=row['Métrica']).alignment = Alignment(horizontal='left')
    ws.cell(row=row_num, column=2, value=row['Valor']).alignment = Alignment(horizontal='center')
    ws.cell(row=row_num, column=3, value=row['Fuente']).alignment = Alignment(horizontal='left')
    for c_num in range(1, 4):
        cell = ws.cell(row=row_num, column=c_num); cell.border = thin_border
        if r_idx % 2 == 1: cell.fill = fill_accent
ws.column_dimensions['A'].width = 28; ws.column_dimensions['B'].width = 22; ws.column_dimensions['C'].width = 26
wb.save(excel_path); print(f"AAPL_EXCEL_SUCCESS: {excel_path}")
