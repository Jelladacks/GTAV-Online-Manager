from Codes.Service.InitDatas import *
import copy

class StorageService:
    """
        Make Garage Map with Property, Vehicle and Storage Datas

        own_vehicle_garage_map : {own property id : { slot type id : {slot index : {own vehicle data}}}}
        own_simple_garage_map : { own property id : [{own vehicle data}] }

    """
    def __init__(self, managers):
        self.prop_mgr = managers.property
        self.veh_mgr = managers.vehicle
        self.str_mgr = managers.storage

        self.own_vehicle_garage_map = defaultdict(lambda: defaultdict(dict))
        self.own_simple_garage_map = defaultdict(list)

        self.veh_mgr.on_vehicle_changed_callbacks.append(self.add_vehicle_to_garage)

    def load_storage_service(self):
        self.own_vehicle_garage_map.clear()
        self.own_simple_garage_map.clear()
        
        ### Iterating All Own Vehicles
        for own_vehicle in self.veh_mgr.own_table.values():
            own_pid = own_vehicle['owned_property_id']
            own_v_stid = own_vehicle['slot_type_id']
            own_v_s_index = own_vehicle['slot_index']
            # print(f"own_vehicle_garage_map[{own_pid}] : {own_v_stid} : {own_v_s_index}")
            self.own_vehicle_garage_map[own_pid][own_v_stid][own_v_s_index] = own_vehicle
            self.own_simple_garage_map[own_pid].append(own_vehicle)
        
        for own_pid in self.own_simple_garage_map.keys():
            self.own_simple_garage_map[own_pid].sort(key=lambda x: (x.get('slot_type', 0), x.get('slot_index', 0)))
        return
    
    def rebuild_garage_slot_map(self, own_property_id):
        """
            Reflect the order of the Vehicles
            designated by carCardDelegate directly into the Slot Data
        """
        self.own_vehicle_garage_map[own_property_id].clear()
        for own_vehicle in self.own_simple_garage_map[own_property_id]:
            own_pid = own_vehicle['owned_property_id']
            own_v_stid = own_vehicle['slot_type_id']
            own_v_s_index = own_vehicle['slot_index']
            # print(f"own_vehicle_garage_map[{own_pid}] : {own_v_stid} : {own_v_s_index}")
            self.own_vehicle_garage_map[own_pid][own_v_stid][own_v_s_index] = own_vehicle
            
            self.veh_mgr.edit_own_vehicle(own_vehicle['id'], slot_type_id=own_vehicle['slot_type_id'], slot_index=own_vehicle['slot_index'])
        self.own_simple_garage_map[own_pid].sort(key=lambda x: x.get('slot_index', 1))

    def is_slot_empty(self, own_property_id, slot_type_id, slot_index):
        """
            Compare slot index with own property's slot list
        """
        owned_prop = self.prop_mgr.owned_property.get(own_property_id)
        if owned_prop is None:
            return False
        ptid = owned_prop['property_type_id']
        max_slot = self.str_mgr.get_max_number_of_slot(ptid, slot_type_id)

        if max_slot == 0 or max_slot is None:
            return False

        if (slot_index < 1) or (slot_index > max_slot):
            return False
        ### 
        return slot_index not in self.own_vehicle_garage_map.get(own_property_id, {}).get(slot_type_id, {})

    def is_slot_full(self, own_property_id, slot_type_id):
        """
            Compare own property type's max slot count with number of own property's slot
        """
        owned_prop = self.prop_mgr.owned_property.get(own_property_id)
        if owned_prop is None:
            return True
        ptid = owned_prop['property_type_id']
        max_slot = self.str_mgr.get_max_number_of_slot(ptid, slot_type_id)

        current_slot = len(self.own_vehicle_garage_map.get(own_property_id, {}).get(slot_type_id, {}))
        return current_slot >= max_slot
    
    def get_number_of_empty_slot(self, own_property_id, slot_type_id):
        """
            Subtract number of own property's slot from own property type's max slot count
        """
        owned_prop = self.prop_mgr.owned_property.get(own_property_id)
        if owned_prop is None:
            return 0
        
        ptid = owned_prop['property_type_id']
        max_slot = self.str_mgr.get_max_number_of_slot(ptid, slot_type_id)

        current_slot = len(self.own_vehicle_garage_map.get(own_property_id, {}).get(slot_type_id, {}))
        return (max_slot - current_slot)
    
    def get_available_slotindex(self, own_property_id, slot_type_id):
        """
            Iterate own property's slot type and get Empty slot
        """
        own_property_data = self.prop_mgr.owned_property.get(own_property_id, {})
        property_type_id = own_property_data.get('property_type_id')
        max_slot_index = self.str_mgr.get_max_number_of_slot(property_type_id, slot_type_id)
        for i in range(1, max_slot_index + 1):
            if self.own_vehicle_garage_map[own_property_id][slot_type_id].get(i) is None:
                return i
            
        return None

    def add_vehicle_to_garage(self, vehicle_data):
        """
            Add Vehicle Data to Garage map\n
            It will try another empty slot indexes If vehicle data's slot is not Empty
        """
        pid, stid, idx = vehicle_data['owned_property_id'], vehicle_data['slot_type_id'], vehicle_data['slot_index']
        if self.own_vehicle_garage_map[pid][stid].get(idx) is None:
            self.own_vehicle_garage_map[pid][stid][idx] = vehicle_data
            self.own_simple_garage_map[pid].append(vehicle_data)
            return True
        else:
            idx = self.get_available_slotindex(pid, stid)
            if idx is not None:
                self.own_vehicle_garage_map[pid][stid][idx] = vehicle_data
                self.own_simple_garage_map[pid].append(vehicle_data)
                return True
        return False
        
    def remove_vehicle_in_garage(self, vehicle_data):
        """
            Pop Vehicle data from Garage map
        """
        vownid = vehicle_data['id']
        self.own_vehicle_garage_map[vehicle_data['owned_property_id']][vehicle_data['slot_type_id']].pop(vehicle_data['slot_index'], None)
        for own_row in self.own_simple_garage_map[vehicle_data['owned_property_id']]:
            if own_row['id'] == vownid:
                self.own_simple_garage_map[vehicle_data['owned_property_id']].remove(own_row)
                return

    def move_vehicle_to_garage(self, vehicle_data, dest_pid, dest_stid, dest_index):
        """
            Check Destination is Empty,
            Then move vehicle data to Destination
        """
        if self.is_slot_empty(dest_pid, dest_stid, dest_index):
            new_vehicle_data = copy.deepcopy(vehicle_data)

            new_vehicle_data['owned_property_id'] = dest_pid
            new_vehicle_data['slot_type_id'] = dest_stid
            new_vehicle_data['slot_index'] = dest_index

            self.remove_vehicle_in_garage(vehicle_data)
            self.own_vehicle_garage_map[dest_pid][dest_stid][dest_index] = new_vehicle_data
            self.own_simple_garage_map[dest_pid].append(new_vehicle_data)
            

            #self.veh_mgr.own_table[new_vehicle_data['id']] = new_vehicle_data
            return True

        return False    


    def get_available_garages(self, vehicle_id):
        """
            DEPRECATED :: Use 'get_potential_garages_onoff' Instead
            Vehicle ID로 저장가능한 부동산과 슬롯정보 리스트를 제공함
        """
        vehicle_row = self.veh_mgr.get_vehicle(vehicle_id)
        if vehicle_row is None:
            return None

        available_list = []
       
        ### Iterates own properties
        for own_prop_id, owned_prop in self.prop_mgr.owned_property.items():
            if owned_prop['is_active'] == False:
                continue
            prop_id = owned_prop['property_id']
            prop_name = self.prop_mgr.property_map.get(prop_id, {}).get('key_name', 'Unknown')
            p_type_id = owned_prop['property_type_id']
            valid_slot_types = []

            # property_type_has_slot에서 해당 부동산 타입이 어떤 슬롯들을 가졌는지 조회
            slots_info = self.str_mgr.ptype_slot_map.get(p_type_id, {})

            for slottype_id, max_count in slots_info.items():
                if self.str_mgr.is_compatible(vehicle_row, slottype_id):
                    if not self.is_slot_full(own_prop_id, slottype_id):
                        valid_slot_types.append(slottype_id)

            for stid in valid_slot_types:
                prop_entry = copy.copy(owned_prop)
                prop_entry['property_name'] = prop_name
                prop_entry['slot_type_id'] = stid

                prop_entry['slot_type_name'] = self.str_mgr.slot_type_map.get(stid, 'Unknown')

                available_list.append(prop_entry)
        
        return available_list
    
    def get_potential_garages_onoff(self, vehicle_id):
        """
            Include every slot type that can store vehicles.
            Slot count validation and checkbox disabling
            will be handled separately
            in the Own Vehicle garage slot selection logic.
        """
        vehicle_row = self.veh_mgr.get_vehicle(vehicle_id)
        if vehicle_row is None:
            return None

        available_list = []

        avail_slot_type_ids = self.str_mgr.get_compatible_slottypes(vehicle_row).copy()
        # print(f"This is Available Slot Types : {avail_slot_type_ids} ")
       
        ### Iterates own properties
        for own_prop_id, owned_prop in self.prop_mgr.owned_property.items():
            if owned_prop['is_active'] == False:
                continue
            prop_id = owned_prop['property_id']
            if (prop_id == 1) and (not vehicle_row.get('is_pegasus')):
                continue
            prop_name = self.prop_mgr.property_map.get(prop_id, {}).get('key_name', 'Unknown')
            p_type_id = owned_prop['property_type_id']

            # property_type_has_slot에서 해당 부동산 타입이 어떤 슬롯들을 가졌는지 조회
            slots_info = self.str_mgr.ptype_slot_map.get(p_type_id, {})

            for slottype_id, max_count in slots_info.items():
                if slottype_id in avail_slot_type_ids:
                    prop_entry = copy.copy(owned_prop)
                    prop_entry['property_name'] = prop_name
                    prop_entry['slot_type_id'] = slottype_id
                    prop_entry['slot_type_name'] = self.str_mgr.slot_type_map.get(slottype_id, 'Unknown')

                    prop_entry['slot_left'] = self.get_number_of_empty_slot(own_prop_id, slottype_id)

                    available_list.append(prop_entry)

        return available_list

    
    def get_vehicles_in_garage(self, own_property_id):
        """
            Get Own Property's Garage from own_vehicle_garage_map
        """
        # Garage Viewer에서 Owned Vehilce의 Slot Index까지 맞춰서 보여줄 것 \n
        # 아마 {garage: {slottype: {slot : vehicle}}} 이런 딕셔너리가 하나 더 필요
        owned_prop = self.prop_mgr.owned_property.get(own_property_id)
        if owned_prop is None:
            print("get_vehicles_in_garage : owned prop is None")
            return {}
        
        ptid = owned_prop['property_type_id']
        target_garage_map = self.own_vehicle_garage_map.get(own_property_id, {})
        garage_result = target_garage_map
        """
        ### It can be removed, own_vehicle_garage_map replaces this code
        garage_result = {}
        for slot_type_id, slot_data in target_garage_map.items():
            max_slot = self.str_mgr.get_max_number_of_slot(ptid, slot_type_id)
            slots_dict = {i: None for i in range(1, max_slot + 1)}

            for slot_index, own_vehicle in slot_data.items():
                if slot_index in slots_dict:
                    slots_dict[slot_index] = own_vehicle

            garage_result[slot_type_id] = slots_dict
        """

        return garage_result

class BuyingService:
    """
        Make Buy Table Map with Property, Vehicle and BuyBonus Datas

        I build remaining_bonuses_keys for Optimizing
        to find bonuses when user purchase something
    """
    def __init__(self, managers):
        self.prop_mgr = managers.property
        self.veh_mgr = managers.vehicle
        self.buy_mgr = managers.buy
        self.remaining_bonuses_keys = set()

    def load_user_data(self):
        """
            Cache unowned Trigger ID / Reward ID pairs
            in remaining_bonuses_keys \n
            while iterating through Buy Bonus Data,
            preventing repeated full-data searches.
        """
        bkeys = set()
        for bbr in self.buy_mgr.buybonus_rule:
            tt_id = self.buy_mgr.target_type_lookup.get(bbr['triggertype_id'], "UNKNOWN") 
            t_id = bbr['trigger_id']
            rt_id = self.buy_mgr.target_type_lookup.get(bbr['rewardtype_id'], "UNKNOWN") 
            r_id = bbr['reward_id']

            addflag = False

            if tt_id.lower() == 'vehicle':
                if not self.veh_mgr.is_owned(t_id):
                    addflag = True
            elif tt_id.lower() == 'property':
                if not self.prop_mgr.is_owned_property(t_id):
                    addflag = True
            elif tt_id.lower() == 'custom':
                if not self.prop_mgr.is_owned_pcustom(t_id):
                    addflag = True
            
            if not addflag:
                if rt_id.lower() == 'vehicle':
                    if not self.veh_mgr.is_owned(r_id):
                        addflag = True
                elif rt_id.lower() == 'property':
                    if not self.prop_mgr.is_owned_property(r_id):
                        addflag = True
                elif rt_id.lower() == 'custom':
                    if not self.prop_mgr.is_owned_pcustom(r_id):
                        addflag = True

            if addflag:
                bkeys.add((tt_id, t_id))
                # print(bbr)
                
        self.remaining_bonuses_keys = bkeys



    def check_have_bonus(self, category, item_id):
        """
            Get item in remaining_bonuses_keys
        """
        if (category, item_id) not in self.remaining_bonuses_keys:
            return None
        
        bonus_map = self.buy_mgr.get_bonus_map()
        bonuslist = bonus_map.get(category, {}).get(item_id, None)
        rewards = list()
        for rw_row in bonuslist:
            rw_tuple = rw_row['rewardtype_id'], rw_row['reward_id']
            rewards.append(rw_tuple)
        print(f"check_have_bonus returns :{rewards}")
        return rewards

        
    def acquire_bonus(self, bonus_info, next_slot_idx=0):
        """
            Processes a bonus reward using a tuple extracted
            from Bonus Keys in the format:
                (category, item_id)
        """
        category_id, item_id = bonus_info
        category = self.buy_mgr.get_type_name(category_id)
        result = False

        if category == 'vehicle':
            result = self.veh_mgr.add_own_vehicle(item_id, slot_index=next_slot_idx)

        elif category == 'property':
            result = self.prop_mgr.add_own_property(item_id)
            
        elif category == 'custom':
            print(f"Maybe You Can't")

        return result
    
    def buy_logic_process(self, category, item_id, **kwargs):
        """
            Simply Purchase Item and Find and Add Bonus item in your User DB

            category = 'vehicle', 'property', 'custom'
            
            When you buy a Custom item you will need 'own_pid' in Kwawrgs

            Returns dict that has keys
              { 'own_vid', 'own_pid' , 'success' , 'msg' , 'bonus_category' , 'bonus_id' }
        """

        result = {
            'success': False,
            'msg': "구매 실패",
            'category': category,
            'own_id': None,    # own vehicle id or own property id
            'bonus_category': None,
            'bonus_id': None            
        }
        

        success = False
        next_slot_idx = kwargs.get('next_slot_idx', 0)
        if category == 'vehicle':
            result['own_vid'] = self.veh_mgr.add_own_vehicle(item_id, slot_index=next_slot_idx)
            next_slot_idx += 1
            success = True
        elif category == 'property':
            result['own_pid'] = self.prop_mgr.add_own_property(item_id)
            success = True
        elif category == 'custom':
            # 커스텀은 own_pid가 필요하므로 kwargs 활용
            own_pid = kwargs.get('own_pid')
            if own_pid is None:
                result['success'] = False
                result['msg'] = "부동산 ID가 없습니다."
                return result
            success = self.prop_mgr.add_own_pcustom(own_pid, item_id)

        if success:
            bonus_list = self.check_have_bonus(category, item_id)
            result['success'] = True
            if bonus_list:
                for bonus in bonus_list:
                    brt = self.acquire_bonus(bonus, next_slot_idx)
                    if brt == False:
                        result['bonus_category'], result['bonus_id'] = bonus
                        result['msg'] = "구매 성공, 보너스 FAIL"
                    else:
                        result['bonus_category'], result['bonus_id'] = bonus
                        result['msg'] = "구매 성공, 보너스 획득"
                        self.remaining_bonuses_keys.discard((category, item_id))
                    print(f"Bonus == {result['bonus_category']}, {result['bonus_id']} : {result['msg']}")
                    
            else:
                result['msg'] = "구매 성공"
        else:
            result['success'] = False
            result['msg'] = "구매 실패"

        return result
    