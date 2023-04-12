import os
import time
from multiprocessing import Process

import poisson as nextTime




def start_simulation(sim_params, seed):
    os.system('sh start_user %d %f' % seed, nextTime(1/5, 0))
    


def main():
    sim_params = {
        'rep': int(os.getenv('Repetition')),
        'users': int(os.getenv('Users')),
        'bs': int(os.getenv('BaseStation'))
    }

    print("Starting simulation with", sim_params['users'], "users")

    users = [i for i in range(sim_params['users'])]

    jobs = []
    while users:
        user = users.pop()
        
        job = Process(target=user.run, args=(sim_params, user))
        jobs.append(job)
        job.start()
        
    
    while jobs:
        job = jobs.pop()
        job.join()

    print("Done.")


if __name__ == '__main__':
    main()
