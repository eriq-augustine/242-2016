# This script is to duplicate similarity scores for restaurants that we know are the same.
# It will also find and remove duplicate scorings.

PAIRS_FILE = 'pairs.txt'

MAX_SIM = 5

SAME_IDS = {
   'SeqfJOg6jZGx2W1bs142cg' => 'r6UzCUbllqkkc9BSV7Vodg',
   'r6UzCUbllqkkc9BSV7Vodg' => 'SeqfJOg6jZGx2W1bs142cg',

   'kEaQt6G55MvXh1OW-1VCzQ' => 'jHte0SjUldZeDDZ5py0ZhA',
   'jHte0SjUldZeDDZ5py0ZhA' => 'kEaQt6G55MvXh1OW-1VCzQ',

   'qlgAl9biUkK1wvmJ4ggDFg' => '-4mNZfAXMd2mxEsD2YRcaQ',
   '-4mNZfAXMd2mxEsD2YRcaQ' => 'qlgAl9biUkK1wvmJ4ggDFg',

   'glLo_FNtgQ7OmAR8hUrDqQ' => 'YHGpemLe7cbnPSubG-cRRg',
   'YHGpemLe7cbnPSubG-cRRg' => 'glLo_FNtgQ7OmAR8hUrDqQ',

   'sY7OAhyojv3YI0EUUW_gUQ' => 'dPg69r5nLzEmug0OvNfkmQ',
   'dPg69r5nLzEmug0OvNfkmQ' => 'sY7OAhyojv3YI0EUUW_gUQ',

   'LxxmtHFNZ5S-MyhykoE4Sg' => '-JpZiiGPKOuCEiODGNyovw',
   '-JpZiiGPKOuCEiODGNyovw' => 'LxxmtHFNZ5S-MyhykoE4Sg',

   'K2_Hmmo5crTYWiT_1sWnfQ' => 'K9hZAkRFuyfmLwceX8K4wg',
   'K9hZAkRFuyfmLwceX8K4wg' => 'K2_Hmmo5crTYWiT_1sWnfQ',

   '8860WNIW_oiLU6XZkGgklg' => 'yXMvhCmUADlaHabo-DiUYw',
   'yXMvhCmUADlaHabo-DiUYw' => '8860WNIW_oiLU6XZkGgklg',

   'cBzZpDqBaTdugB4JvfEhXA' => 'IALApn21BROm-knJfH96eA',
   'IALApn21BROm-knJfH96eA' => 'cBzZpDqBaTdugB4JvfEhXA',

   'w8sRfLP8U7uX4OktcSbb_w' => '2yBk6SvYQPnickE_QJrlaA',
   '2yBk6SvYQPnickE_QJrlaA' => 'w8sRfLP8U7uX4OktcSbb_w',

   '72pUqCkncwVVn65cIiX8aA' => 'GN72XbUh61J5wWQyW2oZsQ',
   'GN72XbUh61J5wWQyW2oZsQ' => '72pUqCkncwVVn65cIiX8aA',

   'MnoF8A3UAghzXKSunNSn2Q' => 'Gly54cM3avJg9n2F0l8V-g',
   'Gly54cM3avJg9n2F0l8V-g' => 'MnoF8A3UAghzXKSunNSn2Q',

   'PfJ17JQJKsX9KHHEkkr6iQ' => 'IRBkVErlqhKMeNCxRgjRQw',
   'IRBkVErlqhKMeNCxRgjRQw' => 'PfJ17JQJKsX9KHHEkkr6iQ',

   'hgy8A1Wnqyi4M-HJIFLpyQ' => 'zjQxaHZSb47p7l-b7Nhzgg',
   'zjQxaHZSb47p7l-b7Nhzgg' => 'hgy8A1Wnqyi4M-HJIFLpyQ',

   '9Y5kXneSwv-l-8TODZWQAQ' => '0hej0FRXraL5BNUKWhY_8w',
   '0hej0FRXraL5BNUKWhY_8w' => '9Y5kXneSwv-l-8TODZWQAQ'
}

# Pairs are kept as {[smallerId, largerId] => score}.

# Load the already evaluated pairs into memory.
def loadPairs()
   pairs = {}

   if (!File.exist?(PAIRS_FILE))
      return pairs
   end

   failure = false
   File.open(PAIRS_FILE, 'r'){|file|
      file.each{|line|
         parts = line.strip().split(',')
         minId = [parts[0], parts[1]].min()
         maxId = [parts[0], parts[1]].max()

         # Skip any self references that got added somehow.
         if (parts[0] == parts[1])
            next
         end

         if (pairs.include?([minId, maxId]))
            if (pairs[[minId, maxId]] == parts[2].to_i())
               next
            end

            $stderr.puts("Inconsistent Duplicate: [#{parts[0]},#{parts[1]}]")
            failure = true
         end

         pairs[[minId, maxId]] = parts[2].to_i()
      }
   }

   if (failure)
      exit(1)
   end

   return pairs
end

# All copy ratings for restaurants known to be the same.
def addSame(pairs)
   toAdd = []
   pairs.each_pair{|pair, value|
      if (SAME_IDS.include?(pair[0]))
         minId = [pair[1], SAME_IDS[pair[0]]].min()
         maxId = [pair[1], SAME_IDS[pair[0]]].max()
         toAdd << [[minId, maxId], value]
      end

      if (SAME_IDS.include?(pair[1]))
         minId = [pair[0], SAME_IDS[pair[1]]].min()
         maxId = [pair[0], SAME_IDS[pair[1]]].max()
         toAdd << [[minId, maxId], value]
      end
   }

   toAdd.each{|val|
      # Don't add self references.
      if (val[0][0] == val[0][1])
         next
      end

      pairs[val[0]] = val[1]
   }
end

# All the same restaurants are 100% (5) similar to itself.
def addIdentity(pairs)
   SAME_IDS.each_pair{|id1, id2|
      minId = [id1, id2].min()
      maxId = [id1, id2].max()

      pairs[[minId, maxId]] = MAX_SIM
   }
end

def writePairs(pairs)
   lines = pairs.to_a().map{|val| "#{val[0][0]},#{val[0][1]},#{val[1]}"}
   File.open(PAIRS_FILE, 'w'){|file|
      file.puts(lines.join("\n"))
   }
end

def main()
   pairs = loadPairs()

   addSame(pairs)
   addIdentity(pairs)

   writePairs(pairs)
end

if (__FILE__ == $0)
   main()
end
