import json
import pandas as pd
import logging

logger = logging.getLogger(__name__)

#Fixme: Change the output structure of the Histogram

def json_builder(df, feature=None, x_feature=None, y_feature=None):
    '''
    Builds the JSON from the DataFrame for the Columns.
    :param df: DataFrame
    :param feature: Column Name
    :return:
    '''
    # if feature:
    #     feature = json.loads(df.to_json())
    #     return feature
    # else:
    df = json.loads(df.to_json(orient='records'))
    return df


def data_organiser(chart, df, x_feature=None, y_feature=None, feature=None):
    if feature and chart != 'Histogram' and chart != 'BoxPlot' and chart != 'piechart':
        # x_feature_data, y_feature_data = groupby_frame_generator(df,feature)
        out_df = groupby_frame_generator(df,feature)
        df_data = {
            "Title": feature,
            "Label": {"x": feature,
                      "y": "Count"},
            # 'values': {'x': x_feature_data,
            #            'y': y_feature_data},
            "chart_type": chart,
            "values": out_df,
            "Legends": {0: feature,
                        1: "Count"}
        }
        logger.debug("Univariate For {}, chart {}".format(feature, chart))

    elif feature and chart == 'piechart':
        out_df = pd.DataFrame({'count': df.groupby(df[feature]).size()}).reset_index()
        out_df = out_df.set_index(out_df.columns[0]).to_dict()['count']
        df_data = {
            "Title": feature,
            "Label": {"x": feature,
                      "y": "Count"},
            # 'values': {'x': x_feature_data,
            #            'y': y_feature_data},
            "chart_type": chart,
            "values": out_df,
            "Legends": {0: feature,
                        1: "Count"}
        }
        logger.debug("Univariate For {}, chart {}".format(feature, chart))

    elif feature and chart == 'BoxPlot' or chart == 'Histogram':
        feature_data = groupby_frame_generator(df,feature,chart_name=chart)
        df_data = {
            "Title": feature,
            "chart_type": chart,
            "Label": {
                "x": feature
            },
            "values": {
                "Data": feature_data
            },
            "Legends": {
                0: feature
            }
        }
        logger.debug("Univariate For {} chart {} x: {}".format(feature, chart, feature))

    elif x_feature != y_feature:
        logger.info("Bivariate x_feature:{}, y_feature:{}".format(x_feature, y_feature))
        if chart == 'Barchart' or chart == 'Histogram':

            grouped_data = groupby_frame_generator(df=df, x_feature=x_feature, y_feature=y_feature)
            #TODO: Need to change the x and y values based on frontend
            df_data = {
                "Title": x_feature + ' vs ' + y_feature,
                "chart_type": chart,
                "Label": {"x": x_feature,
                          'y': y_feature},
                "values": {"data": grouped_data},
                "Legends": {0: x_feature,
                            1: y_feature}
            }
            logger.debug("For {} chart:{} x_feature:{}, y_feature:{}".format(feature, chart, x_feature, y_feature))
        else:
            x_feature_data = json_builder(df[x_feature])
            y_feature_data = json_builder(df[y_feature])
            df_data = {
                "Title": x_feature+' vs '+ y_feature,
                "chart_type": chart,
                "Label": {"x": x_feature,
                          'y': y_feature},
                "values": {"x": x_feature_data,
                           "y": y_feature_data},
                "Legends": {0: x_feature,
                            1: y_feature}
            }
        logger.debug("For {} chart {} x_feature {}, y_feature {}".format(feature, chart, x_feature, y_feature))
    return df_data


def groupby_frame_generator(df,feature=None,x_feature=None, y_feature=None, chart_name=None):
    if feature and not chart_name:
        df = pd.DataFrame({'count': df.groupby(df[feature]).size()}).reset_index()
        # x_value = json_builder(df[feature])
        # y_value = json_builder(df['count'])
        out_df = json_builder(df)
        logger.debug("Univariate Groupby feature:{}".format(feature))
        # return x_value, y_value
        return out_df
    elif feature and chart_name:
        out_df = json_builder(df[feature])
        return out_df
    elif x_feature and y_feature:
        df = pd.DataFrame({'count': df.groupby([x_feature, y_feature]).size()}).reset_index()
        feature_data = json_builder(df)
        # from click import pause
        # print(feature_data)
        # pause()
        logger.debug("Biavriate Groupby x_feature: {}, y_feature: {}".format(x_feature, y_feature))
        return feature_data


# import pandas as pd
# from pprint import pprint
#
# df = pd.read_csv('/Users/rajesh/Desktop/poc-csv-nlp-search/Data/e352007d-eeac-4c36-bebc-d462ac0a1a21')
# pprint(data_organiser(chart='Histogram', feature='PassengerId', df=df))