import collections
from tabulate import tabulate


class FoodCalculator(object):
    def __init__(self):
        self.food_counter = collections.Counter()
        self.category_counter = collections.Counter()

    def update(self, food, category):
        self.food_counter.update(food)
        self.category_counter.update(category)

    def __len__(self):
        return len(self.food_counter) + len(self.category_counter)

    def clear(self):
        """Clear both counters."""
        self.food_counter.clear()
        self.category_counter.clear()

    def popular_food(self, num_top_food):
        popular_food = self.food_counter.most_common(num_top_food)
        return tabulate(popular_food, ['Food ID', 'Count #'],
            tablefmt='grid')

    def popular_category(self, num_top_category):
        popular_categories = self.category_counter.most_common(num_top_category)
        return tabulate(popular_categories, ['Category ID', 'Count #'],
            tablefmt='grid')

    def most_popular(self, num_top_food=100, num_top_category=5):
        return (self.popular_food(num_top_food),
            self.popular_category(num_top_category))

