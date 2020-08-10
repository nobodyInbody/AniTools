import MaxPlus
import timeit
from pymxs import runtime as rt
from PySide2 import QtWidgets, QtCore, QtGui
# 바이패드는 사전형으로 생각해 볼 것
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
        self.log(u'바이패드노드 정보의 생성 대상은 {}입니다.'.format(node.name))
        self.m_com = node
        self.m_bipNodes = self.GetBipedBoneList()
        self.m_bipName = self.m_com.name
        self.log(u'바이패드 노드 정보 생성 완료')
    def log(self, text):
        if self.m_enable_log:
            print(text)
    def GetBipedBoneList(self):
        nodes_dis = {}
        bip_maxlinks =  rt.biped.maxNumLinks (self.m_com)
        twin_maxlinks = rt.biped.maxTwistLinks(self.m_com)
        self.log(u'바이패드 기본 노드 정보를 생성 중입니다.')
        start_time = timeit.default_timer()
        self.AddBipedNodeKeys(dict = nodes_dis, name_list = self.m_limbNames, maxLinks = bip_maxlinks)
        self.log(u'완료 : {}'.format(timeit.default_timer() - start_time))
        self.log(u'바이패드 트위스트 노드 정보를 생성 중입니다.')
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
                    if subNode is not None:
                        node_list.append(subNode)
            value = tuple(node_list)
            dict[key] = value
    def GetChindNode(self, node):
        pass
    def select(self, name = '', index = 0):
        node = self.GetNode(name, index)
        if node is not None:
            rt.select(node)
    def selectMode(self, biped_node, sub_node):
        pass
    def GetNode(self, name = '', index = 0):
        node = None
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
class animationRange():
    m_animSet_list= []
    def __init__(sefl):
        pass
    def add_animSet(sefl):
        pass
class BipedMainWindow(QtWidgets.QDialog):
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
    m_button_h_setMinimumSize = 20
    m_layout_main = None
    m_select_tabWidget = QtWidgets.QTabWidget()
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(BipedMainWindow, self).__init__(parent)
        self.setWindowTitle(self.m_title_text)
        self.m_biped_list = self.GetBipedComs()
        #self.m_biped = bipedSelect(rt.getnodeByName('Bip001'))
        if self.m_biped is not None:
            self.CreditLayout()
        self.show()
    def log(self, text):
        if self.m_enable_log:
            print(text)
    def GetBipedComs(self):
        biped_com_list = []
        bipeds = []
        self.log(u'오브젝트 검색 시작')
        start_time = timeit.default_timer()
        for node in rt.objects:
            if str(rt.classOf(node)) == 'Biped_Object':
                com = rt.biped.getNode(node, rt.Name('vertical'), link = 1)
                if not com in biped_com_list:
                    biped_com_list.append(com)
        end_time = timeit.default_timer()
        self.log(u'검사종료 : {}'.format(end_time - start_time))
        self.log(u'씬의 바이패드는 {}개가 있습니다.'.format(len(biped_com_list)))
        for node in biped_com_list:
            self.log(node.name)
            biped_class = bipedSelect(node)
            bipeds.append(biped_class)
        if len(bipeds) > 0:
            self.m_biped = bipeds[0]
            self.log(u'기본 바이패드로 {}가 선택되었습니다.'.format(self.m_biped.m_bipName))
        return tuple(bipeds)
    def GetQPaletteData(self, qpalette):
        alternateBase_qbrush = qpalette.alternateBase()
        base_qbrush = qpalette.base()
        current_colorgroup = qpalette.currentColorGroup()
        print(current_colorgroup)
    def CreditSelectButton(self, layout , limb_name ='', index = 0, button_text = '', button_color = QtGui.QColor(100,100,100)):
        button = QtWidgets.QPushButton(button_text, default = False, autoDefault = False)
        button.clicked.connect(lambda : self.selectNode(limb_name=limb_name,link_index = index))
        button.setMinimumSize(self.m_button_w_setMinimumSize,self.m_button_h_setMinimumSize)
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
        self.AddButtons(hand_layout, 'neck', self.m_mid_color, add_name = True, max_limit = 1)
        layout.addLayout(hand_layout)
        pony2_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(pony2_layout, 'pony2', self.m_right_color, add_name = True)
        layout.addLayout(pony2_layout)
        return 
    def AddButtons(self, layout, taregt_name = '', button_color = QtGui.QColor(100,100,100), add_name = False, max_limit = 6, revers = False):
        if not taregt_name in self.m_biped.m_bipNodes:
            return None
        biped_tp = self.m_biped.m_bipNodes[taregt_name]
        if revers:
            biped_tp = biped_tp[::-1]
        # 흠 나중에 선택하지 못한 바이패드를 한번에 선택하는 기능도 있으면 좋을듯 해서 변수하나 만들어둠
        need_all_button = False
        # ui에 너무 많은 버튼이 들어가지 않게 제한
        if max_limit > len(biped_tp):
            max_limit = len(biped_tp)
            need_all_button = True
        for bip in biped_tp:
            name = ''
            if add_name:
                name = self.m_biped.GetPartName(bip)
            self.CreditSelectButton(layout, taregt_name, biped_tp.index(bip), name, button_color)
    def CreditBipedSelectTab(self, layout):
        self.log(u'선랙트 탭을 생성한다.')
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
        self.AddButtons(biped_r_arm_layout, 'rArm', self.m_right_color, add_name = True)
        biped_body_layout.addLayout(biped_r_arm_layout)
        spine_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(spine_layout, 'spine', self.m_mid_color, add_name = True, revers = True)
        biped_body_layout.addLayout(spine_layout)
        biped_l_arm_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(biped_l_arm_layout, 'lArm', self.m_lift_color, add_name = True)
        biped_body_layout.addLayout(biped_l_arm_layout)
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
        self.AddButtons(biped_r_leg_layout, 'rleg', self.m_right_color, add_name = True)
        biped_leg_layout.addLayout(biped_r_leg_layout)
        biped_l_leg_layout = QtWidgets.QVBoxLayout()
        self.AddButtons(biped_l_leg_layout, 'lleg', self.m_lift_color, add_name = True)
        biped_leg_layout.addLayout(biped_l_leg_layout)
        layout_bipedSelect.addLayout(biped_leg_layout)
        #
        #parent_layout.addLayout(layout_bipedSelect)
        return layout_bipedSelect
    def SetBipTitleLayout(self, parent_layout):
        self.log(u'바이패드 선택 레이아웃을 생성한다.')
        title_layout = QtWidgets.QHBoxLayout()
        name_qlable = QtWidgets.QLabel(self.m_bip_name_label)
        title_layout.addWidget(name_qlable)
        qcombobox = QtWidgets.QComboBox()
        self.SetBipedSelectQComboBox(qcombobox)
        title_layout.addWidget(qcombobox)
        parent_layout.addLayout(title_layout)
    def CreditLayout(self):
        self.log(u'메인 레이아웃 생성한다.')
        self.m_layout_main = QtWidgets.QVBoxLayout()
        #self.SetBipTitleLayout(self.m_layout_main)
        if not self.m_biped is None:
            self.CreditBipedSelectTab(self.m_layout_main)
        self.setLayout(self.m_layout_main)
    def SetBipedSelectQComboBox(self, qcombobox):
        self.log(u'바이패드를 선택하는 메뉴를 추가한다.')
        for bip in self.m_biped_list:
            qcombobox.addItem(bip.m_com.name)
        qcombobox.currentIndexChanged.connect(self.ChangeBipedSet)
    def ChangeBipedSet(self, index):
        self.log(u'{}을 선택하였습니다.'.format(self.m_lift_color))
        self.m_biped = self.m_biped_list[index]
    def selectNode(self, limb_name = '', link_index = 0):
        self.m_biped.select(limb_name, link_index)
    def TestPrint(self):
        print('test')
    def CreateWindows(self):
        pass

BipedMainWindow()