from datalayer.models.models import TopUp
from sharelib.utils import DateTime

class TopUpSummaryByDayAndAgent():
    def get(self, date_from, date_to, agent_code):
        return self.__get(date_from, date_to, agent_code)
    
    def __get(self, date_from, date_to, agent_code, date_format='%Y%m%d'):
        # get top up
        q = TopUp.query()
        
        if date_from:
            q = q.filter(TopUp.tran_date >= date_from)
            
        if date_to:
            q = q.filter(TopUp.tran_date <= date_to)
            
        if agent_code and len(agent_code) > 0:
            q = q.filter(TopUp.agent_code==agent_code)
            
        q = q.filter(TopUp.void==False)
        top_ups = q.order(TopUp.tran_date, TopUp.agent_code).fetch()
        
        # sum amt
        top_up_list = []
        top_up_days = {}
        for top_up in top_ups:
            key = "%s|%s" % (top_up.tran_date.strftime(date_format), top_up.agent_code)
            
            top_up_day = None
            if top_up_days.has_key(key):
                top_up_day = top_up_days[key]
            else:
                top_up_day = TopUpSummaryViewModel()
                top_up_day.tran_date = top_up.tran_date
                top_up_day.agent_code = top_up.agent_code
                top_up_days[key] = top_up_day
                top_up_list.append(top_up_day)
            
            top_up_day.sub_total += top_up.sub_total
            top_up_day.comm_amt += top_up.comm_amt
            top_up_day.amt += top_up.amt
        
        return top_up_days
    
class TopUpSummaryByMonthAndAgent():
    def get(self, date_from, date_to, agent_code):
        date_from2 = DateTime.first_day_of_month(date_from)
        date_to2 = DateTime.last_day_of_month(date_to)
        
        # get charge
        summary_by_day = TopUpSummaryByDayAndAgent()
        return summary_by_day.__get(date_from2, date_to2, agent_code, '%Y%m')

class TopUpSummaryByDay():
    def get(self, date_from, date_to):
        return self.__get(date_from, date_to)
    
    def __get(self, date_from, date_to, date_format='%Y%m%d'):
        # get top up
        q = TopUp.query()
        
        if date_from:
            q = q.filter(TopUp.tran_date >= date_from)
            
        if date_to:
            q = q.filter(TopUp.tran_date <= date_to)
            
        q = q.filter(TopUp.void==False)
        top_ups = q.order(TopUp.tran_date).fetch()
        
        # sum amt
        top_up_list = []
        top_up_days = {}
        for top_up in top_ups:
            key = "%s" % (top_up.tran_date.strftime(date_format))
            
            top_up_day = None
            if top_up_days.has_key(key):
                top_up_day = top_up_days[key]
            else:
                top_up_day = TopUpSummaryViewModel()
                top_up_day.tran_date = top_up.tran_date
                top_up_days[key] = top_up_day
                top_up_list.append(top_up_day)
            
            top_up_day.sub_total += top_up.sub_total
            top_up_day.comm_amt += top_up.comm_amt
            top_up_day.amt += top_up.amt
        
        return top_up_list
    
class TopUpSummaryByMonth():
    def get(self, date_from, date_to):
        date_from2 = DateTime.first_day_of_month(date_from)
        date_to2 = DateTime.last_day_of_month(date_to)
        
        # get charge
        summary_by_day = TopUpSummaryByDay()
        return summary_by_day.__get(date_from2, date_to2, '%Y%m')
    
class TopUpSummaryViewModel():
    tran_date = None
    agent_code = ''
    sub_total = 0
    comm_amt = 0
    amt = 0