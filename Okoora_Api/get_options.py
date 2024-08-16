import itertools


def get_convert_option():
    options = ["USD","ILS", None, "DDD", "NIS","",True,False]
    matrix = [list(pair) for pair in itertools.product(options, repeat=4)]
    for item in matrix:
        yield item


def get_quote_option():
    options = ["USD","ILS", "EUR","GBP"]
    matrix = [list(pair) for pair in itertools.product(options, repeat=2)]
    for item in matrix:
        if item[0]!= item[1]:
            yield item

