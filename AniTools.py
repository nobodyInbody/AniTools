import pymxs
from PySide2 import QtWidgets, QtCore, QtGui

class bipedSelect(self):
    rt = pymxs.untime
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
    m_L_Clavicle = []
    m_L_UpperArm = []
    m_L_Forearm = []
    m_L_Hand = []
    m_R_Clavicle = []
    m_R_UpperArm = []
    m_R_Forearm = []
    m_R_Hand = []
    m_L_Finger0 = []
    m_L_Finger01 = []
    m_L_Finger02 = []
    m_L_Finger1 = []
    m_L_Finger11 = []
    m_L_Finger12 = []
    m_L_Finger2 = []
    m_L_Finger21 = []
    m_L_Finger22 = []
    m_L_Finger3 = []
    m_L_Finger31 = []
    m_L_Finger32 = []
    m_L_Finger4 = []
    m_L_Finger41 = []
    m_L_Finger42 = []
    m_L_Finger5 = []
    m_L_Finger51 = []
    m_L_Finger52 = []
    m_R_Finger0 = []
    m_R_Finger01 = []
    m_R_Finger02 = []
    m_R_Finger1 = []
    m_R_Finger11 = []
    m_R_Finger12 = []
    m_R_Finger2 = []
    m_R_Finger21 = []
    m_R_Finger22 = []
    m_R_Finger3 = []
    m_R_Finger31 = []
    m_R_Finger32 = []
    m_R_Finger4 = []
    m_R_Finger41 = []
    m_R_Finger42 = []
    m_R_Finger5 = []
    m_R_Finger51 = []
    m_R_Finger52 = []
    m_L_Thigh = []
    m_L_Calf = []
    m_L_HorseLink = []
    m_L_Foot = []
    m_R_Thigh = []
    m_R_Calf = []
    m_R_HorseLink = []
    m_R_Foot = []
    m_bipName = ''
    m_com = None
    m_bipNodes = ()
    def __init__(self, node):
        if rt.GetClassName(node) is not rt.Biped():
            return False
    def GetBipedBoneList(self):
        nodes = []
        for name in m_limbNames:
            temp_list = []
            for i in range(1,20):
                node = None
                node = rt.biped.getNode(self.m_com, name , link=i)
                if node is not None:
                    temp_list.append(node)
            nodes.append(temp_list)
        #RootName = rt.getNodeByName(bipName)
    def GetChindNode(self, node):
        pass
    def selectHead(self):
        pass
    def selectMode(self, biped_node, sub_node):
        pass
class animationRange(self):
    m_animSet_list= []
    def __init__(sefl):
        pass
    def add_animSet(sefl):
        pass
class MainWindow(QtWidgets.Qwidget):
    m_maxScriptPath_str = u""
    def __init__(self):
        bip_ms = ''
    def BipedSelectLayout(self, parent_layout):
        biped_main_layout = QtWidgets.QVBoxLayout()
        biped_head_layout = QtWidgets.QH
        parent_layout.add(biped_main_layout)
    def CreditLayout(self):
        main_layout = QtWidgets.QVBoxLayout()
        BipedSelectLayout(main_layout)
        
    def CreateWindows(self):
        pass
