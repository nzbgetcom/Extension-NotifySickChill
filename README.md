> This extension is compatible to Python 3.8 and above.

## NZBGet Versions

- stable v23 [latest release](https://github.com/nzbgetcom/Extension-NotifySickChill/releases/latest)

# Notify SickChill
[Post-processing](https://github.com/nzbgetcom/nzbget/blob/develop/docs/extensions/POST-PROCESSING.md) extension for [NZBGet](https://nzbget.com) to trigger [SickChill](https://github.com/SickChill/sickchill/wiki/Post-Processing) after downloads.

After every finished download the extension calls the SickChill API (`cmd=postprocess`) so the episode is processed immediately. If a download fails, the extension notifies SickChill about the failure (`failed=1` together with `nzbName`) letting it mark the episode as Failed and automatically search for another release.

## Features

 - Triggers SickChill post-processing for successful downloads;
 - Notifies SickChill about failed downloads for retry search;
 - Optional cleanup of the download directory after post-processing ("Delete" option);
 - Localized settings dialog via `_locales`.

## Installation

 - Download the newest version from the [releases page](https://github.com/nzbgetcom/Extension-NotifySickChill/releases);
 - Unpack into pp-scripts directory. Your pp-scripts directory now should have folder "NotifySickChill" with file "main.py";
 - Open settings tab in NZBGet web-interface and define settings for Notify SickChill;
 - Assign the script in Settings -> Categories -> PostScript for your TV category;
 - Save changes.

## SickChill setup

 - Copy the API Key from the SickChill web interface (Config -> General Interface -> API Key) into the "API Key" option in NZBGet;
 - For failed download handling enable "Use Failed Downloads" in SickChill (Settings -> Search Settings -> Episode Search);
 - Use the **Ping** command in the extension settings to verify the connection.

## Options

| Option | Description |
|--------|-------------|
| Host | SickChill server host. |
| Port | Default port is: 8081 |
| API Key | Used to authenticate and authorize access to the SickChill API. |
| Process Method | How processed files are placed into the show folder: Copy, Move, Hard link or Symbolic link. |
| Force Replace | Force already post-processed files to be post-processed again. |
| Is Priority | Mark Dir/Files as priority download; replaces the file even if it exists at higher quality. |
| Delete | Delete files and folders after completion of Post-Processing. Recommended when Process Method is Copy, Hard link or Symbolic link. With Move it cleans up leftover files and empty folders. |
| Verbose | Print more logging messages. For debugging. |
