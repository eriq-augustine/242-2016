# Look for Rand Indeces in a file and adjust them to the correct values.

R_INDEX_PATTERN = /(0\.\d{3,})/

NUM_PAIRS = 1302177.0
NUM_ENTITIES = 3068.0

def adjustIndex(oldValue)
   return (oldValue * (NUM_PAIRS + NUM_ENTITIES) - NUM_ENTITIES) / NUM_PAIRS
end

def parseFile(path)
   File.open(path, 'r'){|file|
      file.each{|line|
         line.gsub!(R_INDEX_PATTERN){|oldIndex|
            "%6.5f" % adjustIndex(oldIndex.to_f())
         }

         puts line
      }
   }
end

def main(path)
   parseFile(path)
end

if (__FILE__ == $0)
   if (ARGV.size() != 1)
      puts "USAGE: ruby #{__FILE__} <path>"
      exit(1)
   end

   main(ARGV[0])
end
