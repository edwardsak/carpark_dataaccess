from datalayer.models.models import AgentMovement, Tran, Deposit, TopUp
from sharelib.utils import DateTime

from datetime import timedelta
from google.appengine.ext import ndb

class Statement():
    def get_json(self, agent_code, date_from):
        # get tran
        trans = Tran.query(
                           Tran.agent_code==agent_code,
                           Tran.tran_date==date_from,
                           ).order(Tran.seq).fetch()
        
        # get bf amt
        bal_amt = 0
        q = AgentMovement.query(
                                ancestor=ndb.Key('Agent', agent_code),
                                AgentMovement.movement_date==date_from - timedelta(days=1),
                                )
        movement = q.get()
        
        data = []
        if movement:
            bal_amt = movement.bal_amt
            
            data.append({
                         "date": DateTime.to_date_string(date_from),
                         'docNo': '',
                         'description': 'B/F',
                         'dbAmt': 0,
                         'crAmt': 0,
                         'balAmt': bal_amt
                         })
        
        # get deposit
        deposit_ids = {}
        deposits = Deposit.query(
                                 ancestor=ndb.Key('Agent', agent_code),
                                 Deposit.tran_date==date_from 
                                 ).fetch()
        
        for deposit in deposits:
            deposit_ids[deposit.tran_code] = deposit
            
        # get top up
        top_up_ids = {}
        top_ups = TopUp.query(
                              ancestor=ndb.Key('Agent', agent_code),
                              TopUp.tran_date==date_from
                              ).fetch()
        
        for top_up in top_ups:
            top_up_ids[top_up.tran_code] = top_up
            
        # ppl
        for tran in trans:
            if tran.tran_type == Tran.TRAN_TYPE_DEPOSIT:
                deposit = deposit_ids[tran.tran_code]
                
                bal_amt += deposit.amt
                bal_amt = round(bal_amt, 2)
                
                data.append({
                             "date": DateTime.to_date_string(deposit.tran_date),
                             'docNo': deposit.tran_code,
                             'description': deposit.payment_ref_no,
                             'dbAmt': deposit.amt,
                             'crAmt': 0,
                             'balAmt': bal_amt
                             })
                
            elif tran.tran_type == Tran.TRAN_TYPE_TOP_UP:
                top_up = top_up_ids[tran.tran_code]
                
                bal_amt -= top_up.amt
                bal_amt = round(bal_amt, 2)
                
                data.append({
                             "date": DateTime.to_date_string(top_up.tran_date),
                             'docNo': top_up.doc_no,
                             'description': top_up.car_reg_no,
                             'dbAmt': 0,
                             'crAmt': top_up.amt,
                             'balAmt': bal_amt
                             })
        
        json_values = {
                       'data': data
                       }
        return json_values