from zenml import step
from typing import Tuple, Annotated
import h2o
from h2o.automl import H2OAutoML
import pandas as pd
import matplotlib.pyplot as plt


@step(enable_cache = False)
def predict_prod_data(ref_data: pd.DataFrame, curr_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # Initialize the H2O cluster
    h2o.init()
    # Load the trained H2O model
    model_path = "models/best_model.zip/GLM_1_AutoML_1_20231214_194418.zip"
    trained_model = h2o.import_mojo(model_path)

    # Make predictions on the reference and current datasets
    ref_data['prediction'] = trained_model.predict(h2o.H2OFrame(ref_data)).as_data_frame()
    curr_data['prediction'] = trained_model.predict(h2o.H2OFrame(curr_data)).as_data_frame()

    # Generate a scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(ref_data['prediction'], ref_data['Approved_Conversion'], label='Reference Data')
    plt.scatter(curr_data['prediction'], curr_data['Approved_Conversion'], label='Current Data')
    plt.title('Predictions vs Actual')
    plt.xlabel('Predictions')
    plt.ylabel('Actual')
    plt.legend()
    plt.savefig('CML_Reports/predictions_scatter_plot.png')
    
    # Generate a residuals plot
    plt.figure(figsize=(10, 6))
    plt.scatter(ref_data['prediction'], ref_data['prediction'] - ref_data['Approved_Conversion'], label='Reference Data')
    plt.scatter(curr_data['prediction'], curr_data['prediction'] - curr_data['Approved_Conversion'], label='Current Data')
    plt.title('Residuals Plot')
    plt.xlabel('Predictions')
    plt.ylabel('Residuals')
    plt.legend()
    plt.savefig('CML_Reports/residuals_plot.png')

    print(ref_data.head(5))
    print(curr_data.head(5))
    return ref_data, curr_data