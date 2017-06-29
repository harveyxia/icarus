import scraper
import mongo

def main(f, t, days):
    mongo.init()
    name = '_'.join([f,t,str(days)])

    if mongo.collection.find({u'name': name}).limit(1).count(True):
        data = list(mongo.collection.find({u'name': name}))[0]
        mongo.client.close()
        return data
    else:
        scraper.init()
        data = scraper.fetch_all_data(f, t, days)
        if data is not None:
            data_dict = { "name": name, "data": data }
            mongo.collection.insert(data_dict)
            exit()
            return data_dict
        else:
            exit()
            return None

def find(name):
    mongo.init()
    if mongo.collection.find({u'name': name}).limit(1).count(True):
        data = list(mongo.collection.find({u'name': name}))[0]
        print(data[u'data'])
        mongo.client.close()
        return {'name': data['name'], 'data': data['data']}
    else:
        return None

# safely exit, release resources
def exit():
    scraper.driver.quit()
    mongo.client.close()