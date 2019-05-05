**Build Status**: ![Build Status](https://github.com/brandon-kyle-bailey/repo-badges/blob/master/svg/build-passing.svg)

# term-frequency-algorithm

Written in Python 3, This application is designed to return search query items using a "Term frequency Algorithm".

## Summary

The goal of this project was to create a program that would return relevant data to a user via a ranking system.
This ranking system implements the `term frequency inverse document frequency` - TF-IDF algorthim. This algorthim
is designed to reflect how important a word is to a document in a collection or corpus.

The data was to then recieve a score against this algorithm. This score would then be
responsible for the datas visibility. `Higher = More likely / Lower = Less likely`

## Getting Started

```
  - Unzip the file with : tar -xvf term-frequency-algorithm.tar.gz
  - cd term-frequency-algorithm
  - run "python -m virtualenv venv"
  - run "source venv/bin/activate"
  - run "venv/bin/pip install python3"
```
## Running the application

Once python3 is installed to your virtual environment. You can run the program by simply
navigating to the `/app` directory and running : `../venv/bin/python3 search.py "canada goose"`

This will return something along the lines of this:

```
0 {'id': 34322, 'name': 'Canada Goose Trillium Parka', 'brand': 'Canada Goose', 'score': 0.24074074074074073}
1 {'id': 34672, 'name': 'Canada Goose "Chateau" Parka', 'brand': 'Canada Goose', 'score': 0.23809523809523808}
2 {'id': 26578, 'name': 'Canada Goose Faux Fur Chiliwack Jacket', 'brand': 'Canada Goose', 'score': 0.21929824561403508}
3 {'id': 26575, 'name': 'Canada Goose Faux Fur Expedition Jacket', 'brand': 'Canada Goose', 'score': 0.21794871794871795}
4 {'id': 26576, 'name': 'Canada Goose Faux Fur Expedition Jacket', 'brand': 'Canada Goose', 'score': 0.21794871794871795}
5 {'id': 14054, 'name': 'CONSTABLE Parka', 'brand': 'Canada Goose', 'score': 0.16666666666666666}
6 {'id': 66784, 'name': 'Snogoose 09', 'brand': 'Baffin', 'score': 0.09090909090909091}
7 {'id': 62835, 'name': 'Long Sleeve Shirt', 'brand': 'Golden Goose', 'score': 0.08333333333333333}
8 {'id': 62953, 'name': 'Short Sleeve T-Shirt', 'brand': 'Golden Goose', 'score': 0.08333333333333333}
9 {'id': 56783, 'name': 'High-Top Sneaker', 'brand': 'Golden Goose', 'score': 0.08333333333333333}
Executed OK --- 1.0898122787475586 seconds ---
```

## Code run through

Lets break down what this is doing piece by piece.

In order to retrieve the `search_query` string, `sys.argv` is used:

```
        self.search_query = sys.argv[1:]
        if not self.search_query:
            raise RuntimeError("Need to specify search terms.")

```
If the user runs the tool without parsing any string after the script, a `RuntimeError` error will occur and notify the user that they
need to specify a string after the fact.

The rest of the action happens in the `main` function.

`        json_data = self.get_data_set(filename)`
This function acts as a wrapper to retrieve a json object from the search data set.

```
        if not os.path.exists(json_file):
            raise RuntimeError("Json file can not be found. Is it in root?")

```
If the json file cant be found. a `RuntimeError` error will occur and notify the user of this.

```
        for entry in json_data:

            name_frequency_value = self.get_frequency(search_words,
                                                        entry, "name")

            brand_frequency_value = self.get_frequency(search_words,
                                                        entry, "brand")

```
We then iterate over the data in the json object and call the `get_frequency` function.

This function behaves as a wrapper to another function `get_term_frequency`. This allows us to use the function for different types of input. In this case the `name` and `brand` keys respectively.

```
        entry_data = entry.get(name, None)

        # if entry key can not be retrieved, data is corrupt and we
        # should exit and notify the user
        if not entry_data:
            raise ValueError("entry_data for 'name' field is empty.")

```
If no data can be found then a `ValueError` is raised notifying the user there is an issue with the source data.

`get_term_frequency` returns a dictionary of search items
and their corresponding frequency score against entry data.

```
        cleaned_words = [word.lower() for word in words]
        cleaned_entry = ' '.join([item.lower() for item in entry.split(' ')])

```
The data is first standardized, *converted from upper case to lower case*, to allow for more consistent results.

```
        for word, count in word_dict.items():
            frequency_dict[word] = count/float(entry_length)

```
Each word is then given a value based on the number of occurrences within the source data and is then averaged based on the length of the source data array.

```
            sum_dict = name_frequency_value.copy()
            for key, value in name_frequency_value.items():
                sum_dict[key] += brand_frequency_value[key]
```
The returning dictionaries are then flatterned to form a single dictionary of words and their corresponding averaged frequency.

These frequency values are then summed and parsed in to a new `score` key which is defined in the current json data iteration:

`            entry['score'] = sum(sum_dict.values())`

### Getting ranked output

To return the most relevant Nth number of entries in the data, a function called `get_top_ranking` is used.

This function takes default the keyword argument `level` with the value `10`.

```
        temp_data = json_data

        # iterate through the temporary object using the level value as
        # a range and retrieve the highest scoring entry and
        top_rank_list = list()
        for i in range(level):

            top_rank_list.append(max(temp_data,
                                    key=lambda x: x['score']))

            temp_data.remove(max(temp_data,
                                    key=lambda x: x['score']))
```

The json data is parsed to a variable that can be manipulated without sacrificing the integrity of the json data object should any overwritting take place.

- We iterate Nth number of times. Each time obtaining the max score for all elements in `temp_data`
- Then append that specific element to the `top_rank_list`
- And remove the element in question from `temp_data`

Once this is complete, the data is returned to the user in a *0-Nth* list as seen above.

```
0 {'id': 34322, 'name': 'Canada Goose Trillium Parka', 'brand': 'Canada Goose', 'score': 0.24074074074074073}
1 {'id': 34672, 'name': 'Canada Goose "Chateau" Parka', 'brand': 'Canada Goose', 'score': 0.23809523809523808}
2 {'id': 26578, 'name': 'Canada Goose Faux Fur Chiliwack Jacket', 'brand': 'Canada Goose', 'score': 0.21929824561403508}
3 {'id': 26575, 'name': 'Canada Goose Faux Fur Expedition Jacket', 'brand': 'Canada Goose', 'score': 0.21794871794871795}
4 {'id': 26576, 'name': 'Canada Goose Faux Fur Expedition Jacket', 'brand': 'Canada Goose', 'score': 0.21794871794871795}
5 {'id': 14054, 'name': 'CONSTABLE Parka', 'brand': 'Canada Goose', 'score': 0.16666666666666666}
6 {'id': 66784, 'name': 'Snogoose 09', 'brand': 'Baffin', 'score': 0.09090909090909091}
7 {'id': 62835, 'name': 'Long Sleeve Shirt', 'brand': 'Golden Goose', 'score': 0.08333333333333333}
8 {'id': 62953, 'name': 'Short Sleeve T-Shirt', 'brand': 'Golden Goose', 'score': 0.08333333333333333}
9 {'id': 56783, 'name': 'High-Top Sneaker', 'brand': 'Golden Goose', 'score': 0.08333333333333333}
Executed OK --- 1.0898122787475586 seconds ---
```

## Built With

Python3

## Author

* **Brandon Bailey** - *Initial work* - [github-profile](https://github.com/brandon-kyle-bailey)
