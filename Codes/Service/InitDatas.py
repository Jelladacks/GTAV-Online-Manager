from Codes.Service.loadGTAData import *
from Codes.Service.loadUserData import *
from collections import defaultdict
import operator

class VehicleManager:
    """
        Load Vehicle Datas From DB\n

        vehicle_table : {vehicla data}
        vehicle_map : {vehicle_id : vehicla data}
        acquisition_table : {acquisition data}
        own_table : {own_id : own_data}
        own_vehicle_id_map : {vehicle_id : [{own_data}] }
        acq_map : {vehicle_id : [acquisition] }
        acq_set : (acquisition)
        vehicle_class = {class data}
        manufacturer = {manufacturer data}
        drivetrain = {drivetrain data}
    
    """
    def __init__(self):
        self.vehicle_table = []
        self.acquisition_table = []
        self.own_table = []

        self.vehicle_class = []
        self.manufacturer = []
        self.drivetrain = []
        self.acq_set = set()

        self.on_vehicle_changed_callbacks = []
        

    def load_table(self):
        self.vehicle_table = DBLoader_GTA.load_vehicle()
        self.acquisition_table = DBLoader_GTA.load_acquisition()
        raw_owned_data = DBLoader_USER.load_owned_vehicle()
        self.own_table = {item['id']: item for item in raw_owned_data}
        self.own_vehicle_id_map = defaultdict(list)
        for own in raw_owned_data:
            self.own_vehicle_id_map[own['vehicle_id']].append(own)

        # 획득처 그룹화 {vehicle_id: ["Source1", "Source2", ...]}
        self.acq_map = defaultdict(set)
        for acq in self.acquisition_table:
            self.acq_map[acq['vehicle_id']].add(acq['source'])
            self.acq_set.add(acq['source'])

        # vehicle table에 owned 플래그 추가
        owned_ids = {item['vehicle_id'] for item in self.own_table.values() if item['is_sold'] == 0}
        for vehicle in self.vehicle_table:
            vehicle['is_owned'] = vehicle['id'] in owned_ids
            if self.acq_map.get(vehicle['id'], None) is None:
                vehicle['is_owned'] = None

        self.vehicle_map = {item['id']: item for item in self.vehicle_table}

        self.vehicle_class = DBLoader_GTA.load_vehicle_classes()
        self.manufacturer = DBLoader_GTA.load_manufacturer()
        self.drivetrain = DBLoader_GTA.load_drivetrain()

    def filter_vehicle(self, vname, vclasses, mnftrs, acq, seat, op_str="=="):
        """
        Return a list of vehicles that meet the conditions\n
        op_str : ">=", "<=", "==", ">", "<"
        """
        ops = {
        ">=": operator.ge,
        "<=": operator.le,
        "==": operator.eq,
        ">": operator.gt,
        "<": operator.lt
        }
        op_func = ops.get(op_str, operator.eq) ### Default value is '=='

        def is_match(v):
            ### compare name string
            if vname:
                search_term = vname.lower()
                name_match = search_term in v['name'].lower()
                translated_match = search_term in v['translated_name'].lower()
                
                # 두 곳 모두에 검색어가 없으면 필터링(False)
                if not (name_match or translated_match):
                    return False
                
            ### filter vehicle class and manufacturer string
            if vclasses and str(v['vehicle_class']) != vclasses: 
                return False
                
            if mnftrs and str(v['manufacturer']) != mnftrs: 
                return False

            ### compare vehicle seats
            if seat is not None:
                if not op_func(v['seats'], seat):
                    return False

            ### compare acquisition
            if acq:
                v_sources = self.get_vehicle_acquisition(v['id']) # self 중복 전달 수정
                if acq not in v_sources:
                    return False
            
            return True

        return [v for v in self.vehicle_table if is_match(v)]

    
    def get_vehicle_acquisition(self, vehicle_id):
        return self.acq_map.get(vehicle_id, set())
    
    def get_vehicle(self, vehicle_id):
        return self.vehicle_map.get(vehicle_id)
        # return [v for v in self.vehicle_table if vehicle_id == v['id']]

    def is_owned(self, vehicle_id):
        return self.vehicle_map.get(vehicle_id)['is_owned']
    
    def get_own_vehicle_list(self, vehicle_id):
        return self.own_vehicle_id_map.get(vehicle_id, [])
    
    def add_own_vehicle(self, vehicle_id, owned_property_id=1, slot_type_id=1, slot_index=0):
        """
            add Own vehicle to DB and dictionary,\n
            returns new own vehicle's own id
        """
        dbid = DBLoader_USER.insert_user_vehicle(vehicle_id, owned_property_id, slot_type_id, slot_index)
        for vehicle in self.vehicle_table:
            if (vehicle['id'] == vehicle_id) & (vehicle['is_owned'] == False):
                vehicle['is_owned'] == True
                break

        new_entry = {
            'id': dbid,
            'vehicle_id': vehicle_id,
            'owned_property_id': owned_property_id,
            'slot_type_id': slot_type_id,
            'slot_index': slot_index,
            'paint_preset_id' : None,
            'is_reward' : 0,
            'mod_custom' : 0,
            'mod_upgrade' : 0,
            'mod_imani' : 0,
            'mod_hsw' : 0,
            'mod_drift' : 0,
            'limited_mod' : 0,
            'limited_plate' : 0,
            'limited_paint' : 0,
            'limited_livery' : 0,
            'is_sold': 0,
        }

        ### add row in dictionary
        self.own_table[dbid] = new_entry
        self.own_vehicle_id_map[vehicle_id].append(new_entry)

        ### add_vehicle_to_garage / slot counting
        for callback in self.on_vehicle_changed_callbacks:
            callback(new_entry)

        return dbid
    
    def edit_own_vehicle(self, id, **kwargs):
        """
            Edit own vehicle\n
            ex) "mod_upgrade" = True, "paint_preset_id" = 4
        """
        target = self.own_table.get(id)
        if not target:
            print(f"Modify Failed: Cannot Find ID {id}")
            return False
        
        DBLoader_USER.update_user_vehicle(id, **kwargs)

        for key, value in kwargs.items():
            if key in target:
                target[key] = value
        
        print(f"차량 정보 수정 완료: ID {id} -> {kwargs}")
        return True
    
    def sell_own_vehicle(self, id):
        """
            Modify 'is_sold' to True in own vehicle
        """
        DBLoader_USER.update_user_vehicle(id, is_sold=1)
        if id in self.own_table:
            self.own_table[id]['is_sold'] = 1

    def remove_own_vehicle(self, id):
        """
            delete own vehicle has already sold from DB
        """
        target_vehicle = self.own_table.get(id)
        if not target_vehicle:
            print(f"Cannot Find ID {id}")
            return

        ### you can only remove sold vehicle
        if target_vehicle.get('is_sold') == 1:
            DBLoader_USER.delete_user_vehicle(id)

            ### remove from dictionary
            v_id = target_vehicle['vehicle_id']
            if v_id in self.own_vehicle_id_map:
                ### remove only the objects with 
                ### the corresponding ID from the dictionary's list
                self.own_vehicle_id_map[v_id] = [
                    v for v in self.own_vehicle_id_map[v_id] if v['id'] != id
                ]
                ### remove key if dictionary's list is empty
                if not self.own_vehicle_id_map[v_id]:
                    del self.own_vehicle_id_map[v_id]

            # 메모리(딕셔너리)에서 삭제
            self.own_table.pop(id)
            print(f"Vehicle(ID: {id}) Successfully Removed")
        else:
            print("This vehicle is not yet sold (is_sold=1). Please sell vehicle first.")

class PropertyManager:
    """
        Load Property and PCustom Datas From DB\n

        property_table : {property data}
        property_map : {property_id : property data}
        property_type_table : {property type data}
        property_type_map : {ptype_id : property type data}
        property_custom_table : {custom data}
        property_custom_map : {custom_id : custom data }
        property_custom_type_table : (custom type data)
        property_custom_type_map = {ctype_id : custom type data}
        owned_property = {own_pid : own_pdata}
        owned_p_custom = {own_pcid : own_cdata}
        ptype_map = {ptype_id : [{property data}]}
        custom_map = {ptype_id : {ctype_id : [{custom data}]} }
        own_map = {ptype_id : [ {own_pdata} ]}
        owned_custom_map = {own_pid : {ctype_id : [own_cdata]} }
    
    """
    def __init__(self):
        self.property_table = []
        self.property_type_table = []
        self.property_custom_table = []
        self.property_custom_type_table = []
        self.owned_property = []
        self.owned_p_custom = []

    def load_table(self):
        self.property_table = DBLoader_GTA.load_property()
        self.property_map = {item['id']: item for item in self.property_table}
        self.property_type_table = DBLoader_GTA.load_property_type()
        self.property_type_map = {item['id']: item for item in self.property_type_table}
        self.property_custom_table = DBLoader_GTA.load_property_custom()
        self.property_custom_map = {item['id']: item for item in self.property_custom_table}
        self.property_custom_type_table = DBLoader_GTA.load_property_custom_type()
        self.property_custom_type_map = {item['id']: item for item in self.property_custom_type_table}
        raw_owned_property = DBLoader_USER.load_owned_property()
        self.owned_property = {item['id']: item for item in raw_owned_property}
        raw_owned_p_custom = DBLoader_USER.load_owned_property_custom()
        self.owned_p_custom = {item['id']: item for item in raw_owned_p_custom}

        self.ptype_map = defaultdict(list)
        for ppt in self.property_table:
            self.ptype_map[ppt['type_id']].append(ppt)

        self.custom_map = defaultdict(lambda: defaultdict(list))

        for c in self.property_custom_table:
            ct_id = c['customtype_id'] 
            if ct_id in self.property_custom_type_map.keys():
                p_type_id = self.property_custom_type_map[ct_id]['propertytype_id']
                # p_type_id(부동산종류) -> ct_id(개조항목) -> 옵션 리스트
                self.custom_map[p_type_id][ct_id].append(c)

        # own_map 구성: {부동산타입: {부동산슬롯번호: 부동산소유정보}}
        self.own_map = {}
        for p_type in self.property_type_table:
            if p_type['parent_id'] is None:
                t_id = p_type['id']
                if p_type['max_owned'] is None:
                    max_cnt = 100
                else:
                    max_cnt = p_type['max_owned']
                # max_owned 크기만큼 None으로 채워진 리스트 생성
                self.own_map[t_id] = [None] * max_cnt

        for p_type in self.property_type_table:
            if p_type['parent_id'] is not None:
                t_id = p_type['id']
                if p_type['max_owned'] is None:
                    self.own_map[t_id] = self.own_map[p_type['parent_id']]
                else:
                    max_cnt = p_type['max_owned']
                    self.own_map[t_id] = [None] * max_cnt



        for op in self.owned_property.values():
            t_id = op['property_type_id']
            if t_id in self.own_map:
                # 해당 타입 리스트의 첫 번째 None(빈자리)을 찾아 할당
                for i in range(len(self.own_map[t_id])):
                    if self.own_map[t_id][i] is None:
                        self.own_map[t_id][i] = op
                        break

        #own_custom_map {own부동산ID: {custom_type_id: custom_id}}
        self.owned_custom_map = defaultdict(lambda: defaultdict(list))

        for oc in self.owned_p_custom.values():
            cm_id = oc['owned_property_id']
            cm_type = oc['propertycustom_type_id']
            self.owned_custom_map[cm_id][cm_type].append(self.property_custom_map.get(oc['propertycustom_id']))

    def is_owned_property(self, property_id):
        for ownp in self.owned_property.values():
            if ownp.get('property_id') == property_id:
                return True
        return False
    
    def is_owned_pcustom(self, pcustom_id):
        for pcustom in self.owned_p_custom.values():
            if pcustom.get('propertycustom_id') == pcustom_id:
                return True
        return False

    def check_buyable_property(self, property_id):
        """
            Compares the number of properties that can be owned
            with the number currently owned by the user
        """
        type_id = self.property_map[property_id]['type_id']
        max_allowed = self.property_type_map[type_id]['max_owned']
        if max_allowed is None:
            max_allowed = self.property_type_map[ self.property_type_map[type_id]['parent_id'] ]['max_owned']
        current_count = 0
        for i in range(len(self.own_map[type_id])):
            if self.own_map[type_id][i]:   
                if self.own_map[type_id][i]['is_active'] == 1:
                    if self.own_map[type_id][i]['property_id'] == property_id:
                        return False
                    current_count = current_count + 1
        return (current_count < max_allowed)
    
    def get_pcustom_max_owned(self, custom_type_id):
        target = self.property_custom_type_map.get(custom_type_id, {})
        return target.get('max_owned', 0)
    
    def get_pcustom_max_owned_from_cid(self, custom_id):
        custom_type_id = self.property_custom_map.get(custom_id, {}).get('customtype_id', 0)
        target = self.property_custom_type_map.get(custom_type_id, {})
        return target.get('max_owned', 0)
    
    def get_own_custom_list_from_cid(self, own_pid, custom_id):
        """
            Returns owned custom data list
            whose custom type matches
            the custom data of the given custom ID.
        """
        custom_type_id = self.property_custom_map.get(custom_id, {}).get('customtype_id', 0)
        for own_cdata in self.owned_p_custom.values():
            if custom_type_id == own_cdata.get('propertycustom_type_id'):
                if own_pid == own_cdata.get('owned_property_id'):
                    return (self.owned_custom_map[own_pid][custom_type_id].copy())

        return []
    
    def add_own_property(self, property_id):
        """
            Loops through own_map[type_id]
            to find an available slot.\n
            Inserts a new property into empty slots,
            or updates properties in deactivated slots.
        """
        type_id = self.property_map[property_id]['type_id']

        ### if user bought over max_count
        if not self.check_buyable_property(property_id):
            print(f"This Cannot Be Bought")
            return False
        
        for i in range(len(self.own_map[type_id])):
            target = self.own_map[type_id][i]
            # print(f"Finding None >{target}<")
            if target is None:
                tmpid = DBLoader_USER.insert_user_property(property_id, type_id, None, 1)

                new_entry = {
                'id': tmpid,
                'property_id': property_id,
                'property_type_id': type_id,
                'memo': None,
                'is_active': 1,
                }
                
                self.owned_property[tmpid] = new_entry
                self.own_map[type_id][i] = new_entry
                return tmpid
            elif target and target['is_active'] == 0:
                DBLoader_USER.update_user_property(target['id'], property_id=property_id, property_type_id=type_id, is_active=1 )
                target['property_id'] = property_id
                target['property_type_id'] = type_id
                target['is_active'] = 1
                return target['id']
            
        return False
    
    def inactive_own_property(self, property_id):
        """
            Deactivates the owned property
            by setting is_active to False\n
            unless the property type is unchangeable
        """
        type_id = self.property_map[property_id]['type_id']

        if self.property_type_map[type_id]['is_unchangeable'] == 1:
            return False

        for i in range(len(self.own_map[type_id])):
            if self.own_map[type_id][i]:
                if self.own_map[type_id][i]['property_id'] == property_id:
                    DBLoader_USER.update_user_property(self.own_map[type_id][i]['id'], property_id=property_id, is_active=0 )
                    self.own_map[type_id][i]['is_active'] = 0
                    return True
        return False
    
    def edit_memo_own_property(self, own_property_id, memo):
        """
            update own property's memo in DB and dictionary
        """
        target = self.owned_property.get(own_property_id,{})
        target['memo'] = memo
        DBLoader_USER.update_user_property(own_property_id, memo=memo )
        pass

    def get_memo_own_property(self, own_property_id):
        """
            Returns own property's memo
        """
        target = self.owned_property.get(own_property_id,{})
        return target.get('memo', "No Memo")
    
    def add_own_pcustom(self, own_pid, custom_id):
        """
            Add owned custom data to the DB
            when the user has not reached
            the maximum ownership limit.
        """
        pc_data = self.property_custom_map.get(custom_id)
        ct_id = pc_data['customtype_id']

        max_owned = self.get_pcustom_max_owned(ct_id)
        now_owned = len(self.owned_custom_map[own_pid][ct_id])

        if (max_owned - now_owned) <= 0:
            return False

        tmpid = DBLoader_USER.insert_user_property_custom(own_pid, custom_id, ct_id)

        new_entry = {
        'id': tmpid,
        'owned_property_id': own_pid,
        'propertycustom_id': custom_id,
        'propertycustom_type_id': ct_id,
        }

        self.owned_p_custom[tmpid] = new_entry

        self.owned_custom_map[own_pid][ct_id].append(pc_data)

        return True
    
    def edit_own_pcustom(self, own_pid, custom_id, after_custom_id):
        """
            modify own property's custom id
            unless it's unchangeable
        """
        pc_data = self.property_custom_map.get(custom_id)
        ct_id = pc_data['customtype_id']
        if self.property_custom_type_map.get(ct_id)['is_unchangeable'] == 1:
            return False
        
        ### Search for an existing 'owned property custom id'
        opc_id = None
        for pc in self.owned_p_custom.values():
            if own_pid == pc['owned_property_id'] and custom_id == pc['propertycustom_id']:
                opc_id = pc['id']
                break
        
        if opc_id is not None:
            DBLoader_USER.update_user_property_custom(opc_id, propertycustom_id=after_custom_id)
            self.owned_p_custom[opc_id]['propertycustom_id'] = after_custom_id

            ### Sync Dictionary
            after_pc_data = self.property_custom_map.get(after_custom_id)
            if own_pid in self.owned_custom_map:
                for i, row in enumerate(self.owned_custom_map[own_pid][ct_id]):
                    if row['id'] == custom_id:
                        self.owned_custom_map[own_pid][ct_id].pop(i)
                        self.owned_custom_map[own_pid][ct_id].append(after_pc_data)
                        return True
        

    def remove_own_pcustom(self, own_pid, custom_id):
        """
            remove own custom data
            unless it's unchangeable
        """
        pc_data = self.property_custom_map.get(custom_id)

        if not pc_data: 
            return

        ct_id = pc_data['customtype_id']
        if self.property_custom_type_map.get(ct_id)['is_unchangeable'] == 1:
            return
        
        ### Search for an existing 'owned property custom id'
        opc_id = None
        for pc in self.owned_p_custom.values():
            if own_pid == pc['owned_property_id'] and custom_id == pc['propertycustom_id']:
                opc_id = pc['id']
                break
        
        if opc_id is not None:
            DBLoader_USER.delete_user_property_custom(opc_id)
            self.owned_p_custom.pop(opc_id)
            
            ### Sync Dictionary
            if own_pid in self.owned_custom_map and ct_id in self.owned_custom_map[own_pid]:
                for i, row in enumerate(self.owned_custom_map[own_pid][ct_id]):
                    if row['id'] == custom_id:
                        self.owned_custom_map[own_pid][ct_id].pop(i)
                        break


    def get_property_list_from_type(self, property_type_id):
        """
            returns property list from property type map
        """
        return self.ptype_map.get(property_type_id, [])
         

    def get_custom_menu(self, property_id):
        """
            [LEGACY] Not USING THIS NOW
        """
        ### get property
        prop = next((p for p in self.property_table if p['id'] == property_id), None)
        if not prop:
            return {}
        
        t_id = prop['type_id']
        result_custom = {}
        
        # print(f"=== {prop['key_name']} 개조 메뉴 ===")
        
        ### group customs by category
        for ct_id, options in self.custom_map[t_id].items():
            category = self.property_type_map.get(ct_id)
            category_name = category['name'] if category else f"Unknown({ct_id})"
            # print(f"\n[카테고리: {category_name}]")
            
            for opt in options:
                print(f"  - {opt['name']}: ${opt['price']}")

class ColorManager:
    """
        Load Color Datas From DB\n

        render_material : {render_id : render_name}
        chameleon_type : {chameleon_id : chameleon_name}
        gta_sample_preset : {gta_color_id : gta_color_data}
        paint_presets : {preset_id : preset data}
        livery_type : {livery_id : livery data}
        color_refs : {ref_id : gta + user color data }
        last_gta_id : last gta color id in color_refs
    
    """
    def __init__(self):
        self.color_refs = {}
        self.render_material = {}
        self.chameleon_type = {}
        self.gta_sample_preset = {}
        self.paint_presets = {}

    def load_table(self):
        temp_render_material = DBLoader_GTA.load_render_material()
        self.render_material = {item['id']: item['name'] for item in temp_render_material}
        temp_chameleon_type = DBLoader_GTA.load_chameleon_type()
        self.chameleon_type = {item['id']: item['name'] for item in temp_chameleon_type}
        temp_gta_sample_preset = DBLoader_GTA.load_gta_paint_preset()
        self.gta_sample_preset = {item['id']: item for item in temp_gta_sample_preset}
        temp_paint_presets = DBLoader_USER.load_user_paint_preset()
        self.paint_presets = {item['id']: item for item in temp_paint_presets}
        temp_livery_type = DBLoader_GTA.load_livery_type()
        self.livery_type = {item['id']: item for item in temp_livery_type}

        default_color_ref = DBLoader_GTA.load_color_ref()
        #self.last_gta_id = max((color['id'] for color in default_color_ref), default=0)
        self.last_gta_id = 1000
        temp_user_color = DBLoader_USER.load_user_color_ref()

        for color in temp_user_color:
            color['id'] += (self.last_gta_id + 1) 

        temp_color_refs = default_color_ref + temp_user_color
        self.color_refs = {item['id']: item for item in temp_color_refs}
    
    def add_custom_color(self, name, hex_color):
        """
            Returns New Added Crew Color ID
        """

        """
        for refs in self.color_refs.values():
            if refs['gta_color_id'] is None and refs['hex_color'] == hex_color:
                return None
        """
        
        tmpid = DBLoader_USER.insert_user_color_ref(name, 1, hex_color) + self.last_gta_id + 1
        new_entry = {
        'id': tmpid,
        'name': name,
        'gta_color_id': None,
        'default_rendermaterial_id': 1,
        'chameleontype_id': None,
        'hex_color': hex_color,
        'secondary_hex': None,
        'tertiary_hex': None,
        }
        self.color_refs[tmpid] = new_entry
        return tmpid
    
    def edit_custom_color(self, color_id, name, hex_color):
        """
            Update Crew Color name and Hex value
        """
        target = self.color_refs.get(color_id)
        if not target:
            return False
        
        self.color_refs[color_id]['name'] = name
        self.color_refs[color_id]['hex_color'] = hex_color
        dbid = color_id - (self.last_gta_id + 1)
        DBLoader_USER.update_user_color_ref(dbid, name = name, hex_color=hex_color)
        
        return True
    
    def remove_custom_color(self, color_id):
        """
            Remove Crew Color
        """
        target = self.color_refs.get(color_id)
        if not target:
            return False
        self.color_refs.pop(color_id)
        dbid = color_id - (self.last_gta_id + 1)
        DBLoader_USER.delete_user_color_ref(dbid)
        return True
    
    def add_color_preset(self, name, is_hidden, **kwargs):
        """
            Add New Color Preset Data\n
            Returns New Preset ID
        """
        pcolor_id = kwargs.get('pcolor_id', -1)
        prender_id = kwargs.get('prender_id', -1)
        scolor_id = kwargs.get('scolor_id')
        srender_id = kwargs.get('srender_id')
        pearl_color_id = kwargs.get('pearl_color_id')
        wheel_color_id = kwargs.get('wheel_color_id')
        dial_color_id = kwargs.get('dial_color_id')
        trim_color_id = kwargs.get('trim_color_id')
        neon_color_id = kwargs.get('neon_color_id')
        headlight_color_id = kwargs.get('headlight_color_id')
        livery_type_id = kwargs.get('livery_type_id')
        tempid = DBLoader_USER.insert_user_paint_preset(name, is_hidden, 
                                          pcolor_id, prender_id, scolor_id, srender_id,
                                          pearl_color_id, wheel_color_id, dial_color_id, trim_color_id,
                                          neon_color_id, headlight_color_id, livery_type_id)
        new_entry = {
        'id': tempid,
        'name': name,
        'is_hidden': is_hidden,
        'primary_color_id': pcolor_id,
        'primary_render_id': prender_id,
        'secondary_color_id': scolor_id,
        'secondary_render_id': srender_id,
        'pearl_color_id': pearl_color_id,
        'wheel_color_id': wheel_color_id,
        'dial_color_id': dial_color_id,
        'trim_color_id': trim_color_id,
        'neon_color_id': neon_color_id,
        'headlight_color_id': headlight_color_id,
        'livery_type_id': livery_type_id,
        }
        self.paint_presets[tempid] = new_entry
        return tempid
    
    def edit_color_preset(self, presetid, **kwargs):
        """
            Modify Color Preset Data\n
            kwargs must be in\n
            'id',
            'name',
            'is_hidden',\n
            'primary_color_id',
            'primary_render_id',\n
            'secondary_color_id',
            'secondary_render_id',\n
            'pearl_color_id',
            'wheel_color_id',\n
            'dial_color_id',
            'trim_color_id',\n
            'neon_color_id',
            'headlight_color_id',\n
            'livery_type_id'
        """
        target = self.paint_presets.get(presetid, None)
        if not target:
            return False
        
        DBLoader_USER.update_user_paint_preset(presetid, **kwargs)

        for key, value in kwargs.items():
            if key in target:
                target[key] = value
        
        print(f"color preset Successfully Edited: ID {presetid} -> {kwargs}")
        return True
    
    def remove_color_preset(self, presetid):
        """
            Remove Color Preset
        """
        target = self.paint_presets.get(presetid)
        if not target:
            return False
        
        DBLoader_USER.delete_user_paint_preset(presetid)
        self.paint_presets.pop(presetid)

        return True
    
    def get_color_refs(self):
        """
            Returns All GTA + USER Color References
        """
        return self.color_refs
    
    def get_user_presets(self, showHidden ,showVanilaOnly):
        """
            Returns filtered {preset_id : preset data}
        """
        result = {}
        for keys, row in self.paint_presets.items():
            if (showHidden or row['is_hidden'] == 0) and \
            (not self.is_preset_modded(row['id']) or not showVanilaOnly):
                result[keys] = row

        return result
    
    def get_gta_preset_catalogue(self):
        """
            Returns GTA Respray Catalogue\n
            {Category name: {id:color info}}
        """
        # preset_catalogue 구성: {Category name: {id:color info}}
        preset_catalogue = defaultdict(dict)

        for keys, sps in self.gta_sample_preset.items():
            tmp_render_id = sps['category_render_id']
            render_data = self.render_material.get(tmp_render_id, '')
            if render_data:
                preset_catalogue[render_data][keys] = sps

        return preset_catalogue
    
    def get_gta_presets(self):
        return self.gta_sample_preset
    
    def what_gradient_preview(self, color_id):
        """
            Returns String of Gradient Type\n
            ex) chrome, prismatic..
        """
        target = self.color_refs.get(color_id)
        if not target or target.get('gta_color_id') is None:
            return None
        
        render_id = target['default_rendermaterial_id']
        render_name = self.render_material.get(render_id, '').lower()
        
        if render_name == "chrome":
            return "chrome"
        elif render_name == "chameleon":
            c_type_id = target.get('chameleontype_id')
            return self.chameleon_type.get(c_type_id, '')
        
        return None    
    
    def is_preset_modded(self, preset_id:int):
        """
            Returns a Bool value indicating
            whether the Preset with preset_id is in a Modded state
        """
        """
        무광펄, 조직무광 등등 글리치로 가능하니 패스 \n
        1차 2차 렌더링 방식 Worn, Util, light일 경우 모드 \n
        펄,휠,다이얼,트림,네온,라이트 색상 id가  GTA 카탈로그 클래식 내의 주색 id와 같은지
        """
        target = self.paint_presets.get(preset_id)
        if not target:
            return False
        
        ALLOWED_RENDERS = {'classic', 'matte', 'metallic', 'metals', 'chrome', 'chameleon'}
        
        for render_key in ['primary_render_id', 'secondary_render_id']:
            r_id = target.get(render_key)
            if r_id is not None:
                r_name = self.render_material.get(r_id, '').lower()
                if r_name and r_name not in ALLOWED_RENDERS:
                    return True
        
        ### The color can be changed at any time via Crew Color,
        ### and since even the Default GTA color doesn't seem to 
        ### always follow the existing color index, I'm putting it on hold for now.
        """
        catalogue = self.get_gta_preset_catalogue()
        classic_ids = {p['id'] for p in catalogue.get('classic', [])}
        light_ids = {p['id'] for p in catalogue.get('light', [])}

        check_list = [
            ('pearl_color_id', classic_ids),
            ('wheel_color_id', classic_ids),
            ('dial_color_id', classic_ids),
            ('trim_color_id', classic_ids),
            ('neon_color_id', light_ids),
            ('headlight_color_id', light_ids)
        ]

        for key, allowed_set in check_list:
            val = target.get(key)
            if val is not None and val not in allowed_set:
                return True
        """

        return False

class BuyManager:
    """
        Load 'Buy Bonus' Datas From DB\n

        target_type_lookup : {type_id : type_name}
        buybonus_rule : {bonus data}
        bonus_map : {type_name : {bonus trigger id : [{bonus data}]}}
    
    """
    def __init__(self):
        self.buybonus_rule = []
        self.target_type_lookup = []

    def load_table(self):
        bonus_target_type = DBLoader_GTA.load_bonus_target_type()
        self.target_type_lookup = {tt['id']: tt['key_name'] for tt in bonus_target_type}
        
        self.buybonus_rule = DBLoader_GTA.load_buybonus_rule()
        self.bonus_map = defaultdict(lambda: defaultdict(list))
        for bbr in self.buybonus_rule:
            target_name = self.target_type_lookup.get(bbr['triggertype_id'], "UNKNOWN") 
            self.bonus_map[target_name][bbr['trigger_id']].append(bbr)

    def get_type_name(self, type_id):
        return self.target_type_lookup.get(type_id)
    
    def get_bonus_map(self):
        return self.bonus_map

    def check_buy_table(self, type_name, id):
        """
            Returns list of Bonus Data that triggered by given ID
        """
        target = self.bonus_map[type_name]
        if target is not None:
            result = self.bonus_map[type_name].get(id, None)

        return result


class StorageManager:
    """
        Load Storage as Garage Slot Datas From DB\n

        slot_type : {type data}
        slot_type_map : {type_id : type_name}
        property_type_has_slot : {id : property storage data}
        storage_compatibility : {slottype_id : storage compatibility data}
        dedicated_storage : {slottype_id : dedicated storage data}
        ptype_slot_map : {propertytype_id : {slottype_id : number of slot}}
    
    """
    UNIVERSAL_SLOTTYPE = 1

    def __init__(self):
        self.slot_type = []
        self.property_type_has_slot = []
        self.storage_compatibility = []
        self.dedicated_storage = []

    def load_table(self):
        self.slot_type = DBLoader_GTA.load_slot_type()
        self.slot_type_map = {item['id']: item['key_name'] for item in self.slot_type}
        temp_slot_list = DBLoader_GTA.load_property_type_has_slot()
        self.property_type_has_slot = {item['id']: item for item in temp_slot_list}
        temp_storage_compatibility = DBLoader_GTA.load_storage_compatibility()
        self.storage_compatibility = defaultdict(list)
        for sc in temp_storage_compatibility:
            self.storage_compatibility[sc['slottype_id']].append(sc)

        temp_dedicated_storage = DBLoader_GTA.load_dedicated_storage()
        self.dedicated_storage = defaultdict(list)
        for ds in temp_dedicated_storage:
            self.dedicated_storage[ds['slottype_id']].append(ds)

        self.ptype_slot_map = defaultdict(dict)
        for pths_row in self.property_type_has_slot.values():
            if pths_row.get('parent_id', None) is not None:
                pths_row['numberofslot'] = self.property_type_has_slot.get('parent_id', {}).get('numberofslot', 0)
            self.ptype_slot_map[ pths_row['propertytype_id'] ][ pths_row['slottype_id'] ] = pths_row['numberofslot']
            

    def get_max_number_of_slot(self, propertytype_id, slottype_id):
        """
        max number of slottype in ptid.
        """
        return self.ptype_slot_map.get(propertytype_id, {}).get(slottype_id, 0)
        
    
    def is_compatible(self, vehicle, slot_type_id):
        """
            Check if a specific vehicle can fit into a specific slot type
        """
        ### Check Dedicated Storage
        # ex) nightclub terrorbyte slot, terrorbyte oppressor Mk2 slot..
        dedicated = self.dedicated_storage.get(slot_type_id, [])
        if any(d['allowed_vehicle_id'] == vehicle['id'] for d in dedicated):
            return True


        ### Storage Compatibility Cehck
        # ex) Aircraft - Plane and Heli, Garage - Bike Super and Sports..
        compatibilities = self.storage_compatibility.get(slot_type_id, [])
        return any(c['vehicle_class'] == vehicle['vehicle_class'] for c in compatibilities)
    
    def get_compatible_slottypes(self, vehicle):
        """
            Iterates all Slot types and check compatible with vehicle data\n
            unique type vehicle will not check compatible storage data
        """
        allowed_slots = set()
        allowed_slots.add(self.UNIVERSAL_SLOTTYPE)

        is_unique = vehicle['is_unique']
        

        for slot_type_id, slot_name in self.slot_type_map.items():
            if slot_type_id == self.UNIVERSAL_SLOTTYPE:
                continue
            has_added = False
            dedicated = self.dedicated_storage.get(slot_type_id, [])
            compatibilities = self.storage_compatibility.get(slot_type_id, [])

            for ddc in dedicated:
                if ddc['allowed_vehicle_id'] == vehicle['id']:
                    allowed_slots.add(slot_type_id)
                    has_added = True
                    break
            
            if has_added or is_unique:
                continue

            for cpb in compatibilities:
                if cpb['vehicle_class'] == vehicle['vehicle_class']:
                    allowed_slots.add(slot_type_id)
                    break

        return allowed_slots

            