import scraper
import mongo

def main(f, t, days):
    mongo.init()
    name = '_'.join([f,t,str(days)])

    if mongo.collection.find({u'name': unicode(name)}).limit(1).count(True):
        prices = list(mongo.collection.find({u'name': unicode(name)}))[0]
        mongo.client.disconnect()
        return prices
    else:
        scraper.init()
        prices = scraper.fetch_all_prices(f, t, days)
        prices_dict = { "name": name, "prices": prices }
        mongo.collection.insert(prices_dict)
        exit()
        return prices_dict

# safely exit, release resources
def exit():
    scraper.driver.quit()
    mongo.client.disconnect()