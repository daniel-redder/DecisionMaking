from collections import namedtuple
from .property import Property


class Street(Property):
    '''
    A type of Property representing a street.

    Manages rents, house-building and so on.
    '''

    def __init__(self, name, property_set, price, house_price, rents):
        '''
        The 'constructor'.

        rents: passed in as a list: [base, one_house, two_houses, three_houses, four_houses, hotel]
        '''
        # The base class holds the values applicable to all properties...
        super().__init__(name, property_set, price)

        # The price of one house on this street...
        self.house_price = house_price

        # The collection of rents as a list:
        # [base, one_house, two_houses, three_houses, four_houses, hotel]
        self.rents = rents

        # The number of houses on the street.
        # This can go up to 5, indicating that the street has a hotel.
        self.number_of_houses = 0

    async def calculate_rent(self, game, player):
        '''
        The player has landed on a square owned by another player
        and must pay rent.
        '''
        # Are there any houses?
        if self.number_of_houses == 0:
            rent = self.rents[0]
            owner = self.owner
            if self.property_set in owner.state.owned_unmortgaged_sets:
                # The player owns the whole set, so the rent is doubled...
                rent *= 2
        else:
            # The street has houses, so we find the rent for the number
            # of houses there are...
            rent = self.rents[self.number_of_houses]

        return rent


