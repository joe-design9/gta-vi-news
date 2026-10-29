# GTA VI News

Independent German-language fan news site. Standalone HTML/CSS/JavaScript, hosted on GitHub Pages. No Wabi account, paid backend or API key is required to browse it.

## News updates

- `news.json` contains the curated articles carried over from the original Wabi news site and an attributed press-headline feed.
- GitHub Actions fetches the German Google News RSS search for GTA 6 / GTA VI hourly (minute 23) and republishes the site. Scheduled runs can be delayed by GitHub; they are not real-time delivery and cannot guarantee exhaustive coverage.
- Feed headlines are labeled **Pressefeed · nicht geprüft**. They link through Google News to the publisher. They are not independently fact-checked or reproduced full articles.
- Editorial article summaries and official announcements are kept separate. No article contents are generated automatically.
- The refresh button reloads the latest deployed feed. It does not initiate a new GitHub Actions run. The owner can manually run **Update news and deploy Pages** in the repository's Actions tab.
- When RSS retrieval fails, the previous saved feed remains available and the feed timestamp does not advance.
- No live synchronization with the original Wabi app; the two sites are independent after this migration.

## Local preview

Run `python3 -m http.server 8000` in the repository and open http://localhost:8000.
Run `python3 scripts/update_news.py` to refresh headlines locally.

## Attribution

This is an unofficial fan project, not affiliated with Rockstar Games or Take-Two. GTA names and game imagery belong to their respective rights holders. Source links and image descriptions accompany curated articles. No rights to Rockstar imagery are granted by this repository.
