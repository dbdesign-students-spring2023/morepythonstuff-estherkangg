import os
import csv
import random
import pandas as pd
from copy import deepcopy
from solution import *

random.seed(10)

def remove_blank_loc(data):
  result = list()
  for record in data:
    if record['nta'] == "" or record['nta_code'] == "":
      pass
    else:
      result.append(record)
  return result

def remove_outside_range(data, lat_range, lng_range):
  result = list()
  for record in data:
    if lat_range[0] <= float(record['latitude']) <= lat_range[1] and lng_range[0] <= float(record['longitude']) <= lng_range[1]:
      result.append(record)
  return result

def make_default(data):
  result = list()
  for record in data:
    if record['type'] == "":
      record['type'] = "Free"
    result.append(record)
  return result

def keep_free(data):
  result = list()
  for record in data:
    if record['type'] == "Free":
      result.append(record)
  return result

def loc_title(data):
  result = list()
  for record in data:
    record['location'] = record['location'].title()
    result.append(record)
  return result

def provider_fixer(data, new_prov, old_prov):
  result = list()
  for record in data:
    if record['provider'] == old_prov:
      record['provider'] = new_prov
    result.append(record)
  return result

def count_free(data, neighborhood):
  count = 0
  for rec in data:
    if rec['nta'] == neighborhood:
      count += 1
  return count

wifi_data_filepath = os.path.join(os.getcwd(), "data/wifi.csv")
save_path = os.path.join(os.getcwd(), "data/wifi_clean.csv")
exp_wifi_df = pd.read_csv(wifi_data_filepath)
exp_wifi_data = list(csv.DictReader(open(wifi_data_filepath, "r")))
exp_wifi_clean_data = list(csv.DictReader(open(save_path, "r")))

exp_wifi_data_no_blanks = remove_blank_loc(deepcopy(exp_wifi_data))
exp_wifi_df_no_blanks = pd.DataFrame(exp_wifi_data_no_blanks)

exp_wifi_data_within_range = remove_outside_range(deepcopy(exp_wifi_data_no_blanks), (40.5095311, 40.9037228), (-74.244107, -73.714838))
exp_wifi_df_within_range = pd.DataFrame(exp_wifi_data_within_range)

exp_wifi_data_defaulted = make_default(deepcopy(exp_wifi_data_within_range))
exp_wifi_df_defaulted = pd.DataFrame(exp_wifi_data_defaulted)

exp_wifi_data_only_free = keep_free(deepcopy(exp_wifi_data_defaulted))
exp_wifi_df_only_free = pd.DataFrame(exp_wifi_data_only_free)

exp_wifi_data_title_loc = loc_title(deepcopy(exp_wifi_data_only_free))
exp_wifi_df_title_loc = pd.DataFrame(exp_wifi_data_title_loc)

exp_wifi_data_mod_prov = provider_fixer(deepcopy(exp_wifi_data_title_loc), 'SpotOnNetworks', 'Spot On Networks')
exp_wifi_df_mod_prov = pd.DataFrame(exp_wifi_data_mod_prov)

exp_free_wifi_count = count_free(deepcopy(exp_wifi_clean_data), 'Fort Greene')


class Tests:
  def test_get_csv_data_shape(self):
    actual_wifi_data = get_csv_data(wifi_data_filepath)
    assert actual_wifi_data != None
    assert len(actual_wifi_data) == exp_wifi_df.shape[0]
    assert all([len(x) == exp_wifi_df.shape[1] for x in actual_wifi_data])

  def test_remove_rows_with_blank_neighborhood_fields(self):
    returned_data = remove_rows_with_blank_neighborhood_fields(deepcopy(exp_wifi_data))
    assert returned_data != None
    assert len(returned_data) == exp_wifi_df_no_blanks.shape[0]
    assert all([len(x) == exp_wifi_df_no_blanks.shape[1] for x in returned_data])

  def test_remove_out_of_range_entries(self):
    returned_data = remove_out_of_range_entries(deepcopy(exp_wifi_data_no_blanks), (40.5095311, 40.9037228), (-74.244107, -73.714838))
    assert returned_data != None
    assert len(returned_data) == exp_wifi_df_within_range.shape[0]
    assert all([len(x) == exp_wifi_df_within_range.shape[1] for x in returned_data])
    assert all([40.5095311 <= float(x['latitude']) <= 40.9037228 and -74.244107 <= float(x['longitude']) <= -73.714838 for x in returned_data])

  def test_make_type_free_default(self):
    returned_data = make_type_free_default(deepcopy(exp_wifi_data_within_range))
    assert returned_data != None
    assert len(returned_data) == exp_wifi_df_defaulted.shape[0]
    assert all([len(x) == exp_wifi_df_defaulted.shape[1] for x in returned_data])
    assert all([rec['type'] != "" for rec in returned_data])

  def test_remove_non_free_rows(self):
    returned_data = remove_non_free_rows(deepcopy(exp_wifi_data_defaulted))
    assert returned_data != None
    assert len(returned_data) == exp_wifi_df_only_free.shape[0]
    assert all([len(x) == exp_wifi_df_only_free.shape[1] for x in returned_data])
    assert all([rec['type'] == 'Free' for rec in returned_data])
  
  def test_make_location_title_case(self):
    returned_data = make_location_title_case(deepcopy(exp_wifi_data_only_free))
    assert returned_data != None
    assert len(returned_data) == exp_wifi_df_title_loc.shape[0]
    assert all([len(x) == exp_wifi_df_title_loc.shape[1] for x in returned_data])
    assert all([x['location'] == y['location'] for x, y in zip(returned_data, exp_wifi_data_title_loc)])

  def test_fix_provider(self):
    returned_data = fix_provider(deepcopy(exp_wifi_data_title_loc), 'SpotOnNetworks', 'Spot On Networks')
    assert returned_data != None
    assert len(returned_data) == exp_wifi_df_mod_prov.shape[0]
    assert all([len(x) == exp_wifi_df_mod_prov.shape[1] for x in returned_data])
    assert all([x['provider'] != 'SpotOnNetworks' for x in returned_data])

  def test_save_csv_data(self):
    assert os.path.exists(save_path)
    assert os.stat(save_path).st_size > 100

  def test_get_number_free_hotspots(self):
    returned_count = get_number_free_hotspots(save_path, 'Fort Greene')
    assert returned_count != None
    assert returned_count == exp_free_wifi_count