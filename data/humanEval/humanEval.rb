require 'pg' # gem install pg

IDS_FILE = 'ids.txt'
PAIRS_FILE = 'pairs.txt'

# Pairs are always kept as {smallerId => {largerId => score}}.

$conn = PG::Connection.new(:host => 'localhost', :dbname => 'ml', :port => 1046)
# Cache businesses.
$cache = {}

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# |mins| is minutes since midnight.
def formatMins(mins)
   hours = mins / 60
   min = mins - (hours * 60)
   return "#{'%02d' % hours}:#{'%02d' % min}"
end

def parseHours(rawHours)
   hours = Array.new(DAYS.size())

   rawHours.split(';').each{|day|
      parts = day.split(',').map{|val| val.to_i()}
      hours[parts[0]] = "#{formatMins(parts[1])} - #{formatMins(parts[2])}"
   }

   return hours
end

# |hours| should be output from parseHours().
def formatHours(hours, indent)
   rtn = []

   DAYS.each_index{|dayIndex|
      if (hours[dayIndex] == nil)
         rtn << "#{indent}#{"%-10s" % DAYS[dayIndex]}: Closed"
      else
         rtn << "#{indent}#{"%-10s" % DAYS[dayIndex]}: #{hours[dayIndex]}"
      end
   }

   return rtn.join("\n")
end

class Business
   def initialize(info)
      @name = info['name']
      @stars = info['stars'].to_f()
      @reviewCount = info['reviewcount'].to_i()
      @attributes = info['attributes'].split(';;').sort()
      @categories = info['categories'].split(';;').sort()
      @topReviewWords = info['topreviewwords'].split(';;').sort()
      @keyReviewWords = info['keyreviewwords'].split(';;').sort()
      @hours = parseHours(info['hours'])
   end

   def to_s()
      return "
   #{@name}
   Stars: #{@stars}
   Review Count: #{@reviewCount}
   Hours:\n#{formatHours(@hours, '      ')}
   Categories: #{@categories}
   Key Review Words: #{@keyReviewWords}
   Top Review Words:
      #{@topReviewWords[0...5]}
      #{@topReviewWords[5...10]}
   Attrbiutes:\n      #{@attributes.join("\n      ")}"
   end
end

def getTerminalWidth()
   return `tput cols`.strip().to_i()
end

# If necessary, input will lines will get cutt off.
def sideBySidePrint(str1, str2)
   width = getTerminalWidth()

   # Keep it even.
   width = width % 2 == 0 ? width : width - 1

   # We will keep four buffer lines in the middle.
   columnWidth = (width - 4) / 2

   # Get each line remove any trailing whitespace and cutt it down to the required number of columns.
   lines1 = str1.to_s().split("\n").map{|line| line.rstrip()[0...columnWidth]}
   lines2 = str2.to_s().split("\n").map{|line| line.rstrip()[0...columnWidth]}

   # Equlize sizes with empty strings.
   while (lines1.size() < lines2.size())
      lines1 << ""
   end

   while (lines2.size() < lines1.size())
      lines2 << ""
   end

   formatString = "%-#{columnWidth}s"
   lines1.each_index{|i|
      puts "#{"%-#{columnWidth}s" % lines1[i]} || #{"%-#{columnWidth}s" % lines2[i]}"
   }
end

# Load the already evaluated pairs into memory.
def loadPairs()
   pairs = Hash.new{|hash, key| hash[key] = {}}

   if (!File.exist?(PAIRS_FILE))
      return pairs
   end

   File.open(PAIRS_FILE, 'r'){|file|
      file.each{|line|
         parts = line.strip().split(',')
         minId = [parts[0], parts[1]].min()
         maxId = [parts[0], parts[1]].max()

         if (pairs[minId].include?(maxId))
            $stderr.puts("Duplicate Pair: [#{parts[0]},#{parts[1]}]")
         end

         pairs[minId][maxId] = parts[2].to_i()
      }
   }

   return pairs
end

def loadIds()
   ids = []

   File.open(IDS_FILE, 'r'){|file|
      file.each{|line|
         ids << line.strip()
      }
   }

   return ids
end

# Fetch some info from the DB.
def fetchBusiness(id)
   if ($cache.include?(id))
      return $cache[id]
   end

   query = "
		SELECT
			B.name,
			B.stars,
			B.reviewCount,
			COALESCE(BAA.value, '') AS attributes,
			COALESCE(BCA.value, '') AS categories,
			COALESCE(RSW.topWords, '') AS topReviewWords,
		   COALESCE(RSW.keyWords, '') AS keyReviewWords,
			COALESCE(BH.hours, '') AS hours
		FROM
			Businesses B
			LEFT JOIN BusinessAttributesAggregate BAA ON BAA.businessId = B.id
			LEFT JOIN BusinessCategoriesAggregate BCA ON BCA.businessId = B.id
			LEFT JOIN ReviewSpecialWords RSW ON RSW.businessId = B.id
			LEFT JOIN (
				SELECT
					businessId,
					STRING_AGG(CONCAT(day, ',', open, ',', close), ';') AS hours
				FROM BusinessHours
				GROUP BY businessId
			) BH ON BH.businessId = B.id
		WHERE B.yelpId = '#{id}'
	"

	result = $conn.exec(query)

   if (result.num_tuples() != 1)
      $stderr.puts("Error fetching id: #{id}.")
      return nil
   end

   business = Business.new(result[0])
   $cache[id] = business
   return business
end

def writeScore(id1, id2, score)
   minId = [id1, id2].min()
   maxId = [id1, id2].max()

   File.open(PAIRS_FILE, 'a'){|file|
      file.puts("#{minId},#{maxId},#{score}")
   }
end

def compare(id1, id2)
   business1 = fetchBusiness(id1)
   business2 = fetchBusiness(id2)

   sideBySidePrint(business1, business2)

   while (true)
      print("Please score 1 - 5 (1: Very Dissimilar, 5: Very Similar): ")
      score = gets().strip()

      if (['1', '2', '3', '4', '5'].include?(score))
         break
      end
   end

   score = score.to_i()

   # Write out the score every time in case we stop the program unexpectantly.
   writeScore(id1, id2, score)

   return score
end

def main()
   ids = loadIds()
   pairs = loadPairs()

   ids.each{|id1|
      ids.each{|id2|
         if (id1 == id2)
            next
         end

         minId = [id1, id2].min()
         maxId = [id1, id2].max()

         if (pairs.include?(minId) && pairs[minId].include?(maxId))
            next
         end

         score = compare(minId, maxId)
         pairs[minId][maxId] = score
      }
   }
end

if (__FILE__ == $0)
   main()
end
