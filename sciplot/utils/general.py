""" Just some general utilities """

def round_list(input, ndigits=3):
    """ Takes in a list of numbers and rounds them to a particular number of digits """
    return [round(i, ndigits) for i in input]