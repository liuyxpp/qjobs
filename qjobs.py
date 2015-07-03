#!PYTHON_CMD
from subprocess import Popen, PIPE
import argparse
import configparser
import xml.etree.ElementTree as ET

items = 'ipnostqdQl'

parser = argparse.ArgumentParser(\
        description='qstat wrapper for better output',add_help=False)
parser.add_argument('-c','--config',\
        default='PATH_CONFIG',\
        help='specify config file',metavar='FILE')

args, remaining_argv = parser.parse_known_args()
try: 
    conf_parser = configparser.ConfigParser()
    conf_parser.read(args.config)
    defaults = dict(conf_parser.items('Defaults'))
except:
    defaults = {'out':'instq','total':'s'}

parser = argparse.ArgumentParser(parents=[parser])
parser.add_argument('-o','--out',nargs='*',\
        help="""specify output format (default instq):
        i: job id,     p: job prior,  n: job name,
        o: job owner,  s: job state,  t: start/sub time,
        q: queue,      l: slots.""")
parser.add_argument('-t','--total',nargs='*',\
        help='display total number of jobs and their distribution')
parser.add_argument('-f','--file',type=argparse.FileType('r'),\
        help='use given xml file as input (for debug)')

parser.set_defaults(**defaults)
args = parser.parse_args(remaining_argv)

if args.file:
    f = args.file
else:
    f = Popen('\qstat -u USER_NAME -xml -r', shell=True, stdout=PIPE).stdout

columns = ''
for c in ''.join(args.out):
    if c in items: columns += c

totals = ''
for c in ''.join(args.total):
    if c in items: totals += c

jobsTree = ET.parse(f)
jobsList = jobsTree.getroot().iter('job_list')

alljobs = []
jobCounts = {}

for j in jobsList:
    job = {}
    job['i'] = j.find('JB_job_number').text
    job['p'] = j.find('JAT_prio').text
    job['n'] = j.find('JB_name').text
    job['o'] = j.find('JB_owner').text
    job['s'] = j.find('state').text
    job['q'] = ''
    job['d'] = ''
    job['Q'] = ''
    job['l'] = j.find('slots').text
    if job['s']=='r' :
        job['t'] = j.find('JAT_start_time').text
        job['Q'] = j.find('queue_name').text
        job['q'], job['d'] = job['Q'].rsplit('@')
    elif job['s'] in ['dt','dr'] :
        job['t'] = j.find('JAT_start_time').text
    else:
        try:
            job['t'] = j.find('JB_submission_time').text
        except AttributeError:
            job['t'] = None
    if job['t']:
        job['t'] = job['t'].replace('T',' ')
    else:
        job['t'] = 'not set'

    for c in totals:
        if not c in jobCounts: jobCounts[c]={}
        if job[c] in jobCounts[c]:
            jobCounts[c][job[c]] += 1
        else:
            jobCounts[c][job[c]] = 1

    alljobs.append(job)


if not alljobs:
    print('No pending or running job.')
else:
    if columns:
        l = {}
        for c in columns:
            l[c] = max(len(job[c]) for job in alljobs)

        for job in alljobs:
            print(*(job[c].ljust(l[c]) for c in columns), sep='   ')

    if totals:
        print('tot: {}'.format(len(alljobs)))
        for c in totals:
            print(*('{}: {}'.format(k,v) for k,v in jobCounts[c].items()),\
                    sep='   ')