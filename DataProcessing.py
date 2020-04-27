import pandas as pd
import numpy as np
import csv

# define file name
data_folder_path = "event-recommendation-engine-challenge"
event_attendees_file_name = data_folder_path + "/event_attendees.csv"
events_file_name = data_folder_path + "/events.csv"
test_file_name = data_folder_path + "/test.csv"
train_file_name = data_folder_path + "/train.csv"
users_file_name = data_folder_path + "/users.csv"
user_friends_file_name = data_folder_path + "/user_friends.csv"

# read data
print("Reading files ...")
try:
    print(event_attendees_file_name + " ... ", end = "")
    event_attendees = pd.read_csv(event_attendees_file_name)
    print("finished (1/6)")
    print(events_file_name + " ... ", end = "")
    events = pd.read_csv(events_file_name)
    print("finished (2/6)")
    print(test_file_name + " ... ", end = "")
    test = pd.read_csv(test_file_name)
    print("finished (3/6)")
    print(train_file_name + " ... ", end = "")
    train = pd.read_csv(train_file_name)
    print("finished (4/6)")
    print(users_file_name + " ... ", end = "")
    users = pd.read_csv(users_file_name)
    print("finished (5/6)")
    print(user_friends_file_name + " ... ", end = "")
    user_friends = pd.read_csv(user_friends_file_name)
    print("finished (6/6)")
    print("File loading completed!")
except FileNotFoundError as fnf_error:
    print(fnf_error)


def create_event_attendees_dict_and_user_interests_dict(event_attendees):
    event_attendees_dict = {}
    user_interests_dict = {}
    for index, row in event_attendees.iterrows():
        event_dict = {}
        event_id = str(row[0])
        for i in range(1, len(row)):
            l = row[i]
            if str(l) == "nan":
                event_dict[str(i)] = []
            else:
                user_id_list = l.split(" ")
                event_dict[str(i)] = user_id_list
                for user_id in user_id_list:
                    if not user_id in user_interests_dict:
                        user_interests_dict[user_id] = {}
                    if str(i) in user_interests_dict[user_id]:
                        user_interests_dict[user_id][str(i)].append(event_id)
                    else:
                        user_interests_dict[user_id][str(i)] = [event_id]
        event_attendees_dict[event_id] = event_dict
    return [event_attendees_dict, user_interests_dict]


# train_dict = {user_id : {event_id : [invited, interested, not_interested]}}
def create_train_dict(train):
    train_dict = {}
    for index, row in train.iterrows():
        user_id = str(row[0])
        event_id = str(row[1])
        invited = row[2]
        interested = row[4]
        not_interested = row[5]
        if not user_id in train_dict:
            train_dict[user_id] = {}
        if event_id in train_dict[user_id]:
            continue
            # if train_dict[user_id][event_id] == [invited, interested, not_interested]:
            #     print("Duplicated data! for event_id, user_id: " + event_id + ", " + user_id)
            # else:
            #     print("Multiple data! for event_id, user_id: " + event_id + ", " + user_id)
        else:
            train_dict[user_id][event_id] = [invited, interested, not_interested]
    return train_dict


# test_dict = {user_id : {event_id : invited}}
def create_test_dict(test):
    test_dict = {}
    for index, row in test.iterrows():
        user_id = str(row[0])
        event_id = str(row[1])
        invited = row[2]
        if not user_id in test_dict:
            test_dict[user_id] = {}
        if event_id in test_dict[user_id]:
            continue
            # if test_dict[user_id][event_id] == invited:
            #     print("Duplicated data! for event_id, user_id: " + event_id + ", " + user_id)
            # else:
            #     print("Multiple data! for event_id, user_id: " + event_id + ", " + user_id)
        else:
            test_dict[user_id][event_id] = invited
    return test_dict


# {user_id : []}
def create_friends_dict(user_friends):
    user_friends_dict = {}
    for index, row in user_friends.iterrows():
        user_id = str(row[0])
        if str(row[1]) == "nan":
            continue;
        else:
            friends_list = row[1].split(" ")
            user_friends_dict[user_id] = friends_list
    return user_friends_dict


# {user_id : [birthday, gender]}
def create_users_dict(users):
    user_dict = {}
    for index, row in users.iterrows():
        user_id = str(row[0])
        birthday = row[2]
        gender = row[3]
        user_dict[user_id] = [birthday, gender]
    return user_dict


# {event_id : [host_user_id, [c_list]]}
def create_events_dict(events):
    events_dict = {}
    for index, row in events.iterrows():
        event_id = str(row[0])
        host_id = str(row[1])
        c_list = list(row[9 : -1])
        events_dict[event_id] = [host_id, c_list]
    return events_dict


print("Building event_attendees_dict and user_interests_dict ...", end=" ")
event_attendees_dict, user_interests_dict = create_event_attendees_dict_and_user_interests_dict(event_attendees)
print("finished")
print("Building train_dict ...", end=" ")
train_dict = create_train_dict(train)
print("finished")
print("Building test_dict ...", end=" ")
test_dict = create_test_dict(test)
print("finished")
print("Building friends_dict ...", end=" ")
friends_dict = create_friends_dict(user_friends)
print("finished")
print("Building users_dict ...", end=" ")
users_dict = create_users_dict(users)
print("finished")
print("Building events_dict ...", end=" ")
events_dict = create_events_dict(events)
print("finished")

# write train data with 214 features
f = open('train_data.csv', 'w')
print("train_data.cvs file created")
print("data writing ...")
thewriter = csv.writer(f)
title = [None] * 214
title[0] = "user_id"
title[1] = "event_id"
title[2] = "interested"
title[3] = "un_interested"
title[4] = "invited"
title[5] = "friend_yes"
title[6] = "friend_maybe"
title[7] = "friend_invited"
title[8] = "friend_no"
title[9] = "same_gender_yes"
title[10] = "same_gender_maybe"
title[11] = "same_gender_invited"
title[12] = "same_gender_no"
title[13] = "host_is_friend"
for i in range(14, 114):
    title[i] = "event_c_" + str(i - 14)
for i in range(114, 214):
    title[i] = "interest_c_" + str(i - 14)
thewriter.writerow(title)

train_data = []
count = 0
for user_id in train_dict.keys():
    event_inf_dict = train_dict[user_id]
    for event_id in event_inf_dict.keys():
        data = [None] * 214

        # feature 0 - 1: user_id, event id
        data[0] = user_id
        data[1] = event_id

        # feature 2 - 4: interested, un_interested, invited
        data[2] = event_inf_dict[event_id][1]
        data[3] = event_inf_dict[event_id][2]
        data[4] = event_inf_dict[event_id][0]

        friends_list = None
        attended_list = None
        user = None
        event = None
        interest_list = None
        if user_id in friends_dict:
            friends_list = friends_dict[user_id]
        if event_id in event_attendees_dict:
            attended_list = event_attendees_dict[event_id]
        if user_id in users_dict:
            user = users_dict[user_id]
        if event_id in events_dict:
            event = events_dict[event_id]
        if user_id in user_interests_dict:
            interest_list = user_interests_dict[user_id]

        # feature 5 - 8: friends attendency
        number_friends_yes = 0
        number_friends_maybe = 0
        number_friends_invited = 0
        number_friends_no = 0
        if friends_list != None and attended_list != None:
            for friend in friends_list:
                if friend in attended_list["1"]:
                    number_friends_yes += 1
                elif friend in attended_list["2"]:
                    number_friends_maybe += 1
                elif friend in attended_list["3"]:
                    number_friends_invited += 1
                elif friend in attended_list["4"]:
                    number_friends_no += 1
        data[5] = number_friends_yes
        data[6] = number_friends_maybe
        data[7] = number_friends_invited
        data[8] = number_friends_no

        # feature 9 - 12: same gender rate in event
        if user != None and attended_list != None:
            my_gender = user[1]
            for i in range(1, 5):
                same_gender = 0
                total = 0
                for guest_id in attended_list[str(i)]:
                    guest_gender = None
                    if guest_id in users_dict:
                        guest_gender = users_dict[guest_id][1]
                    if guest_gender == my_gender:
                        same_gender += 1
                    if guest_gender != None:
                        total += 1
                if total != 0:
                    data[i + 8] = same_gender / total
                else:
                    data[i + 8] = 0
        else:
            for i in range(9, 13):
                data[i] = 0

        # feature 13: host is friend:
        if event != None and friends_list != None:
            host_id = event[0]
            if host_id in friends_list:
                data[13] = 1
            else:
                data[13] = 0
        else:
            data[13] = 0

        # feature 14 - 113: c1 - c100
        if event != None:
            my_c = event[1]
            for i in range(0, 100):
                data[14 + i] = my_c[i]
        else:
            for i in range(14, 114):
                data[i] = 0

        # feature 114 - 213: my interets c1 - c100 mean
        if interest_list != None:
            if "1" in interest_list:
                my_interest_c_list = []
                for interest_id in interest_list["1"]:
                    if interest_id in events_dict:
                        my_interest_c_list.append(events_dict[interest_id][1])
                if len(my_interest_c_list) != 0:
                    mtx = np.matrix(my_interest_c_list)
                    mean = mtx.mean(0)
                    l = mean.tolist()[0]
                    for i in range(0, len(l)):
                        data[i + 114] = l[i]
                else:
                    for i in range(114, 214):
                        data[i] = 0
            else:
                for i in range(114, 214):
                    data[i] = 0
        else:
            for i in range(114, 214):
                data[i] = 0
        thewriter.writerow(data)

f.close()
print("finished!!!!!!!")


# write test data with 214 features
f2 = open('test_data.csv', 'w')
print("test_data.cvs file created")
print("data writing ...")
thewriter2 = csv.writer(f2)
title = [None] * 214
title[0] = "user_id"
title[1] = "event_id"
title[2] = "interested"
title[3] = "un_interested"
title[4] = "invited"
title[5] = "friend_yes"
title[6] = "friend_maybe"
title[7] = "friend_invited"
title[8] = "friend_no"
title[9] = "same_gender_yes"
title[10] = "same_gender_maybe"
title[11] = "same_gender_invited"
title[12] = "same_gender_no"
title[13] = "host_is_friend"
for i in range(14, 114):
    title[i] = "event_c_" + str(i - 14)
for i in range(114, 214):
    title[i] = "interest_c_" + str(i - 14)
thewriter2.writerow(title)

test_data = []
count = 0
for user_id in test_dict.keys():
    event_inf_dict = test_dict[user_id]
    for event_id in event_inf_dict.keys():
        data = [None] * 214

        # feature 0 - 1: user_id, event id
        data[0] = user_id
        data[1] = event_id

        # feature 2 - 4: interested, un_interested, invited
        data[2] = -1
        data[3] = -1
        data[4] = event_inf_dict[event_id]

        friends_list = None
        attended_list = None
        user = None
        event = None
        interest_list = None
        if user_id in friends_dict:
            friends_list = friends_dict[user_id]
        if event_id in event_attendees_dict:
            attended_list = event_attendees_dict[event_id]
        if user_id in users_dict:
            user = users_dict[user_id]
        if event_id in events_dict:
            event = events_dict[event_id]
        if user_id in user_interests_dict:
            interest_list = user_interests_dict[user_id]

        # feature 5 - 8: friends attendency
        number_friends_yes = 0
        number_friends_maybe = 0
        number_friends_invited = 0
        number_friends_no = 0
        if friends_list != None and attended_list != None:
            for friend in friends_list:
                if friend in attended_list["1"]:
                    number_friends_yes += 1
                elif friend in attended_list["2"]:
                    number_friends_maybe += 1
                elif friend in attended_list["3"]:
                    number_friends_invited += 1
                elif friend in attended_list["4"]:
                    number_friends_no += 1
        data[5] = number_friends_yes
        data[6] = number_friends_maybe
        data[7] = number_friends_invited
        data[8] = number_friends_no

        # feature 9 - 12: same gender rate in event
        if user != None and attended_list != None:
            my_gender = user[1]
            for i in range(1, 5):
                same_gender = 0
                total = 0
                for guest_id in attended_list[str(i)]:
                    guest_gender = None
                    if guest_id in users_dict:
                        guest_gender = users_dict[guest_id][1]
                    if guest_gender == my_gender:
                        same_gender += 1
                    if guest_gender != None:
                        total += 1
                if total != 0:
                    data[i + 8] = same_gender / total
                else:
                    data[i + 8] = 0
        else:
            for i in range(9, 13):
                data[i] = 0

        # feature 13: host is friend:
        if event != None and friends_list != None:
            host_id = event[0]
            if host_id in friends_list:
                data[13] = 1
            else:
                data[13] = 0
        else:
            data[13] = 0

        # feature 14 - 113: c1 - c100
        if event != None:
            my_c = event[1]
            for i in range(0, 100):
                data[14 + i] = my_c[i]
        else:
            for i in range(14, 114):
                data[i] = 0

        # feature 114 - 213: my interets c1 - c100 mean
        if interest_list != None:
            if "1" in interest_list:
                my_interest_c_list = []
                for interest_id in interest_list["1"]:
                    if interest_id in events_dict:
                        my_interest_c_list.append(events_dict[interest_id][1])
                if len(my_interest_c_list) != 0:
                    mtx = np.matrix(my_interest_c_list)
                    mean = mtx.mean(0)
                    l = mean.tolist()[0]
                    for i in range(0, len(l)):
                        data[i + 114] = l[i]
                else:
                    for i in range(114, 214):
                        data[i] = 0
            else:
                for i in range(114, 214):
                    data[i] = 0
        else:
            for i in range(114, 214):
                data[i] = 0
        thewriter2.writerow(data)

f2.close()
print("finished!!!!")