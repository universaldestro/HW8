# Your name: 
# Your student id:
# Your email:
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def connset(db):
    conn = sqlite3.connect('/Users/Danie/Downloads/HW8/South_U_Restaurants.db')
    cur = conn.cursor()
    return (cur,conn)

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    start = connset(db)
    d = {}
    cur = start[0]
    cur2 = cur
    cur3 =cur
    cur.execute( 'SELECT * FROM restaurants')
    restaurants = cur.fetchall()
    for row in restaurants:
      cate_id = row[2]
      build_id = row[3]
      rating = row[4]
      cur2.execute('SELECT category FROM categories WHERE id = ?',(cate_id,))
      cate = cur2.fetchone()[0]
      cur3.execute('SELECT building FROM buildings WHERE id = ?',(build_id,))
      build = cur3.fetchone()[0]
      d[row[1]] = {'category':cate,'building':build,'rating':rating}
    return d


def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    d = {}
    start = connset(db)#
    cur = start[0]
    cur.execute('SELECT id  FROM categories')
    ids = cur.fetchall()
    data = []
    x_axis = [] 
    y_axis=[]
    for id in ids:
        cur.execute('SELECT categories.category, COUNT(restaurants.category_id) FROM restaurants JOIN categories ON categories.id = restaurants.category_id WHERE restaurants.category_id = ?',(id[0],)) 
        cates = cur.fetchone()
        data.append(cates)
        d[cates[0]] =cates[1]
    data = sorted(data, key = lambda x: x[1])
    for tup in data:
        x_axis.append(tup[0])
        y_axis.append(tup[1])
    plt.barh(x_axis,y_axis)
    plt.title('Types of Restaurant on South University Ave')
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Restaurant Categories')
    plt.show()
    return d

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    cur = connset(db)[0]
    cur.execute('SELECT restaurants.name FROM restaurants JOIN buildings ON buildings.id = restaurants.building_id WHERE buildings.building = ? ORDER BY restaurants.rating DESC',(building_num,))
    temp = cur.fetchall()
    lst= []
    for val in temp:
        lst.append(val[0])
    return lst


#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
