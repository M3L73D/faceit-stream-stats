import requests
import time


PER_PAGE = 100
MAX_MATCHES = 500


def get_user_info(nickname):
	try:
		print(f"[~] Getting user info for {nickname}")
		r = requests.get(f"https://api.faceit.com/users/v1/nicknames/{nickname}")
		r = r.json()
		info = {
			'nickname': r['payload']['nickname'],
			'id': r['payload']['id'],
			'avatar': r['payload']['avatar'],
			'steam_id': r['payload']['platforms']['steam']['id'],
			'steam_id64': r['payload']['platforms']['steam']['id64']
		}
		print(f"[+] Got user info for {nickname}")
		return info
	except Exception as error:
		print(f"[-] ERROR: {error}")
		#raise Exception(f"Couldn't get user info for nickname: {nickname}")


def get_user_matches(user_id, last=None, starting_from=None, in_last=None):

	def check_match(match):
		return match['status'] == 'APPLIED' and match['played'] == '1' and match['premade'] == False and 'elo' in match

	page = 0
	matches = []
	counter = 0

	while True:
		
		r = requests.get(f"https://api.faceit.com/stats/v1/stats/time/users/{user_id}/games/csgo?page={page}&size={PER_PAGE}")
		r = r.json()

		print(f"[~] Got {len(r)} matches per page for {user_id}")

		for match in r:
			if check_match(match): # check if it's a real played match
				if counter == MAX_MATCHES:
					print(f"[+] Reached the limit of {MAX_MATCHES} matches for {user_id}")
					return matches, int(match['elo'])

				if last is not None and counter == last:
					print(f"[+] Got {len(matches)} last matches for {user_id}")
					return matches, int(match['elo'])

				if starting_from is not None and match['created_at'] < starting_from * 1000:
					print(f"[+] Got {len(matches)} matches starting from {starting_from} for {user_id}")
					return matches, int(match['elo'])

				if in_last is not None and match['created_at'] < (time.time() - 24 * in_last * 60 * 60) * 1000:
					print(f"[+] Got {len(matches)} matches played in last {in_last} days for {user_id}")
					return matches, int(match['elo'])

				counter += 1

				try:
					matches.append({
						'created_at': match['created_at'],
						'kills': int(match['i6']),
						'assists': int(match['i7']),
						'deaths': int(match['i8']),
						'rounds': int(match['i12']),
						'win': match['i10'] == '1',
						'elo': int(match['elo'])
					})
				except Exception as error:
					print(f"[-] Couldn't append a match {match['matchId']}: {error}")
			else:
				print(f"[~] Skipped a match {match['matchId']}")

		print(f"[~] Counter: {counter}, good matches: {len(matches)}")

		if len(r) < PER_PAGE:
			return matches, 1000

		page += 1


def get_stats(matches, start_elo=None):
	stats = {
		'matches': len(matches),
		'win': 0,
		'loss': 0,
		'win-today': 0,
		'loss-today': 0,
		'kd': 0,
		'kr': 0,
		'avg': 0,
		'elo-dif': 0
	}
	today = (time.time() - 24 * 60 * 60) * 1000
	kills = 0
	deaths = 0
	rounds = 0

	for match in matches:
		if match['win']:
			stats['win'] += 1
			if match['created_at'] > today:
				stats['win-today'] += 1
		else:
			stats['loss'] += 1
			if match['created_at'] > today:
				stats['loss-today'] += 1
		kills += match['kills']
		deaths += match['deaths']
		rounds += match['rounds']

	if deaths != 0:
		stats['kd'] = round(kills / deaths, 2)
	if rounds != 0:
		stats['kr'] = round(kills / rounds, 2)
	if stats['matches'] != 0:
		stats['avg'] = round(kills / stats['matches'], 1)

		if start_elo is not None:
			stats['elo-dif'] = matches[0]['elo'] - start_elo

	return stats


if __name__ == '__main__':

	nickname = 'RachelR'

	info = get_user_info(nickname)
	matches, start_elo = get_user_matches(info['id'], in_last=30)
	print(f'[+] Got matches for {nickname}, total: {len(matches)}')

	stats = get_stats(matches, start_elo)
	print(f'[+] Got stats for {nickname}')
	print(stats)