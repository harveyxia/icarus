import scraper
import mongo

def main(f, t, days):
    mongo.init()
    name = '_'.join([f,t,str(days)])

    if mongo.collection.find({u'name': unicode(name)}).limit(1).count(True):
        mongo.client.disconnect()
        return 'Entry already exists'
    else:
        scraper.init()
        prices = scraper.fetch_all_prices(f, t, days)

        mongo.collection.insert(
            {
                "name": name,
                "prices": prices
            } )
        exit()

# safely exit, release resources
def exit():
    scraper.driver.quit()
    mongo.client.disconnect()