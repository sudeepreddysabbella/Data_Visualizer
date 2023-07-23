import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import io
import base64

app = Flask(__name__)

def plot_to_html_image(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def display_excel_info():
    # Path to the CSV file
    file_path = r"C:\Users\sudee\Desktop\Data_visualizer-main\Data_visualizer-main\project\StudentsPerformance.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Identify unique columns
    unique_columns = df.columns[df.nunique() == df.shape[0]]

    # Filter out unique columns and display them
    df_unique = df[unique_columns]

    # Filter out non-unique columns (categorized values) and sort them alphabetically
    df_categorized = df.drop(columns=unique_columns)
    categorized_columns = sorted(df_categorized.columns)

    # Get the top 5 rows of the DataFrame
    top_5_rows = df.head().to_html()

    selected_columns = request.form.getlist('selected_columns')
    selected_graphs = []

    # Get the selected graph types
    selected_graph_types = request.form.getlist('graph_type')

    # Perform visualizations for selected categorized columns and graph types
    for column in selected_columns:
        column_data = df_categorized[column]
        column_data = column_data.dropna()

        if 'bar' in selected_graph_types and column_data.dtype == 'object':
            # Bar graph for categorical data
            plt.figure()
            column_data.value_counts().plot(kind='bar')
            plt.title(f"{column} - Bar Graph")
            plt.xticks(rotation=45, ha='right')
            plt.xlabel(column)
            plt.ylabel('Count')
            plt.legend()
            graph_html = plot_to_html_image(plt)
            selected_graphs.append({'name': f'{column}_bar', 'html': graph_html})

        if 'pie' in selected_graph_types and column_data.dtype == 'object':
            # Pie chart for categorical data
            plt.figure()
            column_data.value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.title(f"{column} - Pie Chart")
            plt.ylabel('')
            plt.legend()
            graph_html = plot_to_html_image(plt)
            selected_graphs.append({'name': f'{column}_pie', 'html': graph_html})

        if 'line' in selected_graph_types and np.issubdtype(column_data.dtype, np.number):
            # Line plot for numerical data
            plt.figure()
            plt.plot(range(len(column_data)), column_data)
            plt.title(f"{column} - Line Plot")
            plt.xlabel('Index')
            plt.ylabel(column)
            plt.legend()
            graph_html = plot_to_html_image(plt)
            selected_graphs.append({'name': f'{column}_line', 'html': graph_html})

        if 'scatter' in selected_graph_types and np.issubdtype(column_data.dtype, np.number):
            # Scatter plot for numerical data
            plt.figure()
            plt.scatter(range(len(column_data)), column_data)
            plt.title(f"{column} - Scatter Plot")
            plt.xlabel('Index')
            plt.ylabel(column)
            plt.legend()
            graph_html = plot_to_html_image(plt)
            selected_graphs.append({'name': f'{column}_scatter', 'html': graph_html})

        if 'box' in selected_graph_types and np.issubdtype(column_data.dtype, np.number):
            # Box plot for numerical data
            plt.figure()
            plt.boxplot(column_data)
            plt.title(f"{column} - Box Plot")
            plt.ylabel(column)
            plt.legend()
            graph_html = plot_to_html_image(plt)
            selected_graphs.append({'name': f'{column}_box', 'html': graph_html})

        if 'hist' in selected_graph_types and np.issubdtype(column_data.dtype, np.number):
            # Histogram for numerical data
            plt.figure()
            plt.hist(column_data)
            plt.title(f"{column} - Histogram")
            plt.xlabel(column)
            plt.ylabel('Frequency')
            plt.legend()
            graph_html = plot_to_html_image(plt)
            selected_graphs.append({'name': f'{column}_hist', 'html': graph_html})

    return render_template('graphs.html', selected_graphs=selected_graphs, top_5_rows=top_5_rows, categorized_columns=categorized_columns)

if __name__ == '__main__':
    app.run(debug=True)