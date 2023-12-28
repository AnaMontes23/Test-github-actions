import pandas as pd
from datetime import timedelta
import datetime
import psycopg2
import math
import boto3
import json
from botocore.exceptions import ClientError

class Kpi_baja:

    def __init__(self,type_period, get_general=False, **dates):
        self.carriers = ['Y4', 'N3', 'Q6']
        y4_stations = ['MEX', 'GDL', 'TIJ', 'CUN', 'MTY', 'BJX']
        q6_stations = ['SAL', 'LAX', 'SJO', 'GUA', 'MEX']
        n3_stations = ['SAL', 'CUN', 'MEX', 'SAP']
        self.stations = [y4_stations, n3_stations, q6_stations]

        self.type_period = type_period
        self.get_general = get_general
        self.dates = dates
        self.sql_to_database = """SELECT 
                carrier,legkey,start_station,end_station,skd_dst,flight_type,scheduled_start_time,
                actual_start_time,actual_off_time,actual_on_time,actual_end_time,schedule_end_time,
                scheduled_block_time,blocktime,check_in_pax,max_delay_code,turn_time_actual,
                turn_time_scheduled
                FROM joc_report_calculated
                WHERE scheduled_start_time >= '{} 00:00:00' AND scheduled_start_time <= '{} 23:59:59'
                AND flight_type = 'A';"""

        self.secret_name = 'ana_rds'
        self.region_name = 'us-east-1'
        self.data = None
        self.kpis_result = []

    def get_period(self):
        yesterday = datetime.datetime.utcnow() - timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        if self.type_period == 'Daily':
            self.sql_to_database = self.sql_to_database.format(yesterday_str, yesterday_str)
        
        elif self.type_period == 'Monthly':
            start_month = yesterday.replace(day=1)
            start_month = start_month.strftime('%Y-%m-%d')
            self.sql_to_database = self.sql_to_database.format(start_month, yesterday_str)
        
        elif self.type_period == 'Yearly':
            start_year = yesterday.replace(day=1, month = 1)
            start_year= start_year.strftime('%Y-%m-%d')
            self.sql_to_database = self.sql_to_database.format(start_year, yesterday_str)

        elif self.type_period == 'Custom':
            self.sql_to_database = self.sql_to_database.format(self.dates["start_period"], self.dates["end_period"])

    def get_data(self):
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=self.region_name
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            print(e)

        secret = json.loads(get_secret_value_response['SecretString'])
        conn_string = """   dbname={}
                        port={}
                        user= {}
                        password={}
                        host={} """.format(
                            secret['database'], secret['port'], secret['username'], secret['password'], secret['host']

                        )
        try:
            conn = psycopg2.connect(conn_string)
            self.data = pd.read_sql_query(self.sql_to_database, conn)
            conn.close()
        except Exception as e:
            print(e)

    def group_data(self):
        df = self.data.replace('', None)
        grouped_carriers = df.groupby("carrier")
        df_all_stations = []
        for carrier, df_carrier in grouped_carriers:
            stations_carrier = self.stations[self.carriers.index(carrier)]
            df_temp = df_carrier[df_carrier["end_station"].isin(stations_carrier)]
            founded_stations = df_temp.end_station.unique()
            for station in stations_carrier:
                if station not in founded_stations:
                    diccionario_null = self.null_dictionary(df_temp["carrier"].unique()[0], station)
                    self.kpis_result.append(diccionario_null)
            df_station = [group for _, group in df_temp.groupby("end_station")]
            df_all_stations.append(df_station)

        id_carrier = len(df_all_stations)
        for i in range(id_carrier):
            id_station = len(df_all_stations[i])
            for j in range(id_station):
                df_temp = df_all_stations[i][j]
                results = self.get_kpis(df_temp, "stations", True)
                self.kpis_result.append(results)
        
        for carrier, df_carrier in grouped_carriers:
            results = self.get_kpis(df_carrier, "system", True)
            self.kpis_result.append(results)

        if self.get_general:
            df_all = pd.DataFrame()
            for carrier, df_carrier in grouped_carriers:
                results = self.get_kpis(df_carrier, "system")
                self.kpis_result.append(results)
                df_all = pd.concat([df_all, df_carrier])
            results_general = self.get_kpis(df_all, "general")
            self.kpis_result.append(results_general)
        #print(results_general)


    def get_kpis(self, df_temp, type_station, get_coeficients=False):
        ######################Is Revenue ###########################
        df_temp["is_revenue"] = (
                (~df_temp["actual_start_time"].isnull()) &
                ~df_temp["actual_on_time"].isnull() &
                ~df_temp["actual_off_time"].isnull() &
                ~df_temp["actual_end_time"].isnull() &
                (df_temp["flight_type"] == 'A')
        )

        ######################Is disruption ############################
        df_temp["is_disruption"] = df_temp.apply(
            lambda row: 0 if (pd.isna(row["skd_dst"]) or row["skd_dst"] == row["end_station"])
            else 1, axis= 1
        )

        ################################OTP 15####################################
        df_temp["diff_in"] = (df_temp["actual_end_time"] - df_temp["schedule_end_time"]).dt.total_seconds() / 60
        df_temp["opt_15"] = ((df_temp["diff_in"] < 15) & (~df_temp["schedule_end_time"].isnull()) &
                            (df_temp["is_revenue"] == 1) & (df_temp["is_disruption"] == 0)).astype(int)

        ##############################OTP 15 WX & CTA ################################
        lista_codes = ["WC", "RW", "WL", "WG", "WR", "WS", "BA", "BC", "RB", "BD", "BE", "BZ", "BR", ""]
        df_temp["opt_15_code"] = df_temp.apply(
            lambda row: 1 if ((row["diff_in"] >= 15 and row["max_delay_code"] in lista_codes and row["is_revenue"] == 1) or (row["opt_15"] == 1)
            ) else 0, axis=1)
        ############################# BTP0 y BTP5 ####################################
        df_temp["diff_bt"] = df_temp["blocktime"] - df_temp["scheduled_block_time"]
        df_temp["btp_0"] = ((df_temp["diff_bt"] <= 0) & (df_temp["is_revenue"] == 1) & (df_temp["is_disruption"] == 0) &
                        (~df_temp["scheduled_start_time"].isnull()) & (~df_temp["schedule_end_time"].isnull())).astype(int)
        df_temp["btp_5"] = ((df_temp["diff_bt"] <= 5) & (df_temp["is_revenue"] == 1) & (df_temp["is_disruption"] == 0)).astype(int)
        
        ########################### ATD0 y ATD5 #####################################
        df_temp["diff_out"] = (df_temp["actual_start_time"] - df_temp["scheduled_start_time"]).dt.total_seconds() / 60 
        df_temp["atd_0"] = ((df_temp["diff_out"] <= 0) & (df_temp["is_revenue"] == 1)).astype(int)
        df_temp["atd_5"] = ((df_temp["diff_out"] < 5) & (df_temp["is_revenue"] == 1)).astype(int)
        
        ########################### GTP0 y GTP5 #####################################
        df_temp["diff_turn_time"] = df_temp["turn_time_actual"] - df_temp["turn_time_scheduled"]
        df_temp["gtp_0"] = ((df_temp["diff_turn_time"] <= 0) & (df_temp["turn_time_scheduled"] <= 240) &
                        (df_temp["is_revenue"] == 1) & (df_temp["is_disruption"] == 0) &
                        (~df_temp["turn_time_actual"].isnull())).astype(int)
        df_temp["gtp_5"] = ((df_temp["diff_turn_time"] <= 5) & (df_temp["turn_time_scheduled"] <= 240) &
                        (df_temp["is_revenue"] == 1) & (df_temp["is_disruption"] == 0) &
                        (~df_temp["turn_time_actual"].isnull())).astype(int)
        
        ######################### PAX ##############################################
        df_temp["pax_otp_num"] = ((df_temp["diff_in"] < 15) & (df_temp["check_in_pax"] > 0) &
                                (df_temp["is_revenue"] == 1) & (df_temp["is_disruption"] == 0)).astype(int)
        df_temp["pax_otp_den"] = ((df_temp["check_in_pax"] > 0) & (df_temp["is_revenue"] == 1)).astype(int)

        ############################### KPIs ##############################
        otp_15 = self.safe_division(df_temp["opt_15"].sum() , df_temp[df_temp["schedule_end_time"].notna() & df_temp["is_revenue"] == 1].shape[0])
        otp_15_code = self.safe_division(df_temp["opt_15_code"].sum() , df_temp[df_temp["scheduled_start_time"].notna() & df_temp["is_revenue"] == 1].shape[0])
        
        btp_0 = self.safe_division(df_temp["btp_0"].sum() , df_temp[(df_temp["scheduled_start_time"].notna())& (df_temp["schedule_end_time"].notna()) &
                                                                                                            (df_temp["is_revenue"] == 1) &
                                                                                                            (df_temp["is_disruption"] == 0)].shape[0])
        btp_5= self.safe_division(df_temp["btp_5"].sum() , df_temp[(df_temp["scheduled_start_time"].notna())& (df_temp["schedule_end_time"].notna()) &
                                                                                                            (df_temp["is_revenue"] == 1) &
                                                                                                            (df_temp["is_disruption"] == 0)].shape[0])

        atd_0 = self.safe_division(df_temp["atd_0"].sum() , df_temp[df_temp["actual_start_time"].notna() & df_temp["is_revenue"] == 1].shape[0])
        atd_5 = self.safe_division(df_temp["atd_5"].sum() , df_temp[df_temp["actual_start_time"].notna() & df_temp["is_revenue"] == 1].shape[0])
        gtp_0 = self.safe_division(df_temp["gtp_0"].sum() , df_temp[(df_temp["turn_time_scheduled"] <= 240 )& 
                                                                (df_temp["is_revenue"] == 1) &
                                                                ( df_temp["is_disruption"] == 0)].shape[0])
        gtp_5 = self.safe_division(df_temp["gtp_5"].sum() , df_temp[(df_temp["turn_time_scheduled"] <= 240) & 
                                                                (df_temp["is_revenue"] == 1) &
                                                                (df_temp["is_disruption"] == 0)].shape[0])
        
        pax_otp = self.safe_division(df_temp[df_temp["pax_otp_num"]== 1]["check_in_pax"].sum(), df_temp[df_temp["pax_otp_den"]==1]["check_in_pax"].sum())

        if type_station == "system":
            carrier = df_temp["carrier"].unique()[0]
            station = type_station
        elif type_station == 'general':
            carrier = 'ALL'
            station = type_station
        else:
            carrier = df_temp["carrier"].unique()[0]
            station = df_temp["end_station"].unique()[0]

        if get_coeficients == True:
            dict_result = {
                "Carrier": carrier,
                "Estacion": station,
                "OTP_15": otp_15,
                "Num_otp_15": df_temp["opt_15"].sum(),
                "Den_otp_15": df_temp[df_temp["scheduled_start_time"].notna() & df_temp["is_revenue"] == 1].shape[0],
                "OTP_WX&CTA": otp_15_code,
                "Num_otp_wx": df_temp["opt_15_code"].sum(),
                "Den_otp_wx": df_temp[df_temp["scheduled_start_time"].notna() & df_temp["is_revenue"] == 1].shape[0],
                "BTP_0": btp_0,
                "Num_btp0": df_temp["btp_0"].sum(),
                "Den_btp0": df_temp[(df_temp["scheduled_start_time"].notna()) & (df_temp["schedule_end_time"].notna()) &
                                    (df_temp["is_revenue"] == 1) &
                                    (df_temp["is_disruption"] == 0)].shape[0],
                "BTP_5": btp_5,
                "Num_btp5": df_temp["btp_5"].sum(),
                "Den_btp5": df_temp[(df_temp["scheduled_start_time"].notna()) & (df_temp["schedule_end_time"].notna()) &
                                    (df_temp["is_revenue"] == 1) &
                                    (df_temp["is_disruption"] == 0)].shape[0],
                "ATD_0": atd_0,
                "Num_atd0": df_temp["atd_0"].sum(),
                "Den_atd0": df_temp[df_temp["actual_start_time"].notna() & df_temp["is_revenue"] == 1].shape[0],
                "ATD_5": atd_5,
                "Num_atd5": df_temp["atd_5"].sum(),
                "Den_atd5": df_temp[df_temp["actual_start_time"].notna() & df_temp["is_revenue"] == 1].shape[0],
                "GTP_0": gtp_0,
                "Num_gtp0": df_temp["gtp_0"].sum(),
                "Den_gtp0": df_temp[(df_temp["turn_time_scheduled"] <= 240) &
                                    (df_temp["is_revenue"] == 1) &
                                    (df_temp["is_disruption"] == 0)].shape[0],
                "GTP_5": gtp_5,
                "Num_gtp5": df_temp["gtp_5"].sum(),
                "Den_gtp5": df_temp[(df_temp["turn_time_scheduled"] <= 240) &
                                    (df_temp["is_revenue"] == 1) &
                                    (df_temp["is_disruption"] == 0)].shape[0],
                "PAX": pax_otp,
                "Num_pax": df_temp[df_temp["pax_otp_num"] == 1]["check_in_pax"].sum(),
                "Den_pax": df_temp[df_temp["pax_otp_den"] == 1]["check_in_pax"].sum(),
            }
        else:
            day = df_temp["scheduled_start_time"].unique()[0]
            date = str(day).split("T")[0]
            dict_result = {
                "Dia": date,
                "Carrier": carrier,
                "Estacion": station,
                "OTP_15": otp_15,
                "OTP_WX&CTA": otp_15_code,
                "BTP_0": btp_0,
                "BTP_5": btp_5,
                "ATD_0": atd_0,
                "ATD_5": atd_5,
                "GTP_0": gtp_0,
                "GTP_5": gtp_5,
                "PAX": pax_otp
            }
        return dict_result

    @staticmethod
    def safe_division(numerator, denominator):
        if denominator != 0:
            return round((numerator / denominator)*100,2)
        else:
            if numerator == 0:
                return None
            else:
                return 0 
            
    @staticmethod
    def null_dictionary(carrier, station):
        dict_result = {
            "Carrier": carrier,
            "station": station,
            "OTP_15": None,
            "OTP_WX&CTA": None,
            "BTP_0": None,
            "BTP_5": None,
            "ATD_0": None,        
            "ATD_5": None,           
            "GTP_0": None,        
            "GTP_5": None,            
            "PAX": None         
            }
        return dict_result

#kpi= Kpi_baja("Custom", get_general=True, start_period = '2023-01-01', end_period = '2023-09-30')
#kpi.get_period()
#kpi.get_data()
#kpi.group_data()
#kpi.upload_to_dynamodb()



