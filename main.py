# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from stream_read_utils import *

def read_meta(db):
    return {
        "version": read_int(db),
        "folder_count": read_int(db),
        "account_unlocked": read_bool(db),
        "date_unlocked": read_datetime(db),
        "player_name": read_string(db),
        "number_of_beatmaps": read_int(db)
    }


def read_beatmaps(db, meta):
    beatmaps = {}
    for _ in range(meta["number_of_beatmaps"]):
        map_info = {}
        if meta["version"] < 20191106:
            map_info["file_size"] = read_int(db)
        else:
            map_info["file_size"] = -1
        map_info["osu_version"] = meta["version"]
        map_info["artist"] = read_string(db)
        map_info["artist_unicode"] = read_string(db)
        map_info["title"] = read_string(db)
        map_info["title_unicode"] = read_string(db)
        map_info["creator"] = read_string(db)
        map_info["version"] = read_string(db)  # difficulty name
        map_info["audio_filename"] = read_string(db)
        map_info["file_md5"] = read_string(db)
        map_info["filename"] = read_string(db)
        ranked_status = read_byte(db)  # why is this different to the online api
        map_info["approved"] = ranked_status - 3 if ranked_status >= 4 else -2
        map_info["count_normal"] = read_short(db)
        map_info["count_slider"] = read_short(db)
        map_info["count_spinner"] = read_short(db)
        map_info["last_mod_time"] = read_datetime(db)
        if meta["version"] < 20140609:
            map_info["diff_approach"] = int(read_byte(db))
            map_info["diff_size"] = int(read_byte(db))
            map_info["diff_drain"] = int(read_byte(db))
            map_info["diff_overall"] = int(read_byte(db))
        else:
            map_info["diff_approach"] = read_single(db)
            map_info["diff_size"] = read_single(db)
            map_info["diff_drain"] = read_single(db)
            map_info["diff_overall"] = read_single(db)
        map_info["slider_velocity"] = read_double(db)
        if meta["version"] >= 20140609:
            no_pairs = read_int(db)
            map_info["standard_star_ratings"] = [
                read_int_double(db) for _ in range(no_pairs)
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
        map_info["drain_time"] = read_int(db)
        map_info["total_length"] = read_int(db)
        map_info["preview_start_time"] = read_int(db)
        no_timing = read_int(db)
        map_info["timing_points"] = [read_timing(db) for _ in range(no_timing)]
        map_info["beatmap_id"] = read_int(db)
        map_info["beatmapset_id"] = read_int(db)
        map_info["thread_id"] = read_int(db)
        map_info["best_grade_standard"] = read_byte(db)
        map_info["best_grade_taiko"] = read_byte(db)
        map_info["best_grade_ctb"] = read_byte(db)
        map_info["best_grade_mania"] = read_byte(db)
        map_info["local_offset"] = read_short(db)
        map_info["stack_leniency"] = read_single(db)
        map_info["mode"] = read_byte(db)
        map_info["source"] = read_string(db)
        map_info["tags"] = read_string(db)
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
        beatmaps[map_info["beatmap_id"]] = map_info

        print(map_info)
    return beatmaps


def db_test(name):
    path = "D:\osu!\osu!.db"
    with open(path, "rb") as db:
        meta = read_meta(db)
        beatmaps = read_beatmaps(db, meta)
        print(meta)


if __name__ == '__main__':
    db_test('PyCharm')

