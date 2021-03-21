import MaxPlus
import timeit
import os
from pymxs import runtime as rt
from PySide2 import QtWidgets, QtCore, QtGui
in_file_time = timeit.default_timer()
class AniToolsLog():
    #m_Text = u'1.0 바이패드 선택'
    #m_Text = u'1.1 선택시 버그 수정'
    #m_Text = u'1.11 #이름클래스 적용'
    #m_Text = u'1.12 #bip저장'
    #m_Text = u'1.13 #26 선택문제'
    #m_Text = u'1.14 #30 바이페드 전부 선택'
    #m_Text = u'1.15 #29 키 버튼'
    #m_Text = u'1.15 #4 tcb 키 버튼'
    #m_Text = u'1.16 #31 선택기능 강화'
    #m_Text = u'1.17 레아아웃 개선'
    #m_Text = u'1.18 없을때 리셋'
    # m_Text = u'1.19 풋스탭키 오류'
    m_Text = u'1.20 네임선택리스트 추가 #40'
    def __init__(self):
        pass
    def Get(self):
        return self.m_Text
class BipedLimbName():
    in_time = timeit.default_timer()
    bip_class = 'Biped_Object'
    larm = 'lArm'
    rarm = 'rArm'
    lfingers  = 'lfingers'
    rfingers = 'rfingers'
    lleg = 'lleg'
    rleg = 'rleg'
    ltoes = 'ltoes'
    rtoes = 'rtoes'
    spine = 'spine'
    tail = 'tail'
    head = 'head'
    pelvis = 'pelvis'
    com_v = 'vertical'
    com_h = 'horizontal'
    footprints =  'footprints'
    neck = 'neck'
    pony1 = 'pony1'
    pony2 = 'pony2'
    prop1 = 'prop1'
    prop2 = 'prop2'
    prop3 = 'prop3'
    ifArmTwist = 'ifArmTwist'
    rfArmTwist = 'rfArmTwist'
    lUparmTwist = 'lUparmTwist'
    rUparmTwist = 'rUparmTwist'
    lThighTwist = 'lThighTwist'
    rThighTwist = 'rThighTwist'
    lCalfTwist = 'lCalfTwist'
    rCalfTwist = 'rCalfTwist'
    lHorseTwist = 'lHorseTwist'
    rHorseTwist = 'rHorseTwist'
    def __init__(self):
        pass
        #print('BipedLimbName 클래스 실행 완료 시간 : {}'.format(str(timeit.default_timer() - self.in_time)))
class bipedSelect():
    #rt = pymxs.runtime
    m_enable_log = False
    m_limbNames = (
        rt.Name('larm'),
        rt.Name('rarm'),
        rt.Name('lfingers'),
        rt.Name('rfingers'),
        rt.Name('lleg'),
        rt.Name('rleg'),
        rt.Name('ltoes'),
        rt.Name('rtoes'),
        rt.Name('spine'),
        rt.Name('tail'),
        rt.Name('head'),
        rt.Name('pelvis'),
        rt.Name('vertical'),
        rt.Name('horizontal'),
        #rt.Name('footprints'),
        rt.Name('neck'),
        rt.Name('pony1'),
        rt.Name('pony2'),
        rt.Name('prop1'),
        rt.Name('prop2'),
        rt.Name('prop3')
    )
    m_twistNames = (
        rt.Name('ifArmTwist'),
        rt.Name('rfArmTwist'),
        rt.Name('lUparmTwist'),
        rt.Name('rUparmTwist'),
        rt.Name('lThighTwist'),
        rt.Name('rThighTwist'),
        rt.Name('lCalfTwist'),
        rt.Name('rCalfTwist'),
        rt.Name('lHorseTwist'),
        rt.Name('rHorseTwist')
    )
    m_bipName = u''
    m_com = None
    m_bipNodes = {}
    m_bipedAll_nodes = []
    def __init__(self, node = None):
        if node is None:
            #print('node is None')
            return None
        #self.log(u'바이패드노드 정보의 생성 대상은 {}입니다.'.format(node.name))
        in_time = timeit.default_timer()
        self.m_com = node
        self.m_bipedAll_nodes = []
        self.m_bipNodes = self.GetBipedBoneList()
        self.m_bipName = self.m_com.name
        #print('bipedSelect 클래스 실행 완료 시간 : {}'.format(str(timeit.default_timer() - in_time)))
        #self.log(u'바이패드 노드 정보 생성 완료')
    def log(self, text):
        if self.m_enable_log:
            print(text)
    def GetBipedBoneList(self):
        nodes_dis = {}
        bip_maxlinks =  rt.biped.maxNumLinks (self.m_com)
        twin_maxlinks = rt.biped.maxTwistLinks(self.m_com)
        #self.log(u'바이패드 기본 노드 정보를 생성 중입니다.')
        start_time = timeit.default_timer()
        self.AddBipedNodeKeys(dict = nodes_dis, name_list = self.m_limbNames, maxLinks = bip_maxlinks)
        #self.log(u'완료 : {}'.format(timeit.default_timer() - start_time))
        #self.log(u'바이패드 트위스트 노드 정보를 생성 중입니다.')
        self.AddBipedNodeKeys(dict = nodes_dis, name_list = self.m_twistNames, maxLinks = twin_maxlinks)
        return nodes_dis
    def AddBipedNodeKeys(self, dict = {}, name_list = [], maxLinks = 0):
        getNode = rt.biped.getNode
        bipedAllNodeAdd = self.m_bipedAll_nodes.extend
        for name in name_list:
            key = str(name)
            node_list = []
            node = None
            node = getNode(self.m_com, name , link=1)
            if node is not None:
                node_list.append(node)
                for i in range(2,maxLinks):
                    subNode = getNode(self.m_com, name , link=i)
                    if subNode is None:
                        break
                    node_list.append(subNode)
            value = tuple(node_list)
            bipedAllNodeAdd(node_list)
            dict[key] = value
    def GetRootParentNode(self, node):
        isNotParent = True
        if node == None:
            isNotParent = False
        while isNotParent:
            #print(node.name)
            pnode = node.parent 
            if pnode == None:
                isNotParent = False
            else:
                node = pnode
        return node
    def GetChildernNodes(self, node):
        list = [node]
        for c_node in node.Children:
            list.append(c_node)
            list = list + self.GetChildernNodes(c_node)
        return list
    def select(self, name = '', index = 0):
        node = self.GetNode(name, index)
        result = rt.IsValidNode(node)
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if node is not None and result:
            if modifiers == QtCore.Qt.ControlModifier:
                rt.selectMore(node)
            elif modifiers == QtCore.Qt.AltModifier:
                rt.deselect(node)
            else:
                rt.select(node)
        rt.redrawViews()
        return result
    def GetNode(self, name = '', index = 0):
        node = None
        if name not in self.m_bipNodes:
            return node
        target = self.m_bipNodes[name]
        if (len(target) - 1) >= index :
            node = target[index]
        return node
    def GetPartName(self, node):
        part_name = node.name
        name_list = part_name.split()
        if not len(name_list) == 0:
            part_name = name_list[-1]
        return part_name
    def GetPhalanxCount(self, nodeName, bipName):
        ''' return (phalanx_count, link_count) '''
        phalanx_count = 0
        link_count = 0
        target_nodeName = nodeName
        nodes = self.m_bipNodes[bipName]
        for node in nodes:
            if node.name.endswith(target_nodeName, 0,-1):
                phalanx_count += 1
        if phalanx_count > 0:
            link_count = len(nodes)/phalanx_count
        return (phalanx_count, link_count)
    def GetToesCount(self):
        ''' return (rtoes_count, link_count) '''
        result = self.GetPhalanxCount('Toe','rtoes')
        return result
    def GetFingerCount(self):
        ''' return (rfinger_count, link_count) '''
        result = self.GetPhalanxCount('Finger','rfingers')
        return result
    def GetAllBipedAndBone(self):
        if self.m_com == None:
            return []
        # 바이패드까리 링크걸렸을때 다른것 까지 선택되서 com밑에까만 선택되게 수정
        #root_node = self.GetRootParentNode(self.m_com)
        all_bipeds_and_bones = self.GetChildernNodes(self.m_com)
        return all_bipeds_and_bones
class GetKey():
    m_node = None
    m_currentFrame = 0
    m_pos_keys = []
    m_rot_keys = []
    m_scl_keys = []
    m_obj_type_dic = {}
    m_tcb_default_value_list = [25, 25, 25]
    m_tcb_linear_value_list = [25, 0, 25]
    m_tcb_smooth_value_list = [25,25,25]
    m_rotation_name = u'Rotation'
    m_rotation_tcb_name = u'tcb_rotation'
    def __init__(self, node = None):
        self.m_node = node
        self.m_currentFrame = rt.currentTime
    def GetBipedPosKeys(self, node):
        m_posKeys = rt.biped.getTransform(node, rt.Name('pos'))
        ctrl = node.controller
        keys = ctrl.keys
        for key in keys:
            print(key.time)
    def GetKeyTimes(self, node):
        pass
    def SetKey(self, node):
        pass
    def CopyKeys(self, nodes):
        pass
    def PasteKeys(self, nodes):
        pass
    def SetKeyTcb(solf, ctrl, index, tcb_value_list):
        if index == 0:
            return False
        key = rt.getKey(ctrl, index)
        tension, continuity, bias = tcb_value_list
        key.tension = tension
        key.continuity = continuity
        key.bias = bias
class GetBipedKey(GetKey):
    def __init__(self):
        self.m_biped_type_name_class = BipedLimbName()
    def SetKey(self, nodes):
        getNodeType = rt.classOf
        isBipedType = self.m_biped_type_name_class.bip_class
        this_time = rt.currentTime
        biepdAddKey = rt.biped.addNewKey
        boneAddKey = rt.addNewKey
        for node in nodes:
            if node.name.endswith('Footsteps'):
                continue
            ctrl = node.controller
            if str(getNodeType(node)) == isBipedType:
                if ctrl.rootNode == node:
                    biepdAddKey(ctrl.vertical.controller, this_time)
                    biepdAddKey(ctrl.horizontal.controller, this_time)
                    biepdAddKey(ctrl.turning.controller, this_time)
                else:
                    biepdAddKey(ctrl, this_time)
            else:
                boneAddKey(ctrl, this_time)
        rt.redrawViews()
    def SetSliderTimeNextKeyFrame(self, node):
        current_time = rt.currentTime
        ctrl = node.controller
        def getNextTime(current_time, key_list):
            getKey = current_time
            for key in key_list:
                if current_time < key:
                    getKey = key
                    break
            return getKey
        if ctrl.rootNode == node:
            key_list = [x.time for x in ctrl.vertical.controller.keys]
            key_list += [x.time for x in ctrl.horizontal.controller.keys]
            key_list += [x.time for x in ctrl.turning.controller.keys]
            rt.sliderTime = getNextTime(current_time, sorted(key_list))
        else:
            key_list = [x.time for x in ctrl.controller.keys]
            rt.sliderTime = getNextTime(current_time, sorted(key_list))
        rt.redrawViews()
    def SetSliderTimePreviousKeyFrame(self, node):
        ctrl = node.controller
        current_time = rt.currentTime
        def getPreviousTime(current_time, key_list):
            getKey = current_time
            for key in key_list:
                if current_time > key:
                    getKey = key
                    break
            return getKey
        if ctrl.rootNode == node:
            key_list = [x.time for x in ctrl.vertical.controller.keys]
            key_list += [x.time for x in ctrl.horizontal.controller.keys]
            key_list += [x.time for x in ctrl.turning.controller.keys]
            rt.sliderTime = getPreviousTime(current_time, sorted(key_list)[::-1])
        else:
            key_list = [x.time for x in ctrl.controller.keys]
            rt.sliderTime = getPreviousTime(current_time, sorted(key_list)[::-1])
        rt.redrawViews()
    def SetIK(self, ik_type):
        ''' set seletion nodes ik
        ik_type = Plant, Sliding, Free
        '''
        setIK = ik_type
        getNodeType = rt.classOf
        isBipedType = self.m_biped_type_name_class.bip_class
        for node in rt.selection:
            if node.name.endswith('Footsteps'):
                continue
            if str(getNodeType(node)) == isBipedType:
                setIK(node)
        rt.redrawViews()
    def SetIKPlantedKey(self):
        self.SetIK(rt.biped.setPlantedKey)
        rt.redrawViews()
    def SetIKSlidingKey(self):
        self.SetIK(rt.biped.setSlidingKey)
        rt.redrawViews()
    def SetIKFreeKey(self):
        self.SetIK(rt.biped.setFreeKey)
        rt.redrawViews()
    def SetKeyTcb(self, ctrl, getKeyType, index, tcb_value_list):
        if index == 0:
            return False
        key = getKeyType(ctrl, index)
        tension, continuity, bias = tcb_value_list
        key.tension = tension
        key.continuity = continuity
        key.bias = bias
        rt.redrawViews()
    def SetTcbValue(self, tcb_value_list):
        getKeyIndex =  rt.getkeyindex
        getNodeType = rt.classOf
        bipedGetKey = rt.biped.getKey
        boneGetKey = rt.getKey
        isBipedType = self.m_biped_type_name_class.bip_class
        this_time = rt.sliderTime
        getCtrl = rt.getPropertyController
        is_tcb_type = self.m_rotation_tcb_name
        for node in rt.selection:
            if node.name.endswith('Footsteps'):
                continue
            ctrl = node.controller
            if str(getNodeType(node)) == isBipedType:
                if ctrl.rootNode == node:
                    index = getKeyIndex(ctrl.vertical.controller, this_time)
                    self.SetKeyTcb(ctrl.vertical.controller, bipedGetKey, index, tcb_value_list)
                    index = getKeyIndex(ctrl.horizontal.controller, this_time)
                    self.SetKeyTcb(ctrl.horizontal.controller, bipedGetKey, index, tcb_value_list)
                    index = getKeyIndex(ctrl.turning.controller, this_time)
                    self.SetKeyTcb(ctrl.turning.controller,bipedGetKey,index, tcb_value_list)
                else:
                    index = getKeyIndex(ctrl, this_time)
                    self.SetKeyTcb(ctrl, bipedGetKey, index, tcb_value_list)
            else:
                rot_ctrl = getCtrl(node.track, self.m_rotation_name)
                if str(getNodeType(rot_ctrl)) == is_tcb_type:
                    index = getKeyIndex(rot_ctrl, this_time)
                    self.SetKeyTcb(rot_ctrl, boneGetKey, index, tcb_value_list)
        rt.redrawViews()
    def CopyPose(self):
        pass

class animationRange():
    m_animSet_list= []
    def __init__(sefl):
        pass
    def add_animSet(sefl):
        pass
class BipedMainWindow(QtWidgets.QDialog):
    m_file_log = AniToolsLog()
    m_key_class = GetBipedKey()
    m_bipName = BipedLimbName()
    m_title_text = u'Biped Select Tool'
    m_enable_log = False
    m_maxScriptPath_str = u""
    # Biped Select
    m_biped_class = None
    m_biped_list = ()
    m_select_all_biped_text = 'Biped'
    m_select_all_bipedsAndBone_text = 'Children'
    m_select_all_objects_text = 'Scenes'
    m_bip_name_label = u'대상 :'
    m_default_color = QtGui.QColor(100,100,100)
    m_right_color = QtGui.QColor(6, 134, 6)
    m_mid_color = QtGui.QColor(8, 110, 134)
    m_lift_color = QtGui.QColor(28, 28, 177)
    m_com_color = QtGui.QColor(135, 6, 6)
    m_finger_button_min_size = (12, 8) #width, higth
    m_button_min_size = (60, 15) #width, higth
    m_layout_main = None
    m_select_tabWidget = QtWidgets.QTabWidget()
    #key
    m_add_key_button_name = u'Set Key'
    m_next_key_button_name = u'다음키'
    m_prev_key_button_name = u'이전키'
    m_ik_planted_button_name = u'Plant'
    m_ik_sliding_button_name = u'Sliding'
    m_ik_free_button_name = u'Free'
    m_tcb_Linear_min_button_name = u'TCB Linear'
    m_tcb_tension_mid_button_name = u'TCB Smooth'
    #File
    m_bip_save_text_name = u'SaveBip'
    m_bip_path_folder_name = u'_BipFiles\\'
    m_bip_extension = u'.bip'
    m_bip_open_button_text = u'Open Folder'
    m_bip_file_dir = u''
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        #print('BipedMainWindow __init__')
        in_time = timeit.default_timer()
        super(BipedMainWindow, self).__init__(parent)
        #print('super: BipedMainWindow클래스 실행 완료 시간 : {}'.format(str(timeit.default_timer() - in_time)))
        title_text = u'{} - {}'.format(self.m_title_text, self.m_file_log.Get())
        self.setWindowTitle(title_text)
        self.m_biped_list = self.GetBipedComs()
        #self.m_biped_class = bipedSelect(rt.getnodeByName('Bip001'))
        self.CreditLayout()
            #바이페드가 여러게 생성되었을 경우 초기값을 돌려줌
        if self.m_biped_class is not None:
            self.m_biped_class = self.m_biped_list[0]
        self.m_bip_file_dir = os.path.join(rt.maxfilepath, self.m_bip_path_folder_name)
        self.show()
        #print('BipedMainWindow 클래스 실행 완료 시간 : {}'.format(str(timeit.default_timer() - in_time)))
    def log(self, text):
        if self.m_enable_log:
            print(text)
    def GetBipedComs(self):
        biped_com_list = []
        bipeds = []
        #self.log(u'오브젝트 검색 시작')
        in_time = timeit.default_timer()
        classOf = rt.classOf
        bip_class_str = 'Biped_Object'
        getNode = rt.biped.getNode
        name = rt.Name('vertical')
        addList = biped_com_list.append
        #print(str(len(rt.objects)))
        biped_com_list = [node.controller.rootNode for node in rt.objects if node.name.endswith('Footsteps')]
        end_time = timeit.default_timer()
        #print('GetBipedComs 검사종료 시간 : {}'.format(str(timeit.default_timer() - in_time)))
        #self.log(u'검사종료 : {}'.format(end_time - in_time))
        #self.log(u'씬의 바이패드는 {}개가 있습니다.'.format(len(biped_com_list)))
        for node in biped_com_list:
            #self.log(node.name)
            biped_class = bipedSelect(node)
            bipeds.append(biped_class)
        if len(bipeds) > 0:
            self.m_biped_class = bipeds[0]
            #self.log(u'기본 바이패드로 {}가 선택되었습니다.'.format(self.m_biped.m_bipName))
        #print('GetBipedComs 클래스 실행 완료 시간 : {}'.format(str(timeit.default_timer() - in_time)))
        return tuple(bipeds)
    def GetQPaletteData(self, qpalette):
        alternateBase_qbrush = qpalette.alternateBase()
        base_qbrush = qpalette.base()
        current_colorgroup = qpalette.currentColorGroup()
        #print(current_colorgroup)
    def SetButtonSize(self, button, min_size = m_button_min_size):
        w_size, h_size = min_size
        button.setMinimumSize(w_size, h_size)
    def CreditSelectButton(self, layout , limb_name ='', index = 0, button_text = '', button_color = m_default_color, min_size = m_button_min_size):
        w_size, h_size = min_size
        button = QtWidgets.QPushButton(button_text, default = False, autoDefault = False)
        #self.log(limb_name)
        #self.log(str(index))
        button.clicked.connect(lambda : self.selectNode(limb_name=limb_name,link_index = index))
        button.setMinimumSize(w_size, h_size)
        #button.setBaseSize(QtCore.QSize(50, 20))
        qpalette = button.palette()
        qpalette.setColor(QtGui.QPalette.Button, button_color)
        button.setPalette(qpalette)
        layout.addWidget(button)
    def AddHeadButton(self, layout):
        pony1_layout = QtWidgets.QVBoxLayout()
        pony1_button = self.AddBipedSelectButtons(pony1_layout, self.m_bipName.pony1, self.m_right_color, add_name = True)
        if pony1_button:
            layout.addLayout(pony1_layout)
        head_layout = QtWidgets.QVBoxLayout()
        self.AddBipedSelectButtons(head_layout, self.m_bipName.head, self.m_mid_color, add_name = True)
        self.AddBipedSelectButtons(head_layout, self.m_bipName.neck, self.m_mid_color, add_name = True, revers = True)
        layout.addLayout(head_layout)
        pony2_layout = QtWidgets.QVBoxLayout()
        pony2_button = self.AddBipedSelectButtons(pony2_layout, self.m_bipName.pony2, self.m_right_color, add_name = True)
        if pony2_button:
            layout.addLayout(pony2_layout)
        return 
    def AddBipedSelectButtons(self, layout, taregt_name = '', button_color = m_default_color, add_name = False, max_limit = 6, revers = False):
        if not taregt_name in self.m_biped_class.m_bipNodes:
            return None
        biped_tp = self.m_biped_class.m_bipNodes[taregt_name]
        rever_tp = biped_tp[::-1]
        useing_up = biped_tp
        if revers:
            useing_up = biped_tp[::-1]
        # 흠 나중에 선택하지 못한 바이패드를 한번에 선택하는 기능도 있으면 좋을듯 해서 변수하나 만들어둠
        need_all_button = False
        for bip in useing_up:
            name = ''
            if add_name:
                name = self.m_biped_class.GetPartName(bip)
            self.CreditSelectButton(layout, taregt_name, biped_tp.index(bip), name, button_color)
        if len(useing_up) < 1:
            return False
        return True
    def CreditPhalanxLayout(self, parent_layout, limb_name, target_count = (0,0), button_color = m_default_color, revers = False):
        ''' parent_layout add button 
        Is use finger or Tose'''
        toes_count, link_count = target_count
        biped_r_toes_layout = QtWidgets.QVBoxLayout()
        for i in range(0, link_count):
            link_layout = QtWidgets.QHBoxLayout()
            target_index  = i
            if revers:
                target_index = target_index + (link_count * (toes_count - 1))
            for link_index in range(0, toes_count ):
                self.CreditSelectButton(link_layout, limb_name, (target_index), '', button_color, min_size = self.m_finger_button_min_size)
                if revers:
                    target_index = target_index - link_count
                else:
                    target_index = target_index + link_count
            biped_r_toes_layout.addLayout(link_layout)
        parent_layout.addLayout(biped_r_toes_layout)
    def CreditBipedSelectTab(self, layout):
        #self.log(u'선랙트 탭을 생성한다.')
        self.m_select_tabWidget = QtWidgets.QTabWidget()
        tab_tayout = QtWidgets.QVBoxLayout(self.m_select_tabWidget)
        for bip in self.m_biped_list:
            self.m_biped_class = bip
            new_tab = QtWidgets.QWidget()
            new_layout = self.SepBipSelectLayout()
            new_tab.setLayout(new_layout)
            self.m_select_tabWidget.addTab(new_tab, self.m_biped_class.m_bipName)
        self.m_select_tabWidget.currentChanged.connect(self.ChangeBipedSet)
        layout.addWidget(self.m_select_tabWidget)
    def SepBipSelectLayout(self):
        layout_bipedSelect = QtWidgets.QVBoxLayout()
        #최상단
        top_groupbox = QtWidgets.QGroupBox()
        top_layout = QtWidgets.QHBoxLayout()
        select_all_objects_button = QtWidgets.QPushButton(self.m_select_all_objects_text, default = False, autoDefault = False)
        select_all_objects_button.clicked.connect(self.SelectAllSceneObjects)
        top_layout.addWidget(select_all_objects_button)
        select_all_biped_button = QtWidgets.QPushButton(self.m_select_all_biped_text, default = False, autoDefault = False)
        select_all_biped_button.clicked.connect(self.SelectAllBiped)
        top_layout.addWidget(select_all_biped_button)
        select_all_bipedsAndBones_button = QtWidgets.QPushButton(self.m_select_all_bipedsAndBone_text, default = False, autoDefault = False)
        select_all_bipedsAndBones_button.clicked.connect(self.SelectAllBonesAndBipeds)
        top_layout.addWidget(select_all_bipedsAndBones_button)
        #layout_bipedSelect.addLayout(top_layout)
        top_groupbox.setLayout(top_layout)
        layout_bipedSelect.addWidget(top_groupbox)
        # 상단
        head_groupbox = QtWidgets.QGroupBox()
        biped_head_layout = QtWidgets.QHBoxLayout()
        self.AddHeadButton(biped_head_layout)
        #layout_bipedSelect.addLayout(biped_head_layout)
        head_groupbox.setLayout(biped_head_layout)
        layout_bipedSelect.addWidget(head_groupbox)
        # 중단
        body_groupbox = QtWidgets.QGroupBox()
        biped_body_layout = QtWidgets.QHBoxLayout()
        biped_r_arm_layout = QtWidgets.QVBoxLayout()
        finger_count_tp = self.m_biped_class.GetFingerCount()
        biped_r_hand_layout = QtWidgets.QVBoxLayout()
        self.AddBipedSelectButtons(biped_r_hand_layout, self.m_bipName.rarm, self.m_right_color, add_name = True)
        biped_r_arm_layout.addLayout(biped_r_hand_layout)
        self.CreditPhalanxLayout(biped_r_hand_layout, self.m_bipName.rfingers, finger_count_tp, self.m_right_color, revers = True)
        biped_body_layout.addLayout(biped_r_arm_layout)
        spine_layout = QtWidgets.QVBoxLayout()
        self.AddBipedSelectButtons(spine_layout, self.m_bipName.spine, self.m_mid_color, add_name = True, revers = True)
        biped_body_layout.addLayout(spine_layout)
        biped_l_hand_layout = QtWidgets.QVBoxLayout()
        self.AddBipedSelectButtons(biped_l_hand_layout, self.m_bipName.larm, self.m_lift_color, add_name = True)
        self.CreditPhalanxLayout(biped_l_hand_layout,self.m_bipName.lfingers, finger_count_tp, self.m_lift_color)
        biped_body_layout.addLayout(biped_l_hand_layout)
        #layout_bipedSelect.addLayout(biped_body_layout)
        body_groupbox.setLayout(biped_body_layout)
        layout_bipedSelect.addWidget(body_groupbox)
        # 중심
        com_groupbox = QtWidgets.QGroupBox()
        biped_mid_layout = QtWidgets.QVBoxLayout()
        biped_com_layout = QtWidgets.QHBoxLayout()
        #self.AddBipedSelectButtons(biped_com_layout, 'vertical', self.m_mid_color, add_name = True)
        self.AddBipedSelectButtons(biped_com_layout, self.m_bipName.com_h, self.m_com_color, add_name = True)
        self.AddBipedSelectButtons(biped_com_layout, self.m_bipName.pelvis, self.m_mid_color, add_name = True)
        # trun은 못찾네?
        #self.AddBipedSelectButtons(biped_com_layout, 'turn', self.m_mid_color, add_name = True)
        biped_mid_layout.addLayout(biped_com_layout)
        biped_porp_layout = QtWidgets.QHBoxLayout()
        self.AddBipedSelectButtons(biped_porp_layout, self.m_bipName.prop1, self.m_mid_color, add_name = True)
        self.AddBipedSelectButtons(biped_porp_layout, self.m_bipName.prop2, self.m_mid_color, add_name = True)
        self.AddBipedSelectButtons(biped_porp_layout, self.m_bipName.prop3, self.m_mid_color, add_name = True)
        biped_mid_layout.addLayout(biped_porp_layout)
        #layout_bipedSelect.addLayout(biped_mid_layout)
        com_groupbox.setLayout(biped_mid_layout)
        layout_bipedSelect.addWidget(com_groupbox)
        # 하단
        legs_groupbox = QtWidgets.QGroupBox()
        biped_leg_layout = QtWidgets.QHBoxLayout()
        biped_r_leg_layout = QtWidgets.QVBoxLayout()
        toes_count_tp = self.m_biped_class.GetToesCount()
        ## 발가락
        biped_r_foot_layout = QtWidgets.QVBoxLayout()
        self.AddBipedSelectButtons(biped_r_foot_layout, self.m_bipName.rleg, self.m_right_color, add_name = True)
        biped_r_leg_layout.addLayout(biped_r_foot_layout)
        self.CreditPhalanxLayout(biped_r_leg_layout,self.m_bipName.rtoes, toes_count_tp, self.m_right_color)
        biped_leg_layout.addLayout(biped_r_leg_layout)
        biped_tail_layout = QtWidgets.QVBoxLayout()
        self.AddBipedSelectButtons(biped_tail_layout, self.m_bipName.tail, self.m_mid_color, add_name = True)
        biped_leg_layout.addLayout(biped_tail_layout)
        biped_l_leg_layout = QtWidgets.QVBoxLayout()
        ## 왼발
        biped_l_foot_layout = QtWidgets.QVBoxLayout()
        self.AddBipedSelectButtons(biped_l_foot_layout, self.m_bipName.lleg, self.m_lift_color, add_name = True)
        biped_l_leg_layout.addLayout(biped_l_foot_layout)
        self.CreditPhalanxLayout(biped_l_leg_layout, self.m_bipName.ltoes, toes_count_tp, self.m_lift_color, revers = True)
        biped_leg_layout.addLayout(biped_l_leg_layout)
        #layout_bipedSelect.addLayout(biped_leg_layout)
        legs_groupbox.setLayout(biped_leg_layout)
        layout_bipedSelect.addWidget(legs_groupbox)
        #
        #parent_layout.addLayout(layout_bipedSelect)
        return layout_bipedSelect
    def SetBipTitleLayout(self, parent_layout):
        #self.log(u'바이패드 선택 레이아웃을 생성한다.')
        title_layout = QtWidgets.QHBoxLayout()
        name_qlable = QtWidgets.QLabel(self.m_bip_name_label)
        title_layout.addWidget(name_qlable)
        qcombobox = QtWidgets.QComboBox()
        self.SetBipedSelectQComboBox(qcombobox)
        title_layout.addWidget(qcombobox)
        parent_layout.addLayout(title_layout)
    # Key def
    def NextKeyFrame(self):
        if rt.IsValidNode(self.m_biped_class.m_com):
            self.m_key_class.SetSliderTimeNextKeyFrame(self.m_biped_class.m_com)
        else:
            self.ReStart()
    def PreviousKeyFrame(self):
        if rt.IsValidNode(self.m_biped_class.m_com):
            self.m_key_class.SetSliderTimePreviousKeyFrame(self.m_biped_class.m_com)
        else:
            self.ReStart()
    def AddNewKey(self):
        self.m_key_class.SetKey(rt.selection)
    # key layout
    def AddKeyButton(self, layout, button_text, click_def, button_color = m_default_color, min_size = m_button_min_size):
        w_size, h_size = min_size
        qbutton = QtWidgets.QPushButton(button_text, default = False, autoDefault = False)
        qbutton.clicked.connect(click_def)
        qbutton.setMinimumSize(w_size, h_size)
        qpalette = qbutton.palette()
        qpalette.setColor(QtGui.QPalette.Button, button_color)
        qbutton.setPalette(qpalette)
        layout.addWidget(qbutton)
    def CreateKeyLayout(self, parent_layout):
        main_layout = QtWidgets.QVBoxLayout()
        key_layout = QtWidgets.QHBoxLayout()
        self.AddKeyButton(key_layout, self.m_add_key_button_name, self.AddNewKey)
        self.AddKeyButton(key_layout, self.m_prev_key_button_name, self.PreviousKeyFrame)
        self.AddKeyButton(key_layout, self.m_next_key_button_name, self.NextKeyFrame)
        main_layout.addLayout(key_layout)
        # biped IK button
        ik_layout = QtWidgets.QHBoxLayout()
        self.AddKeyButton(ik_layout, self.m_ik_planted_button_name, self.SetIKPlantedKey)
        self.AddKeyButton(ik_layout, self.m_ik_sliding_button_name, self.SetIKSlidingKey)
        self.AddKeyButton(ik_layout, self.m_ik_free_button_name, self.SetIKFreeKey)
        main_layout.addLayout(ik_layout)
        # tcb button
        tcb_layout = QtWidgets.QHBoxLayout()
        self.AddKeyButton(tcb_layout, self.m_tcb_Linear_min_button_name, self.SetTcbLinear)
        self.AddKeyButton(tcb_layout, self.m_tcb_tension_mid_button_name, self.SetTcbSmooth)
        #self.AddKeyButton(ik_layout, self.m_ik_free_button_name, self.SetIKFreeKey)
        main_layout.addLayout(tcb_layout)
        #
        parent_layout.addLayout(main_layout)
    # key biped IK def
    def SetIKPlantedKey(self):
        self.m_key_class.SetIK(rt.biped.setPlantedKey)
    def SetIKSlidingKey(self):
        self.m_key_class.SetIK(rt.biped.setSlidingKey)
    def SetIKFreeKey(self):
        self.m_key_class.SetIK(rt.biped.setFreeKey)
    # key tcb def
    def SetTcbLinear(self):
        self.m_key_class.SetTcbValue(self.m_key_class.m_tcb_linear_value_list)
    def SetTcbSmooth(self):
        self.m_key_class.SetTcbValue(self.m_key_class.m_tcb_smooth_value_list)
    def CreateBipFileLayout(self, parent_layout):
        files_layout = QtWidgets.QHBoxLayout()
        save_bip_file_button = QtWidgets.QPushButton(self.m_bip_save_text_name, default = False, autoDefault = False)
        save_bip_file_button.clicked.connect(self.SaveBipFile)
        files_layout.addWidget(save_bip_file_button)
        open_dir_button = QtWidgets.QPushButton(self.m_bip_open_button_text, default = False, autoDefault = False)
        open_dir_button.clicked.connect(self.OpenBipDir)
        files_layout.addWidget(open_dir_button)
        parent_layout.addLayout(files_layout)
    def SaveBipFile(self):
        self.log(u'SaveBipFile in')
        if not rt.IsValidNode(self.m_biped_class.m_com):
            return self.ReStart()
        file_name = rt.maxfilename[:-4]
        bip_name = self.m_biped_class.m_com.name
        extension = self.m_bip_extension
        file_path = self.m_bip_file_dir
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        save_file_name = u'{file_path}{file_name}_{bip_name}{extension}'.format(file_path = file_path, file_name = file_name, bip_name = bip_name, extension = extension)
        self.log(save_file_name)
        rt.biped.saveBipFile(self.m_biped_class.m_com.controller, save_file_name)
    def OpenBipDir(self):
        #enable = rt.ShellLaunch(self.m_bip_file_dir, "")
        enable = rt.ShellLaunch(rt.maxfilepath, "")
        if not enable:
            pass
    def CreditLayout(self):
        #self.log(u'메인 레이아웃 생성한다.')
        self.m_layout_main = QtWidgets.QVBoxLayout()
        #self.SetBipTitleLayout(self.m_layout_main)
        if not self.m_biped_class is None:
            self.CreditBipedSelectTab(self.m_layout_main)
        #키 관련 버튼
        self.CreateKeyLayout(self.m_layout_main)
        #Tcb조정
        self.CreateBipFileLayout(self.m_layout_main)
        #SeletSet
        self.SelectSetLayout(self.m_layout_main)
        self.setLayout(self.m_layout_main)
    def SetBipedSelectQComboBox(self, qcombobox):
        #self.log(u'바이패드를 선택하는 메뉴를 추가한다.')
        for bip in self.m_biped_list:
            qcombobox.addItem(bip.m_com.name)
        qcombobox.currentIndexChanged.connect(self.ChangeBipedSet)
    def ChangeBipedSet(self, index):
        self.m_biped_class = self.m_biped_list[index]
    def selectNode(self, limb_name = '', link_index = 0):
        isValidNode = self.m_biped_class.select(limb_name, link_index)
        if not isValidNode:
            self.ReStart()
    def selectMode(self, target_node):
        if not rt.IsValidNode(self.m_biped_class.m_com):
            return self.ReStart()
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            rt.selectMore(target_node)
        elif modifiers == QtCore.Qt.AltModifier:
            rt.deselect(target_node)
        else:
            rt.select(target_node)
        rt.redrawViews()
    def SelectAllBiped(self):
        self.selectMode(self.m_biped_class.m_bipedAll_nodes)
    def SelectAllBonesAndBipeds(self):
        self.selectMode(self.m_biped_class.GetAllBipedAndBone())
    def SelectAllSceneObjects(self):
        rt.select(rt.objects)
    def SelectSetLayout(self, main_layout):
        name_set_layout = QtWidgets.QHBoxLayout()
        self.select_set_list_qcombobox = QtWidgets.QComboBox()
        self.select_button = QtWidgets.QPushButton(u'선택', default = False, autoDefault = False)
        self.select_button.clicked.connect(self.SelectNameSet)
        select_set = rt.selectionSets
        menu_item_list = []
        for set in select_set:
            # if set.name.startswith(u'sel'):
            self.select_set_list_qcombobox.addItem(set.name)
        #self.select_set_list_qcombobox.clicked.connect(self.SelectNameSet)
        name_set_layout.addWidget(self.select_set_list_qcombobox)
        name_set_layout.addWidget(self.select_button)
        main_layout.addLayout(name_set_layout)
    def SelectNameSet(self):
        name = self.select_set_list_qcombobox.currentText()
        print(name)
        set_tiem = rt.selectionSets[name]
        rt.select(set_tiem)
    def TestPrint(self):
        print('test')
    def CreateWindows(self):
        pass
    def IsValidNode(self, node):
        result = rt.IsValidNode(node)
        if not result:
            self.ReStart()
        return result
    def ReStart(self):
        self.close()
        BipedMainWindow()

class_out_time = timeit.default_timer()
#print('클래스 읽기 완료시간 : {}'.format(str(class_out_time - in_file_time)))
BipedMainWindow()
#print('클래스 실행 완료 시간 : {}'.format(str(timeit.default_timer() - class_out_time)))
