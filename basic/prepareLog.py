import os
import shutil


print("Directory name [Default: .browser/]:")
dir_name = str(input())

dir_name = 'users/' if dir_name == "" else dir_name

print("Number of users[Default: 10]:")
n_users = str(input())

n_users = 10 if n_users == "" else int(n_users)


for u in range(1, n_users+1):
    
    location = dir_name + '/user-' + str(u)
    pathfile = location + '/Default/chrome_debug.log'
    
    newfile = open(dir_name + '/' + 'user-' + str(u) + '-browser.csv','w')
    newfile.write('K liveQoE videoQuality videoQualitySwitch StallsDuration bufferLevel\n')

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
    
