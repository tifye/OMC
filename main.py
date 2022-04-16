# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from stream_read_utils import *
import csv


def read_meta(db):
    return {
        "version": read_int(db),
        "folder_count": read_int(db),
        "account_unlocked": read_bool(db),
        "date_unlocked": read_datetime(db),
        "player_name": read_string(db),
        "number_of_beatmaps": read_int(db)
    }


def save_to_csv(beatmaps):
    csv_filename = "osu!_beatmaps_data.csv"
    csv_columns = ["beatmap_id", "beatmap_set_id", "artist", "title", "creator", "audio_filename", "difficulty", "status", "count_normal", "count_slider", "count_spinner", "AR", "CS", "HP", "OD", "slider_velocity", "stack_leniency", "stars", "length", "drain_time", "preview_start_time", "time_points", "mode", "tags"]
    try:
        with open(csv_filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for beatmap in beatmaps:
                if beatmap['mode'] != 0x00 or int(beatmap['status']) != 4:
                    continue
                beatmap_info = {
                    "beatmap_id": beatmap["beatmap_id"],
                    "beatmap_set_id": beatmap["beatmapset_id"],
                    "artist": beatmap["artist"].encode('utf-8'),
                    "title": beatmap["title"].encode('utf-8'),
                    "creator": beatmap["creator"].encode('utf-8'),
                    "audio_filename": beatmap["audio_filename"].encode('utf-8'),
                    "difficulty": beatmap["version"],
                    "status": beatmap["status"],
                    "count_normal": beatmap["count_normal"],
                    "count_slider": beatmap["count_slider"],
                    "count_spinner": beatmap["count_spinner"],
                    "AR": beatmap["diff_approach"],
                    "CS": beatmap["diff_size"],
                    "HP": beatmap["diff_drain"],
                    "OD": beatmap["diff_overall"],
                    "slider_velocity": beatmap["slider_velocity"],
                    "stack_leniency": beatmap["stack_leniency"],
                    "stars": beatmap["standard_star_ratings"][0][1],
                    "length": beatmap["total_length"],
                    "drain_time": beatmap["drain_time"],
                    "preview_start_time": beatmap["preview_start_time"],
                    "time_points": beatmap["timing_points"],
                    "mode": beatmap["mode"],
                    "tags": beatmap["tags"].encode('utf-8')
                }
                writer.writerow(beatmap_info)
    except IOError:
        print("I/O Error")


def read_beatmaps(db, meta):
    beatmaps = []
    for _ in range(meta["number_of_beatmaps"]):
        map_info = {}
        if meta["version"] < 20191106:
            map_info["file_size"] = read_int(db)
        else:
            map_info["file_size"] = -1
        map_info["osu_version"] = meta["version"]
        map_info["artist"] = read_string(db)
        map_info["artist_unicode"] = read_string(db) #
        map_info["title"] = read_string(db)
        map_info["title_unicode"] = read_string(db) #
        map_info["creator"] = read_string(db) #
        map_info["version"] = read_string(db)  # difficulty name #
        map_info["audio_filename"] = read_string(db)
        map_info["file_md5"] = read_string(db)
        map_info["filename"] = read_string(db)
        map_info["status"] = read_byte(db)
        map_info["count_normal"] = read_short(db) #
        map_info["count_slider"] = read_short(db) #
        map_info["count_spinner"] = read_short(db) #
        map_info["last_mod_time"] = read_datetime(db)
        if meta["version"] < 20140609:
            map_info["diff_approach"] = int(read_byte(db)) #
            map_info["diff_size"] = int(read_byte(db)) #
            map_info["diff_drain"] = int(read_byte(db)) #
            map_info["diff_overall"] = int(read_byte(db)) #
        else:
            map_info["diff_approach"] = read_single(db)
            map_info["diff_size"] = read_single(db)
            map_info["diff_drain"] = read_single(db)
            map_info["diff_overall"] = read_single(db)
        map_info["slider_velocity"] = read_double(db) #
        if meta["version"] >= 20140609:
            no_pairs = read_int(db)
            map_info["standard_star_ratings"] = [
                read_int_double(db) for _ in range(no_pairs) #
            ]
            no_pairs = read_int(db)
            map_info["taiko_star_ratings"] = [
                read_int_double(db) for _ in range(no_pairs)
            ]
            no_pairs = read_int(db)
            map_info["ctb_star_ratings"] = [
                read_int_double(db) for _ in range(no_pairs)
            ]
            no_pairs = read_int(db)
            map_info["mania_star_ratings"] = [
                read_int_double(db) for _ in range(no_pairs)
            ]
        map_info["drain_time"] = read_int(db) #
        map_info["total_length"] = read_int(db) #
        map_info["preview_start_time"] = read_int(db) #
        no_timing = read_int(db)
        map_info["timing_points"] = [read_timing(db) for _ in range(no_timing)] #
        map_info["beatmap_id"] = read_int(db) #
        map_info["beatmapset_id"] = read_int(db) #
        map_info["thread_id"] = read_int(db)
        map_info["best_grade_standard"] = read_byte(db) #
        map_info["best_grade_taiko"] = read_byte(db)
        map_info["best_grade_ctb"] = read_byte(db)
        map_info["best_grade_mania"] = read_byte(db)
        map_info["local_offset"] = read_short(db)
        map_info["stack_leniency"] = read_single(db) #
        map_info["mode"] = read_byte(db) #
        map_info["source"] = read_string(db) #
        map_info["tags"] = read_string(db) #
        map_info["online_offset"] = read_short(db)
        map_info["title_font"] = read_string(db)
        map_info["unplayed"] = read_bool(db)
        map_info["last_played"] = read_long(db)
        map_info["is_osz2"] = read_bool(db)
        map_info["folder_name"] = read_string(db)
        map_info["last_updated"] = read_long(db)
        map_info["ignore_sound"] = read_bool(db)
        map_info["ignore_skin"] = read_bool(db)
        map_info["disable_storyboard"] = read_bool(db)
        map_info["disable_video"] = read_bool(db)
        map_info["visual_override"] = read_bool(db)
        if meta["version"] < 20140609:
            read_short(db)
        map_info["last_mod_time_2"] = read_int(db)
        map_info["scroll_speed"] = read_byte(db)
        beatmaps.append(map_info)
    return beatmaps


def db_test(name):
    path = "D:\osu!\osu!.db"
    with open(path, "rb") as db:
        meta = read_meta(db)
        beatmaps = read_beatmaps(db, meta)
        save_to_csv(beatmaps)
        print(meta)


if __name__ == '__main__':
    db_test('PyCharm')

