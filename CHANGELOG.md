# Changelog

## [Unreleased]

## [0.9.0]

- Updated vosk STT model to v0.9.
- Auto-downloading of models online if not available locally.
- Progress bars with `tqdm`.

## [0.8.4]

- Automatically converts to wave and keep fillers when creating 'split' files.
- Fixed argument propagation error in istitlan.

## [0.8.3]

- Fixed missing module 'pytz'

## [0.8.2]

- Export to EAF (Elan) files.
- Option '--autosplit' (adaptative splitting of audio file at silences).
- Option '--set-ffmpeg-path' to define the path to ffmpeg explicitely.
- Option '-v/--version' to show the version of the module.

## [0.8.1]

- Fixed dependency in 'normalizan' script.

## [0.8.0]

- 'normalizan' command will normalize a text file or whatever is sent through stdin.
- Updated STT model to v0.8.

## [0.7.12]

- Added option '--keep-fillers' that allows verbal fillers ('euh', 'ebeñ', 'kwa', 'alors'...) in transcriptions.

## [0.7.11]

- Changed option '-d/--translate' to '--translate' because of conflicting '-d' option in 'mikro.py' script.
- Bufixes in script `mikro.py` from @Tornaod

## [0.7.10]

- Fixed setup.py to include non python file, broken by the new folder hierarchy.

## [0.7.9]

- Options -o/--output (output file) and -d/--translate (translate words using a tsv file) added to 'adskrivan', 'istitlan' and 'mikro' scripts.
- Simplified folder hierarchy.
- The scripts can now be called with the python interpreter.

## [0.7.8]

- First version uploaded to pypi.org
