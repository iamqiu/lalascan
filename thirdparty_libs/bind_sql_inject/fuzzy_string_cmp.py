#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import difflib
import pprint

from upper_bounds import UPPER_BOUNDS

def relative_distance_boolean(a_str, b_str, threshold=0.6):
    """
    Indicates if the strings to compare are similar enough. This (optimized)
    function is equivalent to the expression:
        relative_distance(x, y) > threshold

    :param a_str: A string object
    :param b_str: A string object
    :param threshold: Float value indicating the expected "similarity". Must be
                      0 <= threshold <= 1.0
    :return: A boolean value
    """

    if threshold == 0:
        return True
    elif threshold == 1.0:
        return a_str == b_str

    # First we need b_str to be the longer of both
    if len(b_str) < len(a_str):
        a_str, b_str = b_str, a_str

    alen = len(a_str)
    blen = len(b_str)

    if blen == 0 or alen == 0:
        return alen == blen

    if blen == alen and a_str == b_str and threshold <= 1.0:
        return True

    ratio = float(blen) / alen

    last_ratio, last_bound = UPPER_BOUNDS[-1]

    if threshold < last_bound:
        # Bad, we can't optimize anything here
        return relative_distance(a_str, b_str) >= threshold
    else:
        if last_ratio < ratio:
            # Good, we know the upper bound
            return False
        else:
            # We have to step through
            for size_ratio, bound in UPPER_BOUNDS:
                if size_ratio > ratio:
                    # Bad: we have to do the relative_distance
                    #print relative_distance(a_str, b_str)
                    return relative_distance(a_str, b_str) >= threshold
                elif bound < threshold:
                    # Good: We found an upper bound
                    return False


def fuzzy_equal(a_str, b_str, threshold=0.6):
    """
    Indicates if the 'similarity' index between strings
    is *greater equal* than 'threshold'. See 'relative_distance_boolean'.
    """
    return relative_distance_boolean(a_str, b_str, threshold)


def fuzzy_not_equal(a_str, b_str, threshold=0.6):
    """
    Indicates if the 'similarity' index between strings
    is *less than* 'threshold'
    """
    return not relative_distance_boolean(a_str, b_str, threshold)


def relative_distance(a_str, b_str):
    """
    Measures the "similarity" of the strings.

    Depends on the algorithm we finally implement, but usually a return value
    over 0.6 means the strings are close matches.

    :param a_str: A string object
    :param b_str: A string object
    :return: A float with the distance
    """
    set_a = set(a_str.split(' '))
    set_b = set(b_str.split(' '))

    if min(len(set_a), len(set_b)) in (0, 1):
        #
        #   This is a rare case, where the http response body is one long
        #   non-space separated string.
        #
        return difflib.SequenceMatcher(None, a_str, b_str).quick_ratio()

    return 1.0 * len(set_a.intersection(set_b)) / max(len(set_a), len(set_b))


def _generate_upper_bounds():
    """
    This function can be used to produce new upper bounds,
    but shouldn't be used in productive code. Simply run this
    command once and then hardcode the list.
    """

    left_max = 40
    right_max = 30

    UPPER_BOUNDS = set()
    UPPER_BOUNDS.add((1.0, 1.0))

    def add_to_bounds(a, b):
        size = float(len(b)) / len(a)
        upper_bound = relative_distance(a, b)
        UPPER_BOUNDS.add((size, upper_bound))

    for k in range(1, left_max):
        for i in range(1, right_max):
            if k == i == 1:
                continue
            atest = 'm' * k
            btest = 'm' * k + 'm' * (i - 1)
            add_to_bounds(atest, btest)

    # Remove duplicates
    UPPER_BOUNDS = list(UPPER_BOUNDS)

    # Sort
    UPPER_BOUNDS.sort(lambda x, y: cmp(x[0], y[0]))

    fp = file("upper_bounds.py", "w")
    fp.write("UPPER_BOUNDS = ")
    pprint.pprint(UPPER_BOUNDS, fp)
    fp.close()


if __name__ == "__main__":
    # Uncomment next function call to generate 'upper_bounds.py' module
    #_generate_upper_bounds()

    # These tests should be reallocated in a test module.
    import time
    import urllib2

    performance_tests = []

    #performance_tests.append(('a'*25000,'a'*25000,0.999 ))
    #performance_tests.append(('a'*12000, 'a'*25000, 0.9999))
    #performance_tests.append(('a'*20000, 'a'*25000, 0.1))

    #google = urllib2.urlopen("http://demo.aisec.cn/demo/aisec/html_link.php?id=2").read()
    #google2 = urllib2.urlopen("http://demo.aisec.cn/demo/aisec/html_link.php?id=2%27").read()

    '''
    yahoo = urllib2.urlopen("http://www.yahoo.com/").read()
    yahoo2 = urllib2.urlopen("http://uk.yahoo.com/").read()

    bing = urllib2.urlopen("http://www.bing.com/").read()
    bing2 = urllib2.urlopen("http://www.bing.com/?cc=gb").read()

    '''
    #True
    #performance_tests.append((google, google, 0.99999999))
    print relative_distance_boolean("ecd", "ckdp", 0.6)
    #print relative_distance_boolean(google, google2, 0.66)
