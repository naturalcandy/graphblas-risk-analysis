from data_utils import read_data, write_data

if __name__ == "__main__":
    raw_data = read_data('data/raw/synthetic_data.csv')

    #perform preprocessing if needed here

    #use data_utils/preprocess_data functions to perform preprocessing

    write_data('data/processed/preprocessed_data.csv', raw_data)