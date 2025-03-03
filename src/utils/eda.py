import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from openpyxl.drawing.image import Image



def categorical_univariate_summary(df, categorical_columns, data_dict=None, output_file="categorical_univariate_summary.xlsx", save_path=None):
    """
    Generate a summary for categorical columns including:
    - Column name
    - Column description (if provided via data_dict, else blank)
    - Data types
    - Category-wise count and percentage (including missing data)
    - Unique list
    - Bar plots showing percentage distribution
    Save the results in an Excel file at a specified path.

    Parameters:
    - df: pandas DataFrame, the input dataset.
    - categorical_columns: list, the list of categorical columns to summarize.
    - data_dict: dict or None, mapping of column names to their descriptions. 
                 If None, an empty column will be created for descriptions.
    - output_file: str, the name of the output Excel file (default is "categorical_univariate_summary.xlsx").
    - save_path: str or None, the directory path where the file should be saved. 
                 If None, saves in the current working directory.
    """

    # Define the full path for the output file
    if save_path:
        os.makedirs(save_path, exist_ok=True)  # Ensure directory exists
        full_output_path = os.path.join(save_path, output_file)
    else:
        full_output_path = output_file  # Save in the current working directory

    # Create an Excel writer
    with pd.ExcelWriter(full_output_path, engine='openpyxl') as writer:
        # Loop through each categorical column
        for col in categorical_columns:
            # Compute value counts and percentages (including missing data)
            value_counts = df[col].value_counts(dropna=False)
            percentages = (value_counts / len(df)) * 100  # Convert to percentage

            # If data_dict is provided, get column description, else leave it blank
            col_description = data_dict.get(col, "") if data_dict else ""

            # Create a summary dictionary
            summary = {
                'Column Name': [col] * len(value_counts),  # Repeat column name for each category
                'Column Description': [col_description] * len(value_counts),  # Fill with description or blank
                'Data Type': [str(df[col].dtype)] * len(value_counts),  # Repeat data type
                'Category': value_counts.index.tolist(),
                'Count': value_counts.values.tolist(),
                'Percentage': percentages.values.tolist()
            }

            # Convert summary dictionary to DataFrame
            summary_df = pd.DataFrame(summary)

            # Save the summary to Excel
            summary_df.to_excel(writer, sheet_name=f"{col}_summary", index=False)

            # Create a bar plot with percentages
            fig, ax = plt.subplots(figsize=(8, 6))
            percentages.plot(kind='bar', ax=ax, color='#003366')  # Dark blue color
            ax.set_title(f"Percentage Distribution for {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Percentage")
            ax.set_xticklabels(value_counts.index, rotation=45)  # Rotate labels for readability

            # Annotate bars with percentage values
            for i, percentage in enumerate(percentages):
                ax.text(i, percentage + 1, f"{percentage:.1f}%", ha='center', fontsize=10)

            # Save the plot to a BytesIO object
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)

            # Add the plot to the Excel sheet
            img = Image(buf)
            sheet = writer.sheets[f"{col}_summary"]
            sheet.add_image(img, "C7")  # Adjust position as needed

            # Close the figure to suppress output in console
            plt.close(fig)

    print(f"Summary saved to: {full_output_path}")




def numerical_univariate_summary(df, numerical_columns, data_dict=None, output_file="numerical_univariate_summary.xlsx", save_path=None):
    """
    Generate a summary for numerical columns including:
    - Column name
    - Column description (if provided via data_dict, else blank)
    - Data types
    - Missing percentage
    - Mean, Median, Min, Max, Standard Deviation
    - Q1, Q2 (Median), Q3, Q4 (100th percentile)
    - Histogram plots
    Save the results in an Excel file at a specified path.

    Parameters:
    - df: pandas DataFrame, the input dataset.
    - numerical_columns: list, the list of numerical columns to summarize.
    - data_dict: dict or None, mapping of column names to their descriptions. 
                 If None, an empty column will be created for descriptions.
    - output_file: str, the name of the output Excel file (default is "numerical_univariate_summary.xlsx").
    - save_path: str or None, the directory path where the file should be saved. 
                 If None, saves in the current working directory.
    """

    # Define the full path for the output file
    if save_path:
        os.makedirs(save_path, exist_ok=True)  # Ensure directory exists
        full_output_path = os.path.join(save_path, output_file)
    else:
        full_output_path = output_file  # Save in the current working directory

    # Create an Excel writer
    with pd.ExcelWriter(full_output_path, engine='openpyxl') as writer:
        # Loop through each numerical column
        for col in numerical_columns:
            # Compute basic statistics
            missing_percentage = df[col].isnull().mean() * 100
            mean_val = df[col].mean()
            #median_val = df[col].median()
            min_val = df[col].min()
            # Compute quartiles
            P5 = df[col].quantile(0.05)
            Q1 = df[col].quantile(0.25)
            Q2 = df[col].quantile(0.50)  # Median
            Q3 = df[col].quantile(0.75)
            P95 = df[col].quantile(0.95)
            max_val = df[col].max()
            std_dev = df[col].std()
            

            # If data_dict is provided, get column description, else leave it blank
            col_description = data_dict.get(col, "") if data_dict else ""

            # Create a summary dictionary
            summary = {
                'Column Name': [col],
                'Column Description': [col_description],
                'Data Type': [str(df[col].dtype)],
                'Missing Percentage': [missing_percentage],
                'Mean': [mean_val],
                'Min': [min_val],
                'P5 (5%)': [P5],
                'Q1 (25%)': [Q1],
                'Q2 (50%)': [Q2],
                'Q3 (75%)': [Q3],
                'P95 (95%)': [P95],
                'Max': [max_val],
                'Standard Deviation': [std_dev]

            }

            # Convert summary dictionary to DataFrame
            summary_df = pd.DataFrame(summary)

            # Save the summary to Excel
            summary_df.to_excel(writer, sheet_name=f"{col}_summary", index=False)

            # Create a KDE + Histogram plot
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.histplot(df[col].dropna(), kde=True, bins=30, color='#003366', edgecolor='black', alpha=0.7, ax=ax)
            ax.set_title(f"Histogram & KDE for {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Density / Count")

            # Save the plot to a BytesIO object
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)

            # Add the plot to the Excel sheet
            img = Image(buf)
            sheet = writer.sheets[f"{col}_summary"]
            sheet.add_image(img, "C5")  # Adjust position as needed

            # Close the figure to suppress output in console
            plt.close(fig)

    print(f"Summary saved to: {full_output_path}")

