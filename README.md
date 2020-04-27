# 628Project
project for 628

## Language

Pyhton

##

## To Run

* Run DataProcessing.py: processing train_data and test_data for training

* Run Training.ipynb: Train the model and test

##

## Introduction

This program is EE628 individual project written by _**Xinghan Qin**_.

Do you want to colourful your life? Here is a events recommendation system to recommend same suitable events for you based on your interests. To create and verify the model, the training data and testing data are found on Kaggle. Here is reference link:

https://www.kaggle.com/c/event-recommendation-engine-challenge/data

##

## Data

* train.csv:

  6 features: 
  
  user, event, invited, timestamp, interested, not_interested

* test.csv:

  4 features:
  
  user, event, invited, timestamp

* users.csv:

  7 features: 
  
  user_id, locale, birthyear, gender, joinedAt, location, timezone

* event_attendees.csv:

  5 features for attendency list: 
  
  event, yes, maybe, invited, no

* events.csv:

  110 features to descripe event: 
  
  event_id, user_id, start_time, city, state, zip, country, lat, lng, count_1, count_2, ..., count_100, count_other
  
* user_friends.csv:

  2 features to descripe event: 
  
  user_id, firends

## Tool

Python, numpy, csv, panda, pytorch

##

## Data processing

__Features:__

•	user_id: the id of the user

•	event_id: the id of the event

•	interested: does user interest in the event

•	not_interested: does user uninterest the event

•	invited: have user been invited, 1 for yes, 0 for no

•	friend_attend_yes: the number of friends attend the event

•	friend_attend_maybe: the number of friends maybe attend the event

•	friend_attend_invited: the number of friends invited to the event

•	friend_attend_no: the number of friends not attend the event

•	attend_same_gender_rate_yes: the rate of same gender attends the event

•	attend_same_gender_rate_maybe: the rate of same gender maybe attends the event

•	attend_same_gender_rate_invite: the rate of same gender invites by the event

•	attend_same_gender_rate_no: the rate of same gender not attend the event

•	host_is_friend: is host is friend of user, 1 for yes, 0 for no

•	c_1 to c_100: the information about the event

•	interest_c1 to interest_c_100: the mean value of user attended events’ information

__Storage:__

•	train_dict = {user_id : {event_id : [invited, interested, not_interested]}}

•	test_dict = {user_id : {event_id : invited}}

•	friends_dict = {user_id : []}

•	users_dict = {user_id : [birthday, gender]}

•	events_dict = {event_id : [host_user_id, [c_list]]}

•	user_interests_dict = {user_id : {"1" : [], "2" : [], "3" : [], "4" : []}}

•	event_attendees_dict = {event_id : {"1" : [], "2" : [], "3" : [], "4" : []}}

##

## More

More information about model set up, training, result analyse and future improvement are in the report:

_**628 Final Project Report.pdf**_

##

## Author

* Xinghan Qin

##
