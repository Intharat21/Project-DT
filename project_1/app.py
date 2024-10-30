from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load data from the Excel 
@app.route('/')
def index():
    # Read Excel 
    excel_file = 'instance\Prosth-รายการวัสดุนอกเวลาที่ต้องการสั่งซื้อ.xlsx'
    df = pd.read_excel(excel_file)

    # Replace NaN values with an empty string
    df = df.fillna('')

    # Convert the DataFrame 
    DataBase = df.to_dict(orient='records')

    # Pass data to the template
    return render_template('index.html', Data=DataBase)

# Route update data
@app.route('/update_data', methods=['POST'])
def update_data():
    # Read Excel file
    excel_file = 'instance\Prosth-รายการวัสดุนอกเวลาที่ต้องการสั่งซื้อ.xlsx'
    df = pd.read_excel(excel_file)

    # Replace NaN values with empty string
    df = df.fillna('')

    # Get form data and update 
    for i, row in df.iterrows():
        df.at[i, 'Unnamed: 1'] = request.form.get(f'order_{i+1}')
        df.at[i, 'Unnamed: 2'] = request.form.get(f'item_{i+1}')
        df.at[i, 'Unnamed: 3'] = request.form.get(f'unit_{i+1}')
        df.at[i, 'Unnamed: 4'] = request.form.get(f'stock_{i+1}')
        df.at[i, 'Unnamed: 15'] = request.form.get(f'quantity_{i+1}')

    # Write the updated DataFrame back to the Excel file
    df.to_excel(excel_file, index=False)

    return redirect(url_for('index'))

@app.route('/edit/<int:row_index>', methods=['GET', 'POST'])
def edit_row(row_index):
    # Read Excel file
    excel_file = 'instance\Prosth-รายการวัสดุนอกเวลาที่ต้องการสั่งซื้อ.xlsx'
    df = pd.read_excel(excel_file)

    # Replace NaN values 
    df = df.fillna('')

    if request.method == 'POST':
        # Update the specific row 
        df.at[row_index, 'Unnamed: 1'] = request.form['id']
        df.at[row_index, 'Unnamed: 2'] = request.form['item']
        df.at[row_index, 'Unnamed: 3'] = request.form['unit']
        df.at[row_index, 'Unnamed: 4'] = request.form['stock']
        df.at[row_index, 'Unnamed: 15'] = request.form['quantity']

        # Save the updated data back to Excel
        df.to_excel(excel_file, index=False)

        return redirect(url_for('index'))

    # Pass the specific row data to the template
    row_data = df.iloc[row_index].to_dict()

    return render_template('edit_row.html', row_data=row_data, row_index=row_index)


if __name__ == '__main__':
    app.run(debug=True)
