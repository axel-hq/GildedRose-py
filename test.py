# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

def item_to_str(item):
   return item.name + ", " + str(item.sell_in) + ", " + str(item.quality)

def assert_update(items_original, items_EXPECTED):
   n = len(items_EXPECTED)
   if len(items_original) != n:
      raise Exception(" ".join([
         "length conflict between item lists.",
         "Expected: " + str(n) + ".",
         "Actual: " + str(len(items_original))
      ]))
   items_updated = [Item(i.name, i.sell_in, i.quality) for i in items_original]
   items_updated = GildedRose(items_updated).update_quality()
   if len(items_updated) != n:
      raise Exception(" ".join([
         "Updated list changed length.",
         "Expected: " + str(n) + ".",
         "Actual: " + str(len(items_updated))
      ]))

   errs = []
   for i in range(n):
      item_original = items_original[i]
      item_EXPECTED = items_EXPECTED[i]
      item_updated = items_updated[i]
      if item_EXPECTED.name == item_updated.name:
         if item_EXPECTED.sell_in == item_updated.sell_in:
            if item_EXPECTED.quality == item_updated.quality:
               continue # don't error

      errs.append("\n".join([
         "Conflict for item " + str(i) + ": name, sell_in, quality",
         "Original item: " + item_to_str(item_original),
         "Updated  item: " + item_to_str(item_updated),
         "Expected item: " + item_to_str(item_EXPECTED),
      ]))
   if len(errs) > 0:
      raise Exception("\n" + "\n\n".join(errs))

class test_gilded_rose(unittest.TestCase):
   def test_normal_item(self):
      assert_update(
         [
            Item("foo",  2,  4),
            Item("foo",  1,  1),
            Item("foo",  0,  4),
            Item("foo", -1,  4),

            Item("foo",  1,  0), # single overflow
            Item("foo",  0,  1), # single overflow
            Item("foo",  0,  0), # double overflow
            Item("foo", -1,  1), # single overflow
            Item("foo", -1,  0), # double overflow
         ],
         [
            Item("foo",  1,  3),
            Item("foo",  0,  0),
            Item("foo", -1,  2),
            Item("foo", -2,  2),

            Item("foo",  0,  0),
            Item("foo", -1,  0),
            Item("foo", -1,  0),
            Item("foo", -2,  0),
            Item("foo", -2,  0),
         ],
      )

   def test_aged_brie(self):
      assert_update(
         [
            Item("Aged Brie",  2,  4),
            Item("Aged Brie",  1, 49),
            Item("Aged Brie",  0,  4),
            Item("Aged Brie", -1,  4),

            Item("Aged Brie",  1, 50), # single overflow
            Item("Aged Brie",  0, 49), # single overflow
            Item("Aged Brie",  0, 50), # double overflow
            Item("Aged Brie", -1, 49), # single overflow
            Item("Aged Brie", -1, 50), # double overflow
         ],
         [
            Item("Aged Brie",  1,  5),
            Item("Aged Brie",  0, 50),
            Item("Aged Brie", -1,  6),
            Item("Aged Brie", -2,  6),

            Item("Aged Brie",  0, 50),
            Item("Aged Brie", -1, 50),
            Item("Aged Brie", -1, 50),
            Item("Aged Brie", -2, 50),
            Item("Aged Brie", -2, 50),
         ],
      )

   def test_sulfuras(self):
      assert_update(
         [
            Item("Sulfuras, Hand of Ragnaros",  0, 80),
            Item("Sulfuras, Hand of Ragnaros", -1, 80),
         ],
         [
            Item("Sulfuras, Hand of Ragnaros",  0, 80),
            Item("Sulfuras, Hand of Ragnaros", -1, 80),
         ],
      )

   def test_backstage_pass(self):
      assert_update(
         [
            Item("Backstage passes to a TAFKAL80ETC concert", 13, 19),
            Item("Backstage passes to a TAFKAL80ETC concert", 12, 19),
            Item("Backstage passes to a TAFKAL80ETC concert", 11, 19),
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  9, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  8, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  7, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  6, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  3, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  2, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  1, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  0, 19),
            Item("Backstage passes to a TAFKAL80ETC concert",  0, 50),
            Item("Backstage passes to a TAFKAL80ETC concert", -1, 19),

            Item("Backstage passes to a TAFKAL80ETC concert", 13, 50), # single overflow
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 49), # single overflow
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 50), # double overflow
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 48), # single overflow
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 49), # double overflow
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 50), # triple overflow
         ],
         [
            Item("Backstage passes to a TAFKAL80ETC concert", 12, 20),
            Item("Backstage passes to a TAFKAL80ETC concert", 11, 20),
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 20),
            Item("Backstage passes to a TAFKAL80ETC concert",  9, 21),
            Item("Backstage passes to a TAFKAL80ETC concert",  8, 21),
            Item("Backstage passes to a TAFKAL80ETC concert",  7, 21),
            Item("Backstage passes to a TAFKAL80ETC concert",  6, 21),
            Item("Backstage passes to a TAFKAL80ETC concert",  5, 21),
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 22),
            Item("Backstage passes to a TAFKAL80ETC concert",  3, 22),
            Item("Backstage passes to a TAFKAL80ETC concert",  2, 22),
            Item("Backstage passes to a TAFKAL80ETC concert",  1, 22),
            Item("Backstage passes to a TAFKAL80ETC concert",  0, 22),
            Item("Backstage passes to a TAFKAL80ETC concert", -1,  0),
            Item("Backstage passes to a TAFKAL80ETC concert", -1,  0),
            Item("Backstage passes to a TAFKAL80ETC concert", -2,  0),

            Item("Backstage passes to a TAFKAL80ETC concert", 12, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  9, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  9, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 50),
            Item("Backstage passes to a TAFKAL80ETC concert",  4, 50),
         ]
      )

   def test_conjured(self):
      assert_update(
         [
            Item("Conjured foo",  4, 19),
            Item("Conjured foo",  1,  1),
            Item("Conjured foo",  0, 19),
            Item("Conjured foo", -1, 19),
            Item("Conjured foo",  0, 4),

            Item("Conjured foo",  1,  1), # single overflow
            Item("Conjured foo",  1,  0), # double overflow
            Item("Conjured foo",  0,  3), # single overflow
            Item("Conjured foo",  0,  2), # double overflow
            Item("Conjured foo",  0,  1), # triple overflow
            Item("Conjured foo",  0,  0), # quadruple overflow
            Item("Conjured foo", -1,  3), # single overflow
            Item("Conjured foo", -1,  2), # double overflow
            Item("Conjured foo", -1,  1), # triple overflow
            Item("Conjured foo", -1,  0), # quadruple overflow
         ],
         [
            Item("Conjured foo",  3, 17),
            Item("Conjured foo",  0,  0),
            Item("Conjured foo", -1, 15),
            Item("Conjured foo", -2, 15),
            Item("Conjured foo", -1,  0),

            Item("Conjured foo",  0,  0),
            Item("Conjured foo",  0,  0),
            Item("Conjured foo", -1,  0),
            Item("Conjured foo", -1,  0),
            Item("Conjured foo", -1,  0),
            Item("Conjured foo", -1,  0),
            Item("Conjured foo", -2,  0),
            Item("Conjured foo", -2,  0),
            Item("Conjured foo", -2,  0),
            Item("Conjured foo", -2,  0),
         ]
      )

if __name__ == '__main__':
   unittest.main()
