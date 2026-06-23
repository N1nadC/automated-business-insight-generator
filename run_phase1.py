import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_ingestion import load_raw_data
from utils.data_processing import process_data
from utils.save_processed import save_processed

datasets = load_raw_data()
processed_data = process_data(datasets)
save_processed(processed_data)