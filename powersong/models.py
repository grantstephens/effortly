from django.db import models
from datetime import datetime
from django.db.models import Q

from powersong.unit_conversion import *
import logging


logger = logging.getLogger(__name__)

class Athlete(models.Model):
    ATHELETE_TYPE = (
        (0, 'Running'),
        (1, 'Cycling'),
        (2, 'Other'),
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    athlete_id = models.CharField(max_length=12,unique=True)
    profile_image_url = models.URLField()

    first_login = models.BooleanField()

    email = models.EmailField()

    date_preference = models.CharField(max_length=10)
    measurement_preference = models.PositiveSmallIntegerField()
    sex = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=50)
    athlete_type = models.PositiveSmallIntegerField(choices=ATHELETE_TYPE)
    last_sync_date = models.DateTimeField(blank=True,null=True)
    
    activity_count = models.IntegerField()
    runs_count = models.IntegerField()
    rides_count = models.IntegerField()
    first_activity_date = models.DateTimeField(blank=True,null=True)
    last_activity_date = models.DateTimeField(blank=True,null=True)
    updated_strava_at = models.DateTimeField()

    last_celery_task_id = models.UUIDField(blank=True,null=True)

    strava_token = models.CharField(max_length=100)

class ActivitiesToIgnore(models.Model):
    activity_id = models.CharField(max_length=16,unique=True)
    
class Activity(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)

    activity_id = models.CharField(max_length=16,unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200,blank=True,null=True)

    act_type = models.PositiveSmallIntegerField()

    distance = models.FloatField()
    moving_time = models.IntegerField()
    elapsed_time = models.IntegerField()

    calories = models.IntegerField(blank=True,null=True)
    suffer_score = models.IntegerField(blank=True,null=True)

    start_date = models.DateTimeField()
    start_date_local = models.DateTimeField()

    upload_id = models.CharField(max_length=100,blank=True,null=True)

    embed_token = models.CharField(max_length=100,blank=True,null=True)
    workout_type = models.PositiveSmallIntegerField() # or runs: 0 -> ‘default’, 1 -> ‘race’, 2 -> ‘long run’, 3 -> ‘workout’; for rides: 10 -> ‘default’, 11 -> ‘race’, 12 -> ‘workout’

    avg_speed = models.FloatField() #:  float meters per second
    max_speed = models.FloatField() #:  float meters per second
    avg_cadence = models.FloatField(blank=True,null=True) #:    float RPM

    avg_temp = models.FloatField(blank=True,null=True) #:   float celsius
    
    avg_hr = models.FloatField(blank=True,null=True)
    max_hr = models.IntegerField(blank=True,null=True)

    last_sync_date = models.DateTimeField(null=True)
    
    avg_watts = models.FloatField(blank=True,null=True)
    max_watts = models.IntegerField(blank=True,null=True)

class Listener(models.Model):
    nickname = models.CharField(max_length=30,unique=True)
    real_name = models.CharField(max_length=30) 
    profile_image_url = models.URLField()
    country = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()

    scrobble_count = models.IntegerField()

    last_sync_date = models.DateTimeField(null=True)
    last_scrobble_date = models.DateTimeField(blank=True,null=True)

    lastfm_token = models.CharField(max_length=100)

class Tags(models.Model):
    name = models.CharField(max_length=100,unique=True)
    url = models.URLField()

    reach = models.IntegerField()
    taggings_count = models.IntegerField()

    last_sync_date = models.DateTimeField()

class Artist(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True,null=True)
    url = models.URLField(blank=True,null=True)
    mb_id = models.UUIDField(blank=True,null=True,unique=True)

    listeners_count = models.IntegerField(blank=True,null=True)
    plays_count = models.IntegerField(blank=True,null=True)

    last_sync_date = models.DateTimeField(blank=True,null=True)

    tags = models.ManyToManyField(Tags)

class Song(models.Model):
    title = models.CharField(max_length=100)    
    artist_name = models.CharField(max_length=100)    
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    duration = models.IntegerField(blank=True,null=True)
    listeners_count = models.IntegerField(blank=True,null=True)
    plays_count = models.IntegerField(blank=True,null=True)

    last_sync_date = models.DateTimeField(blank=True,null=True)

    image_url = models.URLField(blank=True,null=True)
    url = models.URLField(blank=True,null=True)

    mb_id = models.UUIDField(blank=True,null=True)
    tags = models.ManyToManyField(Tags)

class Effort(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    act_type = models.PositiveSmallIntegerField()

    idx_in_activity = models.PositiveSmallIntegerField()

    start_time = models.IntegerField()
    duration = models.IntegerField()

    start_distance = models.FloatField()
    distance = models.FloatField()

    avg_speed = models.FloatField()
    diff_last_speed = models.FloatField() #m/s
    diff_avg_speed = models.FloatField() #m/s

    diff_last_speed_s = models.FloatField() #s/m
    diff_avg_speed_s = models.FloatField() #s/m
    
    avg_hr = models.FloatField(blank=True,null=True)
    diff_avg_hr = models.FloatField(blank=True,null=True)
    diff_last_hr = models.FloatField(blank=True,null=True)

    avg_cadence = models.FloatField(blank=True,null=True)
    diff_avg_cadence = models.FloatField(blank=True,null=True)
    diff_last_cadence = models.FloatField(blank=True,null=True)

    total_ascent = models.FloatField()
    total_descent = models.FloatField()

    avg_watts = models.FloatField(blank=True,null=True)
    diff_avg_watts = models.FloatField(blank=True,null=True)
    diff_last_watts = models.FloatField(blank=True,null=True)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


#https://docs.djangoproject.com/en/1.11/topics/db/queries/#lookups-that-span-relationships


def create_athlete_from_dict(athlete_api):
    athlete = Athlete()

    athlete.first_name = athlete_api.firstname
    athlete.last_name = athlete_api.lastname
    athlete.athlete_id = athlete_api.id
    athlete.profile_image_url = athlete_api.profile

    athlete.first_login = True

    athlete.email = athlete_api.email

    athlete.date_preference = athlete_api.date_preference

    if athlete_api.measurement_preference == 'meters':
        athlete.measurement_preference = 0
    else:
        athlete.measurement_preference = 1

    if athlete_api.sex == None:
        athlete.sex = 0
    elif athlete_api.sex == 'M':
        athlete.sex = 1
    elif athlete_api.sex == 'F':
        athlete.sex = 2
    else:
        athlete.sex = 3

    if athlete_api.athlete_type == 'runner':
        athlete.athlete_type = 0
    elif athlete_api.athlete_type == 'cyclist':
        athlete.athlete_type = 1
    else:
        athlete.athlete_type = 2

    athlete.country = athlete_api.country

    
    stats = athlete_api.stats

    athlete.activity_count = stats.all_ride_totals.count
    athlete.runs_count = stats.all_run_totals.count
    athlete.rides_count = stats.all_ride_totals.count
    athlete.activity_count = stats.all_ride_totals.count + stats.all_run_totals.count
    athlete.updated_strava_at = athlete_api.updated_at

    return athlete


def create_listener_from_dict(listener_api):
    listener = Listener()

    listener.nickname = listener_api['name']
    listener.real_name = listener_api['realname']
    listener.profile_image_url = listener_api['image'][-1]['#text']
    listener.country = listener_api['country']
    listener.age = int(listener_api['age'])
    listener.scrobble_count = int(listener_api['playcount'])

    return listener

def lastfm_get_largest_image(image_list):
    order = ['extralarge','large','medium','small','','mega']
    if not "#text" in image_list[-1] or not image_list[-1]["#text"].strip() != "":
        return None
    for size in order:
        for image in image_list[::-1]:
            if image["size"] == size and image["#text"].strip() != "":
                return image["#text"]
    return image_list[-1]["#text"]

def create_song_from_dict(song_api):

    songs = Song.objects.filter(artist_name=song_api['artist']['name'],title=song_api['name'])

    if songs:
        return songs[0]

    song = Song()
    
    song.title = song_api['name']
    song.url = song_api['url']
    song.artist_name = song_api['artist']['name']

    if ('mbid' in song_api and song_api['mbid'].strip() != ""):
        song.mb_id = song_api['mbid']

    if len(song_api['image']) > 0:
        lastfm_get_lastest_image
        song.image_url = lastfm_get_largest_image(song_api['image'])

    if ('mbid' in song_api['artist'] and song_api['artist']['mbid'].strip() != ""):
        artist_mb_id = song_api['artist']['mbid']
        artists = Artist.objects.filter(Q(name=song_api['artist']['name']) | Q(mb_id=artist_mb_id))
    else:
        artists = Artist.objects.filter(name=song_api['artist']['name'])

    if artists:
        artist = artists[0]
    else:
        artist = Artist()
        artist.name = song_api['artist']['name']
        if ('mbid' in song_api['artist'] and song_api['artist']['mbid'].strip() != ""):
            artist.mb_id = song_api['artist']['mbid']
        if song.image_url != None:
            artist.image_url = song.image_url
        artist.save()

    song.artist = artist

    song.save()
    return song

def create_activity_from_dict(activity_api):
    activities = Activity.objects.filter(activity_id=activity_api['id'])

    if activities:
        return activities[0]
    
    activity = Activity()
    if activity_api['type'] == 'Ride':
        activity.act_type = 1
    elif activity_api['type'] == 'Run':
        activity.act_type = 0
    else:
        return None
    
    athletes = Athlete.objects.filter(athlete_id=activity_api['athlete_id'])

    athlete = None
    if athletes:
         athlete = athletes[0]
    else:
        return None
    
    activity.athlete = athlete
    activity.activity_id = activity_api['id']

    activity.date = activity_api['start_date']
    activity.name = activity_api['name']
    activity.description = activity_api['description']
    activity.distance = float(activity_api['total_distance'])
    activity.moving_time = int(activity_api['moving_time'])
    activity.elapsed_time = int(activity_api['elapsed_time'])

    

    activity.start_date = activity_api['start_date']
    activity.start_date_local = activity_api['start_date_local']

    activity.upload_id = activity_api['upload_id']

    activity.embed_token = activity_api['embed_token']

    # or runs: 0 -> ‘default’, 1 -> ‘race’, 2 -> ‘long run’, 3 -> ‘workout’; for rides: 10 -> ‘default’, 11 -> ‘race’, 12 -> ‘workout’
    activity.workout_type = 0
    if activity_api['workout_type'] == "race":
        activity.workout_type = 1
    elif activity_api['workout_type'] == "long run":
        activity.workout_type = 2
    elif activity_api['workout_type'] == "workout":
        activity.workout_type = 3

    activity.avg_speed = float(activity_api['average_speed'])
    activity.max_speed = float(activity_api['max_speed'])

    if activity_api['calories']:
        activity.calories = int(activity_api['calories'])
    if activity_api['suffer_score']:
        activity.suffer_score = int(activity_api['suffer_score'])
    
    if activity_api['average_cadence']:
        activity.avg_cadence = float(activity_api['average_cadence'])

    if activity_api['average_temp']:
        activity.avg_temp = float(activity_api['average_temp'])


    if activity_api['average_heartrate']:
        activity.avg_hr = float(activity_api['average_heartrate'])
    if activity_api['max_heartrate']:
        activity.max_hr = int(activity_api['max_heartrate'])

    activity.last_sync_date = datetime.now()

    if activity_api['type'] == 'Ride':
        if activity_api['average_watts']:
            activity.avg_watts = float(activity_api['average_watts'])
        if activity_api['max_watts']:
            activity.max_watts = int(activity_api['max_watts'])

    activity.save()
    return activity


def lastfm_get_artist(name,mbid=None):
    if mbid == None or mbid == "":
        artists = Artist.objects.filter(name=name)
    else:
        artists = Artist.objects.filter(mb_id=mbid)

    if artists:
        return artists[0]



def strava_get_activity_by_id(act_id):
    if strava_is_activity_to_ignore(act_id):
        return None
        
    activities = Activity.objects.filter(activity_id=act_id)

    if activities:
        return activities[0]

    return None

def strava_is_activity_to_ignore(act_id):
    activities = ActivitiesToIgnore.objects.filter(activity_id=act_id)

    if activities:
        return True
    return False



speed    = ['activity__avg_speed','activity__max_speed','avg_speed','diff_avg_speed','diff_last_speed']
speed_s1 = ['activity__avg_speed','activity__max_speed','avg_speed']
speed_s  = ['activity__avg_speed_s','activity__max_speed_s','avg_speed_s','diff_avg_speed_s','diff_last_speed_s']

distanceSmall = ['total_ascent','total_descent','distance']
distanceBig = ['activity__distance','start_distance']
temperature = ['activity__avg_temp']
timeBig = ['start_time','duration']
timeSmall = []

heartrate = ['avg_hr','diff_avg_hr','diff_last_hr','activity__avg_hr','activity__max_hr']

cadence = ['avg_cadence','diff_avg_cadence','diff_last_cadence','activity__avg_cadence']

watts = ['avg_watts','diff_avg_watts','diff_last_watts','activity__avg_watts','activity__max_watts']

common = {'timeBig':'minutes','timeSmall':'seconds','heartrate':'bpm','cadence':'spm','watts':'W'}
metric_legends   = {'speed': 'km/h','speed_s': '/km','distanceSmall': 'm','distanceBig': 'km', 'temperature': 'ºC'} 
imperial_legends = {'speed': 'mi/h','speed_s': '/mi','distanceSmall': 'ft','distanceBig': 'mi', 'temperature': 'ºF'}  


def effort_convert(effort_dict, units):
    if units == 'metric':
        effort_dict = effort_to_metric(effort_dict)
    elif units == 'imperial':
        effort_dict = effort_to_imperial(effort_dict)
    else:
        effort_dict = effort_to_metric(effort_dict)
    logger.debug(effort_dict)
    return effort_commom(effort_dict)


def effort_commom(effort_dict):
    if 'sort_key' in effort_dict and effort_dict['sort_key'] in heartrate:
        effort_dict['sort_value'] = "{:.2f}".format(effort_dict['sort_value'])
        effort_dict['sort_value_unit'] = common['heartrate']
    elif 'sort_key' in effort_dict and effort_dict['sort_key'] in cadence:
        effort_dict['sort_value'] = "{}".format(int(effort_dict['sort_value']))
        effort_dict['sort_value_unit'] = common['cadence']
    elif 'sort_key' in effort_dict and effort_dict['sort_key'] in watts:
        effort_dict['sort_value'] = "{}".format(int(effort_dict['sort_value']))
        effort_dict['sort_value_unit'] = common['watts']
    return effort_dict

def effort_to_metric(effort_dict):
    new_effort_dict = effort_dict


    for key in speed_s1:
        if key in effort_dict:
            new_effort_dict[key+'_s'] = invertTimeDistance(effort_dict[key])
        if 'sort_key' in new_effort_dict and new_effort_dict['sort_key'] == key+'_s':
            new_effort_dict['sort_value'] = new_effort_dict[key+'_s']
            new_effort_dict['sort_value_unit'] = metric_legends['speed_s']

    for key in speed_s:
        if key in effort_dict:
            new_effort_dict[key] = secondsPerMeterToMinPerKm(new_effort_dict[key])
        if 'sort_key' in new_effort_dict and new_effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = secondsPerMeterToMinPerKm(new_effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = metric_legends['speed_s']
    
    for key in speed:
        if key in effort_dict:
            new_effort_dict[key] = metersPerSecondToKmH(effort_dict[key])
        if 'sort_key' in new_effort_dict and new_effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = metersPerSecondToKmH(effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = metric_legends['speed']
    for key in timeBig:
        if key in new_effort_dict:
            new_effort_dict[key] = secondsToMinutesSecs(effort_dict[key])
        if 'sort_key' in effort_dict and effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = secondsToMinutesSecs(effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = common['timeBig']

    for key in distanceBig:
        if key in new_effort_dict:
            new_effort_dict[key] = metersToKm(effort_dict[key])
        if 'sort_key' in effort_dict and effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = metersToKm(effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = metric_legends['distanceBig']

    for key in distanceSmall:
        if key in new_effort_dict:
            new_effort_dict[key] = metersToMeters(effort_dict[key])
        if 'sort_key' in effort_dict and effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = metersToMeters(effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = metric_legends['distanceSmall']

    new_effort_dict["units"] = {**metric_legends, **common}

    return new_effort_dict

def effort_to_imperial(effort_dict):
    new_effort_dict = effort_dict

    for key in speed_s1:
        if key in effort_dict:
            new_effort_dict[key+'_s'] = invertTimeDistance(effort_dict[key])
        if 'sort_key' in new_effort_dict and new_effort_dict['sort_key'] == key+'_s':
            new_effort_dict['sort_value'] = new_effort_dict[key+'_s']
            new_effort_dict['sort_value_unit'] = imperial_legends['speed_s']

    for key in speed_s:
        if key in effort_dict:
            new_effort_dict[key] = secondsPerMeterToMinPerMi(new_effort_dict[key])
        if 'sort_key' in new_effort_dict and new_effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = secondsPerMeterToMinPerMi(new_effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = imperial_legends['speed_s']
    
    for key in speed:
        if key in effort_dict:
            new_effort_dict[key] = metersPerSecondToMiH(effort_dict[key])
        if 'sort_key' in new_effort_dict and new_effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = metersPerSecondToMiH(effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = imperial_legends['speed']

    for key in timeBig:
        if key in effort_dict:
            new_effort_dict[key] = secondsToMinutesSecs(effort_dict[key])
        if 'sort_key' in new_effort_dict and new_effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = secondsToMinutesSecs(effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = common['timeBig']

    for key in distanceBig:
        if key in effort_dict:
            new_effort_dict[key] = metersToMiles(effort_dict[key])
        if 'sort_key' in new_effort_dict and new_effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = metersToMiles(effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = imperial_legends['distanceBig']

    for key in distanceSmall:
        if key in effort_dict:
            new_effort_dict[key] = metersToFeet(effort_dict[key])      
        if 'sort_key' in effort_dict and effort_dict['sort_key'] == key:
            new_effort_dict['sort_value'] = metersToFeet(effort_dict['sort_value'])
            new_effort_dict['sort_value_unit'] = imperial_legends['distanceSmall']

    new_effort_dict["units"] = {**imperial_legends, **common}

    return new_effort_dict