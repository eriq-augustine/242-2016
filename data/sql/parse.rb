require 'json'
require 'pg'
require 'pp'

# Parse all the yelp dataset located in JSON_DATA_DIR and PHOTO_DATA_DIR.
# Put the results in SQL_DATA_DIR.

if (ARGV.size() == 0)
   DEBUG = false
elsif (ARGV.size() == 1 && ['-d', '--debug'].include?(ARGV[0].downcase))
   DEBUG = true
else
   puts "USAGE ruby #{__FILE__} [--debug]"
   exit 1
end

JSON_DATA_DIR = File.join('..', 'json')
PHOTO_DATA_DIR = File.join('..', 'photos')

BUSINESS_FILE = File.join(JSON_DATA_DIR, 'yelp_academic_dataset_business.json')
CHECKIN_FILE = File.join(JSON_DATA_DIR, 'yelp_academic_dataset_checkin.json')
REVIEW_FILE = File.join(JSON_DATA_DIR, 'yelp_academic_dataset_review.json')
TIP_FILE = File.join(JSON_DATA_DIR, 'yelp_academic_dataset_tip.json')
USER_FILE = File.join(JSON_DATA_DIR, 'yelp_academic_dataset_user.json')
PHOTO_FILE = File.join(PHOTO_DATA_DIR, 'photo_id_to_business_id.json')

SQL_DATA_DIR = 'data'
BUSINESS_OUT_FILE = File.join(SQL_DATA_DIR, 'insert_businesses.sql')
CHECKIN_OUT_FILE = File.join(SQL_DATA_DIR, 'insert_checkins.sql')
REVIEW_OUT_FILE = File.join(SQL_DATA_DIR, 'insert_reviews.sql')
TIP_OUT_FILE = File.join(SQL_DATA_DIR, 'insert_tips.sql')
USER_OUT_FILE = File.join(SQL_DATA_DIR, 'insert_users.sql')
PHOTO_OUT_FILE = File.join(SQL_DATA_DIR, 'insert_photos.sql')

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
INSERT_ROW_MAX = 5000

`mkdir -p #{SQL_DATA_DIR}`

# Takes raw JSON checkin_info, returns [{:day => dayOfWeek, :hour => hourInDay, :count => count}].
def normalizeCheckin(checkin)
   rtn = []

   checkin.each{|time, count|
      hour, day = time.strip().split('-').map{|val| val.to_i()}
      rtn << {:day => day, :hour => hour, :count => count}
   }

   return rtn
end

# Returns {businessId => [{:day => dayOfWeek, :hourInDay => hour, :count => count}, ...], ...}
def parseCheckins()
   checkins = {}

   file = File.open(CHECKIN_FILE)
   file.each{|line|
      checkinObj = JSON.parse(line.strip())
      checkins[checkinObj['business_id']] = normalizeCheckin(checkinObj['checkin_info'])

      if (DEBUG)
         break
      end
   }
   file.close()

   return checkins
end

# Returns [{:day => dayOfWeek, :open => timeOfDayMins, :close => timeOfDayMins}].
def normalizeHours(hours)
   rtn = []

   hours.each{|day, times|
      openHour, openMin = times['open'].split(':').map{|val| val.to_i()}
      closeHour, closeMin = times['close'].split(':').map{|val| val.to_i()}

      rtn << {:day => DAYS.index(day.downcase()), :open => (openHour * 60 + openMin), :close => (closeHour * 60 + closeMin)}
   }

   return rtn
end

# Object attributes will be flattened by combining each key: "#{key1}:#{key2}".
# Returns {attributeKey => attributeValue}
def parseAttributes(attributes)
   rtn = {}

   attributes.each{|key, value|
      if (value.instance_of?(String) || value.instance_of?(FalseClass) || value.instance_of?(TrueClass) || value.instance_of?(Fixnum))
         rtn[key.strip()] = value.to_s().strip()
      elsif (value.instance_of?(Hash))
         value.each{|innerKey, innerValue|
            rtn["#{key.strip()}:#{innerKey.strip()}"] = innerValue.to_s().strip()
         }
      else
         $stderr.puts "Unknown attribute value class (#{value.class()})."
         exit
      end
   }

   return rtn
end

# Returns {businessId => {all the info}, ...}
def parseBusinesses()
   businesses = {}

   file = File.open(BUSINESS_FILE)
   file.each{|line|
      businessObj = JSON.parse(line.strip())
      businesses[businessObj['business_id']] = {
         :name => businessObj['name'],
         :address => businessObj['full_address'],
         :city => businessObj['city'],
         :state => businessObj['state'],
         :latitude => businessObj['latitude'],
         :longitude => businessObj['longitude'],
         :stars => businessObj['stars'],
         :reviewCount => businessObj['review_count'],
         :active => businessObj['open'],
         :hours => normalizeHours(businessObj['hours']),
         :neighborhoods => businessObj['neighborhoods'].map{|val| val.strip()},
         :categories => businessObj['categories'].map{|val| val.strip()},
         :attributes => parseAttributes(businessObj['attributes'])
      }

      if (DEBUG)
         break
      end
   }
   file.close()

   return businesses
end

def parseReviews()
   reviews = {}

   file = File.open(REVIEW_FILE)
   file.each{|line|
      reviewObj = JSON.parse(line.strip())
      reviews[reviewObj['review_id']] = {
         :userId => reviewObj['user_id'],
         :businessId => reviewObj['business_id'],
         :stars => reviewObj['stars'],
         :text => reviewObj['text'],
         :date => reviewObj['date'],
         :votesFunny => reviewObj['votes']['funny'],
         :votesUseful => reviewObj['votes']['useful'],
         :votesCool => reviewObj['votes']['cool']
      }

      if (DEBUG)
         break
      end
   }
   file.close()

   return reviews
end

def parseTips()
   tips = []

   file = File.open(TIP_FILE)
   file.each{|line|
      tipObj = JSON.parse(line.strip())
      tips << {
         :userId => tipObj['user_id'],
         :businessId => tipObj['business_id'],
         :text => tipObj['text'],
         :date => tipObj['date'],
         :likes => tipObj['likes']
      }

      if (DEBUG)
         break
      end
   }
   file.close()

   return tips
end

def parseUsers()
   users = {}

   file = File.open(USER_FILE)
   file.each{|line|
      userObj = JSON.parse(line.strip())

      yelpingSinceYear, yelpingSinceMonth = userObj['yelping_since'].split('-').map{|val| val.to_i()}

      users[userObj['user_id']] = {
         :firstName => userObj['name'],
         :reviewCount => userObj['review_count'],
         :averageStars => userObj['average_stars'],
         :votesFunny => userObj['votes']['funny'],
         :votesUseful => userObj['votes']['useful'],
         :votesCool => userObj['votes']['cool'],
         :fans => userObj['fans'],
         :yelpingSinceYear => yelpingSinceYear,
         :yelpingSinceMonth => yelpingSinceMonth,
         :friends => userObj['friends'],
         :eliteYears => userObj['elite'],
         :complimentCool => userObj['compliments'].has_key?('cool') ? userObj['compliments']['cool'] : 0,
         :complimentCute => userObj['compliments'].has_key?('cute') ? userObj['compliments']['cute'] : 0,
         :complimentFunny => userObj['compliments'].has_key?('funny') ? userObj['compliments']['funny'] : 0,
         :complimentHot => userObj['compliments'].has_key?('hot') ? userObj['compliments']['hot'] : 0,
         :complimentList => userObj['compliments'].has_key?('list') ? userObj['compliments']['list'] : 0,
         :complimentMore => userObj['compliments'].has_key?('more') ? userObj['compliments']['more'] : 0,
         :complimentNote => userObj['compliments'].has_key?('note') ? userObj['compliments']['note'] : 0,
         :complimentPhotos => userObj['compliments'].has_key?('photos') ? userObj['compliments']['photos'] : 0,
         :complimentPlain => userObj['compliments'].has_key?('plain') ? userObj['compliments']['plain'] : 0,
         :complimentProfile => userObj['compliments'].has_key?('profile') ? userObj['compliments']['profile'] : 0,
         :complimentWriter => userObj['compliments'].has_key?('writer') ? userObj['compliments']['writer'] : 0
      }

      if (DEBUG)
         break
      end
   }
   file.close()

   return users
end

def parsePhotos()
   photos = {}

   file = File.open(PHOTO_FILE)
   photoObjs = JSON.parse(file.read().strip())

   photoObjs.each{|photoObj|

      photos[photoObj['photo_id']] = {
         :businessId => photoObj['business_id'],
         :caption => photoObj['caption'],
         :label => photoObj['label'] == 'none' ? nil : photoObj['label']
      }

      if (DEBUG)
         break
      end
   }
   file.close()

   return photos
end

def numOrNull(val)
   if (val == nil)
      return "NULL"
   end

   return "#{val}"
end

def stringOrNull(val)
   if (val == nil || val == '')
      return "NULL"
   end

   return "'#{PG::Connection::escape_string(val)}'"
end

def boolOrNull(val)
   if (val == nil)
      return "NULL"
   end

   return val ? 'TRUE' : 'FALSE'
end

def insertUsers(out, users)
   insertStrings = []
   users.each{|id, user|
      insertStrings << "         (#{stringOrNull(id)}, #{stringOrNull(user[:firstName])}, #{numOrNull(user[:reviewCount])}, #{numOrNull(user[:averageStars])}, #{numOrNull(user[:votesFunny])}, #{numOrNull(user[:votesUseful])}, #{numOrNull(user[:votesCool])}, #{numOrNull(user[:yelpingSinceYear])}, #{numOrNull(user[:yelpingSinceMonth])}, #{numOrNull(user[:fans])}, #{numOrNull(user[:complimentCool])}, #{numOrNull(user[:complimentCute])}, #{numOrNull(user[:complimentFunny])}, #{numOrNull(user[:complimentHot])}, #{numOrNull(user[:complimentList])}, #{numOrNull(user[:complimentMore])}, #{numOrNull(user[:complimentNote])}, #{numOrNull(user[:complimentPhotos])}, #{numOrNull(user[:complimentPlain])}, #{numOrNull(user[:complimentProfile])}, #{numOrNull(user[:complimentWriter])})"
   }

   insertHeader = '
      INSERT INTO Users
         (yelpId, firstName, reviewCount, averageStars, votesFunny, votesUseful, votesCool, yelpingSinceYear, yelpingSinceMonth, fans, complimentCool, complimentCute, complimentFunny, complimentHot, complimentList, complimentMore, complimentNote, complimentPhotos, complimentPlain, complimentProfile, complimentWriter)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertEliteYears(out, users)
   insertStrings = []
   users.each{|id, user|
      user[:eliteYears].each{|year|
         insertStrings << "         (#{stringOrNull(id)}, #{numOrNull(year)})"
      }
   }

   insertHeader = '
      INSERT INTO UserEliteYears
         (userYelpId, year)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertFriends(out, users)
   insertStrings = []
   users.each{|id, user|
      user[:friends].each{|friendId|
         insertStrings << "         (#{stringOrNull(id)}, #{stringOrNull(friendId)})"
      }
   }

   insertHeader = '
      INSERT INTO Friendships
         (sourceUserYelpId, targetUserYelpId)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertBusinesses(out, businesses)
   insertStrings = []
   businesses.each{|id, business|
      insertStrings << "         (#{stringOrNull(id)}, #{stringOrNull(business[:name])}, #{stringOrNull(business[:address])}, #{stringOrNull(business[:city])}, #{stringOrNull(business[:state])}, #{stringOrNull(business[:latitude].to_s())}, #{stringOrNull(business[:longitude].to_s())}, #{numOrNull(business[:stars])}, #{numOrNull(business[:reviewCount])}, #{boolOrNull(business[:active])})"
   }

   insertHeader = '
      INSERT INTO Businesses
         (yelpId, name, address, city, state, latitude, longitude, stars, reviewCount, active)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertBusinessesAttributes(out, businesses)
   insertStrings = []
   businesses.each{|id, business|
      business[:attributes].each{|key, value|
         insertStrings << "         (#{stringOrNull(id)}, #{stringOrNull(key)}, #{stringOrNull(value)})"
      }
   }

   insertHeader = '
      INSERT INTO BusinessAttributes
         (businessYelpId, name, value)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertBusinessesCategories(out, businesses)
   insertStrings = []
   businesses.each{|id, business|
      business[:categories].each{|value|
         insertStrings << "         (#{stringOrNull(id)}, #{stringOrNull(value)})"
      }
   }

   insertHeader = '
      INSERT INTO BusinessCategories
         (businessYelpId, name)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertBusinessesHours(out, businesses)
   insertStrings = []
   businesses.each{|id, business|
      business[:hours].each{|hours|
         insertStrings << "         (#{stringOrNull(id)}, #{numOrNull(hours[:day])}, #{numOrNull(hours[:open])}, #{numOrNull(hours[:close])})"
      }
   }

   insertHeader = '
      INSERT INTO BusinessHours
         (businessYelpId, day, open, close)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertBusinessesNeighborhoods(out, businesses)
   insertStrings = []
   businesses.each{|id, business|
      business[:neighborhoods].each{|value|
         insertStrings << "         (#{stringOrNull(id)}, #{stringOrNull(value)})"
      }
   }

   insertHeader = '
      INSERT INTO BusinessNeighborhoods
         (businessYelpId, name)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertTips(out, tips)
   insertStrings = []
   tips.each{|tip|
      insertStrings << "         (#{stringOrNull(tip[:businessId])}, #{stringOrNull(tip[:userId])}, #{stringOrNull(tip[:text])}, #{stringOrNull(tip[:date])}, #{numOrNull(tip[:likes])})"
   }

   insertHeader = '
      INSERT INTO Tips
         (businessYelpId, userYelpId, text, date, likes)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertCheckins(out, checkins)
   insertStrings = []
   checkins.each{|id, checkinCounts|
      checkinCounts.each{|checkin|
         insertStrings << "         (#{stringOrNull(id)}, #{numOrNull(checkin[:day])}, #{numOrNull(checkin[:hour])}, #{numOrNull(checkin[:count])})"
      }
   }

   insertHeader = '
      INSERT INTO CheckIns
         (businessYelpId, day, time, count)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertReviews(out, reviews)
   insertStrings = []
   reviews.each{|id, review|
      insertStrings << "         (#{stringOrNull(id)}, #{stringOrNull(review[:businessId])}, #{stringOrNull(review[:userId])}, #{numOrNull(review[:stars])}, #{stringOrNull(review[:text])}, #{stringOrNull(review[:date])}, #{numOrNull(review[:votesFunny])}, #{numOrNull(review[:votesUseful])}, #{numOrNull(review[:votesCool])})"
   }

   insertHeader = '
      INSERT INTO Reviews
         (yelpId, businessYelpId, userYelpId, stars, text, date, votesFunny, votesUseful, votesCool)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def insertPhotos(out, photos)
   insertStrings = []
   photos.each{|id, photo|
      insertStrings << "         (#{stringOrNull(id)}, #{stringOrNull(photo[:businessId])}, #{stringOrNull(photo[:caption])}, #{stringOrNull(photo[:label])})"
   }

   insertHeader = '
      INSERT INTO Photos
         (yelpId, businessYelpId, caption, label)
      VALUES'
   outputInserts(out, insertHeader, insertStrings)
end

def outputInserts(out, insertHeader, insertStrings)
   if (insertStrings.size() == 0)
      return
   end

   insertStrings.each_slice(INSERT_ROW_MAX).each{|strings|
      out.puts insertHeader
      out.puts strings.join(",\n")
      out.puts '      ;'
   }
end

def inserts(users, businesses, reviews, tips, checkins, photos)
   usersFile = File.new(USER_OUT_FILE, 'w')
   businessesFile = File.new(BUSINESS_OUT_FILE, 'w')
   checkinsFile = File.new(CHECKIN_OUT_FILE, 'w')
   reviewsFile = File.new(REVIEW_OUT_FILE, 'w')
   tipsFile = File.new(TIP_OUT_FILE, 'w')
   photosFile = File.new(PHOTO_OUT_FILE, 'w')

   insertUsers(usersFile, users)
   insertEliteYears(usersFile, users)
   insertFriends(usersFile, users)

   insertBusinesses(businessesFile, businesses)
   insertBusinessesAttributes(businessesFile, businesses)
   insertBusinessesCategories(businessesFile, businesses)
   insertBusinessesHours(businessesFile, businesses)
   insertBusinessesNeighborhoods(businessesFile, businesses)

   insertPhotos(photosFile, photos)

   insertTips(tipsFile, tips)

   insertCheckins(checkinsFile, checkins)

   insertReviews(reviewsFile, reviews)

   usersFile.close()
   businessesFile.close()
   checkinsFile.close()
   reviewsFile.close()
   tipsFile.close()
   photosFile.close()
end

users = parseUsers()
checkins = parseCheckins()
businesses = parseBusinesses()
reviews = parseReviews()
tips = parseTips()
photos = parsePhotos()

inserts(users, businesses, reviews, tips, checkins, photos)
