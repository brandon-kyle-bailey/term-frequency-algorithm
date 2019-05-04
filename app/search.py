#!/usr/bin/env python3

import os
import sys
import json
import math
import time


class Search:

    def __init__(self):

        self.search_query = sys.argv[1:]
        self.main()

    def get_data_set(self, filename):
        """ Retrieves json object from json file specifiec

        args:
            filename : name of file

        returns:
            data : json data object
        """

        root = os.getcwd()

        json_file = os.path.join(root, filename)

        if not os.path.exists(json_file):
            raise RuntimeError("Json file can not be found. Is it in root?")

        # open json file and explicity define utf8 encoding as
        # explicit defining is needed if running on windows
        with open(json_file, encoding="utf8") as data_set:
            data = json.load(data_set)

        return data

    def get_term_frequency(self, words, entry):
        """algorithm to return a dictionary of search items
        and their corresponding frequency score against entry
        data.

        args:
            words : search item words
            entry : speicif entry from json object

        returns:
            frequency_dict : dictionary of word/score pairs
        """

        # clean data for both search items and json entry data
        cleaned_words = [word.lower() for word in words]
        cleaned_entry = ' '.join([item.lower() for item in entry.split(' ')])

        # form dictionary template using cleaned search items
        word_dict = dict.fromkeys(cleaned_words, 0)

        # append word frequency value with its count presense in json
        # data object
        for word in cleaned_words:
            word_dict[word] = cleaned_entry.count(word)

        frequency_dict = dict()
        entry_length = len(cleaned_entry)

        # iterate over words in dictionary and devide its
        # count value by the length of the entry to create
        # an average frequency value
        for word, count in word_dict.items():
            frequency_dict[word] = count/float(entry_length)

        return frequency_dict

    def get_frequency(self, search_words, entry, name):
        """Retrieves the specific key value from the entry and
        returns the frequency value of the search items

        args:
            search_words : list of search items
            entry : specific entry from json data
            name : name of key to retrieve value of

        returns:
            frequency_value : dictionary value of words and frequencies
        """

        entry_data = entry.get(name, None)

        # if entry key can not be retrieved, data is corrupt and we
        # should exit and notify the user
        if not entry_data:
            raise ValueError("entry_data for 'name' field is empty.")

        frequency_value = self.get_term_frequency(search_words, entry_data)

        return frequency_value

    def get_top_ranking(self, json_data, level=10):
        """Used to retrieve N number of highest ranks.
        default is 10

        args:
            json_data : json_data for rank retrieval
            level : number of returned highest ranks

        returns:
            top_rank_list : list of top ranked items
        """

        # create a temporary data object for iteration
        temp_data = json_data

        # iterate through the temporary object using the level value as
        # a range and retrieve the highest scoring entry and
        top_rank_list = list()
        for i in range(level):

            top_rank_list.append(max(temp_data,
                                    key=lambda x: x['score']))

            temp_data.remove(max(temp_data,
                                    key=lambda x: x['score']))

        return top_rank_list

    def main(self):

        filename = "search_dataset.json"
        json_data = self.get_data_set(filename)

        search_words = self.search_query[0].split(' ')

        # for each entry in json data, retrieve the frequency of
        # name and brand objects, flattern the frequency values.
        # create a score key for the entry and append current score.
        for entry in json_data:

            name_frequency_value = self.get_frequency(search_words,
                                                        entry, "name")

            brand_frequency_value = self.get_frequency(search_words,
                                                        entry, "brand")

            # here we flattern the two frequency dictionaries to get
            # a single dictionary of words and their frequency values.
            sum_dict = name_frequency_value.copy()
            for key, value in name_frequency_value.items():
                sum_dict[key] += brand_frequency_value[key]

            entry['score'] = sum(sum_dict.values())

        # return top ranking entries
        top_ranking = self.get_top_ranking(json_data, level=10)
        for tally, result in enumerate(top_ranking):
            print(tally, result)


if __name__ == "__main__":

    start = time.time()

    Search()

    print(f"Executed OK --- {(time.time() - start)} seconds ---")
