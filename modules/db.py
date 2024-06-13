import motor.motor_asyncio
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Dict
from .schemas import Group, PeriodData

class MongoAggregator:

    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]


    async def aggregate_data(self, period_data: PeriodData) -> Dict[str, List]:
        """ Aggregate data from database, return dict[dataset(sum)|labels(datetime)]"""
        dt_from_dt = period_data.dt_from
        dt_upto_dt = period_data.dt_upto
        group_type = period_data.group_type

        if group_type == Group.MONTH:
            step = relativedelta(months=1)
        elif group_type == Group.WEEK:
            step = timedelta(weeks=1)
        elif group_type == Group.HOUR:
            step = timedelta(hours=1)
        else:
            step = timedelta(days=1)
        
        date_format = "%Y-%m-%dT%H:%M:%S"

        pipeline = [
            {
                "$match": {
                    "dt": {"$gte": dt_from_dt, "$lte": dt_upto_dt}
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateTrunc": {"unit": group_type, "date": "$dt"}
                    },
                    "total": {"$sum": "$value"}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]

        cursor = self.collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)
        print(result)

        data = {item["_id"].strftime(date_format): item["total"] for item in result}

        final_dt = []
        current_date = dt_from_dt

        if group_type == Group.WEEK:
            # Adjust to the nearest Sunday before the start date
            current_date -= timedelta(days=current_date.weekday() + 1)

        while current_date <= dt_upto_dt:
            final_dt.append(current_date.strftime(date_format))
            current_date += step

        final_sum = []
        for i in final_dt:
            final_sum.append(data.get(i, 0))

        return {"dataset": final_sum, "labels": final_dt}
