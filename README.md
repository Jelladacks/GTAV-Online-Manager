# Grand Theft Auto V Online Manager

> This is an **external companion app** for Easy managing your Vehicles and Properties
> It is a **standalone application** that runs completely outside of the game, meaning it does not modify or inject any code into the GTA game client.
> 
> Click [🎬 HERE ](https://youtu.be/BwFk0pHFWbo) to watch Tutorial Video
> 
![Main UI](https://github.com/user-attachments/assets/c78b1aba-2014-4710-b03b-6a762ccc4540)
>
> 
>
> 

## Features
* **Search Vehicle Info**

  Find a vehicle Easily using the filters at the top
  * Designed for multilingual users, this project allows transit searches in multiple languages.
  * Currently, it supports Korean only, but you can add or modify other languages by following the data customization guide below
  ![Search](https://github.com/user-attachments/assets/70584799-afc1-4703-8421-90aca9376ae6)
  
* **Manage Your Own Vehicle**
  
  Check vehicle details
  and track the location and quantity of each vehicle
  ![Vehicle](https://github.com/user-attachments/assets/8ff0c428-1f87-452c-af42-5fa8568ee963)
  
* **Manage Your Property and Customs**
  
  Click the checkbox and Open Custom Dialog for purchasing Customs
  ![Property](https://github.com/user-attachments/assets/b733ca60-dd98-4b55-a249-b0b4ebac07a7)
  
* **Paint Preset**
  
  Save your Cutom Paint Preset
  and Apply it to Your Vehicles
  ![Paint](https://github.com/user-attachments/assets/d88b4bb5-1eab-425d-acf8-eba8fe5c248b)

* **Customize Your Data**
  
  You can replace the vehicle or garage images with any picture you like
  ![Custom](https://github.com/user-attachments/assets/79a61712-1625-4dd6-8245-e92e1f65b26b)

* **Statistics**
  
  Track your stats and manage your garage effortlessly
  ![Stats](https://github.com/user-attachments/assets/e470e490-70c5-4f41-9425-106cc919a222)

* **Back up and Sharing**
  
  Backup and sharing are possible by simply copying and pasting the entire `Customs` folder.

  
## Automated Data Sync & Easy Maintenance 
  Every time the app launches, it scans the CSV files in the `Datas/Database/seed` folder.
  If any changes are detected, the app's database is automatically updated to match.
  Therefore, even when GTA receives an update, you can support it simply by adding rows to the CSV files and inserting new image files, without needing to update the app itself.

**Custom Language Support**

If you want Manufacturer names and Vehicle names to be displayed in a language other than Korean,
you can modify the `KorName` column in the following files:

* `Datas/Database/seed/GTAVOManufacturerDataTable.csv`
* `Datas/Database/seed/GTAVOVehicleTranslation.csv`

You may replace the Korean text with your preferred language.

**Adding or Editing Liveries**

If you want to add or edit liveries manually:

1. Add a new row to:
   `Datas/Database/seed/GTAVOLiveryType.csv`

2. Assign a unique ID and enter the livery name.

3. Place a `.webp` image file inside:
   `Datas/images/Liveries`

4. The image filename must match the livery name added in the CSV row.

**Adding Custom Vehicles**

The same process also applies to vehicles.

1. Add vehicle information to:
   `Datas/Database/seed/GTAVOVehicleDataTable.csv`

2. Add a vehicle image to:
   `Datas/images/Vehicles`

3. The image filename format must be:
   `vehicleID.jpg`

  
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
* Color Picker from **tomfln** (https://github.com/tomfln/pyqt-colorpicker) licensed under the MIT License.

## References
* **Color Picker** - [tomfln](https://github.com/tomfln/pyqt-colorpicker)
* **laptime and Top speed** - **BROUGHY1322** (https://broughy.com/)
* **Image Sources**
  * [Rockstar Games](https://rockstargames.com) (All rights reserved by Rockstar Games and Take-Two Interactive) 
  * [GTA Wiki (Fandom)](https://gta.fandom.com/wiki/GTA_Wiki:Copyright)
  * [GTABase](https://www.gtabase.com/grand-theft-auto-v/)

*Disclaimer: This is an unofficial, non-commercial, fan-made app.*

## License
This software is licensed under the MIT License.
More information is provided in the dedicated LICENSE file.
