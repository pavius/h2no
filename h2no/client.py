import pandas as pd
import numpy as np
import matplotlib.backends.backend_pdf
import matplotlib.pyplot

from h2no import controller


class Client:

    def __init__(self, host, password):
        self._controller_client = controller.Client(host=host, password=password)

    def create_report(self, days, output_path):
        # get the logs
        logs_df = self._controller_client.get_logs(days)
        self._print_dataframe(logs_df)

        # create a pdf output
        pdf = matplotlib.backends.backend_pdf.PdfPages(output_path)

        # plot the data
        for figure in [
            self._get_line_figure(self._get_pivot_dataframe(logs_df, 'liters_per_minute'), 'Liters/Min',
                                  'Rate over Time'),
            self._get_line_figure(self._get_pivot_dataframe(logs_df, 'liters'), 'Liters', 'Volume over Time'),
            self._get_table_figure(self._get_weekly_total_dataframe(logs_df, 'liters'), 'Liters')
        ]:
            pdf.savefig(figure, dpi=600, bbox_inches="tight")

        # flush
        pdf.close()

    def _print_dataframe(self, df):
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.width', 1000):
            print(df)

    def _sanitize_dataframe(self, df):
        # replace all zeros with NaN
        columns = list(df.columns.values)
        df[columns] = df[columns].replace({0.0: np.nan})

        # drop all columns (stations) whose values are all NaN, or it borks the x axis
        return df.dropna(axis=1, how='all')

    def _get_pivot_dataframe(self, logs_df, value):
        # pivot on the value
        pivot_df = logs_df.pivot(values=value, index=['start_time'], columns=['station_name'])

        # sum all values for a given day
        pivot_df = pivot_df.groupby(pivot_df.index.date).sum()

        return self._sanitize_dataframe(pivot_df)

    def _get_weekly_total_dataframe(self, logs_df, value):
        # pivot on the value
        pivot_df = logs_df.pivot(values=value, index=['start_time'], columns=['station_name'])

        pivot_df = pivot_df.groupby(pd.Grouper(freq='W-SAT')).sum()
        pivot_df['Total'] = pivot_df.sum(axis=1)

        # round everything down
        columns = list(pivot_df.columns.values)
        pivot_df[columns] = pivot_df[columns].round(decimals=2)

        return self._sanitize_dataframe(pivot_df)

    def _get_line_figure(self, df, y_label, title):
        plot = df \
            .interpolate(method='linear') \
            .plot \
            .line(marker='o', markersize=2, rot=45)

        plot.set_xlabel('Date')
        plot.set_ylabel(y_label)
        plot.set_title(title)

        return plot \
            .legend(loc='center left', bbox_to_anchor=(1, 0.5)) \
            .get_figure()

    def _get_table_figure(self, df, y_label):
        figure, subaxes = matplotlib.pyplot.subplots(1, 1)
        pd.plotting.table(subaxes, df, loc='top')

        plot = df.plot(ax=subaxes)
        plot.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plot.set_xlabel('Date')
        plot.set_ylabel(y_label)
        plot.set_title('Weekly Summary', pad=80)

        return figure


