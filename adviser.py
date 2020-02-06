import utils as helper
# import schemer as plotter
import logging
import json

logger = logging.getLogger(__name__)


class GraphAdviser:
    # TODO: Check for connecting loading pandas df directly from here
    def __init__(self, continous_data, categorical_data, dataframe, id, cat_bus_columns, cont_bus_columns):
        logger.info("Inside Graphadvisor")
        self.continuous_data = continous_data
        self.categorical_data = categorical_data
        self.df = dataframe
        self.id = id
        self.cat_business_colum = cat_bus_columns,
        self.cont_business_colum = cont_bus_columns


    def output_architect(self):
        '''
        Architect the dict from the Univariate and Bultivariate Analysis
        :return: Dict of Univariate and Multivariate
        '''
        logger.info("Inside the output architect")
        charts = {
            "analysis":[
            {
                "data":self.univariate_analysis(),
                'analysis_name': 'Univariate Analysis',
                'analysis_type': 'Univariate analysis'
            },
            {
                'data': self.bivariate_analysis(),
                'analysis_name': 'Bivariate Analysis',
                'analysis_type': 'Bivariate analysis'
            }
        ]
        }
        with open('Data/'+self.id+'.txt', 'w+') as file:
            json.dump(charts, file)
        return charts

    def univariate_analysis(self):
        '''
        Based on the type of data, Which type of chart is going to be suggested.
        :return: Dict with chart Names.
        '''
        logger.info("Inside the Univariate Analysis")
        histogram = []
        piechart = []
        barchart = []
        # scatter_plot = []
        box_plot = []
        line_plot = []

        univariate_charts = []

        for idx, feature in enumerate(self.categorical_data):
            logger.info("Categorical Column {}".format(feature))
            piechart.append(helper.data_organiser(feature=feature, df=self.df, chart='piechart'))
            # plotter.univariate_piechart_maker(self.df, feature)
            barchart.append(helper.data_organiser(feature=feature, df=self.df, chart='barchart'))
            # plotter.univariate_barchart_maker(self.df, feature)
            # scatter_plot.append(helper.data_organiser(feature=feature, df=self.df, aggregate='count'))

            univariate_charts.append({"data":{'chart_type': 'piechart',
                                              'chart_data': piechart},
                                      'column_name': [feature],
                                      'data_type':['categorical'],
                                      'business_name': self.cat_business_colum[0][idx]})
            print(self.cat_business_colum, "kvfbksdhkfbksbfblblkflkb")
            # 'Need to reconsider the Histogrqam'
            univariate_charts.append({"data":{'chart_type': 'Barchart',
                                              'chart_data': barchart},
                                      'column_name': [feature],
                                      'data_type':['categorical'],
                                      'business_name': self.cat_business_colum[0][idx]})

            univariate_charts.append({"data": {'chart_type': 'Histogram',
                                               'chart_data': histogram},
                                      'column_name': [feature],
                                      'data_type': ['categorical'],
                                      'business_name': self.cat_business_colum[0][idx]})

        for idx, feature in enumerate(self.continuous_data):
            logger.info("Continuous Column {}".format(feature))
            histogram.append(helper.data_organiser(feature=feature, df=self.df, chart='Hstogram'))
            # plotter.univariate_histogram_maker(self.df, feature)
            # scatter_plot.append(helper.data_organiser(feature=feature, df=self.df, aggregate='Feature values'))
            # TODO: Check with frontend for boxplot whether they need quartile values or data .
            box_plot.append(helper.data_organiser(feature=feature, df=self.df, chart='BoxPlot'))
            # plotter.univariate_boxplot_maker(self.df, feature)

            #TODO: Need to add a logic for Date column. Damo bro said we can ask that from User end.

            # line_plot.append(helper.data_organiser(feature=feature, df=self.df, chart='LinePlot'))
            # plotter.univariate_line_plot_maker(df=self.df, column=feature)

            univariate_charts.append({"data": {'chart_type': 'Boxplot',
                                               'chart_data': box_plot},
                                      'column_name': [feature],
                                      'data_type': ['continuous'],
                                      'business_name': self.cont_business_colum[idx]})

        # univariate_charts.append({'chart_type': 'Lineplot',
        #                           'chart_data': line_plot})

        return univariate_charts


    # @property
    def bivariate_analysis(self):
        '''
        Based on the type of Data charts are recommended
        :return: Dict with Chart Names
        '''
        scatter_plot = []
        barchart =[]
        histogram = []
        dot_plot = []
        line_chart = []
        bivariate_charts = []

        #FIXME: check for the list inside the list.

        logger.info("Inside Bivariate analysis")
        for idx, x_feature in enumerate(self.categorical_data):
            for idx_1, y_feature in enumerate(self.continuous_data):
                if x_feature != y_feature:

                    logger.info("Category vs Continuous")
                    logger.info("X_feature: {}, y_feature: {}".format(x_feature, y_feature))
                    scatter_plot.append(helper.data_organiser(df=self.df, chart='Ordinalscatterplot', x_feature=x_feature,
                                                              y_feature=y_feature))
                    # plotter.bivariate_scatterplot_maker(df=self.df, x=x_feature, y=y_feature)
                    barchart.append(helper.data_organiser(df=self.df, chart='Barchart', x_feature=x_feature,
                                                          y_feature=y_feature))
                    line_chart.append(helper.data_organiser(df=self.df, chart='linechart', x_feature=x_feature,
                                                            y_feature=y_feature))

                    bivariate_charts.append({"data":{'chart_type': 'Line Chart',
                                                     'chart_data': line_chart},
                                             'column_name': [x_feature, y_feature],
                                             'data_type': ['categorical', 'continuous'],
                                             'business_name': [self.cat_business_colum[0][idx],self.cont_business_colum[idx_1]]})

                    bivariate_charts.append({"data":{'chart_type': 'Bar chart',
                                                     'chart_data': barchart},
                                            'column_name': [x_feature, y_feature],
                                            'data_type': ['categorical', 'continuous'],
                                            'business_name': [self.cat_business_colum[0][idx],self.cont_business_colum[idx_1]]})

        # for x_feature in self.continous_data:
        #     for y_feature in self.categorical_data:
        #         dot_plot.append(helper.data_organiser(df=self.df, aggregate='Feature Values', x_feature=x_feature,
        #                                               y_feature=y_feature))

        for idx, x_feature in enumerate(self.continuous_data):
            for idx_1, y_feature in enumerate(self.continuous_data):
                if x_feature != y_feature:
                    logger.info("Continuous vs Continuous")
                    logger.info("X_feature: {}, Y_feature: {}".format(x_feature, y_feature))
                    histogram.append(helper.data_organiser(df=self.df, chart='Histogram', x_feature=x_feature,
                                                           y_feature=y_feature))
                    # plotter.bivariate_histogram_maker(df=self.df, x=x_feature, y=y_feature)
                    scatter_plot.append(helper.data_organiser(df=self.df, chart='scatterplot', x_feature=x_feature,
                                                              y_feature=y_feature))
                    # plotter.bivariate_scatterplot_maker(df=self.df, x=x_feature, y=y_feature)
                    line_chart.append(helper.data_organiser(df=self.df, chart='linechart', x_feature=x_feature,
                                                            y_feature=y_feature))
                    # plotter.bivariate_line_plot_maker(df=self.df, x=x_feature, y=y_feature)


                    bivariate_charts.append({"data":{'chart_type':'scatter plot',
                                             'chart_data': scatter_plot},
                                             'column_name': [x_feature, y_feature],
                                             'data_type': ['continuous', 'continuous'],
                                             'business_name': [self.cont_business_colum[idx],self.cont_business_colum[idx_1]]})

                    bivariate_charts.append({"data":{'chart_type': 'Histogram',
                                             'chart_data': histogram},
                                             'column_name': [x_feature, y_feature],
                                             'data_type': ['continuous', 'continuous'],
                                             'business_name': [self.cont_business_colum[idx],self.cont_business_colum[idx_1]]})



        #TODO: Think both dot plot and scatter are giving the same kind of graphs

        return bivariate_charts
