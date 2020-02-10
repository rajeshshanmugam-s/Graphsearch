from urllib import error

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DataLumper:
    '''
    DataLumper loads the data from the file has been passed,
    and differentiate the Data as Continous and Category columns
    '''
    def __init__(self, file_path):
        self.file_path = file_path
        # self.columns, self.df = DataLumper.data_frame_loader(self)

    def data_frame_loader(self):
        '''
        Load the Data as a Data frame
        :return: Data frame
        '''

        df = pd.read_csv(self.file_path, encoding="ISO-8859-1", error_bad_lines=False)
        logger.debug("Dataframe created")
        df = self.null_handler(df)
        logger.info("After Null handler")
        df.to_csv(self.file_path)
        logger.info("Cleaned data frame is written under the file name {}".format(self.file_path))
        return df.columns, df

    def null_handler(self, df):
        '''
        Which checks for the percentage of Null variables in the Data frame and if it is less than 25% Null variables
        Will be Removed.
        :param df: DataFrame
        :return: DataFrame
        '''
        # TODO: Null Value threshold is modifiable, Below is the Vague Implementation and it needs to be added in the
        #  Data Cleansing Module.
        # if (df.isna().sum() / df.shape[0]) * 100 <= 25:
        df = df.dropna()
        return df



    def data_type_explorer(self, df):
        '''
        Differentiates the columns in the data frame as Continous and Categorical values.
        :return: Continous and Categorical Values
        '''
        categorical_column = []
        other_columns = []

        descrb_columns = df.describe().columns
        logger.info("Columns in DF describe {}".format(descrb_columns))
        df_columns = df.columns
        logger.info("DataFrame Columns {}".format(df_columns))

        for column in df_columns:
            # Checking the column values are not in monotonic and also no of Uniques in a
            # Column are not equal to Total no of Rows
            if not df[column].is_monotonic and df.shape[0] != len(df[column].unique()):
                logger.debug("Column is not monotonic and No of Unique value are less than No of Rows")
                # if self.df[column].dtype == np.number:
                #     print(column)
                #     other_columns.append(column)

                # Checking if column values are numeric and comparing with orginal values and converted float values.
                if df[column].dtype == np.number and np.array_equal(df[column],
                                                                         df[column].astype(float)):
                    logger.debug("Column type is Numeric and Float {}".format(column))
                    logger.info("Column added in Continuous category {}".format(column))
                    other_columns.append(column)

                # Check for unique values of a column is less than 1/4 of the total rows
                elif len(df[column].unique()) < len(df[column])/4:
                    logger.debug("No of Unique value is less than 1/4th of the no of Rows")
                    logger.info("Column added in Categorical Data {}".format(column))
                    categorical_column.append(column)

                # elif len(self.df[column].unique()) > len(self.df[column]) / 2:
                #     other_columns.append(column)
                # elif max(max([[y.isdigit() for y in x.split()] for x in self.df[column]])) and column in descrb_columns:
                #     print(column)
                #     other_columns.append(column)

                # Based on the Summary stats table if a column is not in that table it will be taken as continous
                elif column not in descrb_columns:
                    logger.debug("Column not in dataframe describe")
                    logger.info("Column added to categorical column {}".format(column))
                    categorical_column.append(column)
                # Checking max value of the column is 1 or 75th Percentile is 1 or 0 and checking for the column is int
                elif (df[column].max() == 1 or np.percentile(df[column], 75, interpolation='midpoint') == 1
                      or np.percentile(df[column], 75, interpolation='midpoint') == 0) and \
                        np.array_equal(df[column], df[column].astype(int)):
                    logger.debug("column max value is 1 or 3rd Quartile value is 1 or 0, and the column is Integer")
                    logger.info("Column added to Category {}".format(column))
                    categorical_column.append(column)
                else:
                    logger.debug("Not in any criteria")
                    logger.info("Column added to Continous {}".format(column))
                    other_columns.append(column)
        return categorical_column, other_columns


# '/Users/rajesh/Documents/Clothing Sales/April_sales_19.csv'
# x = DataLumper('train.csv')
# print(x.data_type_explorer())
