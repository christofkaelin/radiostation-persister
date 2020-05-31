# radiostation-persister
## Description 
Python utility which allows to save the playlist from a radio station into a database

## List of radio stations
Radio Pilatus ([Stream](https://radiopilatus.ice.infomaniak.ch/pilatus128.mp3)):\
```https://radio.radiopilatus.ch/api/pub/gql/radiopilatus/AudioLiveData/e8ed774ebb6a811303ea3ff7078581730ff3914c```

Radio FM1 ([Stream](https://radiofm1.ice.infomaniak.ch/radiofm1-128.mp3)):\
```https://www.radiofm1.ch/api/pub/gql/radiofm1/AudioLiveData/e8ed774ebb6a811303ea3ff7078581730ff3914c```

Radio 24 ([Stream](https://icecast.radio24.ch/radio24-rc-96-aac)):\
```https://www.radio24.ch/api/pub/gql/radio24/AudioLiveData/e8ed774ebb6a811303ea3ff7078581730ff3914c```

Virgin Radio Hits Switzerland ([Stream](https://icecast.argovia.ch/vhits)):\
```https://www.virginradiohits.ch/api/pub/gql/virginhits/AudioLiveData/e8ed774ebb6a811303ea3ff7078581730ff3914c```

## Usage
1) Clone the repo:
```git clone https://github.com/christofkaelin/radiostation-persister.git```
2) Install the necessary requirements:
```pip3 install -r requirements.txt```
3) Create your own config file based on the sample:
```cp config-sample.yaml config.yaml```
And adapt the config with your preferred text editor (e.g. `vim` or `nano`)
4) Run the script:
```python3 run.py```
