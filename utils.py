import json
import pandas as pd
import logging

logger = logging.getLogger(__name__)


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
    if feature and chart != 'Histogram':
        x_feature_data, y_feature_data = groupby_frame_generator(df,feature)
        df_data = {
            'Title': feature,
            'Label': {'x': feature,
                      'y': 'Count'},
            'values': {'x': x_feature_data,
                       'y': y_feature_data},
            'Legends': {0: feature,
                        1: 'Count'}
        }
        logger.debug("Univariate For {}, chart {}".format(feature, chart))
    elif feature and (chart == 'Histogram' or chart == 'barchart'):
        feature_data = json_builder(df, feature)
        df_data = {
            'Title': feature,
            'Label': {
                'x': feature
            },
            'values': {
                'x': feature_data
            },
            'Legends': {
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
                'Title': x_feature + ' vs ' + y_feature,
                'Label': {'x': x_feature,
                          'y': y_feature},
                'values': {'data': grouped_data},
                'Legends': {0: x_feature,
                            1: y_feature}
            }
            logger.debug("For {} chart:{} x_feature:{}, y_feature:{}".format(feature, chart, x_feature, y_feature))
        else:
            x_feature_data = json_builder(df[x_feature])
            y_feature_data = json_builder(df[y_feature])
            df_data = {
                'Title': x_feature+' vs '+ y_feature,
                'Label': {'x': x_feature,
                          'y': y_feature},
                'values': {'x': x_feature_data,
                           'y': y_feature_data},
                'Legends': {0: x_feature,
                            1: y_feature}
            }
        logger.debug("For {} chart {} x_feature {}, y_feature {}".format(feature, chart, x_feature, y_feature))
    return df_data


def groupby_frame_generator(df,feature=None,x_feature=None, y_feature=None):
    if feature:
        df = pd.DataFrame({'count': df.groupby(df[feature]).size()}).reset_index()
        x_value = json_builder(df[feature])
        y_value = json_builder(df['count'])
        logger.debug("Univariate Groupby feature:{}".format(feature))
        return x_value, y_value
    elif x_feature and y_feature:
        df = pd.DataFrame({'count': df.groupby([x_feature, y_feature]).size()}).reset_index()
        feature_data = json_builder(df)
        # from click import pause
        # print(feature_data)
        # pause()
        logger.debug("Biavriate Groupby x_feature: {}, y_feature: {}".format(x_feature, y_feature))
        return feature_data

