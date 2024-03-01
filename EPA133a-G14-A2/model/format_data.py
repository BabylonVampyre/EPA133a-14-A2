import pandas as pd

# To help with printing
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 10)


def extract_data():
    """
    Extracts the data from the Excel file and removes all unnecessary information, and returns a dataframe.
    """
    # Assuming _roads3.csv is in the current directory
    file_path = "../data/BMMS_overview.xlsx"
    # Read the CSV file into a DataFrame
    df_read = pd.read_excel(file_path, header=0)  # header=0 means use the first row as column names
    # Select all rows where the column "road" is equal to "N1"
    bridge_df = df_read[df_read['road'] == 'N1']
    # List of column names to remove
    columns_to_remove = ['type', 'name',
                       'condition', 'structureNr', 'roadName',
                       'width', 'constructionYear', 'spans', 'zone', 'circle',
                       'division', 'sub-division', 'EstimatedLoc']
    # Drop the specified columns
    bridge_df = bridge_df.drop(columns=columns_to_remove)
    return bridge_df


def sort_and_remove_duplicates(df):
    """
    This method sorts the dataframe based on the LRPName, and then removes any duplicates from those columns
    """
    sorted_df = df.sort_values(by='LRPName')
    dropped_df = sorted_df.drop_duplicates(subset='LRPName', keep='first')
    dropped_df.reset_index(drop=True, inplace=True)
    return dropped_df


def add_modeltype_id_name(df):
    """
    This method adds a modeltype of bridge, renames the LRPName to id, and adds a name for each bridge
    """
    # Label all bridges as a bridge
    df['model_type'] = 'bridge'
    df = df.rename(columns={'LRPName': 'id'})
    # Add a column called 'name' filled with 'link' and a number from 1 to n
    df['name'] = 'bridge ' + (df.index + 1).astype(str)
    return df


def reorder_columns(df):
    """
    This method reorders the column so that they match the demo csv files.
    """
    # Define the desired column order
    desired_column_order = ['road', 'id', 'model_type', 'name', 'lat', 'lon', 'length']
    # Reassign the DataFrame with the desired column order
    df = df[desired_column_order]
    return df


def create_source_sink():
    """
    This method makes a source and a sink dataframe
    """
    global start_of_road_df, end_of_road_df
    # Read the CSV file into a DataFrame
    df = pd.read_csv("../data/_roads3.csv", header=0)
    # Select all rows where the column "road" is equal to "N1"
    road_df = df[df['road'] == 'N1']
    # add model types and names for the source and sink dataframes
    start_of_road_df = road_df[road_df['name'].str.startswith('Start of Road')].copy()
    start_of_road_df['model_type'] = 'source'
    start_of_road_df['name'] = 'source'
    end_of_road_df = road_df[road_df['name'].str.startswith('End of Road')].copy()
    end_of_road_df['model_type'] = 'sink'
    end_of_road_df['name'] = 'sink'
    return start_of_road_df, end_of_road_df


def format_source_sink(source_sink_df):
    """
    This method removes unnecessary columns from the dataframe, renames lrp to id, and adds a length
    of 0. It also calls the reorder method to order to columns in the same format.
    """
    # Remove unnecessary columns
    source_sink_df.drop(columns=['chainage', 'gap', 'type'], inplace=True)
    # Rename lrp to id
    source_sink_df = source_sink_df.rename(columns={'lrp': 'id'})
    # Add a length column, which is assumed to be 0
    source_sink_df['length'] = 0
    # Put them in the correct order.
    source_sink_df = reorder_columns(source_sink_df)
    return source_sink_df


# Here, all functions are called sequentially

# Get the right data, in this case: the N1 road without irrelevant columns
extracted_df = extract_data()

# Sort the data and remove the duplicates
sorted_df = sort_and_remove_duplicates(extracted_df)

# Add missing columns: model_type, id, name
full_df = add_modeltype_id_name(sorted_df)

# Reorder the columns so they match the format
reordered_df = reorder_columns(full_df)

# Create dataframes for the source and sink line
start_of_road_df, end_of_road_df = create_source_sink()

# Format these source and sink dataframes
formatted_start_of_road_df = format_source_sink(start_of_road_df)
formatted_end_of_road_df = format_source_sink(end_of_road_df)

# Insert the source before the main dataframe and the sink after words
combined_df = pd.concat([formatted_start_of_road_df, reordered_df, formatted_end_of_road_df])

# Display the DataFrame
print(combined_df)

# Save to a csv file in the same folder as the other demos
combined_df.to_csv('../data/N1.csv', index=False)
