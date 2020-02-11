from pprint import pprint
import json

#Fixme: rewrite the below function for directly extracting values from the dataframe itself

def data_finder(column_name, id):
    # plot_data = {}
    plot_data_ = []
    with open('Data/'+id+'.txt') as file:
        data = json.load(file)
        charts = 0
        for analysis in data['analysis']:
            for each_variate in analysis:
                for data in analysis[each_variate]:
                    for chart_data in data['chart_data']:
                        if column_name in chart_data['Label']['x'] or column_name in chart_data['Label']['y']:
                            plot_data_.append(chart_data)
                            # plot_data.update({"chart_no_"+str(charts) :chart_data})
                            # charts = charts+1
    return plot_data_


# pprint(data_finder('PassengerId', 'd43131d0-58aa-4194-848e-d0f13be29126'))