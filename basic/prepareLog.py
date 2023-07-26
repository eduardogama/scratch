import os
import shutil


print("Directory name [Default: users/]:")
dir_name = str(input())

dir_name = 'users' if dir_name == "" else dir_name

print("Number of seeds[Default: 10]:")
seeds = str(input())

seeds = 10 if seeds == "" else int(seeds)


for s in range(seeds):
    location = dir_name + '/' + str(s) + '/'
    users = [ x for x in os.listdir(location) if os.path.isdir(location + x)] 
    
    
    for u in users:
    
        newfile = open(location + u + '-player.csv','w')
        newfile.write('K liveQoE videoQuality videoQualitySwitch StallsDuration bufferLevel throughput\n')

        pathfile = location + u + '/Default/chrome_debug.log'
        
        with open(pathfile) as f:
            lines = f.readlines()
            
            count = 0
            for line in lines:
                cells = line.split('"')
                print(cells)
                if not "http://143.106.73.50:30002/samples/ericsson/js/main.js" in cells[-1] or cells[1] == "ok":
                    continue
                
                if count < 2:
                    count += 1
                    continue
                    
                newfile.write(cells[1] + "\n")
    
    newfile.close()

#    shutil.rmtree(location)
    
