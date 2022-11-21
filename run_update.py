from gilded_rose import Item, GildedRose

items = [
   Item("+5 Dexterity Vest", 10, 20),
   Item("Aged Brie", 2, 0),
   Item("Elixir of the Mongoose", 5, 7),
   Item("Sulfuras, Hand of Ragnaros", 0, 80),
   Item("Sulfuras, Hand of Ragnaros", -1, 80),
   Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
   Item("Backstage passes to a TAFKAL80ETC concert", 10, 49),
   Item("Backstage passes to a TAFKAL80ETC concert", 5, 49),

   # This Conjured item does not work properly yet
   Item("Conjured Mana Cake", 3, 6),
]

days = 2
shop = GildedRose(items)

for day in range(days):
   print("\n-------- day " + str(day) + " --------")
   print("name, sellIn, quality")
   for item in items:
      print(item.name + ", " + str(item.sell_in) + ", " + str(item.quality))
   shop.update_quality()
