import math
import pandas as pd
import matplotlib.pyplot as plt
import calendar as cal
import numpy as np


def exercise_one_a(data_frame):
    data_frame['invoiceCreated'] = pd.to_datetime(data_frame['invoiceCreated'])

    invoice_created_rows = data_frame[data_frame['type'] == 'created'].copy()
    invoice_created_rows.loc[:, 'hour'] = invoice_created_rows['invoiceCreated'].dt.hour
    hour_count_created = invoice_created_rows.groupby('hour').size()

    plt.figure(figsize=(8, 5))
    plt.bar(hour_count_created.index, hour_count_created.values, color='green')
    plt.xlabel('Hour', fontsize=14)
    plt.ylabel('Number of created invoices', fontsize=14)
    plt.title('Invoices created per hour', fontsize=17)
    plt.xticks(hour_count_created.index)

    data_frame['logCreated'] = pd.to_datetime(data_frame['logCreated'])
    data_frame.loc[:, 'hour'] = data_frame['logCreated'].dt.hour
    hour_count_any_log = data_frame.groupby('hour').size()

    plt.figure(figsize=(8, 5))
    plt.bar(hour_count_any_log.index, hour_count_any_log.values, color='blue')
    plt.xlabel('Hour', fontsize=14)
    plt.ylabel('Number of invoices changes (log activity)', fontsize=14)
    plt.title('Invoices changes per hour', fontsize=17)
    plt.xticks(hour_count_any_log.index)

    plt.show()


def exercise_two_a(data_frame):
    # study of invoicesIds without created type
    all_invoices = set(data_frame['invoiceId'])
    invoices_with_created_type = set(data_frame[data_frame['type'] == 'created']['invoiceId'])
    print("Invoices without created type:", all_invoices - invoices_with_created_type)
    # found that invoiceId {
    #   'd762BdRtiTCVc+0Iu7P2zbiE8JJhmRwFLHKaDnq1Tk8=',
    #   'WpauoWsDoKzSM41W+H3cVfQprdndvCfKffKq29IFLwg=',
    #   'KUZGVLUcWb+a4qyyJoe+vQyt9MrAOFJLapdf2QsId7Q='
    # } were demonstrated without created type, so we have difference between
    #                                               1. the total number of rows of unique invoiceIds (131462) and
    #                                               2. the total number of rows of invoices with created type (131459)
    # Keeping this in mind, it is more coherent to have a comparison between paid invoices and both above items (1, 2)

    invoice_unique_id_rows_count = data_frame['invoiceId'].nunique()
    invoice_created_rows_count = data_frame['type'].value_counts().get('created', 0)
    invoice_paid_rows_count = data_frame['type'].value_counts().get('paid', 0)

    percentage_paid_over_created = (invoice_paid_rows_count / invoice_created_rows_count) * 100
    percentage_paid_over_unique_id = (invoice_paid_rows_count / invoice_unique_id_rows_count) * 100

    print("Percentage of paid invoices over all created invoices: {:.3f}%"
          .format(round(percentage_paid_over_created, 3)))
    print("Percentage of paid invoices over all unique invoiceId: {:.3f}%"
          .format(round(percentage_paid_over_unique_id, 3)))

    invoice_paid_list = data_frame[data_frame['type'] == 'paid'].copy()
    invoice_paid_list['paidAfterDue'] = pd.to_datetime(invoice_paid_list['invoiceDue']) < pd.to_datetime(
        invoice_paid_list['logCreated'])

    paid_after_due_count = invoice_paid_list['paidAfterDue'].sum()
    percentage_paid_after_due_over_created = (paid_after_due_count / invoice_created_rows_count) * 100
    percentage_paid_after_due_over_unique_id = (paid_after_due_count / invoice_unique_id_rows_count) * 100

    print("Percentage of paid invoices after due date over all created invoices: {:.3f}%"
          .format(round(percentage_paid_after_due_over_created, 3)))
    print("Percentage of paid invoices after due date over all unique invoiceId: {:.3f}%"
          .format(round(percentage_paid_after_due_over_unique_id, 3)))

    labels = ['Unique invoiceId',
              'Created',
              'Paid',
              'Paid after due date']
    values = [invoice_unique_id_rows_count,
              invoice_created_rows_count,
              invoice_paid_rows_count,
              paid_after_due_count]
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['green', 'orange', 'blue', 'red'])
    plt.title('Invoices situation count', fontsize=17)
    plt.xlabel('Situation', fontsize=14)
    plt.ylabel('Rows count', fontsize=14)

    percentage_label = ['Paid', 'Paid after due date']

    values_over_created = [percentage_paid_over_created, percentage_paid_after_due_over_created]
    plt.figure(figsize=(8, 5))
    plt.bar(percentage_label, values_over_created, color=['blue', 'red'])
    plt.title('Percentage over all created invoices', fontsize=17)
    plt.xlabel('Situation', fontsize=14)
    plt.ylabel('Percentage (%)', fontsize=14)
    plt.ylim(0, 100)

    values_over_unique_id = [percentage_paid_over_unique_id, percentage_paid_after_due_over_unique_id]
    plt.figure(figsize=(8, 5))
    plt.bar(percentage_label, values_over_unique_id, color=['blue', 'red'])
    plt.title('Percentage over all unique invoiceIds', fontsize=17)
    plt.xlabel('Situation', fontsize=14)
    plt.ylabel('Percentage (%)', fontsize=14)
    plt.ylim(0, 100)

    plt.show()


def exercise_two_b(data_frame):
    data_frame['invoiceCreated'] = pd.to_datetime(data_frame['invoiceCreated'])

    invoice_overdue_rows = data_frame[data_frame['type'] == 'overdue'].copy()
    invoice_overdue_rows['month'] = invoice_overdue_rows['invoiceCreated'].dt.strftime('%B')
    overdue_by_months = invoice_overdue_rows.groupby('month').size()

    plt.figure(figsize=(8, 5))
    plt.bar(
        overdue_by_months.reindex(list(cal.month_name[1:])).index,
        overdue_by_months.reindex(list(cal.month_name[1:])).values,
        color='grey'
    )
    for i, value in enumerate(overdue_by_months.reindex(list(cal.month_name[1:])).values):
        if not math.isnan(value):
            plt.text(i, value + 1, str(int(value)), va='bottom', ha='center')
    plt.title('Overdue Invoices by Months', fontsize=14)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Overdue Invoices', fontsize=12)

    plt.show()


def exercise_two_c(data_frame):
    invoice_created_list = data_frame[data_frame['type'] == 'created'].copy()
    invoice_paid_list = data_frame[data_frame['type'] == 'paid'].copy()
    invoice_overdue_list = data_frame[data_frame['type'] == 'overdue'].copy()
    invoice_expired_list = data_frame[data_frame['type'] == 'expired'].copy()

    invoice_id_overdue = invoice_overdue_list['invoiceId'].unique()
    invoice_paid_in_time = invoice_paid_list[~invoice_paid_list['invoiceId'].isin(invoice_id_overdue)].copy()
    invoice_id_paid_in_time = invoice_paid_in_time['invoiceId'].unique()

    bins = [
        0, 1, 2, 5, 10, 20, 30, 60, 90, 120, 180, np.inf
    ]
    labels = [
        'Less than 1 min', '1 to 2 min', '2 to 5 min', '5 to 10 min',
        '10 to 20 min', '20 to 30 min', '30 to 60 min', '60 to 90 min',
        '90 to 120 min', '120 to 180 min', 'more than 180 min'
    ]

    # invoices paid in time, invoices that have paid type but do not have overdue type
    invoice_created_list_paid_in_time = invoice_created_list[
        invoice_created_list['invoiceId'].isin(invoice_id_paid_in_time)].copy()

    invoice_created_list_paid_in_time.loc[:, 'timeToOverdue'] = (pd.to_datetime(
        invoice_created_list_paid_in_time['invoiceDue']) - pd.to_datetime(
        invoice_created_list_paid_in_time['invoiceCreated'])).dt.total_seconds() / 60

    invoice_created_list_paid_in_time.loc[:, 'interval'] = pd.cut(invoice_created_list_paid_in_time['timeToOverdue'],
                                                                  bins=bins,
                                                                  labels=labels)

    plt.figure(figsize=(11, 15))
    invoice_created_list_paid_in_time['interval'].value_counts().sort_index().plot(kind='bar', color='green')
    plt.title('Due time limit by number of paid in time invoices', fontsize=17)
    plt.xlabel('Due time limit', fontsize=14)
    plt.ylabel('Number of paid in time invoices', fontsize=14)
    plt.xticks(rotation=45)

    # invoices not paid in time, invoices that have both paid and overdue types
    invoice_paid_overdue = np.intersect1d(invoice_paid_list['invoiceId'], invoice_overdue_list['invoiceId'])
    invoice_created_list_merge_paidoverdue = invoice_created_list[
        invoice_created_list['invoiceId'].isin(invoice_paid_overdue)].copy()
    invoice_created_list_merge_paidoverdue.loc[:, 'timeToOverdue'] = (pd.to_datetime(
        invoice_created_list_merge_paidoverdue['invoiceDue']) - pd.to_datetime(
        invoice_created_list_merge_paidoverdue['invoiceCreated'])).dt.total_seconds() / 60

    invoice_created_list_merge_paidoverdue.loc[:, 'interval'] = pd.cut(
        invoice_created_list_merge_paidoverdue['timeToOverdue'],
        bins=bins, labels=labels, right=False)

    plt.figure(figsize=(11, 15))
    invoice_created_list_merge_paidoverdue['interval'].value_counts().sort_index().plot(kind='bar', color='orange')
    plt.title('Due time limit by number of invoices paid in overdue', fontsize=17)
    plt.xlabel('Due time limit', fontsize=14)
    plt.ylabel('Number of invoices paid in overdue', fontsize=14)
    plt.xticks(rotation=45)

    # expired invoices, invoices that have been created but was not paid
    invoice_id_expired = invoice_expired_list['invoiceId'].unique()

    invoice_created_list_merge_expired = invoice_created_list[
        invoice_created_list['invoiceId'].isin(invoice_id_expired)].copy()

    invoice_created_list_merge_expired.loc[:, 'timeToOverdue'] = (pd.to_datetime(
        invoice_created_list_merge_expired['invoiceDue']) - pd.to_datetime(
        invoice_created_list_merge_expired['invoiceCreated'])).dt.total_seconds() / 60

    invoice_created_list_merge_expired.loc[:, 'interval'] = pd.cut(invoice_created_list_merge_expired['timeToOverdue'],
                                                                   bins=bins,
                                                                   labels=labels)
    plt.figure(figsize=(11, 15))
    invoice_created_list_merge_expired['interval'].value_counts().sort_index().plot(kind='bar', color='purple')
    plt.title('Due time limit by number of expired invoices', fontsize=17)
    plt.xlabel('Due time limit', fontsize=14)
    plt.ylabel('Number of expired invoices', fontsize=14)
    plt.xticks(rotation=45)

    plt.show()


def exercise_three_a(data_frame):
    invoice_unique_id_rows_count = data_frame['invoiceId'].nunique()
    invoice_reversed_rows_count = data_frame[data_frame['type'] == 'reversed']['invoiceId'].nunique()

    percentage_reversed_over_unique_id = (invoice_reversed_rows_count / invoice_unique_id_rows_count) * 100
    print("Percentage of reversed invoices over all unique invoiceIds: {:.3f}%"
          .format(round(percentage_reversed_over_unique_id, 3)))

    labels = ['Not reversed', 'Reversed']
    values = [invoice_unique_id_rows_count - invoice_reversed_rows_count, invoice_reversed_rows_count]
    plt.figure(figsize=(8, 10))
    plt.bar(labels, values, color=['blue', 'red'])
    for i, value in enumerate(values):
            plt.text(i, value + 1, str(int(value)), va='bottom', ha='center')
    plt.title('Invoices situation count', fontsize=17)
    plt.xlabel('Situation', fontsize=14)
    plt.ylabel('Rows count', fontsize=14)

    plt.figure(figsize=(8, 10))
    plt.bar('Reversed', percentage_reversed_over_unique_id, color=['green'])
    plt.title('Percentage over all unique invoiceIds', fontsize=17)
    plt.xlabel('Situation', fontsize=14)
    plt.ylabel('Percentage out of 100 (%)', fontsize=14)
    plt.ylim(0, 0.5)

    plt.show()


def exercise_three_b(data_frame):
    invoice_reversing_list = data_frame[data_frame['type'] == 'reversing'].groupby(['invoiceId', 'amount'])
    invoice_reversed_list = data_frame[data_frame['type'] == 'reversed'].groupby(['invoiceId', 'amount'])

    time_to_reverse_invoice_table = []

    for invoiceId in invoice_reversing_list.groups.keys():
        if invoiceId in invoice_reversed_list.groups:
            for i, reserving_invoice in invoice_reversing_list.get_group(invoiceId).iterrows():
                for j, reversed_invoice in invoice_reversed_list.get_group(invoiceId).iterrows():
                    time_to_reverse_invoice_table.append(
                        {'invoiceId': invoiceId,
                         'time_to_reverse': (
                                 pd.to_datetime(reversed_invoice['logCreated'])
                                 - pd.to_datetime(reserving_invoice['logCreated'])).total_seconds()}
                    )

    data_frame_time_to_reverse = pd.DataFrame(time_to_reverse_invoice_table)
    print("Average time to reverse in seconds: {:.3f} sec"
          .format(round(data_frame_time_to_reverse['time_to_reverse'].mean(), 3)))

    bins = [
        0, 5, 10, 20, 30, 40, 50, 60, 120, 300, 600, 1800, np.inf
    ]
    labels = [
        'Less than 5 sec', '5 to 10 sec', '10 to 20 sec', '20 to 30 sec', '30 to 40 sec',
        '40 to 50 sec', '50 sec to 60 sec', '1 to 2 min', '2 to 5 min',
        '5 to 10 min', '10 to 30 min', 'more than 30 min'
    ]

    data_frame_time_to_reverse.loc[:, 'interval'] = pd.cut(data_frame_time_to_reverse['time_to_reverse'],
                                                           bins=bins,
                                                           labels=labels)

    plt.figure(figsize=(12, 14))
    data_frame_time_to_reverse['interval'].value_counts().sort_index().plot(kind='bar', color='green')
    plt.title('Due time limit by number of paid in time invoices', fontsize=17)
    plt.xlabel('Due time limit', fontsize=14)
    plt.ylabel('Number of paid in time invoices', fontsize=14)
    plt.xticks(rotation=45)

    plt.show()


def exercise_three_c(data_frame):

    total_reverse = data_frame[(data_frame['type'] == 'reversed') & (data_frame['amount'] == 0)].copy()
    partial_reverse = data_frame[(data_frame['type'] == 'reversed') & (data_frame['amount'] != 0)].copy()

    total_reverse['time_since_creation'] = (pd.to_datetime(total_reverse['logCreated']) - pd.to_datetime(total_reverse['invoiceCreated'])).dt.total_seconds() / 60
    partial_reverse['time_since_creation'] = (pd.to_datetime(partial_reverse['logCreated']) - pd.to_datetime(partial_reverse['invoiceCreated'])).dt.total_seconds() / 60

    one_day_in_min = 1440
    one_week_in_min = one_day_in_min * 7
    bins = [
        0, 10, 60, 720, one_day_in_min, 2 * one_day_in_min, 3 * one_day_in_min, 4 * one_day_in_min,
        5 * one_day_in_min, 6 * one_day_in_min, one_week_in_min, 2 * one_week_in_min, 3 * one_week_in_min,
        np.inf
    ]
    labels = [
        'Less than 10 min', '10 to 60 min', '1 to 12 h', '12 to 24 h',
        '1 to 2 days', '2 to 3 days', '3 to 4 days', '4 to 5 days',
        '5 to 6 days', '6 to 7 days', '1 to 2 week', '2 to 3 weeks',
        'More than 3 weeks'
    ]

    total_reverse.loc[:, 'interval'] = pd.cut(total_reverse['time_since_creation'], bins=bins, labels=labels)
    plt.figure(figsize=(12, 14))
    total_reverse['interval'].value_counts().sort_index().plot(kind='bar', color='green')
    plt.title('Total reversed invoices since creation date', fontsize=17)
    plt.xlabel('Creation age', fontsize=14)
    plt.ylabel('Number of total reserves', fontsize=14)
    plt.xticks(rotation=45)

    partial_reverse.loc[:, 'interval'] = pd.cut(partial_reverse['time_since_creation'], bins=bins, labels=labels)
    plt.figure(figsize=(12, 14))
    partial_reverse['interval'].value_counts().sort_index().plot(kind='bar', color='orange')
    plt.title('Partial reversed invoices since creation date', fontsize=17)
    plt.xlabel('Creation age', fontsize=14)
    plt.ylabel('Number of partial reserves', fontsize=14)
    plt.xticks(rotation=45)

    plt.show()


df = pd.read_csv('InvoiceLogDataset.csv')
exercise_one_a(df)
exercise_two_a(df)
exercise_two_b(df)
exercise_two_c(df)
exercise_three_a(df)
exercise_three_b(df)
exercise_three_c(df)
