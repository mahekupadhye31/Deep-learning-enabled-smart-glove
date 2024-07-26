import pandas as pd

# # Read the CSV file
# data = pd.read_csv("gesture_data_test_A.csv")

# # Group data by 'id' and 'gesture'
# grouped_data = data.groupby(['id', 'gesture'])

# # Initialize an empty DataFrame for the transformed data
# transformed_data = pd.DataFrame()

# # Iterate over each group
# for key, group in grouped_data:
#     # Concatenate the flex values, accelerometer, and gyroscope values into a single row
#     row = group[['flex0', 'flex1', 'flex2', 'flex3', 'flex4', 'ax', 'ay', 'az', 'gx', 'gy', 'gz']].values.flatten()
    
#     # Append the 'id' and 'gesture' columns
#     row = [key[0]] + row.tolist() + [key[1]]
    
#     # Create a DataFrame from the row
#     row_df = pd.DataFrame([row]).rename(columns={i: str(i) for i in range(len(row))})
    
#     # Append the row DataFrame to the transformed data
#     transformed_data = pd.concat([transformed_data, row_df], ignore_index=True)

# # Save the transformed data to a new CSV file
# transformed_data.to_csv("transformed_A.csv", index=False)



data = pd.read_csv('gesture_data_test_A.csv')
if data.empty:
        raise ValueError("Data file is empty")
flattened_data = data.values.flatten()

new_column_names = [f"{col}{i+1}" for i in range(data.shape[0]) for col in data.columns]
        
transformed_data = pd.DataFrame([flattened_data], columns=new_column_names)
transformed_data.to_csv("transformed_A.csv", index=False)
