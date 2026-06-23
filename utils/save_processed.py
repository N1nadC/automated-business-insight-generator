def save_processed(processed_data):

    for name, df in processed_data.items():
        path = f"data/processed/{name}.csv"
        df.to_csv(path, index=False)

    print("Processed datasets saved successfully.")