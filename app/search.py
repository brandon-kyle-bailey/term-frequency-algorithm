#!/usr/bin/env python3.7

import os
import sys
import json
import math



class Search:

	def __init__(self):
		self.search_query = sys.argv[1:]
		self.main()


	def get_data_set(self, filename):

		json_file = os.path.join(os.getcwd(),
									filename)

		with open(json_file) as data_set:
			data = json.load(data_set)

		return data

	def get_term_frequency(self, words, entry):

		words = [w.lower() for w in words]
		entry = ' '.join([e.lower() for e in entry.split(' ')])

		word_dict = dict.fromkeys(words, 0)

		for word in words:
			word_dict[word] = entry.count(word)

		out_dict = dict()
		counter = len(entry)

		for word, count in word_dict.items():
			out_dict[word] = count/float(counter)

		return out_dict

	def get_frequency(self, search_words, entry, name):

		entry_data = entry.get(name, None)
		if not entry_data:
			raise ValueError("entry_data for 'name' field is empty.")

		frequency_value = self.get_term_frequency(search_words, entry_data)
		# print(frequency_value)

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

		temp_data = json_data

		top_rank_list = list()
		for i in range(level):
			top_rank_list.append(max(temp_data, key=lambda x: x['score']))
			temp_data.remove(max(temp_data, key=lambda x: x['score']))

		return top_rank_list		 

	def main(self):

		filename = "search_dataset.json"
		json_data = self.get_data_set(filename)

		search_words = self.search_query[0].split(' ')
		
		for entry in json_data:

			name_frequency_value = self.get_frequency(search_words, entry, "name")
			brand_frequency_value = self.get_frequency(search_words, entry, "brand")

			out_dict = name_frequency_value.copy()
			for key, value in name_frequency_value.items():
				out_dict[key] += brand_frequency_value[key]

			entry['score'] = sum(out_dict.values())


		top_ranking = self.get_top_ranking(json_data, level=10)
		for num, i in enumerate(top_ranking): print(num, i)


if __name__ == "__main__":

    Search()

