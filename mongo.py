import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["tnf"]

table = mydb["articles"]

# row = {
#   "url": "https://www.tnp.sg/news/singapore/virgin-active-members-slam-fitness-club-response-use-cctv-camera",
#   "headline": "Virgin Active members slam fitness club for 'rude' response over use of CCTV camera",
#   "published_date": "Mar 19, 2019 06:00 am",
#   "standfirst": "Members of Fitness club unhappy with its response over use of CCTV camera",
#   "lead": "After a closed-circuit television camera was discovered in a women-only area adjoining the showers and changing room in its Raffles Place outlet, Virgin Active Singapore did not initially apologise to its outraged members.",
#   "keywords": "CONSUMER ISSUES",
#   "tag": "Singapore",
#   "img_src": "https://www.tnp.sg/sites/default/files/styles/rl380/public/articles/2019/03/19/NP_20190319_CAMERA19A_4702363.jpg?itok=Ef9WL7aO",
#   "facebook_engagements": 40,
#   "shares": 12,
#   "comments": 6,
#   "reactions": 22,
#   "breaking": True
# }

# inserted = table.insert_one(row)
# print(inserted.inserted_id)

# result = []
# for x in table.find():
#   result.append(x)
  
# print(result)