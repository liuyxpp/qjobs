"""defines constants for qjobs"""

from collections import OrderedDict, namedtuple
from os.path import expandvars, expanduser

Itmtp = namedtuple('Itmtp', ['dscr', 'xml_tag'])

itms = OrderedDict((
    ('i', Itmtp('job id', ['Job_Id'])),
    ('p', Itmtp('job priority', ['Priority'])),
    ('n', Itmtp('job name', ['Job_Name'])),
    ('o', Itmtp('job owner', ['Job_Owner'])),
    ('s', Itmtp('job state', ['job_state'])),
    ('t', Itmtp('job start/submission time', ['start_time',
                                              'qtime'])),
    ('e', Itmtp('elapsed time since start/submission', [])),
    ('q', Itmtp('queue name without domain', ['queue'])),
    ('d', Itmtp('queue domain', ['server'])),
    ('k', Itmtp('queue name with domain', [])),
    ('r', Itmtp('requested queue(s)', ['hard_req_queue'])),
    ('l', Itmtp('number of slots used', ['slots']))
    ))

path_config = '/home/lyx/.config/qjobs/qjobs.rc'
path_config = expanduser(expandvars(path_config))

dflt_section = 'Defaults'

default_config = OrderedDict((
    ('out', 'inesq'),
    ('total', 's'),
    ('sort', 'ips'),
    ('reversed_itms', 'psl'),
    ('out_format', ''),
    ('start_format', '{Y}-{m}-{d} {H}:{M}:{S}'),
    ('elapsed_format', '{H:02d}:{m:02d}'),
    ('width_tot', 80),
    ('sep_tot', '[     ]'),
    ('sep', '[   ]'),
    ('users', 'lyx'),
    ('editor', 'vim'),
    ('qstat_cmd', '/usr/local/bin/qstat')
    ))
