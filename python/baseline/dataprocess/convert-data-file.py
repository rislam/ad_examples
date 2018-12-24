import numpy as np
import pandas as pd
import os, time
from os.path import join
from ..malware.baseline_util import parse_arguments, compute_f1, get_seed
from aad.data_stream import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common.utils import *
from pprint import pprint

# missing value handling
from io import StringIO
import pickle
import random
from random import shuffle

def read_pickle(file_name=None):
    """
    Read a pickle file and return the dictionary
    :param file_name:
    :return: dictionary
    """
    if file_name is not None:
        loaded_file = open(file_name, "rb")
        features = pickle.load(loaded_file, encoding="UTF8")
        return features
    return None


def convert_dictionary_to_df(feature_dictionary):
    """
    process a given feature dictionary to a nice data frame format
    :param feature_dictionary:
    :return: dataframe in apk indexed
    """
    df_features = pd.DataFrame(feature_dictionary)
    df_features_T = df_features.T
    assert len(df_features.index) == len(set(df_features_T))
    return df_features_T


def get_all_apk_count(years, features, directory):
    """
    Produce the APK count and feature count for each feature file
    :return:
    """
    for year in years:
        apks_list_all = []
        print("##########year-start##########")
        dir_str = "malware-" + str(year) + "-all-" + str(year)
        year_directory = join(directory, dir_str)
        for feature in features:
            print("****reading for year %d and feature type %s " % (year, feature), end="\n")
            year_feature_directory = join(year_directory, feature)

            for dirname, dirnames, filenames in os.walk(year_feature_directory):
                #                 print(dirname, dirnames, filenames)
                for f_name in filenames:
                    #                     if "zoobenign" not in f_name or
                    year_feature_file_name = join(year_feature_directory, f_name)
                    if "csv" not in f_name:
                        print("feature count for ", f_name, end=" ")
                        dict_features = read_pickle(file_name=year_feature_file_name)
                        apks_list = list(dict_features.index)
                        apks_list_all.append(apks_list)
                    #                         dictonary_to_dataframe(dict_features)
                    else:
                        data = pd.read_csv(year_feature_file_name)
                        print(f_name, " shape ", data.shape)
        print("##########year-end##########")
        return apks_list_all


def in_ignore_list(file_name):
    return "static.pickle.benign" in file_name or "combined" in file_name


def is_benign_file(file_name):
    return "benign" in file_name \
           or "zoobenign" in file_name \
           or "benigns" in file_name


def is_malware_file(file_name):
    return not is_benign_file(file_name) or "anomalies" in file_name


def get_AdaDroid_apks(directory, dir_str):
    """
    Return Adadroid Features as a data-frame
    :param directory:
    :param year:
    :return:
    """
    year_feature_directory = join(directory, dir_str, "fullsamples")
    print(year_feature_directory)
    malware_apks = None
    benign_apks = None
    for dirname, dirnames, filenames in os.walk(year_feature_directory):
        for f_name in filenames:
            file_to_read = join(year_feature_directory, f_name)
            if "anomalies" in f_name:
                df = pd.read_csv(file_to_read, skiprows=1, header=None)
                malware_apks = list(df[0])
            elif "benigns" in f_name:
                df = pd.read_csv(file_to_read, skiprows=1, header=None)
                benign_apks = list(df[0])
    print(len(benign_apks), len(malware_apks))
    return benign_apks, malware_apks


def get_MamaDroid_features(directory, year):
    """
    Return MamaDroid Features as a data-frame
    :param directory:
    :param year:
    :return:
    """
    pass


def get_year_apks(year=2010, directory=None, features=None):
    """
    Return all features common apks for the given year.
    :param year:int
    :param directory:str
    :param features:pandas data-frame
    :return:
    """
    dir_str = "malware-" + str(year) + "-all-" + str(year)
    year_directory = join(directory, dir_str)
    apks_map = {}

    for feature in features:
        # print("****For year %d and feature name %s " % (year, feature), end="\n")
        if "AdaDroid" in feature:
            adadroid_directory = "/Users/mislam1/Documents/RA/research-2018/sequential-anomaly-detection/src/temp/dataset-checking"
            benign, anomaly = get_AdaDroid_apks(adadroid_directory, dir_str)
            apks_map[feature + "-malware"] = anomaly
            apks_map[feature + "-benign"] = benign
        else:
            year_feature_directory = join(year_directory, feature)
            for dirname, dirnames, filenames in os.walk(year_feature_directory):
                for f_name in filenames:
                    # print("processing file: ", f_name)
                    if in_ignore_list(f_name) or ".DS_Store" in f_name:
                        print("ignoring file ", f_name)
                        continue
                    if is_malware_file(f_name):
                        key = feature + "-malware"
                    if is_benign_file(f_name):
                        key = feature + "-benign"
                    year_feature_file_name = join(year_feature_directory, f_name)
                    # print("key name ", key)
                    # print("year_feature_file_name ", year_feature_file_name)
                    if "csv" not in f_name:
                        # print("feature count for ", f_name, end=" ")
                        dict_features = read_pickle(file_name=year_feature_file_name)
                        features_df = convert_dictionary_to_df(dict_features)
                        apks_list = features_df.index.values
                        # dictonary_to_dataframe(dict_features)
                    else:
                        features_df = pd.read_csv(year_feature_file_name)
                        col_names = list(features_df.columns.values)
                        mod_col_name = list()
                        for item in col_names:
                            mod_col_name.append(item.replace("\'", "").replace(".", "")
                                                .replace("\'", ""))
                        features_df.columns = mod_col_name
                        # print(f_name, " shape ", features_df.shape)
                        # print(features_df.columns)
                        # print(features_df.head())
                        if 'Unnamed: 0' in features_df.columns:
                            apks_list = list(features_df['Unnamed: 0'].values)
                        else:
                            apks_list = list(features_df['filename'].values)
                    features_df.fillna(0)
                    apks_map[key] = apks_list
                    # print("adding ", key, " length ", len(apks_list))
    return apks_map


def get_AdaDroid_feature(directory, dir_str):
    year_feature_directory = join(directory, dir_str, "fullsamples")
    print(year_feature_directory)
    feat_filename = join(year_feature_directory, dir_str + "_1.csv")
    feat_df = pd.read_csv(feat_filename)
    return feat_df


def convert_column_names(column_names):
    mod_col_name = list()
    for item in column_names:
        mod_col_name.append(item.replace("\'", "").replace(".", "")
                            .replace("\'", "").lower())

    return mod_col_name


def save_apk_features(benign_apks, malware_apks, year=2010, directory=None, features=None):
    dir_str = "malware-" + str(year) + "-all-" + str(year)
    year_directory = join(directory, dir_str)
    year_feature_directory = None
    combined_apks = list()
    combined_apks.extend(benign_apks)
    combined_apks.extend(malware_apks)
    shuffle(combined_apks)
    all_feature_map = {}
    for feature in features:
        # print("****For year %d and feature name %s " % (year, feature), end="\n")
        if "AdaDroid" in feature:
            year_feature_directory = "/Users/mislam1/Documents/RA/research-2018/sequential-anomaly-detection/src/temp/dataset-checking"
            feature_df = get_AdaDroid_feature(year_feature_directory, dir_str)
            # print(feature_df.ix[combined_apks])
            combined_features = feature_df.ix[combined_apks]
        else:
            year_feature_directory = join(year_directory, feature)
            combined_features = None
            combined_df = None
            for dirname, dirnames, filenames in os.walk(year_feature_directory):
                for f_name in filenames:
                    print("processing file: ", f_name)
                    features_df = None
                    if in_ignore_list(f_name) or ".DS_Store" in f_name:
                        print("ignoring file ", f_name)
                        continue
                    if is_malware_file(f_name):
                        key = feature + "-malware"
                    if is_benign_file(f_name):
                        key = feature + "-benign"
                    year_feature_file_name = join(year_feature_directory, f_name)
                    # print("key name ", key)
                    # print("year_feature_file_name ", year_feature_file_name)
                    if "csv" not in f_name:
                        # print("feature count for ", f_name, end=" ")
                        dict_features = read_pickle(file_name=year_feature_file_name)
                        features_df = convert_dictionary_to_df(dict_features)
                        col_names = list(features_df.columns.values)
                        print("before set ", len(col_names), end="")
                        features_df.columns = convert_column_names(col_names)
                        col_set = set(features_df.columns.values)
                        sorted_col = sorted(list(col_set))
                        # features_df = features_df[sorted_col]
                        features_df = features_df.loc[:, ~features_df.columns.duplicated()]
                        print(" after set ", len(sorted_col), " feature df ", features_df.shape)
                    else:
                        features_df = pd.read_csv(year_feature_file_name)
                        col_names = list(features_df.columns.values)
                        print("before set ", len(col_names), end="")
                        features_df.columns = convert_column_names(col_names)
                        col_set = set(features_df.columns.values)
                        sorted_col = sorted(list(col_set))
                        # features_df = features_df[sorted_col]
                        features_df = features_df.loc[:, ~features_df.columns.duplicated()]
                        print(" after set ", len(sorted_col), " feature df ", features_df.shape)

                        print(f_name, " shape ", features_df.shape)
                        # print(features_df.columns)
                        # apks_list = list(features_df['Unnamed: 0'].values)
                        if 'Unnamed: 0' in features_df.columns:
                            apks_list = list(features_df['Unnamed: 0'].values)
                            features_df.set_index('Unnamed: 0', inplace=True)
                        else:
                            apks_list = list(features_df['filename'].values)
                            features_df.set_index('filename', inplace=True)
                    # print("adding ", key, " length ", len(apks_list))

                    if "malware" in key and 'label' not in features_df.columns:
                        labels = ['anomaly'] * features_df.shape[0]
                        features_df.insert(loc=0, column='label', value=labels)
                    elif 'benign' in key and 'label' not in features_df.columns:
                        labels = ['nominal'] * features_df.shape[0]
                        features_df.insert(loc=0, column='label', value=labels)
                    print("after addition \n", features_df.columns[:3])

                    if combined_df is None:
                        combined_df = features_df.copy()
                        print("**Initial combined df, ", combined_df.shape)
                    else:
                        print("features_df.shape ", features_df.shape, features_df.columns[:3])
                        combined_df = combined_df.append(features_df)
                        print("**joint combined df, ", combined_df.shape)
                    print(combined_df.columns[:3])

                combined_df.fillna(0)
                print(combined_df.shape, year_feature_directory)
                combined_features = combined_df.ix[combined_apks]
        write_to_file(combined_features, combined_apks, year_feature_directory, feature)
        all_feature_map [str(year) + "-" + feature + "-merged"] = combined_features
        print("%% saved ", str(year) + "-" + feature + "-merged")
    return all_feature_map


def write_to_file(df, apks_list, directory=None, feature=None):
    save_directory = join(directory, feature + "combined.csv")
    df.to_csv(save_directory)
    print("saved file ", save_directory)


def find_common_keys(apks_map):
    all_keys = apks_map.keys()
    common_malwares = None
    common_benigns = None
    for key in all_keys:
        if "malware" in key:
            if common_malwares is None:
                common_malwares = set(apks_map[key])
            common_malwares = common_malwares.intersection(set(apks_map[key]))

        if "benign" in key:
            if common_benigns is None:
                common_benigns = set(apks_map[key])
            common_benigns = common_benigns.intersection(set(apks_map[key]))
    print("#################")
    print("common benings ", len(common_benigns), " malwares ",
          len(common_malwares))
    print("#################")
    return common_benigns, common_malwares


def merge_all_years(yearwise_map, features, years):
    """
    Merge all years data frames using concat and outrt join of pandas
    :param yearwise_map:
    :param features:
    :param years:
    :return:
    """
    for feature in features:
        data_frames_list = list()
        for year in years:
            feature_keys = yearwise_map[str(year)].keys()
            print(feature_keys)
            for fk in feature_keys:
                if feature in fk:
                    data_frames_list.append(yearwise_map[str(year)][fk])
        # print(data_frames_list)
        result = data_frames_list[0].append(data_frames_list[1:])
        print(result.shape)
        with open(feature + "-columns.csv", "w") as f:
            col = result.columns.values
            for item in col:
                f.write(item + ",")
        result = None


def main():
    """main function, entry point"""
    random.seed(42)
    np.random.seed(5)
    start = time.time()
    directory = "/Users/mislam1/Documents/RA/research-2018/malware-detection/malware-dataset1218"
    years = [i for i in range(2010, 2017, 1)]
    # features = ['AdaDroid', 'DroidSieve', 'Revealdroid', 'Mamadroid',]
    features = ['AdaDroid', 'DroidSieve']
    feature_year_map = {}
    for y in years:
        apks_map = get_year_apks(y, directory, features)
        # print(apks_map)
        common_benigns, common_malwares = find_common_keys(apks_map)
        all_merged = save_apk_features(common_benigns, common_malwares, y, directory, features)
        feature_year_map[str(y)] = all_merged
        apks_map = None
    merge_all_years(feature_year_map, features, years)
    print("finished!! time taken ", (time.time() - start)/60.0)


if __name__ == '__main__':
    main()