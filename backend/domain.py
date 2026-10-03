import csv, hashlib, io, json, math, re
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from .validation import validate_input, http_url, unique

def now(): return datetime.now(timezone.utc).isoformat()
def validate(data,records): return initialize(validate_input(data,CONFIG['example']),records)

def initialize(row,records):
    unique(records,row,['name'])
    return dict(row,movements=[{'type':'opening','delta':row['quantity'],'balance':row['quantity'],'at':now()}])
def summary(rows): return {'items':len(rows),'units':sum(r['quantity'] for r in rows),'low_stock':sum(r['quantity']<=r['reorder_level'] for r in rows),'movements':sum(len(r.get('movements',[])) for r in rows)}
def transition(row,action):
    if action not in ['consume','restock']: raise ValueError('Unsupported inventory action')
    if action=='consume' and row['quantity']==0: raise ValueError('No stock available')
    delta=1 if action=='restock' else -1; quantity=row['quantity']+delta
    movement={'type':action,'delta':delta,'balance':quantity,'at':now()}
    return dict(row,quantity=quantity,movements=row.get('movements',[])+[movement])
