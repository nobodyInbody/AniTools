import MaxPlus
import timeit
from pymxs import runtime as rt
from PySide2 import QtWidgets, QtCore, QtGui
in_file_time = timeit.default_timer()
class AniToolsLog():
    m_Text = u'1.1 선택시 버그 수정'
    def __init__(self):
        pass
    def Get(self):
        return self.m_Text
class BipedLimbName():
    lram = 'larm',
    rarm = 'rarm'
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
        rt.Name('footprints'),
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
    def __init__(self, node = None):
        if node is None:
            print('node is None')
            return None
        #self.log(u'바이패드노드 정보의 생성 대상은 {}입니다.'.format(node.name))
        self.m_com = node
        self.m_bipNodes = self.GetBipedBoneList()
        self.m_bipName = self.m_com.name
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
        for name in name_list:
            key = str(name)
            node_list = []
            node = None
            node = rt.biped.getNode(self.m_com, name , link=1)
            if node is not None:
                node_list.append(node)
                for i in range(2,maxLinks):
                    subNode = rt.biped.getNode(self.m_com, name , link=i)
                    if subNode is None:
                        break
                    node_list.append(subNode)
                    #if subNode is not None:
                    #    node_list.append(subNode)
            value = tuple(node_list)
            dict[key] = value
    def GetChindNode(self, node):
        pass
    def select(self, name = '', index = 0):
        node = self.GetNode(name, index)
        if node is not None and rt.isValidNode(node):
            rt.select(node)
        #rt.gw.updateScreen()
        rt.redrawViews()
    def selectMode(self, biped_node, sub_node):
        pass
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

class animationRange():
    m_animSet_list= []
    def __init__(sefl):
        pass
    def add_animSet(sefl):
        pass
class BipedMainWindow(QtWidgets.QDialog):
    m_file_log = AniToolsLog()
    m_bipName = BipedLimbName()
    m_title_text = u'Biped Select Tool'
    m_enable_log = False
    m_maxScriptPath_str = u""
    m_biped = None
    m_biped_list = ()
    m_bip_name_label = u'대상 :'
    m_default_color = QtGui.QColor(100,100,100)
    m_right_color = QtGui.QColor(6, 134, 6)
    m_mid_color = QtGui.QColor(8, 110, 134)
    m_lift_color = QtGui.QColor(28, 28, 177)
    m_com_color = QtGui.QColor(135, 6, 6)
    m_button_w_setMinimumSize = 5
    m_button_h_setMinimumSize = 14
    m_layout_main = None
    m_select_tabWidget = QtWidgets.QTabWidget()
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(BipedMainWindow, self).__init__(parent)
        title_text = u'{} - {}'.format(self.m_title_text, self.m_file_log.Get())
        self.setWindowTitle(title_text)
        self.m_biped_list = self.GetBipedComs()
        #self.m_biped = bipedSelect(rt.getnodeByName('Bip001'))
        if self.m_biped is not None:
            self.CreditLayout()
        #self.setBaseSize(QtCore.QSize(195,350))
        self.show()
    def log(self, text):
        if self.m_enable_log:
            print(text)
    def GetBipedComs(self):
        biped_com_list = []
        bipeds = []
        #self.log(u'오브젝트 검색 시작')
        start_time = timeit.default_timer()
        for node in rt.objects:
            if str(rt.classOf(node)) == 'Biped_Object':
                com = rt.biped.getNode(node, rt.Name('vertical'), link = 1)
                if not com in biped_com_list:
                    biped_com_list.append(com)
        end_time = timeit.default_timer()
        #self.log(u'검사종료 : {}'.format(end_time - start_time))
        #self.log(u'씬의 바이패드는 {}개가 있습니다.'.format(len(biped_com_list)))
        for node in biped_com_list:
            #self.log(node.name)
            biped_class = bipedSelect(node)
            bipeds.append(biped_class)
        if len(bipeds) > 0:
            self.m_biped = bipeds[0]
            #self.log(u'기본 바이패드로 {}가 선택되었습니다.'.format(self.m_biped.m_bipName))
        return tuple(bipeds)
    def GetQPaletteData(self, qpalette):
        alternateBase_qbrush = qpalette.alternateBase()
        base_qbrush = qpalette.base()
        current_colorgroup = qpalette.currentColorGroup()
        #print(current_colorgroup)
    def CreditSelectButton(self, layout , limb_name ='', index = 0, button_text = '', button_color = m_default_color):
        button = QtWidgets.QPushButton(button_text, default = False, autoDefault = False)
        #self.log(limb_name)
        #self.log(str(index))
        button.clicked.connect(lambda : self.selectNode(limb_name=limb_name,link_index = index))
        button.setMinimumSize(self.m_button_w_setMinimumSize,self.m_button_h_setMinimumSize)
        #button.setBaseSize(QtCore.QSize(50, 20))
        qpalette = button.palette()
        qpalette.setColor(QtGui.QPalette.Button, button_color)
        button.setPalette(qpalette)
        layout.addWidget(button)
    def AddHeadButton(self, layout):
        pony1_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(pony1_layout, 'pony1', self.m_right_color, add_name = True)
        layout.addLayout(pony1_layout)
        hand_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(hand_layout, 'head', self.m_mid_color, add_name = True)
        self.AddButtons(hand_layout, 'neck', self.m_mid_color, add_name = True, max_limit = 1, revers = True)
        layout.addLayout(hand_layout)
        pony2_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(pony2_layout, 'pony2', self.m_right_color, add_name = True)
        layout.addLayout(pony2_layout)
        return 
    def AddButtons(self, layout, taregt_name = '', button_color = m_default_color, add_name = False, max_limit = 6, revers = False):
        if not taregt_name in self.m_biped.m_bipNodes:
            return None
        biped_tp = self.m_biped.m_bipNodes[taregt_name]
        rever_tp = biped_tp[::-1]
        useing_up = biped_tp
        if revers:
            useing_up = biped_tp[::-1]
        # 흠 나중에 선택하지 못한 바이패드를 한번에 선택하는 기능도 있으면 좋을듯 해서 변수하나 만들어둠
        need_all_button = False
        for bip in useing_up:
            name = ''
            if add_name:
                name = self.m_biped.GetPartName(bip)
            self.CreditSelectButton(layout, taregt_name, biped_tp.index(bip), name, button_color)
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
                self.CreditSelectButton(link_layout, limb_name, (target_index), '', button_color)
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
            self.m_biped = bip
            new_tab = QtWidgets.QWidget()
            new_layout = self.SepBipSelectLayout()
            new_tab.setLayout(new_layout)
            self.m_select_tabWidget.addTab(new_tab, self.m_biped.m_bipName)
        self.m_select_tabWidget.currentChanged.connect(self.ChangeBipedSet)
        layout.addWidget(self.m_select_tabWidget)
    def SepBipSelectLayout(self):
        layout_bipedSelect = QtWidgets.QVBoxLayout()
        # 상단
        biped_head_layout = QtWidgets.QHBoxLayout()
        self.AddHeadButton(biped_head_layout)
        layout_bipedSelect.addLayout(biped_head_layout)
        # 중단
        biped_body_layout = QtWidgets.QHBoxLayout()
        biped_r_arm_layout = QtWidgets.QVBoxLayout()
        finger_count_tp = self.m_biped.GetFingerCount()
        biped_r_hand_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(biped_r_hand_layout, 'rArm', self.m_right_color, add_name = True)
        biped_r_arm_layout.addLayout(biped_r_hand_layout)
        self.CreditPhalanxLayout(biped_r_hand_layout,'rfingers', finger_count_tp, self.m_right_color, revers = True)
        biped_body_layout.addLayout(biped_r_arm_layout)
        spine_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(spine_layout, 'spine', self.m_mid_color, add_name = True, revers = True)
        biped_body_layout.addLayout(spine_layout)
        biped_l_hand_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(biped_l_hand_layout, 'lArm', self.m_lift_color, add_name = True)
        self.CreditPhalanxLayout(biped_l_hand_layout,'lfingers', finger_count_tp, self.m_lift_color)
        biped_body_layout.addLayout(biped_l_hand_layout)
        layout_bipedSelect.addLayout(biped_body_layout)
        # 중심
        biped_mid_layout = QtWidgets.QVBoxLayout()
        biped_com_layout = QtWidgets.QHBoxLayout()
        #self.AddButtons(biped_com_layout, 'vertical', self.m_mid_color, add_name = True)
        self.AddButtons(biped_com_layout, 'horizontal', self.m_com_color, add_name = True)
        self.AddButtons(biped_com_layout, 'pelvis', self.m_mid_color, add_name = True)
        # trun은 못찾네?
        #self.AddButtons(biped_com_layout, 'turn', self.m_mid_color, add_name = True)
        biped_mid_layout.addLayout(biped_com_layout)
        biped_porp_layout = QtWidgets.QHBoxLayout()
        self.AddButtons(biped_porp_layout, 'prop1', self.m_mid_color, add_name = True)
        self.AddButtons(biped_porp_layout, 'prop2', self.m_mid_color, add_name = True)
        self.AddButtons(biped_porp_layout, 'prop3', self.m_mid_color, add_name = True)
        biped_mid_layout.addLayout(biped_porp_layout)
        layout_bipedSelect.addLayout(biped_mid_layout)
        # 하단
        biped_leg_layout = QtWidgets.QHBoxLayout()
        biped_r_leg_layout = QtWidgets.QVBoxLayout()
        toes_count_tp = self.m_biped.GetToesCount()
        ## 발가락
        biped_r_foot_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(biped_r_foot_layout, 'rleg', self.m_right_color, add_name = True)
        biped_r_leg_layout.addLayout(biped_r_foot_layout)
        self.CreditPhalanxLayout(biped_r_leg_layout,'rtoes', toes_count_tp, self.m_right_color)
        biped_leg_layout.addLayout(biped_r_leg_layout)
        biped_tail_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(biped_tail_layout, 'tail', self.m_mid_color, add_name = True)
        biped_leg_layout.addLayout(biped_tail_layout)
        biped_l_leg_layout = QtWidgets.QVBoxLayout()
        ## 왼발
        biped_l_foot_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(biped_l_foot_layout, 'lleg', self.m_lift_color, add_name = True)
        biped_l_leg_layout.addLayout(biped_l_foot_layout)
        self.CreditPhalanxLayout(biped_l_leg_layout,'ltoes', toes_count_tp, self.m_lift_color, revers = True)
        biped_leg_layout.addLayout(biped_l_leg_layout)
        layout_bipedSelect.addLayout(biped_leg_layout)
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
    def CreateTCBLayout(self, parent_layout):
        pass
    def CreditLayout(self):
        #self.log(u'메인 레이아웃 생성한다.')
        self.m_layout_main = QtWidgets.QVBoxLayout()
        #self.SetBipTitleLayout(self.m_layout_main)
        if not self.m_biped is None:
            self.CreditBipedSelectTab(self.m_layout_main)
        #Tcb조정
        self.CreateTCBLayout(self.m_layout_main)
        self.setLayout(self.m_layout_main)
        
    def SetBipedSelectQComboBox(self, qcombobox):
        #self.log(u'바이패드를 선택하는 메뉴를 추가한다.')
        for bip in self.m_biped_list:
            qcombobox.addItem(bip.m_com.name)
        qcombobox.currentIndexChanged.connect(self.ChangeBipedSet)
    def ChangeBipedSet(self, index):
        self.m_biped = self.m_biped_list[index]
    def selectNode(self, limb_name = '', link_index = 0):
        self.m_biped.select(limb_name, link_index)
    def TestPrint(self):
        print('test')
    def CreateWindows(self):
        pass

class_out_time = timeit.default_timer()
print('클래스 읽기 완료시간 : {}'.format(str(class_out_time - in_file_time)))
BipedMainWindow()
print('클래스 실행 완료 시간 : {}'.format(str(timeit.default_timer() - class_out_time)))