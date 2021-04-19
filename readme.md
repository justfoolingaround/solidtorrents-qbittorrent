SolidTorrents Extension for qBittorrent
---

**Disclaimer**

This project, despite of the use case wasn't and isn't intended directly for piracy and is inclined towards automation techniques and their implementations. 
Using peer-to-peer connections for piracy may be illegal in your country. 

API provides developer with an easier and a much cleaner way for automation; this project is a demonstration of just that.

**Usage**

This program can be installed in your qBittorrent client by following the instructions [here.](https://github.com/qbittorrent/search-plugins/wiki/Install-search-plugins)

**Modifications**

For this project, modifications aren't really a 'discouraged' idea; you may modify the code according to your need, however, your modifications will not be assisted with by the developer.

That means, you are free to do whatever you want with this code.

**TODO(s)**

For now, the next step for this project would be to implement asyncio/threading to fetch & stream all the results to the client. 

This would solve the issue with the latency seen during the search result view (as 20 results, at most get generated at a time); however, this wouldn't increase the quality of the 'top' results as the results remain in the same order.

**Advantages**

The massive advantage of this project is perhaps the fast search results from the DHT crawler.

The provider for this project is stacked with a massive number of torrents, check out the number [here.](https://solidtorrents.net/api/v1/)

Additionally, `--no-query` wildcard (`*` will also work just fine) has been added to retrieve latest torrent(s) from the site without having to deal with qBittorrent's input validations.

**Issues**

The extension will percentage encode everything that's not ASCII and is `|` (characters that will cause stdout read cause some issues), hence, certain languages might be fully percentage encoded.

**Requirements**

- Python 3.9 +
- python-requests
- qBittorrent (tested on v4.3.3.1; expected to run on versions newer than that.)