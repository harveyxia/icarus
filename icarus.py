import scraper
import mongo

def main(f, t, days):
    mongo.init()
    name = '_'.join([f,t,str(days)])

    if mongo.collection.find({u'name': unicode(name)}).limit(1).count(True):
        data = list(mongo.collection.find({u'name': unicode(name)}))[0]
        mongo.client.disconnect()
        return data
    else:
        scraper.init()
        data = scraper.fetch_all_data(f, t, days)
        data_dict = { "name": name, "data": data }
        mongo.collection.insert(data_dict)
        exit()
        return data_dict

# safely exit, release resources
def exit():
    scraper.driver.quit()
    mongo.client.disconnect()