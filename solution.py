
import csv

def get_csv_data(filepath):
    """
    Opens the file at filepath, reads the data using the csv module's DictReader, 
    converts that data to a regular list and returns that list.

    :param filepath: The file path of the CSV data file to open
    :returns: A list of dictionaries, where each dictionary represents one row from the file
    """
    
    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    
    return data

def remove_rows_with_blank_neighborhood_fields(data):
    """
    Removes any rows with blank 'nta' or 'nta_code' fields from the data set

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """

    return [row for row in data if row['nta'] and row['nta_code']]

def remove_out_of_range_entries(data, lat_range, lng_range):
    """
    Removes any entries which has latitude and longitude values out of range.
    
    :param data: The data, as a list of dictionaries
    :param lat_range: tuple (Float, Float) representing the permissable range of latitude values
    :param long_range: tuple (Float, Float) representing the permissable range of longitude values
    :returns: The modified data, as a list of dictionaries
    """

    return [row for row in data if lat_range[0] <= float(row['latitude']) <= lat_range[1] and lng_range[0] <= float(row['longitude']) <= lng_range[1]]

def make_type_free_default(data):
    """
    Makes 'Free' as the default 'type'. Any entries with empty values of 'type' are set to 'Free'.

    :param data: The data, as a list of dictionaries
    :returns: The modified data as a list of dictionaries
    """
    for row in data:
        if not row['type']:
            row['type'] = 'Free'
    return data

def remove_non_free_rows(data):
    """
    Removes any rows with anything other than 'Free' in the 'type' field.

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    return [row for row in data if row['type'] == 'Free']

def make_location_title_case(data):
    """
    Puts the data in the 'location' field into Title Case, where the first letter of each word is capitalized.

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    for row in data:
        row["location"] = row["location"].title()
    return data

def fix_provider(data, old_provider, new_provider):
    """
    Swaps out the old provider name with the updated new provider name for any rows that match.

    :param data: The data, as a list of dictionaries
    :param old_provider: The old provider name to remove, e.g. 'SpotOnNetworks'
    :param new_provider: The new domain to replace the old_domain with, e.g. 'Spot On Networks'
    :returns: The modified data, as a list of dictionaries
    """
    for row in data:
        if row["provider"] == old_provider:
            row["provider"] = new_provider
    return data

def save_csv_data(data, filepath):
    """
    Saves the data into the specified file.  Include the field headers as the first row.

    :param data: The data, as a list of dictionaries
    :param filepath: The file path of the CSV data file to save to
    """
    with open(filepath, mode='w', newline='') as csv_file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def get_number_free_hotspots(filepath, neighborhood):
    """
    Calculates the number of free Wi-Fi hotspots in the given neighborhood.

    :param filepath: The file path of the CSV data file to open
    :param neighborhood: The neighborhood within which to count free wifi hotspots
    :returns: The number of free wifi hotspots within the indicated neighborhood
    """
    with open(filepath, mode= "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        num = sum(1 for row in csv_reader if row["nta"] == neighborhood and row['type'] == 'Free')
    return num

#################################################
## Do not modify the code below this line      ##
## except to comment out any function calls    ##
## that you do not wish to test at the moment  ##
#################################################

def main():
    ## use the functions defined above to complete munging of the data file

    # get the data from the file
    data = get_csv_data('data/wifi.csv')
    
    # munge it
    data = remove_rows_with_blank_neighborhood_fields(data)
    data = remove_out_of_range_entries(data, (40.5095311, 40.9037228), (-74.244107, -73.714838))
    data = make_type_free_default(data)
    data = remove_non_free_rows(data)
    data = make_location_title_case(data)
    data = fix_provider(data, 'SpotOnNetworks', 'Spot On Networks')

    # save to the new csv file
    save_csv_data(data, 'data/wifi_clean.csv')

    # print the average cost per impression from the data in the file
    num = get_number_free_hotspots('data/wifi_clean.csv', 'Fort Greene')
    print('There are ' + str(num) + ' free Wi-Fi hotspots in Fort Greene, Brooklyn.') 

if __name__ == "__main__":
    main()
