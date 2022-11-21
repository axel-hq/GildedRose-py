# -*- coding: utf-8 -*-
import unittest

from gilded_rose_legacy import Item, GildedRose

def assert_items_eq(items_actual, items_EXPECTED):
   if len(items_EXPECTED) != len(items_actual):
      raise Exception(" ".join([
         "length conflict between item lists.",
         "Expected: " + str(len(items_EXPECTED)) + ".",
         "Actual: " + str(len(items_actual))
      ]))

   n = len(items_EXPECTED)
   errs = []
   for i in range(n):
      item_EXPECTED = items_EXPECTED[i]
      item_actual = items_actual[i]
      if item_EXPECTED.name != item_actual.name:
         errs.append(" ".join([
            "name conflict, item " + str(i) + ".",
            "Expected: " + str(item_EXPECTED.name) + ".",
            "Actual: " + str(item_actual.name) + ".",
         ]))
      if item_EXPECTED.sell_in != item_actual.sell_in:
         errs.append(" ".join([
            "sell_in conflict, item " + str(i) + ".",
            "Expected: " + str(item_EXPECTED.sell_in) + ".",
            "Actual: " + str(item_actual.sell_in) + ".",
         ]))
      if item_EXPECTED.quality != item_actual.quality:
         errs.append(" ".join([
            "quality conflict, item " + str(i) + ".",
            "Expected: " + str(item_EXPECTED.quality) + ".",
            "Actual: " + str(item_actual.quality) + ".",
         ]))
   if len(errs) > 0:
      raise Exception("\n".join(errs))

class test_normal_item(unittest.TestCase):
   def test_standard_update(self):
      assert_items_eq(
         GildedRose([
            Item("foo",  1,  4),
         ]).update_quality(), # returns items
         [
            Item("foo",  0,  3),
         ],
      )
   def test_expired_update(self):
      assert_items_eq(
         GildedRose([
            Item("foo", -1,  4),
         ]).update_quality(), # returns items
         [
            Item("foo", -2,  2),
         ],
      )
   def test_just_expired_update(self):
      assert_items_eq(
         GildedRose([
            Item("foo",  0,  4),
         ]).update_quality(), # returns items
         [
            Item("foo", -1,  2),
         ],
      )
   def test_minimum_0(self):
      assert_items_eq(
         GildedRose([
            Item("foo",  1,  0),
            Item("foo",  0,  1), # single overflow
            Item("foo",  0,  0), # double overflow
            Item("foo", -1,  1), # single overflow
            Item("foo", -1,  0), # double overflow
         ]).update_quality(), # returns items
         [
            Item("foo",  0,  0),
            Item("foo", -1,  0),
            Item("foo", -1,  0),
            Item("foo", -2,  0),
            Item("foo", -2,  0),
         ],
      )

class test_aged_brie(unittest.TestCase):
   def test_standard_update(self):
      assert_items_eq(
         GildedRose([
            Item("Aged Brie",  1,  4),
         ]).update_quality(), # returns items
         [
            Item("Aged Brie",  0,  5),
         ],
      )
   def test_expired_update(self):
      assert_items_eq(
         GildedRose([
            Item("Aged Brie", -1,  4),
         ]).update_quality(), # returns items
         [
            Item("Aged Brie", -2,  6),
         ],
      )
   def test_just_expired_update(self):
      assert_items_eq(
         GildedRose([
            Item("Aged Brie",  0,  4),
         ]).update_quality(), # returns items
         [
            Item("Aged Brie", -1,  6),
         ],
      )
   def test_maximum_50(self):
      assert_items_eq(
         GildedRose([
            Item("Aged Brie",  1, 50),
            Item("Aged Brie",  0, 49), # single overflow
            Item("Aged Brie",  0, 50), # double overflow
            Item("Aged Brie", -1, 49), # single overflow
            Item("Aged Brie", -1, 50), # double overflow
         ]).update_quality(), # returns items
         [
            Item("Aged Brie",  0, 50),
            Item("Aged Brie", -1, 50),
            Item("Aged Brie", -1, 50),
            Item("Aged Brie", -2, 50),
            Item("Aged Brie", -2, 50),
         ],
      )

class test_sulfuras(unittest.TestCase):
   def test_standard_nonupdate(self):
      assert_items_eq(
         GildedRose([
            Item("Sulfuras, Hand of Ragnaros",  0, 80),
         ]).update_quality(), # returns items
         [
            Item("Sulfuras, Hand of Ragnaros",  0, 80),
         ],
      )

class test_backstage_pass(unittest.TestCase):
   def test_standard_update(self):
      assert_items_eq(
         GildedRose([
            Item("Backstage passes to a TAFKAL80ETC concert", 13, 19),
            Item("Backstage passes to a TAFKAL80ETC concert", 12, 19),
            Item("Backstage passes to a TAFKAL80ETC concert", 11, 19),
         ]).update_quality(), # returns items
         [
            Item("Backstage passes to a TAFKAL80ETC concert", 12, 20),
            Item("Backstage passes to a TAFKAL80ETC concert", 11, 20),
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 20),
         ]
      )
   def test_10_day_update(self):
      assert_items_eq(
         GildedRose([
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  9, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  8, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  7, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  6, 19),
         ]).update_quality(), # returns items
         [
            Item("Backstage passes to a TAFKAL80ETC concert",  9, 21),
            Item("Backstage passes to a TAFKAL80ETC concert",  8, 21),
            Item("Backstage passes to a TAFKAL80ETC concert",  7, 21),
            Item("Backstage passes to a TAFKAL80ETC concert",  6, 21),
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 21),
         ]
      )
   def test_5_day_update(self):
      assert_items_eq(
         GildedRose([
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  3, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  2, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  1, 19),
         ]).update_quality(), # returns items
         [
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 22),
            Item("Backstage passes to a TAFKAL80ETC concert",  3, 22),
            Item("Backstage passes to a TAFKAL80ETC concert",  2, 22),
            Item("Backstage passes to a TAFKAL80ETC concert",  1, 22),
            Item("Backstage passes to a TAFKAL80ETC concert",  0, 22),
         ]
      )
   def test_expired_update(self):
      assert_items_eq(
         GildedRose([
            Item("Backstage passes to a TAFKAL80ETC concert", -1, 19),
         ]).update_quality(), # returns items
         [
            Item("Backstage passes to a TAFKAL80ETC concert", -2, 0),
         ]
      )
   def test_just_expired_update(self):
      assert_items_eq(
         GildedRose([
            Item("Backstage passes to a TAFKAL80ETC concert",  0, 19),
         ]).update_quality(), # returns items
         [
            Item("Backstage passes to a TAFKAL80ETC concert", -1, 0),
         ]
      )
   def test_maximum_50(self):
      assert_items_eq(
         GildedRose([
            Item("Backstage passes to a TAFKAL80ETC concert", 13, 50),
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 49), # single overflow
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 50), # double overflow
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 48), # single overflow
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 49), # double overflow
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 50), # triple overflow
         ]).update_quality(), # returns items
         [
            Item("Backstage passes to a TAFKAL80ETC concert", 12, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  9, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  9, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 50),
         ],
      )

if __name__ == '__main__':
   unittest.main()
