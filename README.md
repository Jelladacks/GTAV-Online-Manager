# Grand Theft Auto V Online Manager

> Tool for Easy managing your Vehicles and Properties
![Main UI](이미지_주소_또는_경로)

## Features
* **Search Vehicle Info**
  Find a vehicle Easily using the filters at the top
  
* **Manage Your Own Vehicle**
  Check vehicle details
  and track the location and quantity of each vehicle
  
* **Manage Your Property and Customs**
  Click the checkbox and Open Custom Dialog for purchasing Customs
  
* **Paint Preset**
  Save your Cutom Paint Preset
  and Apply it to Your Vehicles

* **Customize Your Data**
  You can replace the vehicle or garage images with any picture you like

* **Statistics**
  Track your stats and manage your garage effortlessly

* **Back up and Sharing**
  Backup and sharing are possible by simply copying and pasting the entire `Customs` folder.
  
## Automated Data Sync & Easy Maintenance 
  Every time the app launches, it scans the CSV files in the `Datas/Database/seed` folder.
  If any changes are detected, the app's database is automatically updated to match.
  Therefore, even when GTA receives an update, you can support it simply by adding rows to the CSV files and inserting new image files, without needing to update the app itself.
  
## Database Reset Option via CLI Args
  Running the app with the `--reset` argument will fully reset the database.
  Warning: This will also permanently delete all user data in the Customs folder.

### Installation
1. Download Recent Version at Releases Tab [Releases]((https://github.com/Jelladacks/GTAV-Online-Manager/releases/tag/v1.0.0)) 
2. Extract and Launch `GTAV Online Manager.exe`

## Built With
* Python 3.13.1
* PySide6
* SQLite
* Color Picker from **tomfln**(https://github.com/tomfln/pyqt-colorpicker) licensed under the MIT License.

## References
* **Color Picker** - [tomfln](https://github.com/tomfln/pyqt-colorpicker)
* **Image Sources**
  * [Rockstar Games](https://rockstargames.com) (All rights reserved by Rockstar Games and Take-Two Interactive) 
  * [GTA Wiki (Fandom)](https://gta.fandom.com/wiki/GTA_Wiki:Copyright)
  * [GTABase](https://www.gtabase.com/grand-theft-auto-v/)

*Disclaimer: This is an unofficial, non-commercial, fan-made app.*

## License
This software is licensed under the MIT License.
More information is provided in the dedicated LICENSE file.
