from Codes.Service.InitDatas import *
from Codes.Service.DataServices import *
from operator import itemgetter

class Managers:
    """
        Group All managers for Main Use
    """
    def __init__(self):
        self.vehicle = VehicleManager()
        self.property = PropertyManager()
        self.color = ColorManager()
        self.buy = BuyManager()
        self.storage = StorageManager()
        
class MainFundamentalFunc:
    """
        The Main Data Library for UI
    """
    UNDEFINED_PROPERTY_ID = 0 
    UNDEFINED_SLOT_TYPE = 0
    UNDEFINED_SLOT_INDEX = -1  

    def __init__(self, managers:Managers):
        self.mgr = managers
        self.strg_svc = StorageService(self.mgr)
        self.buy_svc = BuyingService(self.mgr)

        self.color_palette = defaultdict(lambda: defaultdict(list))

    def load_all_services(self):
        """
            load All Manager' datas
        """
        self.mgr.vehicle.load_table()
        self.mgr.property.load_table()
        self.mgr.color.load_table()
        self.mgr.buy.load_table()
        self.mgr.storage.load_table()


        self.strg_svc.load_storage_service()
        self.buy_svc.load_user_data()

        self.color_palette = self.get_paint_list()

        ### Setting Undefined Garage Slot
        property_none_id = next((prow['id'] for prow in self.mgr.property.property_table if prow['key_name'] == 'Temporary'), None)
        ptype_none_id = next((prow['id'] for prow in self.mgr.property.property_type_table if prow['key_name'] == 'Temporary'), None)
        self.UNDEFINED_PROPERTY_ID = next((opid for opid, oprow in self.mgr.property.owned_property.items() if (oprow['property_id'] == property_none_id) and (oprow['property_type_id'] == ptype_none_id)), 0)
        self.UNDEFINED_SLOT_TYPE = next((stid for stid, stname in self.mgr.storage.slot_type_map.items() if (stname == 'Universal')), 0)

    def get_vehicle_classes(self):
        """
            get Sorted Vehicle Classes' Names
        """
        raw_names = [row['key_name'] for row in self.mgr.vehicle.vehicle_class]
        return sorted(raw_names, key=str.lower)
    
    def get_vehicle_manufacturers(self):
        """
            get Sorted Manufacturers' Names
        """
        raw_names = [row['key_name'] for row in self.mgr.vehicle.manufacturer]
        return sorted(raw_names, key=str.lower)
    
    def get_vehicle_acqs(self):
        """
            get Sorted Acquisition Sources
        """
        raw_names = [row['source'] for row in self.mgr.vehicle.acquisition_table]
        return sorted(raw_names, key=str.lower)
    
    def get_vehicle_drivetrain(self):
        """
            get All Drivetrain names
        """
        result_list = []
        for row in self.mgr.vehicle.drivetrain:
            result_list.append(row['key_name'])
        return result_list

    def get_clicked_vehicle_data(self, vehicle_id):
        return self.mgr.vehicle.get_vehicle(vehicle_id)
    
    def get_clicked_vehicle_acq(self, vehicle_id):
        return self.mgr.vehicle.get_vehicle_acquisition(vehicle_id)
    
    def get_clicked_vehicle_own(self, vehicle_id):
        return self.mgr.vehicle.get_own_vehicle_list(vehicle_id)
    
    def get_garages_for_own_vehicle(self, vehicle_id):
        """
            get All Garage Slots by Vehicle ID
        """
        return self.strg_svc.get_potential_garages_onoff(vehicle_id)
    
    def is_unique_own_vehicle(self, own_vehicle_id):
        """
            check Unique by Own Vehicle ID
        """
        own_data = self.mgr.vehicle.own_table.get(own_vehicle_id, {})
        vehicle_id = own_data.get('vehicle_id', 0)
        veh_data = self.get_clicked_vehicle_data(vehicle_id)
        return veh_data.get('is_unique', False)
    
    def add_own_vehicle(self, vehicle_id):
        """
            Purchase a Vehicle
        """
        target_vehicle = self.mgr.vehicle.get_vehicle(vehicle_id)
        ### Cannot Purchase Already owned and unique vehicle
        if target_vehicle['is_owned'] and target_vehicle['is_unique']:
            return False
        
        ### It is not necessary
        ### But it's good to have slot index for Temporary Garage
        next_slot_idx = self.strg_svc.get_available_slotindex(1,1)
        
        result = self.buy_svc.buy_logic_process('vehicle', vehicle_id, next_slot_idx=next_slot_idx)

        return result
    
    def edit_own_vehicle(self, own_id, **kwargs):
        """
            Modify Own Vehicle Data
        """
        flg = False
        target_data = self.mgr.vehicle.own_table.get(own_id)
        if not target_data:
            return False
        
        ### Changing Garage Logic
        move_keys = {'owned_property_id', 'slot_type_id', 'slot_index', 'is_sold'}
        if any(key in kwargs for key in move_keys):
            
            ### Confirm new location information (use existing data if not in kwargs)
            new_prop = kwargs.get('owned_property_id', target_data['owned_property_id'])
            new_type = kwargs.get('slot_type_id', target_data['slot_type_id'])
            new_idx = kwargs.get('slot_index', target_data['slot_index'])
            is_sold = kwargs.get('is_sold', target_data['is_sold'])

            ### Check if movement is possible Using Storage Service's Validation Logic
            if is_sold or not self.strg_svc.is_slot_empty(new_prop, new_type, new_idx):
                ### Sold or Cannot Find New Location > 'Temporary'
                kwargs['owned_property_id'] = self.UNDEFINED_PROPERTY_ID
                kwargs['slot_type_id'] = self.UNDEFINED_SLOT_TYPE
                kwargs['slot_index'] = self.strg_svc.get_available_slotindex(self.UNDEFINED_PROPERTY_ID, self.UNDEFINED_SLOT_TYPE)
                print(f"Target slot full or vehicle sold. Moving {own_id} to Undefined Storage.")
            else:
                kwargs['owned_property_id'] = new_prop
                kwargs['slot_type_id'] = new_type
                kwargs['slot_index'] = new_idx

            self.strg_svc.move_vehicle_to_garage(target_data, kwargs.get('owned_property_id'), kwargs.get('slot_type_id'), kwargs.get('slot_index'))

        ### You must Remove Paint Preset If it had hidden Color preset has changed
        if 'paint_preset_id' in kwargs.keys():
            paint_id = target_data['paint_preset_id']
            paint_data = self.mgr.color.paint_presets.get(paint_id)
            if paint_data is not None:
                if paint_data['is_hidden'] == True:
                    self.remove_paint_preset(paint_id)

        ### Modify DB
        flg = self.mgr.vehicle.edit_own_vehicle(own_id, **kwargs)
        
        if not flg:
            return flg
        
        ### Re-Sync Owned Flag in vehicle Data (not Owned Vehicle Data)
        self.check_vehicle_owned_flag(target_data['vehicle_id'])
            
        return flg
    
    def disable_own_vehicle(self, own_id):
        """
            DEPRECATED :: Use Edit Own Vehicle Instead
        """
        
        target_data = self.mgr.vehicle.own_table.get(own_id)
        target_vid = target_data['vehicle_id']
        """
        # unique일 경우 비활성 안됨
        if self.mgr.vehicle.get_vehicle(target_vid)['is_unique']:
            return False
        """

        self.strg_svc.remove_vehicle_in_garage(target_data)
        self.mgr.vehicle.sell_own_vehicle(own_id)

        self.check_vehicle_owned_flag(target_vid)

        return True
    
    def check_vehicle_owned_flag(self, vehicle_id):
        """
            Re-Sync Vehicle's 'is Owned' Flag by Iterating vehicle_map[vehicle_id]
        """
        tmpmap = self.mgr.vehicle.own_vehicle_id_map.get(vehicle_id, {})

        is_all_sold = True
        for row in tmpmap:
            if row.get('is_sold', True) == False:
                is_all_sold = False
                break
        
        if is_all_sold or len(tmpmap) == 0:
            self.mgr.vehicle.vehicle_map[vehicle_id]['is_owned'] = False

            ### Set is_owned None If vehicle cannot be Acquired
            if self.mgr.vehicle.acq_map.get(vehicle_id, None) is None:
                self.mgr.vehicle.vehicle_map[vehicle_id]['is_owned'] = None
        else:
            self.mgr.vehicle.vehicle_map[vehicle_id]['is_owned'] = True
    
    def remove_own_vehicle(self, own_id):
        """
            Remove Vehicle from DB and Manager Data
        """
        target_data = self.mgr.vehicle.own_table.get(own_id)
        target_vid = target_data['vehicle_id']

        ### You can Remove Only vehicle disabled
        if target_data.get('is_sold', False) == False:
            return
        """
        if self.mgr.vehicle.get_vehicle(target_vid)['is_unique']:
            return False
        """
        self.strg_svc.remove_vehicle_in_garage(target_data)
        self.mgr.vehicle.remove_own_vehicle(own_id)
        return
    
    def get_vehicle_list(self, sorting_order, reversed=False, vname=None, vclasses=None, mnftrs=None, acq=None, seat=None, op_str="=="):
        """
            Gets all vehicles matching the filters and returns them as a sorted list
        """
        if vname or vclasses or mnftrs or acq or seat:
            vehicle_list = self.mgr.vehicle.filter_vehicle(vname, vclasses, mnftrs, acq, seat, op_str)
        else:
            vehicle_list = self.mgr.vehicle.vehicle_table

        ### Sort ID, name and laptime should have order reversed
        sort_keys = {
            1: 'id',
            2: 'name',
            3: 'price',
            4: 'laptime_ms',
            5: 'topspeed_10mtph',
            6: 'mass'
        }
        if sorting_order in (2, 4):
            reversed = not reversed

        target_key = sort_keys.get(sorting_order, 'id')

        vehicle_list.sort(
            key=lambda v: (
                v.get(target_key) is None if not reversed else v.get(target_key) is not None, 
                v.get(target_key) or 0
            ),
            reverse=reversed)
        #print("Vehicle List Sorted")
        return vehicle_list
    
    def get_own_vehicle_dict_in_garage(self, own_property_id):
        return self.strg_svc.get_vehicles_in_garage(own_property_id)
    
    def get_own_vehicle_list_in_garage(self, own_property_id, slot_type_id):
        """
            Get Vehicle List by Garage Tuple (own_property_id, slot_type_id)
        """
        temp_dict = self.strg_svc.get_vehicles_in_garage(own_property_id)
        target_dict = temp_dict.get(slot_type_id, {})
        result_list = []
        for slotid, veh_data in target_dict.items():
            if veh_data is not None:
                result_list.append(veh_data)
        return result_list
    
    def get_own_vehicle_simple_in_garage(self, own_property_id):
        return self.strg_svc.own_simple_garage_map.get(own_property_id, [])
    
    def get_garage_list(self):
        """
            Convert all owned properties into a list of Garage with Tuples( opid, stype_id )
        """
        result_list = []
        target_keys = self.mgr.storage.ptype_slot_map.keys()
        garage_id = 0
        
        for ptype_id in target_keys:
            target_list = self.mgr.property.own_map.get(ptype_id, {})

            for own_prop_data in target_list:
                if own_prop_data and own_prop_data.get('is_active') == 1:
                    
                    if own_prop_data.get('property_type_id') != ptype_id:
                        continue

                    slots_definition = self.mgr.storage.ptype_slot_map[ptype_id]
                    
                    for slot_type_id, max_count in slots_definition.items():
                        target_data = copy.deepcopy(own_prop_data)
                        target_data['own_property_id'] = own_prop_data.get('id')

                        garage_own_data = self.strg_svc.own_vehicle_garage_map.get(target_data['id'], {})
                        slot_indexes = garage_own_data.get(slot_type_id, {})

                        target_data['slot_type_id'] = slot_type_id
                        target_data['total_slot'] = max_count
                        target_data['filled_slot'] = len(slot_indexes)

                        garage_id += 1
                        target_data['ui_garage_id'] = garage_id

                        result_list.append(target_data)

        return result_list
    
    def get_custom_paint_preset_list(self, only_vanila=False):
        
        return self.mgr.color.get_user_presets(False, only_vanila)
    
    def get_color_ref_list(self):
        
        return self.mgr.color.get_color_refs()

    def get_paint_list(self):
        """
            Return all Datas about Paint.
            includes : 
              GTA Presets ['Classic'] ['Matte'] ['Metallic'] ... all Categories, 
              ['Custom'] User Preset, 
              ['Index'] All Color References
        """
        result_list = self.mgr.color.get_gta_preset_catalogue()
        result_list['Custom'] = (self.mgr.color.get_user_presets(False, False))
        result_list['Index'] = (self.mgr.color.color_refs)
        return result_list

    def add_crew_color(self, name, hex_color):
        """
            Add Crew color to DB and Self color_palette
        """
        new_ref = self.mgr.color.add_custom_color(name, hex_color)
        if new_ref:
            self.color_palette['Index'][new_ref] = self.mgr.color.color_refs.get(new_ref)
            return new_ref
        return None
    
    def edit_crew_color(self, color_id, name, hex_color):
        """
            Modify Crew color to DB
            # color_palette synced DB
        """
        if self.mgr.color.edit_custom_color(color_id, name, hex_color):
            # self.color_palette['Index'].get( color_id )
            return True
        return False
    
    def remove_crew_color(self, color_id):
        """
            Remove Crew color from DB and Self color_palette
        """
        self.mgr.color.remove_custom_color(color_id)
        self.color_palette['Index'].pop(color_id)
        return True

    def add_paint_preset(self, **kwargs):
        """
            Add Custom Paint Preset to DB and Self color_palette
        """
        cname = kwargs.pop('name', None)
        is_hidden = kwargs.pop('is_hidden', None)
        if cname is None:
            ### Auto Naming
            cname = f"Custom Preset {(len(self.color_palette['Custom']) + 1)}"
            if (is_hidden is None) or (is_hidden == True):
                is_hidden = True
                cname = "Hidden " + cname 
        tempid = self.mgr.color.add_color_preset(cname, is_hidden, **kwargs)
        self.color_palette['Custom'][tempid] = (self.mgr.color.paint_presets.get(tempid))
        return tempid
    
    def edit_paint_preset(self, presetid, **kwargs):
        """
            Modify Custom Paint Preset to DB
            # color_palette synced DB
        """
        return self.mgr.color.edit_color_preset(presetid, **kwargs)
        
    def remove_paint_preset(self, presetid):
        """
            Remove Custom Paint Preset from DB and Self color_palette
        """
        result = self.mgr.color.remove_color_preset(presetid)
        self.color_palette['Custom'].pop(presetid, None)
        return result
        

    def get_property_dict(self):
        """
            {Property type id : [Property List]}
        """
        # Hide 'is hidden' flagged items
        ptypelist = self.mgr.property.property_type_table
        property_showlist = copy.deepcopy(self.mgr.property.ptype_map)

        for ptype in ptypelist:
            if ptype['is_hidden'] == 1:
                #print(f"Removing Hidden Property ID : {ptype['id']} :: {ptype['key_name']}")
                property_showlist.pop(ptype['id'], None)

        owned_ids = {p['property_id'] for p in self.mgr.property.owned_property.values() if p['is_active'] == 1}
    
        ### generates 'is_owned' flag here
        for type_id, properties in property_showlist.items():
            for prop in properties:
                prop['is_owned'] = prop['id'] in owned_ids

        return property_showlist
    
    def get_clicked_property_data(self, property_id):
        """
            get Clicked Property's All Custom data\n
            { Custom type id : [ {Custom data} ] }
        """
        target = self.mgr.property.property_map.get(property_id)
        if not target:
            return None
        
        target_type_id = target['type_id']
        result = copy.deepcopy(self.mgr.property.custom_map.get(target_type_id, {}))
        
        ptype_ownmap = self.mgr.property.own_map.get(target_type_id, {})
        pown_id = None

        # get own property id
        for own_data in ptype_ownmap:
            if (property_id == own_data['property_id']) and (own_data['is_active'] == 1):
                pown_id = own_data['id']
                break

        poc_map = self.mgr.property.owned_custom_map.get(pown_id, {})

        for ctype_id, custom_list in result.items():
            # checking all custom items are 'owned'
            currently_owned_custom_list = poc_map.get(ctype_id) 

            for custom_item in custom_list:
                custom_item['is_owned'] = False
                if currently_owned_custom_list is None:
                    custom_item['is_owned'] = False
                    continue

                for own_item in currently_owned_custom_list:
                    if own_item and (custom_item['id'] == own_item['id']):
                        custom_item['is_owned'] = True
                        break
                    
        # DEPRECATED Owned Flag
        # result['is_property_owned'] = (pown_id is not None)
        # print(result)
        return result
    
    def enable_own_property(self, property_id):
        """
            Purchase a property
        """
        result = self.buy_svc.buy_logic_process('property', property_id)

        return result
    
    
    def change_own_property(self, before_id ,property_id):
        """
            Modify Own property Data's 'Property ID'
        """
        # 바꾸기 가능한앤지 먼저 체크
        # 바꾸면서 딸린 차고 슬롯같은거 잇으면 그거도 바꿔줄 것
        result = self.mgr.property.inactive_own_property(before_id)

        if result == False:
            return False
        
        result = self.mgr.property.add_own_property(property_id)

        return result
    
    def disable_own_property(self, property_id):
        """
            Inactive own property, there will be no removing
        """
        result = self.mgr.property.inactive_own_property(property_id)
        return result
    
    def enable_own_property_custom(self, own_pid, pcustom_id):
        """
            Purchase a property Custom
        """
        result = self.buy_svc.buy_logic_process('custom', pcustom_id, own_pid=own_pid)

        return result
    
    def change_own_property_custom(self, own_pid, pcustom_id, after_custom_id):
        """
            Modify Own property Custom Data's 'Custom ID'
        """
        # 바꾸기 가능한앤지 먼저 체크
        # 바꾸면서 딸린 차고 슬롯같은거 잇으면 그거도 바꿔줄 것
        result = self.mgr.property.edit_own_pcustom(own_pid, pcustom_id, after_custom_id)
        return result
    
    def disable_own_property_custom(self, own_pid, pcustom_id):
        """
            Remove own property's custom 
        """
        # disable 가능한앤지 먼저 체크
        result = self.mgr.property.remove_own_pcustom(own_pid, pcustom_id)
        return result
    
    def get_stat_data(self):
        """
            Returns Stats\n

            "total_price" : Sum of All Vehicle Prices,
            "own_price" : Sum of Owned Vehicle Prices,
            "total_count" : Number of All Vehicles,
            "own_count" : Number of Owned Vehicles,
            "total_slot" : Number of All Ownable Storage Slots,
            "slot_count" : Number of Owned Storage Slots,
            "slot_filled" : Number of Filled Storage Slots,
            "car_slot_count" : Number of Owned Garage Slots,
            "car_filled" : Number of Filled Garage Slots
        """
        # 모든 이동수단 가치, 소유 가치, 전체 개수, 소유 개수, 보유 차고 슬롯 수..(자전거 제외)
        
        totalprice = 0
        ownprice = 0

        totalcount = 0
        owncount = 0
        slotcount = 0
        totalslot = 0

        slotfilled = 0

        car_slot = 0
        car_filled = 0

        for vehicle in self.mgr.vehicle.vehicle_table:
            thisprice = vehicle.get('price', 0)
            if thisprice is None:
                thisprice = 0
            
            totalprice += thisprice
            totalcount += 1

            if vehicle.get('is_owned') == True:
                ownprice += thisprice
                owncount += 1


        # count에서 제외할 목록
        no_count_ptid_set = {0, 1}
        no_count_stid_set = {1, 3}
        tmpset = no_count_ptid_set.copy()

        # get garage list에서 slotcount 뽑아올 것
        glist = self.get_garage_list()
        for garage in glist:
            ptid = garage.get('property_type_id', None)
            if ptid in tmpset:
                tmpset.remove(ptid)
                continue

            stid = garage.get('slot_type_id', None)
            if stid in no_count_stid_set:
                continue

            slotcount += garage.get('total_slot', 0)
            slotfilled += garage.get('filled_slot', 0)
            if stid == 2:
                car_slot += garage.get('total_slot', 0)
                car_filled += garage.get('filled_slot', 0)

        tmpset = no_count_ptid_set.copy()

        for row in self.mgr.storage.property_type_has_slot.values():
            pid = row.get('propertytype_id')
            if pid in tmpset:
                tmpset.remove(pid)
                continue

            stid = garage.get('slottype_id', None)
            if stid in no_count_stid_set:
                continue

            targetpdata = self.mgr.property.property_type_map.get(pid)
            if targetpdata:
                max_owned = targetpdata.get('max_owned', 0)
                if max_owned is None:
                    max_owned = 0
                
                totalslot += max_owned * row.get('numberofslot', 0)
            
        return {
            "total_price": totalprice,
            "own_price": ownprice,
            "total_count": totalcount,
            "own_count": owncount,
            "total_slot": totalslot,
            "slot_count": slotcount,
            "slot_filled" : slotfilled,
            "car_slot_count" : car_slot,
            "car_filled" : car_filled
        }

