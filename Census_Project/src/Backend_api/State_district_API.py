# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 12:08:14 2021

@author: Arya Kapoor
"""

from flask import Flask,request,make_response,jsonify
from flask_cors import CORS,cross_origin
import pyodbc
from flask_restful import Resource, Api, reqparse
import pandas as pd
from skcriteria import Data,MAX,MIN
from skcriteria.madm import simple
import numpy as np
from statistics import mean
import ast

#Created flask application object
app=Flask(__name__)
#app.config["DEBUG"]=
#Enabled CORS
CORS(app)


api=Api(app)
#@app.route('/states',methods=['GET'])

class States_old(Resource):
    def get(self):
        
        state_excel=pd.read_excel(r'C:\Users\Arya Kapoor\.spyder-py3\State_ranks.xlsx')
        state_df=pd.DataFrame(state_excel)
        state_list=list(state_df.iloc[:,1])
        bd_list=list(state_df.iloc[:,2])
        pt_list=list(state_df.iloc[:,3])
        rk_list=list(state_df.iloc[:,4])
        rs_list=[]
        for i in range(len(state_list)):
            s_dict={'State':state_list[i],'Best_District':bd_list[i],'Points':pt_list[i],'Rank':rk_list[i]}
            rs_list.append(s_dict)

        #print(rs_list)
        #Returning the rs_list
        return {'data':rs_list},200

#creating the endpoint for url '/states_old'
api.add_resource(States_old,'/states_old')
def prelight_response():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
class States(Resource):
    def get(self):
        if request.method=="OPTIONS":
            return prelight_response()
        elif request.method=="GET": 
            state_excel=pd.read_excel(r'C:\Users\Arya Kapoor\.spyder-py3\State_ranks.xlsx')
            state_df=pd.DataFrame(state_excel)
            state_list=list(state_df.iloc[:,1])
            bd_list=list(state_df.iloc[:,2])
            pt_list=list(state_df.iloc[:,3])
            rk_list=list(state_df.iloc[:,4])
            rs_list=[]
            for i in range(len(state_list)):
                s_dict={'State':state_list[i],'Best_District':bd_list[i],'Points':pt_list[i],'Rank':rk_list[i]}
                rs_list.append(s_dict)
                
            
            print("State API running...")
            #print(rs_list)
            
            '''
            response=rs_list
            response.headers.add("Access-Control-Allow-Origin","*")
            '''
            #returning the rs_list containing the data about state rankings
            return jsonify(rs_list)
        

#creating the endpoint for url '/state'        
api.add_resource(States,'/states')
'''
class Districtsnew(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('state',required=True)
        args=parser.parse_args()
        print("State name:",args['state'])  
        return {'data':args},200
api.add_resource(States,'/states')     
'''
class Districts(Resource):
    def get(self):
        try:
            #Initialising the parser object
            parser=reqparse.RequestParser()
            #Specifying the arguments needed
            parser.add_argument('state',required=True)
            #Adding the arguments to a dictionary
            args=parser.parse_args()
            print("District API running....")
            print("State name:",args['state'])
            #Retreiving the state name
            state_name=args['state']
            #Established Connection to the Data Base using SQL Server Authentication
            connect=pyodbc.connect('DRIVER={SQL Server};Server=LAPTOP-V5I3M0RK\SQLEXPRESS;Database=stock;UID=ABC_login;PWD=abc;Trusted_connection=yes;')
            print("Connection Established")
            #Declared Cursor Object
            #Created different lists which can contain the average points of different districts for the 4 algo's being used.
            sum_ws_l=[]
            max_ws_l=[]
            sum_wp_l=[]
            max_wp_l=[]
            dis_l=[]
            res_l=[]
            cursor=connect.cursor()
            #cursor.execute("select top 1 distinct(district_name) from census where state_name=(?)",state_name)
            cursor.execute("select district_name from census where state_name=(?) group by DISTRICT_NAME;",state_name)
            district_list=list(cursor.fetchall())
            print(district_list)
            for d in district_list:
                print("\nDistrict name:",d)
                
                cursor.execute("select census_id from census where district_name=?",d)
                
                l_cid=list(cursor.fetchall())
                #print(l_cid)
            
            
                #Since we already added the first row in the numpy array we loop from the next ID
                
                
                data=np.array([[55.3, 42.6, 2.1, 1.3, 2.5, 0.2, 4.1, 2.8, 7.7, 43.7, 36.1, 0.3, 1.9, 3.8, 0.3, 2.1, 7.0, 1.8, 78.7, 0.0, 0.9, 2.4, 0.1, 5.5, 37.4, 1.5, 7.6, 58.3, 13.1, 10.0, 6.5, 3.1, 69.7, 26.7, 3.6, 94.6, 3.3, 0.2, 0.5, 0.0, 0.0, 0.1, 0.0, 0.9, 51.3, 40.6, 8.1, 95.9, 3.2, 0.4, 0.1, 0.0, 0.4, 35.2, 3.9, 0.5, 71.1, 17.3, 11.6, 89.2, 6.0, 4.7, 1.0, 0.2, 0.1, 0.0, 34.3, 63.1, 0.0, 0.1, 0.0, 1.1, 98.7, 64.3, 34.3, 0.2, 0.1, 0.2, 1.1, 28.0, 74.2, 20.1, 10.8, 4.3, 62.6, 23.5, 16.1, 10.1, 19.2, 18.8, 90.7, 5.4, 2.4, 1.6]])
            
            
            
            #Looping to retreive data for each census ID
                for i in l_cid:
                    #print("\n Data for Census_ID:",i)
                    cursor.execute("select NOH_TOTAL_GOOD,NOH_TOTAL_LIVABLE,NOH_TOTAL_DILAPIDATED,MOR_GLASS,MOR_PLASTIC_POLYTHENE,MOR_HAND_MADE_TILES,MOR_MACHINE_MADE_TILES,MOR_BURNT_BRICK,MOR_STONE,MOR_GI,MOR_CONCRETE,MOW_GRASS,MOW_PLASTIC,MOW_MUD,MOW_WOOD,MOW_STONE_NOT_PACKED_WITH_MORTAR,MOW_STONE_PACKED_WITH_MORTAR,MOW_GI,MOW_BURNT_BRICK,MOF_MUD,MOF_WOOD,MOF_BURNT_BRICK,MOF_STONE,MOF_CEMENT,MOF_MOSAIC,NOD_NO,NOD_ONE_ROOM,NOD_TWO_ROOM,NOD_THREE_ROOM,NOD_FOUR_ROOM,NOD_FIVE_ROOM,NOD_SIX_ROOM_AND_ABOVE,OWNERSHIP_STATUS_OWNED,OWNERSHIP_STATUS_RENTED,OWNERSHIP_STATUS_ANY_OTHERS,MSDW_TAP_WATER_FROM_TREATED_SOURCE,MSDW_TAP_WATER_FROM_UN_TREATED_SOURCE,MSDW_COVERED_WELL,MSDW_UNCOVERED_WELL,MSDW_HANDPUMP,MSDW_TUBEWELL,MSDW_SPRING,MSDW_RIVER,MSDW_TANK,LDW_WITHIN_PREMISES,LDW_NEAR_PREMISES,LDW_AWAY,MSL_ELECTRICITY,MSL_KEROSENE,MSL_SOLAR_ENERGY,MSL_OTHER_OIL,MSL_ANY_OTHER,MSL_NO_LIGHTNING,FLUSH_PIPED_SEWER_SYSTEM,FLUSH_SEPTIC_TANK,FLUSH_OTHER_SYSTEM,NUMBER_OF_HOUSEHOLDS_YES_BATHROOM,NUMBER_OF_HOUSEHOLDS_YES_ENCLOSURE_WITHOUT_ROOF,NUMBER_OF_HOUSEHOLDS_NO,WWO_CONNECTED_TO_CLOSED_DRAINAGE,WWO_CONNECTED_TO_OPEN_DRAINAGE,WWO_CONNECTED_TO_NO_DRAINAGE,TFUC_FIRE_WOOD,TFUC_CROP_RESIDUE,TFUC_COWDUNG_CAKE,TFUC_COAL,TFUC_KEROSENE,TFUC_LPG,TFUC_ELECTRICITY,TFUC_BIOGAS,TFUC_ANY_OTHER,TFUC_NO_COOKING,KF_COOKING_INSIDE_HOUSE,KF_HAS_KITCHEN,KF_HAS_DOES_NOT_HAVE_KITCHEN,KF_COOKING_OUTSIDE_HOUSE,KF_CO_HAS_KITCHEN,KF_CO_HAS_NO_KITCHEN,KF_NO_COOKING,AOA_RADIO,AOA_TELEVISION,AOA_COMPUTER_HAS_INTERNET,AOA_COMPUTER_HAS_NO_INTERNET,AOA_TELEPHONE_LANDLINE,AOA_TELEPHONE_MOBILE,AOA_TELEPHONE_BOTH,AOA_BICYCLE,AOA_SCOOTER,AOA_VAN,AOA_HOUSEHOLD_WITH_TV,HOUSEHOLD_PERMANENT,HOUSEHOLD_SEMI_PERMANENT,HOUSEHOLD_TOTAL_TEMPORARY,HOUSEHOLD_UNCLASSIFABLE from census where  CENSUS_ID IN(?)",(i))
                    l=list(cursor.fetchone())
                    #print(l)
                    #Converting list into numpy array
                    row=np.array(l)
                    #Appended the array to the 2D- Matrix
                    data=np.append(data,[row],axis=0)
                print("\nData Matrix:")    
                print(data)
            
            
            #Printing the dimensions of the Matrix
                print("\nSize of Data Matrix:",data.shape)
            #cursor.execute("select NOH_TOTAL_GOOD,NOH_TOTAL_LIVABLE,NOH_TOTAL_DILAPIDATED,MOR_GLASS,MOR_PLASTIC_POLYTHENE,MOR_HAND_MADE_TILES,MOR_MACHINE_MADE_TILES,MOR_BURNT_BRICK,MOR_STONE,MOR_GI,MOR_CONCRETE,MOW_GRASS,MOW_PLASTIC,MOW_MUD,MOW_WOOD,MOW_STONE_NOT_PACKED_WITH_MORTAR,MOW_STONE_PACKED_WITH_MORTAR,MOW_GI,MOW_BURNT_BRICK,MOF_MUD,MOF_WOOD,MOF_BURNT_BRICK,MOF_STONE,MOF_CEMENT,MOF_MOSAIC,NOD_NO,NOD_ONE_ROOM,NOD_TWO_ROOM,NOD_THREE_ROOM,NOD_FOUR_ROOM,NOD_FIVE_ROOM,NOD_SIX_ROOM_AND_ABOVE,OWNERSHIP_STATUS_OWNED,OWNERSHIP_STATUS_RENTED,OWNERSHIP_STATUS_ANY_OTHERS,MSDW_TAP_WATER_FROM_TREATED_SOURCE,MSDW_TAP_WATER_FROM_UN_TREATED_SOURCE,MSDW_COVERED_WELL,MSDW_UNCOVERED_WELL,MSDW_HANDPUMP,MSDW_TUBEWELL,MSDW_SPRING,MSDW_RIVER,MSDW_TANK,LDW_WITHIN_PREMISES,LDW_WITHIN_PREMISES,LDW_NEAR_PREMISES,LDW_AWAY,MSL_ELECTRICITY,MSL_KEROSENE,MSL_SOLAR_ENERGY,MSL_OTHER_OIL,MSL_ANY_OTHER,MSL_NO_LIGHTNING,FLUSH_PIPED_SEWER_SYSTEM,FLUSH_SEPTIC_TANK,FLUSH_OTHER_SYSTEM,NUMBER_OF_HOUSEHOLDS_YES_BATHROOM,NUMBER_OF_HOUSEHOLDS_YES_ENCLOSURE_WITHOUT_ROOF,NUMBER_OF_HOUSEHOLDS_NO,WWO_CONNECTED_TO_CLOSED_DRAINAGE,WWO_CONNECTED_TO_OPEN_DRAINAGE,WWO_CONNECTED_TO_NO_DRAINAGE,TFUC_FIRE_WOOD,TFUC_CROP_RESIDUE,TFUC_COWDUNG_CAKE,TFUC_COAL,TFUC_KEROSENE,TFUC_LPG,TFUC_ELECTRICITY,TFUC_BIOGAS,TFUC_ANY_OTHER,TFUC_NO_COOKING,KF_COOKING_INSIDE_HOUSE,KF_HAS_KITCHEN,KF_HAS_DOES_NOT_HAVE_KITCHEN,KF_COOKING_OUTSIDE_HOUSE,KF_CO_HAS_KITCHEN,KF_CO_HAS_NO_KITCHEN,KF_NO_COOKING,AOA_RADIO,AOA_TELEVISION,AOA_COMPUTER_HAS_INTERNET,AOA_COMPUTER_HAS_NO_INTERNET,AOA_TELEPHONE_LANDLINE,AOA_TELEPHONE_MOBILE,AOA_TELEPHONE_BOTH,AOA_BICYCLE,AOA_SCOOTER,AOA_VAN,AOA_HOUSEHOLD_WITH_TV,HOUSEHOLD_PERMANENT,HOUSEHOLD_SEMI_PERMANENT,HOUSEHOLD_TOTAL_TEMPORARY,HOUSEHOLD_UNCLASSIFABLE from census where  CENSUS_ID IN(?)",(582602))
                
            #Reading the weights for each attribute from excel
                w=pd.read_excel(r'C:\Users\Arya Kapoor\.spyder-py3\Weights.xlsx')
            
                #Made a dataframe
                df=pd.DataFrame(w)
                #This is for displaying entire dataframe
                pd.set_option("display.max_rows",None,"display.max_columns",None)
                
                #Created np array with the first row inserted already
                w1=np.array([[3.0, 2.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
                #Getting the total no of rows
                rows=df.shape[0]
                
                #Looping through each row
                for i in range(1,rows):
                    #Converting each row in dataframe to list
                    r=list(df.iloc[i])
                    #Then converting it into numpy array
                    ins=np.array(r)
                    #Appending it to the w1 2D-Matrix
                    w1=np.append(w1,[ins],axis=0)
                
                #Got the weights matrix by taking the transpose of w1 matrix
                weights=np.transpose(w1)       
                print("\nWeights Matrix:",weights)
                print("\nSize of Weights Matrix:",weights.shape)
                
                #Multiplying the Data Matrix to Weights Matrix
                result=np.matmul(data,weights)
                print("\nResult Matrix:")
                print(result)
                print("\nSize of Result Matrix:",result.shape)
            
                l_cid.insert(0,582602)
                c_names=['NOH_Score', 'MOR_Score', 'MOW_Score', 'MOF_Score', 'NOD_Score',
                       'OWNERSHIP_Score', 'MSDW_Score', 'LDW_Score', 'MSL_Score',
                       'FLUSH_Score', 'BATHROOM_Score', 'WWO_Score', 'TFUC_Score', 'KF_Score',
                       'AOA_Score', 'House_Classification_Score']
                
                
                #Converting the Numpy Array into Dataframe
               #print("\nData Frame:")
                df=pd.DataFrame(data=result,index=l_cid,columns=c_names)
                df.index.name='CENSUS_ID'
                df.reset_index(level=0,inplace=True)
                #Creating data Object for MCDA
                df.drop('CENSUS_ID',axis='columns',inplace=True)
                data=Data(df,[MIN,MAX,MAX,MAX,MAX,MAX,MAX,MIN,MAX,MAX,MAX,MAX,MAX,MAX,MAX,MIN],
                          weights=[0.02,0.1,0.1,0.1,0.03,0.05,0.1,0.03,0.1,0.02,0.05,0.05,0.05,0.05,0.1,0.05],
                          anames=l_cid,
                          cnames=df.columns)
                
                
                #print(data)
                #Taking the copy of the data frame in census data
                census_data=df.copy()
                
                
                
                # Weighted Sum
                print("\nPerforming Weighted Sum MCDA:")
                dm=simple.WeightedSum(mnorm="sum")
                #Made Decision using decide()
                dec_sum_ws=dm.decide(data)
                #print(dec)
                #Using sum normalisation in weighted sum
                print("\nSum normalisation:")
                #print("Points:")
                points=dec_sum_ws.e_.points
                #print(points)
                #print("Ranks:")
                ranks=dec_sum_ws.rank_
                #print(ranks)
                #Appedning the points in the copied data frame
                census_data.loc[:,'Points_Sum_WS']=points
                census_data.loc[:,'Ranks_Sum_WS']=ranks
                
                #Using max normalisation in weighted sum
                #print("\nMax Normalisation:")
                dm=simple.WeightedSum(mnorm='max')
                dec_max_ws=dm.decide(data)
                #print("Points:\n",dec_max_ws.e_.points)
                #print("Ranks:\n",dec_max_ws.rank_)
                census_data.loc[:,'Points_Max_WS']=dec_max_ws.e_.points
                census_data.loc[:,'Ranks_Max_WS']=dec_max_ws.rank_
                
                
                # Weighted Product
                print("\nPerforming Weighted Product MCDA:")
                #Using sum normalisation in weighted product
                print("\nSum normalisation:")
                dm=simple.WeightedProduct(mnorm='sum')
                dec_sum_wp=dm.decide(data)
                #print("Points:\n",dec_sum_wp.e_.points)
                #print("Ranks:\n",dec_sum_wp.rank_)
                census_data.loc[:,'Points_Sum_WP']=dec_sum_wp.e_.points
                census_data.loc[:,'Ranks_Sum_WP']=dec_sum_wp.rank_
                
                #Using max normalisation in weighted product
                print("\nMax normalisation:")
                dm=simple.WeightedProduct(mnorm='max')
                dec_max_wp=dm.decide(data)
                #print("Points:\n",dec_max_wp.e_.points)
                #print("Ranks:\n",dec_max_wp.rank_)
                census_data.loc[:,'Points_Max_WP']=dec_max_wp.e_.points
                census_data.loc[:,'Ranks_Max_WP']=dec_max_wp.rank_
                
                #The Data Frame containing points
                #print("\n",census_data)
                census_data.insert(0,column='CENSUS_ID',value=list(l_cid))
                
                print("\nBefore removing:")
                #print("\n",census_data)
                #Converting Data Frame to Excel File
                census_data=census_data.iloc[1:,:]
                print("\nAfter Removing:")
                #print("\n",census_data)
                #i=census_data[(census_data.CENSUS_ID==582602)].index
                #census_data.drop(i)
                #print("\nIndex:",i)
                '''
                Average of Points using different algorithms
                Here have used the mean function to calculate the average
                '''
                #print("\nCensus Data:",census_data)
                #Retreived the Population for respective districts from the population table
                #Note pop variable is not being used becuase it is not yielding ideal results for WS algo
                #cursor.execute('Select Population from population where Sub_districts=(?)',d)
                #pop=list(cursor.fetchone())[0]
                #print(pop)
                Points_Sum_WS_l=list(census_data['Points_Sum_WS'])
                print("\nAvg of Points_Sum_WS:",mean(Points_Sum_WS_l))
                sum_ws_l.append(mean(Points_Sum_WS_l))
                Points_Max_WS_l=list(census_data['Points_Max_WS'])
                print("\nAvg of Points_Max_WS:",mean(Points_Max_WS_l))
                max_ws_l.append(mean(Points_Max_WS_l))
                Points_Sum_WP_l=list(census_data['Points_Sum_WP'])
                print("\nAverage of Points_Sum_WP:",mean(Points_Sum_WP_l))
                sum_wp_l.append(mean(Points_Sum_WP_l))
                Points_Max_WP_l=list(census_data['Points_Max_WP'])
                print("\nAverage of Points_Max_WP:",mean(Points_Max_WP_l))
                max_wp_l.append(mean(Points_Max_WP_l))
                #The district list for the dataframe
                print(list(d))
                d_name=list(d)[0]
                dis_l.append(list(d)[0])
                small_dict={'District':d_name,'Avg_Points_Max_WS':mean(Points_Max_WP_l)}
                res_l.append(small_dict)
                
            
            #Res dictionary created to make the final dataframe containing the average points of all the districts
            #res_dict={'Avg_Points_Sum_WS':sum_ws_l,'Avg_Points_Max_WS':max_ws_l,'Avg_Sum_WP':sum_wp_l,'Avg_Max_WP':max_wp_l}
            #print(res_l)
            res_dict={'District':dis_l,'Avg_Max_WP':max_wp_l}
            #print(res_dict)
            #Converted the dictionary into Dataframe
            res_df=pd.DataFrame(res_dict)
            #Appended Rank attribute in the dataframe 
            #Sorted by Avg_Max_WP points
            res_df['Rank']=res_df['Avg_Max_WP'].rank(ascending=0)
            #res_df.set_index('Rank')
            #Sorted the values accordingly
            resfin_df=res_df.sort_values('Rank')
            
            print(resfin_df)
            
            #Retreiving all lists from the dataframe to construct JSON value for the front-end
            district_list=list(resfin_df.iloc[:,0])
            #print("\nDistrict list: ",district_list)
            points_list=list(resfin_df.iloc[:,1])
            #print("\nPoints list: ",points_list)
            result_list=list(resfin_df.iloc[:,2])
            #print("\nResult list: ",result_list)
            return_list=[]
            length=len(district_list)
            for i in range(length):
                return_dict={'District':district_list[i],'Points':points_list[i],'Rank':result_list[i]}
                return_list.append(return_dict)
            
            #Printing the return list which is going to be sent to the front-end    
            print(return_list)
            
            cursor.close()
            connect.close()
            
            #return {'data':res_dict},200
            #JSON data sent
            return {'data':return_list},200
            '''
            #Converted to excel for manual ranking
            res_df.to_excel('Maharashtra_Output.xlsx')
            print("Dataframe converted to excel successfully..")
            '''
        except Exception as e:
            print("Exception occured as:",e)
            return {'data':e}
        finally:
            print("Code executed finally")
    

#Adding the endpoint '/districts'       
api.add_resource(Districts,'/districts')
#Running the API
if __name__=='__main__':
    app.run()
    