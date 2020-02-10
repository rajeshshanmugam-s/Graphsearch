from pprint import pprint
import json

#Fixme: rewrite the below function for directly extracting values from the dataframe itself

def data_finder(column_name, id):
    with open('Data/'+id+'.txt') as file:
        data = json.load(file)
        for analysis in data['analysis']:
            for each_variate in analysis:
                for data in analysis[each_variate]:
                    for chart_data in data['chart_data']:
                        if column_name in chart_data['Label']['x'] or column_name in chart_data['Label']['y']:
                            return chart_data


# data_finder('PassengerId', '186afc22-57d0-4832-8feb-b39e857e2bf4')